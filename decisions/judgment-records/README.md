# Judgment records

One JSON file per `ReviewRecord` (`src/toaster/evidence.py`), named `<identifier>.json`. Written
by `save_record()`, read by `load_record()` and `records_citing()`
(`src/toaster/judgment_store.py`). A chapter notebook that builds a judgment record saves it here
once, where the judgment is made; a later chapter that needs it loads it from here instead of
retyping it. See `docs/superpowers/specs/2026-10-02-judgment-record-store-design.md`.
