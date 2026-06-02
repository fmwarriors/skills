---
name: filemaker-mcp-bridge
description: Unifies the two complementary FileMaker Server MCP tools into one transparent data layer — filemaker-odata (npm filemaker-odata-mcp, standards-based schema, tables, fields, relationships, CRUD, aggregations) and filemaker-dapi (npm filemaker-data-api-mcp, binary filemaker-mcp, FileMaker-proprietary layouts, scripts, containers, global fields). Use whenever working with a FileMaker Server database through MCP (querying records, exploring schema, running aggregations, accessing layouts, executing scripts, or documenting/auditing a solution) or when either the filemaker-odata or filemaker-dapi tool is invoked. Routes every request to OData by default and falls back to the Data API only for layouts, scripts, containers, and globals, merging both into one picture. Also use when either MCP is missing or misconfigured, detecting and explaining the gap and (with confirmation) installing and configuring the missing server with the correct per-tool FM_SERVER format and environment variables.
license: Complete terms in LICENSE.txt
compatibility: FileMaker Server 19+ (Data API + OData); aggregations and casting require FileMaker Server 2024+. Requires Node.js for the MCP servers and Python 3 for the bundled check script.
metadata:
  author: FMWarriors — Francesc Sans
  version: "1.0"
  org: FMWarriors
---

# FileMaker MCP Bridge

## Overview

Two MCP servers expose a FileMaker Server database, and they are **complementary, not redundant**:

- **filemaker-odata** speaks the OData 4.01 standard. It sees the *true data model* — base tables, fields, relationships, plus CRUD, server-side filtering/sorting/paging, counting, and (FM 2024/2025+) aggregations and casting.
- **filemaker-dapi** speaks the FileMaker Data API. It sees the *application layer* that no database standard can describe — **layouts and scripts** (and their relatives: layout metadata, script execution, container fields, global fields, value lists).

This skill makes them behave as a single tool: pick the right server automatically, fall back when needed, and present one merged answer to the user.

## Core Routing Principle

**Default to OData. Fall back to the Data API only for what is FileMaker-proprietary.**

Layouts and scripts are not database standards — they are FileMaker-exclusive constructs, so only the proprietary REST API (DAPI) knows about them. Everything else is handled cleanly and standards-compliantly by OData.

| The task is about… | Use | Why |
|---|---|---|
| Tables, fields, base-table schema, relationships | **OData** (`fm_odata_list_tables`, `fm_odata_get_metadata`) | True data model |
| Reading / querying / counting records | **OData** (`fm_odata_query_records`, `fm_odata_count_records`) | Standard filter/sort/page |
| Create / update / delete records | **OData** (`fm_odata_*_record`) | Standards-based CRUD |
| Aggregations, grouping, sums (FM 2024/2025+) | **OData** (`fm_odata_aggregate`) | Server-side, DAPI cannot |
| Related-record expansion | **OData** (`$expand` via `fm_odata_query_records`) | Native OData |
| **Layouts / layout metadata / value lists** | **DAPI** (`fm_get_layouts`, `fm_get_layout_metadata`) | FileMaker-only concept |
| **Scripts (list & execute)** | **DAPI** (`fm_get_scripts`, `fm_execute_script`) | FileMaker-only concept |
| **Container fields (upload)** | **DAPI** (`fm_upload_to_container*`) | FileMaker-only concept |
| **Global fields** | **DAPI** (`fm_set_global_fields`) | FileMaker-only concept |
| Layout-context find (a stored FileMaker layout view) | **DAPI** (`fm_find_records`) | When the layout itself matters |

When a request mixes both (e.g. "document this database" or "show me the Invoices layout and its fields' real types"), gather the schema/data from OData and the layout/script detail from DAPI, then merge.

See `references/tool-map.md` for the full inventory of all ~54 tools across both servers and the complementary pairings.

## Operating Procedure

Follow these steps whenever a FileMaker task arrives or either MCP tool is invoked.

### 1. Ensure both servers are available

Both servers are normally configured. Only run a check when a tool errors as unavailable, when the user reports a problem, or when explicitly setting up. Run:

```bash
python3 scripts/check_filemaker_mcp.py
```

It reports, per server, whether the npm package is installed and whether an MCP config entry exists, and prints remediation. If one is **missing or misconfigured**:

1. Explain *why it matters* using the Core Routing Principle (e.g. "OData is present but the Data API is missing, so layout and script operations won't work").
2. **Ask for confirmation** before changing anything.
3. On approval, install and configure it following `references/config-and-install.md`, **deriving the missing server's config from the one that already works** — credentials and database are identical; only the `FM_SERVER` format and a couple of env keys differ (see below).

Never run npm or edit config files without confirmation.

### 2. Route the request

Apply the Core Routing Principle: OData by default, DAPI only for layouts/scripts/containers/globals.

### 3. Merge transparently

Enrich silently — the user should get one coherent answer, not two tool dumps. But when the answer required a DAPI fallback, **note it briefly** so the source is visible, e.g. *"(layouts/scripts via the Data API)"*. Reconcile naming: OData reports base-table and field names; DAPI reports layout and layout-field names, which may be renamed aliases of the same underlying fields.

## Configuration at a Glance

The two servers share credentials but need **different `FM_SERVER` formats and optional keys** — the single most common configuration mistake:

| Env var | filemaker-odata | filemaker-dapi |
|---|---|---|
| `FM_SERVER` | **Full URL**: `https://192.168.0.24` | **Bare host/IP**: `192.168.0.24` |
| `FM_DATABASE`, `FM_USER`, `FM_PASSWORD` | identical | identical |
| `FM_VERIFY_SSL` | `false` for self-signed/IP hosts | — (not used) |
| `FM_VERSION` | — (not used) | `vLatest` |

To derive one from the other: copy database + credentials verbatim, then add/remove the scheme on `FM_SERVER` and swap the optional key. Full canonical config blocks and install commands are in `references/config-and-install.md`.

## Specialized Workflows

For multi-step "teamworking" tasks that combine both servers, load `references/workflows.md`. It contains step-by-step recipes for:

- **Query routing** — choosing the optimal tool/endpoint per task (OData aggregates vs. DAPI scripts) for performance and correctness.
- **Full solution audit / documentation** — producing complete documentation of a database (tables, fields, relationships from OData; layouts, scripts, value lists from DAPI) as one merged report.
- **Schema reconciliation** — comparing OData base tables/fields against DAPI layouts to surface orphan fields, layout-only fields, type mismatches, and renamed aliases.

## Resources

- `scripts/check_filemaker_mcp.py` — read-only detector: reports install + config status of both servers and prints remediation.
- `references/tool-map.md` — full tool inventory of both servers and complementary pairings.
- `references/config-and-install.md` — env-var mapping, config derivation rules, canonical MCP config blocks, and install commands.
- `references/workflows.md` — specialized multi-server recipes.
