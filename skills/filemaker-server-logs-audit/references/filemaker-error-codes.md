# FileMaker error code reference

Source of truth: Claris FileMaker Pro Help, "FileMaker error codes":
https://help.claris.com/es/pro-help/content/error-codes.html

Claris describes this as the table of numbered errors returned by `Get(LastError)`,
Script Debugger, and other FileMaker Platform technologies. Codes marked with an
asterisk in the Claris table are returned by the web publishing engine or a
FileMaker REST API.

When reporting logs, show codes as `code - description`; do not show bare
numbers. If the code is not listed here, check the official Claris page.

## Frequently seen codes in server logs

| Code | Description | Reporting hint |
| --- | --- | --- |
| 0 | No hay error | Treat as informational unless the log text says otherwise. |
| 3 | El comando no esta disponible | Usually context/mode/server-side incompatibility. |
| 5 | El comando no es valido | Check required calculation/options for the script step. |
| 9 | Privilegios insuficientes | Check account privilege set and script step permissions. |
| 10 | Faltan los datos solicitados | Often missing input, missing related data, or failed URL/file data. |
| 101 | Falta un registro | Common after `Go to Related Record`, `Go to Record`, or searches returning no current record. |
| 102 | Falta un campo | Check layout/table context and renamed/deleted fields. |
| 103 | Falta una relacion | Check graph relationship names and context. |
| 116 | Falta un objeto de presentacion | Check object names used by script steps. |
| 201 | No es posible modificar el campo | Field editability or privileges issue. |
| 212 | Cuenta de usuario o contrasena no validas | Authentication failure. |
| 301 | Hay otro usuario utilizando el registro | Record locking/contention. |
| 401 | Ningun registro coincide con la peticion | Search found no matching records; often expected unless the script does not handle it. |
| 507 | El valor del campo no ha superado la prueba de calculo especificada como opcion de validacion de entrada | Validation rule failure. |
| 736 | Demasiados datos que exportar para este formato; se truncaran los datos | Export size/format limitation. |
| 720 | Error al exportar; el formato de destino no admite campos repetidos | Export format limitation. |
| 800 | No es posible crear el archivo en el disco | Check path, permissions, disk, and server-side accessible folders. |
| 802 | No se puede abrir el archivo | Check path, file existence, permissions, and server-side visibility. |
| 1408 | Error extendido (ODBC) | Check the external ODBC error detail and SQL/driver response. |
| 1629 | Se ha agotado el tiempo de espera de la conexion; el valor de tiempo de espera es de 60 segundos | Network/API/Insert from URL timeout. |
| 1631 | Error de conexion | Network/API/Insert from URL connection failure. |
| 1638 | El anfitrion no permite nuevas conexiones. Intentelo de nuevo mas tarde. | Host connection capacity or temporary refusal. |
| 1708* | Parameter value is invalid | REST/Data API parameter validation. |

## Human output rules

- Group by code + schedule/script/step or code + API endpoint, not by raw line.
- Add an `Interpretacion` or `Impacto probable` column for the local context.
- For code `401`, distinguish harmless "no matches" from problematic repeated
  failures by checking whether the script handles no-found-set cases.
- For code `9`, highlight account/privilege set and server-side script context.
- For URL/API logs, trim long query strings and payloads before placing them in
  tables.
