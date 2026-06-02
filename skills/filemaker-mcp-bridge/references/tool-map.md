# Tool Map — filemaker-odata + filemaker-dapi

Complete inventory of both MCP servers and how their tools pair up. Tool names are
the MCP tool identifiers (the host may prefix them with the server name).

## filemaker-odata (package `filemaker-odata-mcp`) — 26 tools

OData 4.01 layer. The standards-based default for all schema, data, and analytics.

**Discovery (3)**
- `fm_odata_list_tables` — enumerate base tables.
- `fm_odata_get_metadata` — full OData `$metadata` (fields, types, relationships).
- `fm_odata_get_service_document` — service root / entity sets.

**Queries (4)**
- `fm_odata_query_records` — filter/sort/select/paginate/`$expand`.
- `fm_odata_get_record` — single record by key.
- `fm_odata_get_records` — straight record list.
- `fm_odata_count_records` — server-side count.

**CRUD (3)**
- `fm_odata_create_record`, `fm_odata_update_record`, `fm_odata_delete_record`.

**FM 2024/2025+ analytics (3)**
- `fm_odata_aggregate` — server-side grouping/sum/count (DAPI cannot do this).
- `fm_odata_cast` — type casting.
- `fm_odata_build_filter` — parameterized filter construction.

**Connection (5)**
- `fm_odata_connect`, `fm_odata_connect_multi`, `fm_odata_set_connection`,
  `fm_odata_list_connections`, `fm_odata_get_current_connection`.

**Sessions (2)**
- `fm_odata_list_active_sessions`, `fm_odata_describe_sessions`.

**Config (5)**
- `fm_odata_config_add_connection`, `fm_odata_config_remove_connection`,
  `fm_odata_config_list_connections`, `fm_odata_config_get_connection`,
  `fm_odata_config_set_default_connection`.

## filemaker-dapi (package `filemaker-data-api-mcp`, binary `filemaker-mcp`) — 28 tools

FileMaker Data API layer. The fallback for FileMaker-proprietary constructs only.

**Authentication (3)**
- `fm_login`, `fm_logout`, `fm_validate_session`.

**Metadata (5)** — note `fm_get_layouts`, `fm_get_scripts`, `fm_get_layout_metadata` are the proprietary value
- `fm_get_product_info`, `fm_get_databases`, `fm_get_layouts`, `fm_get_scripts`,
  `fm_get_layout_metadata`.

**Records (7)** — prefer OData for these unless the *layout context* matters
- `fm_get_records`, `fm_get_record_by_id`, `fm_create_record`, `fm_edit_record`,
  `fm_delete_record`, `fm_duplicate_record`, `fm_find_records`.

**Container fields (2)** — proprietary
- `fm_upload_to_container`, `fm_upload_to_container_repetition`.

**Global fields (1)** — proprietary
- `fm_set_global_fields`.

**Scripts (1)** — proprietary
- `fm_execute_script`.

**Configuration (5)**
- `fm_config_add_connection`, `fm_config_remove_connection`,
  `fm_config_list_connections`, `fm_config_get_connection`,
  `fm_config_set_default_connection`.

**Connections (4)**
- `fm_set_connection`, `fm_connect`, `fm_list_connections`,
  `fm_get_current_connection`.

## Complementary pairings

Use these when a task spans both layers:

| Goal | OData part | DAPI part |
|---|---|---|
| Understand a table fully | `fm_odata_get_metadata` → true field types & relationships | `fm_get_layout_metadata` → how a layout exposes/renames those fields |
| Document the whole solution | tables, fields, relationships, counts | layouts, scripts, value lists |
| Run business logic then read result | read/verify with `fm_odata_query_records` | trigger with `fm_execute_script` |
| Reconcile model vs. UI | base tables & fields | layouts & layout-fields (alias detection) |
| Bulk analytics | `fm_odata_aggregate` | — (not available) |
| Store a file in a record | — | `fm_upload_to_container` |

## Overlap rule

Both servers can do record CRUD. **Always prefer OData** for CRUD/queries —
standards-based, supports `$expand`/aggregation/paging. Use DAPI record tools
only when the operation depends on a specific FileMaker layout context.
