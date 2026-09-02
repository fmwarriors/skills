#!/usr/bin/env python3
"""Baseline analyzer for Claris FileMaker Server logs.

Reads a FileMaker Server log directory and emits a JSON summary focused on
operational problems plus TopCallStats performance cost.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import re
import statistics
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable


ENCODINGS = ("utf-8-sig", "utf-8", "cp1252", "latin-1")

EVENT_NAMES = {"event.log", "event-old.log"}
ACCESS_NAMES = {"access.log", "access-old.log"}
TOPCALL_RE = re.compile(r"^topcallstats(?:-old)?\.log$", re.IGNORECASE)
STATS_RE = re.compile(r"^stats(?:-old)?\.log$", re.IGNORECASE)
SCRIPT_RE = re.compile(r"^(?:scriptEvent|FMSEScriptErrors)(?:-old)?\.log$", re.IGNORECASE)
FMDAPI_RE = re.compile(r"^fmdapi(?:-old)?\.log$", re.IGNORECASE)


ISSUE_PATTERNS = [
    "error",
    "advertencia",
    "warning",
    "failed",
    "fallo",
    "fallido",
    "no se ha",
    "no pudo",
    "not successful",
    "deneg",
    "denied",
    "limit",
    "limite",
    "consistency",
    "coherencia",
    "no se cerro",
    "not closed",
    "restaur",
    "restor",
    "abort",
    "timeout",
    "certificate",
    "certificado",
]


def read_lines(path: Path) -> tuple[list[str], str]:
    data = path.read_bytes()
    for enc in ENCODINGS:
        try:
            return data.decode(enc).splitlines(), enc
        except UnicodeDecodeError:
            continue
    return data.decode("latin-1", errors="replace").splitlines(), "latin-1-replace"


def norm(value: Any) -> str:
    text = "" if value is None else str(value)
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = text.lower().strip()
    text = text.replace("\u00c3\u00b3", "o").replace("\u00c3\u00a9", "e")
    text = text.replace("\u00c3\u00a1", "a").replace("\u00c3\u00ad", "i")
    text = text.replace("\u00c3\u00ba", "u").replace("\u00c3\u00b1", "n")
    text = re.sub(r"\s+", " ", text)
    return text


def number(value: Any) -> float | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    text = text.replace(" ", "").replace(",", ".")
    try:
        return float(text)
    except ValueError:
        return None


def micros_to_seconds(value: float | None) -> float | None:
    if value is None:
        return None
    return round(value / 1_000_000, 6)


def safe_ratio(part: float | None, whole: float | None) -> float | None:
    if not part or not whole or whole <= 0:
        return None
    return round(part / whole, 4)


def percentile(values: list[float], pct: float) -> float | None:
    if not values:
        return None
    values = sorted(values)
    if len(values) == 1:
        return values[0]
    pos = (len(values) - 1) * pct
    low = math.floor(pos)
    high = math.ceil(pos)
    if low == high:
        return values[int(pos)]
    return values[low] * (high - pos) + values[high] * (pos - low)


def get(row: dict[str, Any], aliases: Iterable[str]) -> Any:
    lookup = row.get("_norm")
    if lookup is None:
        lookup = {norm(k): v for k, v in row.items() if not str(k).startswith("_")}
    for alias in aliases:
        key = norm(alias)
        if key in lookup:
            return lookup[key]
    for key, value in lookup.items():
        if any(norm(alias) in key for alias in aliases):
            return value
    return None


def dict_rows(path: Path) -> tuple[list[dict[str, Any]], str]:
    lines, enc = read_lines(path)
    if not lines:
        return [], enc
    reader = csv.DictReader(lines, delimiter="\t")
    rows: list[dict[str, Any]] = []
    for idx, row in enumerate(reader, start=2):
        clean = {k or f"column_{i}": v for i, (k, v) in enumerate(row.items(), start=1)}
        clean["_line"] = idx
        clean["_file"] = str(path)
        clean["_norm"] = {norm(k): v for k, v in clean.items() if not str(k).startswith("_")}
        rows.append(clean)
    return rows, enc


def fixed_log_rows(path: Path) -> tuple[list[dict[str, Any]], str]:
    lines, enc = read_lines(path)
    rows = []
    for idx, line in enumerate(lines, start=1):
        parts = line.split("\t")
        if len(parts) >= 5:
            rows.append(
                {
                    "_file": str(path),
                    "_line": idx,
                    "timestamp": parts[0],
                    "level": parts[1],
                    "message_id": parts[2],
                    "source": parts[3],
                    "message": "\t".join(parts[4:]),
                }
            )
        elif line.strip():
            rows.append(
                {
                    "_file": str(path),
                    "_line": idx,
                    "timestamp": "",
                    "level": "",
                    "message_id": "",
                    "source": "",
                    "message": line,
                }
            )
    return rows, enc


def summarize_inventory(files: list[Path]) -> list[dict[str, Any]]:
    return [
        {
            "file": str(path),
            "name": path.name,
            "bytes": path.stat().st_size,
            "last_write_time": path.stat().st_mtime,
        }
        for path in sorted(files, key=lambda p: p.name.lower())
    ]


def summarize_topcalls(paths: list[Path], limit: int) -> dict[str, Any]:
    records = []
    encodings = {}
    for path in paths:
        rows, enc = dict_rows(path)
        encodings[str(path)] = enc
        for row in rows:
            elapsed = number(get(row, ["Tiempo transcurrido", "Elapsed Time"]))
            total_elapsed = number(get(row, ["Tiempo total transcurrido", "Total Elapsed"]))
            wait = number(get(row, ["Tiempo de espera", "Wait Time"]))
            io_time = number(get(row, ["Tiempo de E/S", "I/O Time", "IO Time"]))
            net_in = number(get(row, ["Entrada de bytes de red", "Network Bytes In"]))
            net_out = number(get(row, ["Salida de bytes de red", "Network Bytes Out"]))
            records.append(
                {
                    "file": str(path),
                    "line": row.get("_line"),
                    "timestamp": get(row, ["Fecha y hora", "Timestamp"]),
                    "operation": get(row, ["Operacion", "Operation"]),
                    "target": get(row, ["Objetivo", "Target"]),
                    "client": get(row, ["Nombre del cliente", "Client Name"]),
                    "elapsed_us": elapsed,
                    "total_elapsed_us": total_elapsed,
                    "wait_us": wait,
                    "io_us": io_time,
                    "network_bytes_in": net_in,
                    "network_bytes_out": net_out,
                    "wait_ratio": safe_ratio(wait, elapsed),
                    "io_ratio": safe_ratio(io_time, elapsed),
                }
            )

    elapsed_values = [r["elapsed_us"] for r in records if r["elapsed_us"] is not None]
    total_values = [r["total_elapsed_us"] for r in records if r["total_elapsed_us"] is not None]

    groups: dict[tuple[str, str], dict[str, Any]] = {}
    for r in records:
        key = (str(r.get("operation") or ""), str(r.get("target") or ""))
        g = groups.setdefault(
            key,
            {
                "operation": key[0],
                "target": key[1],
                "count": 0,
                "elapsed_values": [],
                "total_elapsed_values": [],
                "wait_us": 0.0,
                "io_us": 0.0,
                "network_bytes_in": 0.0,
                "network_bytes_out": 0.0,
                "clients": Counter(),
            },
        )
        g["count"] += 1
        if r["elapsed_us"] is not None:
            g["elapsed_values"].append(r["elapsed_us"])
        if r["total_elapsed_us"] is not None:
            g["total_elapsed_values"].append(r["total_elapsed_us"])
        g["wait_us"] += r["wait_us"] or 0
        g["io_us"] += r["io_us"] or 0
        g["network_bytes_in"] += r["network_bytes_in"] or 0
        g["network_bytes_out"] += r["network_bytes_out"] or 0
        if r.get("client"):
            g["clients"][str(r["client"])] += 1

    grouped = []
    for g in groups.values():
        elapsed = g.pop("elapsed_values")
        total_elapsed = g.pop("total_elapsed_values")
        clients = g.pop("clients")
        elapsed_sum = sum(elapsed)
        grouped.append(
            {
                **g,
                "elapsed_sum_s": micros_to_seconds(elapsed_sum),
                "elapsed_max_s": micros_to_seconds(max(elapsed) if elapsed else None),
                "elapsed_avg_s": micros_to_seconds(statistics.mean(elapsed) if elapsed else None),
                "elapsed_p95_s": micros_to_seconds(percentile(elapsed, 0.95)),
                "total_elapsed_max_s": micros_to_seconds(max(total_elapsed) if total_elapsed else None),
                "wait_ratio": safe_ratio(g["wait_us"], elapsed_sum),
                "io_ratio": safe_ratio(g["io_us"], elapsed_sum),
                "top_clients": clients.most_common(5),
            }
        )

    top_slow = sorted(
        records,
        key=lambda r: (r["elapsed_us"] or r["total_elapsed_us"] or 0),
        reverse=True,
    )[:limit]

    return {
        "files": [str(p) for p in paths],
        "encodings": encodings,
        "record_count": len(records),
        "elapsed_max_s": micros_to_seconds(max(elapsed_values) if elapsed_values else None),
        "elapsed_p95_s": micros_to_seconds(percentile(elapsed_values, 0.95)),
        "total_elapsed_max_s": micros_to_seconds(max(total_values) if total_values else None),
        "top_slow_calls": [
            {
                **r,
                "elapsed_s": micros_to_seconds(r["elapsed_us"]),
                "total_elapsed_s": micros_to_seconds(r["total_elapsed_us"]),
                "wait_s": micros_to_seconds(r["wait_us"]),
                "io_s": micros_to_seconds(r["io_us"]),
            }
            for r in top_slow
        ],
        "top_operation_targets": sorted(
            grouped,
            key=lambda r: (r["elapsed_sum_s"] or 0, r["count"]),
            reverse=True,
        )[:limit],
    }


def scan_fixed_logs(paths: list[Path], limit: int) -> dict[str, Any]:
    all_rows = []
    encodings = {}
    for path in paths:
        rows, enc = fixed_log_rows(path)
        encodings[str(path)] = enc
        all_rows.extend(rows)

    levels = Counter(norm(r["level"]) for r in all_rows if r.get("level"))
    message_ids = Counter(str(r["message_id"]) for r in all_rows if r.get("message_id"))
    sources = Counter(str(r["source"]) for r in all_rows if r.get("source"))

    issue_rows = []
    for r in all_rows:
        text = norm(" ".join([str(r.get("level", "")), str(r.get("message", ""))]))
        if any(pat in text for pat in ISSUE_PATTERNS):
            issue_rows.append(r)

    issue_messages = Counter(norm(r["message"])[:180] for r in issue_rows)

    return {
        "files": [str(p) for p in paths],
        "encodings": encodings,
        "record_count": len(all_rows),
        "levels": levels.most_common(),
        "top_message_ids": message_ids.most_common(limit),
        "top_sources": sources.most_common(limit),
        "issue_count": len(issue_rows),
        "top_issue_messages": issue_messages.most_common(limit),
        "sample_issues": issue_rows[:limit],
    }


def summarize_access(paths: list[Path], limit: int) -> dict[str, Any]:
    base = scan_fixed_logs(paths, limit)
    rows = []
    for path in paths:
        parsed, _ = fixed_log_rows(path)
        rows.extend(parsed)

    client_re = re.compile(r'cliente "([^"]+)"', re.IGNORECASE)
    ip_re = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
    clients = Counter()
    ips = Counter()
    actions = Counter()
    guest_rows = []
    denied_rows = []

    for r in rows:
        message = str(r.get("message", ""))
        normalized = norm(message)
        for match in client_re.finditer(message):
            clients[match.group(1)] += 1
        for match in ip_re.finditer(message):
            ips[match.group(0)] += 1
        if "abriendo una conexion" in normalized or "opening a connection" in normalized:
            actions["connections_opened"] += 1
        if "cerrando una conexion" in normalized or "closing a connection" in normalized:
            actions["connections_closed"] += 1
        if "abriendo la base de datos" in normalized or "opening database" in normalized:
            actions["databases_opened"] += 1
        if "cerrando la base de datos" in normalized or "closing database" in normalized:
            actions["databases_closed"] += 1
        if "guest" in normalized or "invitado" in normalized:
            guest_rows.append(r)
        if "deneg" in normalized or "denied" in normalized or "limit" in normalized or "limite" in normalized:
            denied_rows.append(r)

    base.update(
        {
            "actions": dict(actions),
            "top_clients": clients.most_common(limit),
            "top_ips": ips.most_common(limit),
            "guest_access_count": len(guest_rows),
            "denied_or_limit_count": len(denied_rows),
            "sample_guest_access": guest_rows[: min(5, limit)],
            "sample_denied_or_limit": denied_rows[: min(5, limit)],
        }
    )
    return base


def summarize_stats(paths: list[Path], limit: int) -> dict[str, Any]:
    rows = []
    encodings = {}
    for path in paths:
        parsed, enc = dict_rows(path)
        encodings[str(path)] = enc
        rows.extend(parsed)

    metrics = {
        "network_in_kbps": ["Entrada de KB/s de red", "Network KB/s In"],
        "network_out_kbps": ["Salida de KB/s de red", "Network KB/s Out"],
        "disk_read_kbps": ["Lectura de KB/s de disco", "Disk KB/s Read"],
        "disk_write_kbps": ["Escritura de KB/s de disco", "Disk KB/s Write"],
        "cache_hit_percent": ["% de aciertos de cache", "Cache Hit %"],
        "unsaved_cache_percent": ["% de cache sin guardar", "Unsaved Cache %"],
        "pro_clients": ["Clientes Pro", "Pro Clients"],
        "open_databases": ["Bases de datos abiertas", "Open Databases"],
        "webdirect_clients": ["Clientes de WebDirect", "WebDirect Clients"],
        "remote_calls_per_s": ["Llamadas remotas/s", "Remote Calls/s"],
        "remote_calls_in_progress": ["Llamadas remotas en curso", "Remote Calls In Progress"],
        "elapsed_per_call_us": ["Tiempo transcurrido/llamada", "Elapsed Time/Call"],
        "wait_per_call_us": ["Tiempo de espera/llamada", "Wait Time/Call"],
        "io_per_call_us": ["Tiempo de E/S/llamada", "I/O Time/Call"],
    }

    summary = {}
    for name, aliases in metrics.items():
        values = [number(get(row, aliases)) for row in rows]
        values = [v for v in values if v is not None]
        if values:
            summary[name] = {
                "max": max(values),
                "avg": round(statistics.mean(values), 4),
                "p95": round(percentile(values, 0.95) or 0, 4),
            }

    samples = []
    for row in rows:
        remote = number(get(row, metrics["remote_calls_per_s"]))
        in_progress = number(get(row, metrics["remote_calls_in_progress"]))
        wait = number(get(row, metrics["wait_per_call_us"]))
        io_time = number(get(row, metrics["io_per_call_us"]))
        score = max(remote or 0, in_progress or 0, wait or 0, io_time or 0)
        if score > 0:
            samples.append(
                {
                    "timestamp": get(row, ["Fecha y hora", "Timestamp"]),
                    "line": row.get("_line"),
                    "file": row.get("_file"),
                    "remote_calls_per_s": remote,
                    "remote_calls_in_progress": in_progress,
                    "wait_per_call_us": wait,
                    "io_per_call_us": io_time,
                    "_score": score,
                }
            )

    return {
        "files": [str(p) for p in paths],
        "encodings": encodings,
        "record_count": len(rows),
        "metrics": summary,
        "activity_samples": sorted(samples, key=lambda r: r["_score"], reverse=True)[:limit],
    }


def classify_files(root: Path) -> dict[str, list[Path]]:
    files = [p for p in root.rglob("*") if p.is_file()]
    buckets = defaultdict(list)
    for path in files:
        name = path.name.lower()
        if name in EVENT_NAMES:
            buckets["event"].append(path)
        elif name in ACCESS_NAMES:
            buckets["access"].append(path)
        elif TOPCALL_RE.match(path.name):
            buckets["topcall"].append(path)
        elif STATS_RE.match(path.name):
            buckets["stats"].append(path)
        elif SCRIPT_RE.match(path.name):
            buckets["script"].append(path)
        elif FMDAPI_RE.match(path.name):
            buckets["fmdapi"].append(path)
        else:
            buckets["other"].append(path)
    buckets["all"] = files
    return buckets


def build_report(root: Path, limit: int) -> dict[str, Any]:
    buckets = classify_files(root)
    report: dict[str, Any] = {
        "log_root": str(root),
        "inventory": summarize_inventory(buckets["all"]),
        "included_files": {k: [str(p) for p in v] for k, v in buckets.items() if k != "all"},
    }

    if buckets["topcall"]:
        report["topcallstats"] = summarize_topcalls(buckets["topcall"], limit)
    if buckets["event"]:
        report["event"] = scan_fixed_logs(buckets["event"], limit)
    if buckets["access"]:
        report["access"] = summarize_access(buckets["access"], limit)
    if buckets["stats"]:
        report["stats"] = summarize_stats(buckets["stats"], limit)
    if buckets["script"]:
        report["script_events"] = scan_fixed_logs(buckets["script"], limit)
    if buckets["fmdapi"]:
        report["fmdapi"] = scan_fixed_logs(buckets["fmdapi"], limit)

    findings = []
    top = report.get("topcallstats", {})
    if top.get("elapsed_max_s"):
        findings.append(
            {
                "severity": "info",
                "area": "performance",
                "message": f"Slowest TopCallStats interval call was {top['elapsed_max_s']} seconds.",
            }
        )
    for area in ("event", "access", "script_events", "fmdapi"):
        section = report.get(area, {})
        if section.get("issue_count"):
            findings.append(
                {
                    "severity": "review",
                    "area": area,
                    "message": f"{section['issue_count']} rows matched warning/error/failure patterns.",
                }
            )
    access = report.get("access", {})
    if access.get("denied_or_limit_count"):
        findings.append(
            {
                "severity": "review",
                "area": "access",
                "message": f"{access['denied_or_limit_count']} access rows mention denial or limits.",
            }
        )
    report["headline_findings"] = findings
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze FileMaker Server log folder.")
    parser.add_argument("log_folder", type=Path, help="Folder containing FileMaker Server logs")
    parser.add_argument("--out", type=Path, help="Write JSON report to this path")
    parser.add_argument("--limit", type=int, default=20, help="Maximum ranked rows per section")
    args = parser.parse_args()

    root = args.log_folder.expanduser().resolve()
    if not root.exists() or not root.is_dir():
        raise SystemExit(f"Log folder not found or not a directory: {root}")

    report = build_report(root, args.limit)
    text = json.dumps(report, indent=2, ensure_ascii=False)
    if args.out:
        args.out.write_text(text, encoding="utf-8")
        print(f"Wrote {args.out}")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
