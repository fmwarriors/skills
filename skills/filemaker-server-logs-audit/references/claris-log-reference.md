# Claris FileMaker Server log reference

Sources checked from Claris FileMaker Server Help:

- Top call statistics log: https://help.claris.com/en/server-help/content/monitor-top-call-log.html
- Event log: https://help.claris.com/en/server-help/content/monitor-event-log.html
- Access log: https://help.claris.com/en/server-help/content/monitor-access-log.html

## Event.log

Claris says Event.log is a tab-delimited file created in `FileMaker Server/Logs/`. It is enabled by default while the Database Server is running.

Use it for:

- Database Server starting or stopping.
- Database files opened and closed by the Database Server.
- Consistency checks for files not closed properly.
- New, completed, upcoming, and currently running schedules.
- Reasons enabled schedules were not successful.
- FileMaker script schedule errors.
- Configuration errors and conditions detected by the Database Server.
- Server property settings at startup and settings changed during a session.
- Startup restoration status and restored database information.

Windows also records these events in the Windows Application Log. When Event.log reaches the configured size limit it rotates to `Event-old.log`.

## Access.log

Claris says Access.log is a tab-delimited file created in `FileMaker Server/Logs/` and contains information-level messages only. Warning and error-level messages are in Event.log.

Use it for:

- Clients connecting to and disconnecting from the Database Server.
- Databases accessed with named accounts or Guest.
- Clients denied access due to FileMaker Pro, FileMaker Go, WebDirect, or Data API connection limits.

When Access.log reaches the configured size limit it rotates to `Access-old.log`.

## TopCallStats.log

Claris says TopCallStats.log is created only when Top Call Statistics is enabled in Logs > Log Settings. It can identify hosted database performance problems, but the logging process can negatively affect server performance, so disable it when detailed analysis is no longer needed.

It records the client requests, up to 25 per collection interval, with the longest elapsed time. Treat it as a sampled "slow call" log, not a complete transaction ledger.

Important columns:

- `Timestamp`: Database Server timestamp for the collection interval.
- `Start Time` and `End Time`: seconds.fraction since Database Server startup; end can be empty for calls in progress.
- `Total Elapsed`: total microseconds elapsed for the remote call so far.
- `Operation`: remote call name, for example Query, Upload, Download; some values include task progress such as indexing percent.
- `Target`: hosted file plus table/field/layout details when available.
- `Network Bytes In` and `Network Bytes Out`: client/server bytes during the interval.
- `Elapsed Time`: microseconds elapsed in this interval.
- `Wait Time`: microseconds waiting for other clients in this interval.
- `I/O Time`: microseconds waiting for disk input/output in this interval.
- `Client Name`: client name, IP, or WebDirect identifier.

When the size limit is reached, it rotates to `TopCallStats-old.log`.

## Interpretation guardrails

- Convert microseconds before reporting: 1,000,000 microseconds = 1 second.
- High wait ratio means contention is plausible; high I/O ratio means storage pressure is plausible.
- Repeated expensive operation + target combinations are more actionable than one isolated spike.
- Correlate TopCallStats timestamps with Event.log restarts, schedule activity, backups, and script errors before assigning root cause.
- In Spanish-localized logs, headers and messages may be translated; rely on column positions and normalized headers when possible.
