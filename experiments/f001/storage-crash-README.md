# Storage Crash Model

Run: `python3 storage_crash_model.py`

The model explores crashes around simplified write-ahead-log and copy-on-write publication steps and checks the old-or-new recovery property. It is deliberately a tiny transaction model.

Important limitations: it assumes atomic individual abstract steps and does not model torn sectors, volatile device caches, flush/FUA ordering, checksums, concurrent writers, log corruption, allocator metadata, or real power loss. The in-place contrast also assumes one atomic overwrite and therefore is not a realistic general filesystem model.
