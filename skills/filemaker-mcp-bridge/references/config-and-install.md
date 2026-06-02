# Configuration & Installation

How to install and configure each server, and how to derive one server's config
from the other. **Always ask for confirmation before running npm or editing any
config file.**

## Canonical MCP config blocks

These go in the `mcpServers` object of the relevant config file (see "Where config
lives" below). Values shown are an example; copy database + credentials from the
working server.

```jsonc
"filemaker-dapi": {
  "command": "filemaker-mcp",
  "args": ["start"],
  "env": {
    "FM_SERVER": "192.168.0.24",        // BARE host/IP — no scheme
    "FM_DATABASE": "Contacts",
    "FM_USER": "admin",
    "FM_PASSWORD": "wakawaka",
    "FM_VERSION": "vLatest"             // DAPI-only
  }
},
"filemaker-odata": {
  "command": "npx",
  "args": ["-y", "filemaker-odata-mcp"],
  "env": {
    "FM_DATABASE": "Contacts",
    "FM_PASSWORD": "wakawaka",
    "FM_SERVER": "https://192.168.0.24", // FULL URL — include scheme
    "FM_USER": "admin",
    "FM_VERIFY_SSL": "false"            // OData-only; false for self-signed / IP
  }
}
```

## Installation commands

- **filemaker-dapi**: requires a global install so the `filemaker-mcp` binary is on PATH.
  ```bash
  npm install -g filemaker-data-api-mcp
  ```
  Verify: `command -v filemaker-mcp` and `filemaker-mcp --version` (or `filemaker-mcp config`).

- **filemaker-odata**: the canonical config uses `npx -y filemaker-odata-mcp`, which
  fetches on first run — **no install step required**. A global install is optional:
  ```bash
  npm install -g filemaker-odata-mcp   # optional; then command can be "filemaker-odata-mcp"
  ```

Source repos (for reference / troubleshooting / version pinning):
- OData: https://github.com/fsans/FMS-ODATA-MCP
- Data API: https://github.com/fsans/FileMaker-Server-DAPI-MCP

## Deriving one config from the other

Credentials and database are **identical** across both servers. Only `FM_SERVER`
formatting and the optional key differ. To generate the missing server's `env`:

**From filemaker-odata → filemaker-dapi**
1. Copy `FM_DATABASE`, `FM_USER`, `FM_PASSWORD` verbatim.
2. `FM_SERVER`: strip the scheme and any trailing path. `https://192.168.0.24` → `192.168.0.24`.
3. Drop `FM_VERIFY_SSL` / `FM_TIMEOUT`. Add `FM_VERSION` (default `vLatest`).
4. Set `command: "filemaker-mcp"`, `args: ["start"]`.

**From filemaker-dapi → filemaker-odata**
1. Copy `FM_DATABASE`, `FM_USER`, `FM_PASSWORD` verbatim.
2. `FM_SERVER`: prepend `https://` if no scheme present. `192.168.0.24` → `https://192.168.0.24`.
3. Drop `FM_VERSION`. Add `FM_VERIFY_SSL` — use `"false"` for an IP address or a
   self-signed cert, `"true"` for a host with a valid public certificate.
4. Set `command: "npx"`, `args: ["-y", "filemaker-odata-mcp"]`.

## Optional environment variables

| Var | Server | Default | Use |
|---|---|---|---|
| `FM_VERSION` | dapi | `vLatest` | Pin Data API version |
| `FM_VERIFY_SSL` | odata | `true` | Set `false` for self-signed certs / IP hosts |
| `FM_TIMEOUT` | odata | `30000` (ms) | Raise for slow servers / large queries |
| `MCP_TRANSPORT` | odata | `stdio` | `http`/`https` only for remote transport setups |

## Where config lives

MCP server definitions can live in several places depending on the host. When
adding a server, detect which file already contains the *working* server and add
the new one alongside it. Common locations:

- **Claude Code (project)**: `.mcp.json` in the project root.
- **Claude Code (user)**: `~/.claude.json` (per-project `mcpServers` blocks).
- **Claude Desktop (macOS)**: `~/Library/Application Support/Claude/claude_desktop_config.json`.

After editing, the MCP host must be restarted/reloaded to pick up the new server.
Inform the user of this.

## Common configuration mistakes

1. **Wrong `FM_SERVER` format** — OData needs the `https://` scheme; DAPI must NOT
   have it. Swapping these is the #1 cause of "connection refused" / parse errors.
2. **SSL verification on a self-signed server** — OData defaults `FM_VERIFY_SSL=true`;
   set it `false` for IP addresses or self-signed certs, or connections fail.
3. **Missing global install for DAPI** — `command: "filemaker-mcp"` fails if the
   package was not installed with `-g`.
