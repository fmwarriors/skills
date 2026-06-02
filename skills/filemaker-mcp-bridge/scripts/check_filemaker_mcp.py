#!/usr/bin/env python3
"""
check_filemaker_mcp.py — read-only detector for the two FileMaker MCP servers.

Reports, per server, whether the npm package is installed and whether an MCP
config entry exists in the known host config files, then prints remediation.

This script NEVER installs anything or edits any file. It only reads.

Exit code: 0 if both servers are usable, 1 otherwise.
"""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

HOME = Path.home()

# Known MCP host config files (Claude Code project/user + Claude Desktop on macOS).
CONFIG_PATHS = [
    Path.cwd() / ".mcp.json",
    HOME / ".claude.json",
    HOME / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json",
]

SERVERS = {
    "filemaker-odata": {
        "package": "filemaker-odata-mcp",
        "needs_global": False,  # runs via `npx -y`, no install required
        "purpose": "standards-based schema, tables, fields, relationships, CRUD, aggregations (the DEFAULT layer)",
    },
    "filemaker-dapi": {
        "package": "filemaker-data-api-mcp",
        "binary": "filemaker-mcp",
        "needs_global": True,   # `command: filemaker-mcp` must be on PATH
        "purpose": "FileMaker-proprietary layouts, scripts, containers, global fields (the FALLBACK layer)",
    },
}


def npm_global_packages():
    """Return set of globally installed npm package names (best-effort)."""
    npm = shutil.which("npm")
    if not npm:
        return None  # npm not found -> cannot determine
    try:
        out = subprocess.run(
            [npm, "ls", "-g", "--depth=0", "--json"],
            capture_output=True, text=True, timeout=30,
        )
        data = json.loads(out.stdout or "{}")
        return set((data.get("dependencies") or {}).keys())
    except Exception:
        return None


def find_config_entries():
    """Scan known config files; return {server_key: [config_file_paths]}.

    Tries structured parsing first (top-level and per-project mcpServers), then
    falls back to a raw substring scan so entries in host config layouts not
    modelled here are still detected rather than reported as missing.
    """
    found = {key: [] for key in SERVERS}
    for path in CONFIG_PATHS:
        try:
            if not path.is_file():
                continue
            raw = path.read_text(encoding="utf-8")
        except Exception:
            continue
        matched = set()
        try:
            data = json.loads(raw)
            blocks = []
            if isinstance(data.get("mcpServers"), dict):
                blocks.append(data["mcpServers"])
            for proj in (data.get("projects") or {}).values():
                if isinstance(proj, dict) and isinstance(proj.get("mcpServers"), dict):
                    blocks.append(proj["mcpServers"])
            for servers in blocks:
                for key in SERVERS:
                    if key in servers:
                        matched.add(key)
        except Exception:
            pass
        # Raw fallback: catch keys in structures not modelled above.
        for key in SERVERS:
            if key not in matched and f'"{key}"' in raw:
                matched.add(key)
        for key in matched:
            found[key].append(str(path))
    return found


def main():
    globals_set = npm_global_packages()
    config_entries = find_config_entries()
    all_ok = True

    print("FileMaker MCP Bridge — environment check\n" + "=" * 42)
    for key, meta in SERVERS.items():
        pkg = meta["package"]
        binary = meta.get("binary")
        installed = None
        if globals_set is not None:
            installed = pkg in globals_set
        elif binary:
            installed = shutil.which(binary) is not None

        configured = bool(config_entries[key])

        # Usable rule: dapi needs the binary/global install; odata can run via npx.
        if meta["needs_global"]:
            usable = bool(installed) and configured
        else:
            usable = configured  # npx fetches on demand

        status = "OK" if usable else "ACTION NEEDED"
        all_ok = all_ok and usable

        print(f"\n[{key}]  {status}")
        print(f"  purpose      : {meta['purpose']}")
        inst_str = {True: "yes", False: "no", None: "unknown (npm not found)"}[installed]
        print(f"  npm package  : {pkg} (global install: {inst_str})")
        if configured:
            print(f"  config entry : found in {', '.join(config_entries[key])}")
        else:
            print(f"  config entry : NOT FOUND in any known config file")

        if not usable:
            print("  remediation  :")
            if meta["needs_global"] and not installed:
                print(f"      • install: npm install -g {pkg}")
            if not configured:
                other = "filemaker-dapi" if key == "filemaker-odata" else "filemaker-odata"
                print(f"      • add a '{key}' entry to your MCP config")
                if config_entries[other]:
                    print(f"        (derive it from the working '{other}' entry — "
                          "see references/config-and-install.md; same creds, "
                          "different FM_SERVER format)")
                print("      • restart the MCP host to load it")

    print("\n" + "=" * 42)
    if all_ok:
        print("Both servers are usable. OData is the default; DAPI handles layouts & scripts.")
    else:
        print("One or more servers need attention. See remediation above and "
              "references/config-and-install.md. Ask the user before installing or editing config.")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
