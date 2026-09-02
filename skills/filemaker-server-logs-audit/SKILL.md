---
name: filemaker-server-logs-audit
description: Audit Claris FileMaker Server logs on Windows to investigate performance, access, schedules, scripts, database events, restarts, Data API failures, and TopCallStats transaction costs. Use when analyzing Event.log, Access.log, TopCallStats.log, Stats.log, scriptEvent.log, FMSEScriptErrors.log, or fmdapi.log. Do not use for direct server administration when no log analysis is requested.
license: MIT
compatibility: FileMaker Server on Windows; bundled analyzer requires Python 3.10 or later.
metadata:
  author: albizum
  version: "1.0"
---

# Auditoria De Logs De FileMaker Server

## Inicio Rapido

Usa esta skill para investigar logs de FileMaker Server en Windows. Determina la version a partir de los logs o de una comprobacion segura cuando afecte a la interpretacion; no atribuyas al servidor funciones de otra version.

Trata la carpeta de logs indicada por el usuario como fuente de verdad, conserva los archivos y reporta hallazgos con timestamps, base de datos/cliente/cuenta afectada cuando este disponible, severidad, causa probable y siguiente accion. Verifica en la documentacion oficial los significados, campos, codigos y capacidades dependientes de version.

Para una primera pasada, ejecuta el analizador incluido sobre la carpeta de logs:

```powershell
& "<python>" "<skill>/scripts/analyze_fms_logs.py" "<log-folder>" --out "<log-folder>\fms-log-analysis.json"
```

Usa el Python incluido con Codex cuando no haya Python de sistema disponible. Despues lee el resumen JSON e inspecciona lineas fuente alrededor de timestamps importantes con `rg`, `Select-String` o un parser estructurado.

## Flujo De Investigacion

1. Inventaria primero la carpeta: nombres de archivo, tamanos, fechas de modificacion y pares rotados como `Event-old.log`, `Access-old.log` y `TopCallStats-old.log`.
2. Confirma la version desde los logs o mediante una lectura segura cuando la compatibilidad sea relevante.
3. Lee [references/claris-log-reference.md](references/claris-log-reference.md) cuando importen significados de campos, proposito de logs o matices especificos de Claris. Contrasta con documentacion oficial si el dato depende de version. Lee [references/filemaker-error-codes.md](references/filemaker-error-codes.md) cuando informes codigos de error de guion, Data API, ODBC, archivo, validacion o seguridad.
4. Ejecuta `scripts/analyze_fms_logs.py` para una linea base repetible.
5. Correlaciona logs por timestamp:
   - `Event.log`: warnings, errores, reinicios, apertura/cierre de bases, comprobaciones de coherencia, schedules, cambios de configuracion.
   - `Access.log`: conexiones, desconexiones, bases abiertas, uso de cuentas, accesos denegados por limites.
   - `TopCallStats*.log`: llamadas remotas mas largas, elapsed/wait/I/O time, bytes de red, operacion, objetivo y cliente.
   - `scriptEvent.log` o `FMSEScriptErrors.log`: fallos de scripts programados y errores de guion.
   - `Stats.log`: tendencias de recursos del servidor cuando exista.
   - `fmdapi.log`: actividad y fallos de FileMaker Data API cuando exista.
6. Separa evidencia de inferencia. Di "los logs muestran" para hechos directos y "probablemente" para hipotesis de causa raiz.
7. Preserva privacidad: evita volcar nombres de cuenta completos, inventarios de IP o bloques crudos salvo que el usuario lo pida.

## Triage De Rendimiento

Trata `TopCallStats.log` y `TopCallStats-old.log` como dataset de rendimiento separado. Estos archivos muestran hasta 25 peticiones de cliente con mayor elapsed time por intervalo de recogida, no todas las peticiones.

Prioriza:

- Operaciones con mayor `Total Elapsed` y `Elapsed Time`.
- Ratios altos de `Wait Time`, que sugieren contencion con otros clientes.
- Ratios altos de `I/O Time`, que sugieren presion de disco/almacenamiento.
- Pares `Operation` + `Target` repetidos en varios intervalos.
- Busquedas, indexacion, subidas/descargas o layouts/campos que dominen el uso diario.
- Clientes o bases de datos que aparezcan repetidamente en llamadas lentas.

Reporta TopCallStats en tablas ordenadas: operacion, objetivo, cliente, cuenta, max elapsed, p95/promedio si hay suficientes filas, ratio wait, ratio I/O y totales de red in/out. Convierte microsegundos a ms/segundos para legibilidad.

Para ejemplos de llamadas lentas, no repitas las primeras N filas si son la misma operacion/objetivo/cliente en muestras adyacentes. Deduplica por `Operation` + `Target` + `Client Name`, conserva la peor fila y reporta count, max elapsed, p95/promedio si procede, senal wait/I/O y una nota humana.

Cuando exista un DDR autorizado para la base analizada, traduce IDs tecnicos de `TopCallStats` antes de reportar:

- `<DATABASE>::tabla(<TABLE_ID>)` debe resolverse al nombre real de tabla/base table del DDR y conservar el ID solo como apoyo.
- `definiciones de campos(2)` debe resolverse al nombre real del campo.
- Para IDs largos, resuelve el ancla como `<tableId><fieldId>FieldAnchor_`, por ejemplo tabla `129` + campo `51693` -> `12951693FieldAnchor_`.
- Si no se puede traducir, conserva el ID original y marcalo como no resuelto.

## Triage Operativa

Para `Event.log`, agrupa hallazgos por:

- Arranques/paradas de servidor y reinicios inesperados.
- Archivos no cerrados correctamente, comprobaciones de coherencia, mensajes de recuperacion/restauracion.
- Fallos de schedules, schedules omitidos, errores de guion o schedules largos.
- Warnings/errores de configuracion detectados por Database Server.
- Apertura/cierre de bases cerca de incidentes.

Para `Access.log`, agrupa hallazgos por:

- Picos de login/conexion y tormentas de desconexion.
- Acceso denegado por limites de conexion.
- Acceso con cuenta Guest.
- Conexiones repetidas del mismo cliente/IP.
- Acceso a bases por cuenta y tipo de cliente cuando este disponible.

Cuando el usuario pida "problemas de rendimiento u otro tipo de problemas", incluye siempre una seccion de rendimiento y otra operativa/seguridad, aunque una diga que no se ha encontrado un problema claro.

## Patrones Frecuentes

- `Access.log` mensaje `730` con texto SSO no es el error FileMaker de Excel. Interpretalo como intento fallido de autenticacion SSO/inicio de sesion unico. Si despues aparece apertura correcta de la base con la misma cuenta, puede ser ruido de fallback; si no, revisar AD/SSO, grupos externos, `fmapp`, DNS/FQDN y hora del servidor.
- Un error `9 - Privilegios insuficientes` en un schedule Data API puede originarse en un subguion o paso de inicio, no necesariamente en la accion principal. Revisa la cadena de guiones, el conjunto de privilegios, `fmrest` y si ciertos pasos deben omitirse en sesiones Data API.
- `TopCallStats` operacion `Comparar recuentos de modificacion` indica comprobaciones de sincronizacion/cambios entre cliente y servidor. No es un error de seguridad; suele apuntar a layouts, relaciones, portales, listas, calculos no almacenados, ordenaciones o datos relacionados caros para el cliente indicado.

## Informe De Codigos De Error

Para `scriptEvent.log`, `FMSEScriptErrors.log`, `fmdapi.log`, schedules y Data API, no informes solo numeros. Adjunta la descripcion FileMaker desde [references/filemaker-error-codes.md](references/filemaker-error-codes.md), e indica si el codigo pertenece a REST/Data API o Web Publishing cuando aplique.

Usa bloques humanos compactos:

- `Codigo`: `401 - Ningun registro coincide con la peticion`, no solo `401`.
- `Impacto probable`: explica el significado en el contexto local, por ejemplo busqueda sin resultados o privilegios insuficientes.
- `Donde se repite`: incluye schedule, guion FileMaker y paso exacto cuando exista, por ejemplo `<SCHEDULE> en <SCRIPT> : <STEP> : Insert from URL`.
- `Ocurrencias`: count.
- `Primer/ultimo`: rango de fechas cuando ayude.

Los codigos recurrentes `401`, `101`, `301`, `103` y `10`, ademas de "clientes no responden", pueden ser condiciones controladas por guiones o logica de sesion. No presupongas que son ruido: evalua frecuencia, contexto, manejo del error e impacto antes de asignar severidad.

Para rankings, reduce ruido: menciona totales de `401`, `101` y `301` en texto, pero omitelos de tablas "top 10 errores mas frecuentes" y "pasos con error mas repetidos". No incluyas "cliente no responde" / Event code `30` como hallazgo operativo salvo que el usuario pida analizar desconexiones.

En tablas de frecuencia de endpoints Data API, omite endpoints de login/sesion como `POST .../sessions` y `DELETE .../sessions/{token}`. En secciones `fmdapi.log`, muestra siempre `codigo - descripcion`.

## Formato De Salida

Por defecto responde en castellano si el usuario escribe en castellano. Mantén informes concisos pero con evidencia:

- `Resumen ejecutivo`: 3-6 bullets con severidad.
- `Hallazgos`: problemas ordenados con evidencia y timestamps.
- `TopCallStats`: tabla o subseccion separada para coste diario de transacciones/recursos.
- `Correlaciones`: eventos coincidentes entre logs.
- `Siguientes pasos`: comprobaciones o acciones FileMaker concretas, no consejos genericos.

Incluye rutas y numeros de linea cuando sea practico. Si hay logs rotados, indica que generaciones se incluyeron.

No uses por defecto tablas Markdown con tuberias para informes que se leeran como `.md` crudo en editor; son dificiles de escanear. Prefiere secciones numeradas, bullets y bloques repetidos tipo tarjeta. Usa tablas solo para matrices pequenas con valores cortos.

Cuando el usuario pida tablas responsivas o lectura pulida en navegador, crea tambien un informe `.html` con CSS responsive y enlazalo desde el Markdown. El HTML debe aplicar los mismos criterios de severidad, mostrar descripciones de errores Data API, excluir endpoints de sesion/login de rankings de negocio y traducir IDs tecnicos cuando haya un DDR autorizado.

## Recursos Incluidos

- `scripts/analyze_fms_logs.py`: analizador base para logs FileMaker Server tabulados y de texto.
- `references/claris-log-reference.md`: referencia compacta derivada de Claris para Event, Access y Top Call Statistics.
- `references/filemaker-error-codes.md`: descripciones de codigos de error FileMaker y reglas de reporte legible.
