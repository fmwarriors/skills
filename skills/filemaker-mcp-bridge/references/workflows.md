# Specialized Workflows (teamworking recipes)

Multi-step recipes that combine both servers. All follow the Core Routing
Principle: OData by default, DAPI only for layouts/scripts/containers/globals.

---

## 1. Query routing

Pick the optimal tool/endpoint per task. Decision order:

1. **Does it touch layouts, scripts, containers, or global fields?**
   → DAPI. (`fm_get_layouts`, `fm_get_scripts`, `fm_execute_script`,
   `fm_upload_to_container*`, `fm_set_global_fields`.) These have no OData equivalent.
2. **Is it grouping/summing/counting many records (analytics)?**
   → OData `fm_odata_aggregate` (FM 2024/2025+). DAPI cannot aggregate server-side;
   never pull all records to count them — use `fm_odata_count_records`.
3. **Is it reading/filtering/sorting/paging records, or following relationships?**
   → OData `fm_odata_query_records` with `$filter`/`$orderby`/`$top`/`$skip`/`$expand`.
4. **Is it plain CRUD on a known key?**
   → OData `fm_odata_*_record`.
5. **Does the operation depend on a specific FileMaker layout's behavior** (e.g. a
   find that must run in a layout's stored context)? → DAPI `fm_find_records`.

Performance notes: prefer one OData query with `$expand` over N follow-up reads;
prefer `$count`/aggregate over client-side counting; page with `$top`/`$skip`.

---

## 2. Full solution audit / documentation

Produce one merged document describing a database. Steps:

1. **Inventory (OData)**
   - `fm_odata_list_tables` → table list.
   - `fm_odata_get_metadata` → fields, types, relationships per table.
   - `fm_odata_count_records` per table → row counts (optional).
2. **Application layer (DAPI)**
   - `fm_get_layouts` → layout list.
   - `fm_get_layout_metadata` per layout → fields shown, value lists, related portals.
   - `fm_get_scripts` → script names.
3. **Merge & write**
   - Group by table: real schema (OData) + the layouts that expose it (DAPI).
   - Separate section for scripts.
   - Flag fields present in the base table but on no layout, and layout fields with
     no obvious base-table match (likely calculated/related — see workflow 3).
4. **Output** — write the report to the project's `output/` directory (this
   workspace convention) as Markdown; offer a `mermaid` ER diagram of relationships.

State clearly which facts came from OData (data model) vs. DAPI (application layer).

---

## 3. Schema reconciliation

Compare the true data model against the application layer to surface drift.

1. Pull base tables + fields via OData `fm_odata_get_metadata`.
2. Pull layouts + layout fields via DAPI `fm_get_layouts` / `fm_get_layout_metadata`.
3. Cross-reference and report:
   - **Orphan fields** — base-table fields exposed on no layout.
   - **Layout-only fields** — fields on a layout with no base-table column (calculated,
     summary, or related fields, or fields from another table occurrence).
   - **Alias mismatches** — same underlying field, different name on the layout.
   - **Type mismatches** — OData-reported type vs. how the layout treats the field.
4. Present as a table grouped by base table; note that OData sees base tables while
   DAPI sees table-occurrence/layout context, so some "mismatches" are expected
   (relationships, calculations) rather than errors.

---

## 4. Read-via-one / write-via-other (data movement)

When moving or syncing data:

- **Read** with OData (`fm_odata_query_records`) — fast, filterable, paginated.
- **Write** with OData (`fm_odata_*_record`) for plain field data; use `fm_odata_cast`
  for type coercion (FM 2024+).
- **Containers** must go through DAPI (`fm_upload_to_container`) — OData has no
  container upload. Read the target record key via OData, then upload via DAPI.
- **Post-write logic** (validation, triggers packaged as FileMaker scripts) runs via
  DAPI `fm_execute_script`.

Always verify a write by re-reading through OData.
