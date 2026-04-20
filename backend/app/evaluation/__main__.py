"""Run: python -m app.evaluation [--dataset PATH] [--out PATH] [--top-k N]"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def main() -> int:
    # Ensure repository root is on path when invoked as python -m app.evaluation from backend/
    here = Path(__file__).resolve()
    backend_root = here.parents[2]
    if str(backend_root) not in sys.path:
        sys.path.insert(0, str(backend_root))

    from app.evaluation.runner import default_dataset_path, default_report_path, run_evaluation

    p = argparse.ArgumentParser(description="RAG evaluation (keyword vs semantic)")
    p.add_argument("--dataset", type=Path, default=None, help="Path to JSON or CSV dataset")
    p.add_argument("--out", type=Path, default=None, help="Output JSON report path")
    p.add_argument("--top-k", type=int, default=5, dest="top_k")
    args = p.parse_args()

    report = run_evaluation(
        dataset_path=args.dataset,
        top_k=args.top_k,
        report_path=args.out,
    )
    out = args.out or default_report_path()
    print(json.dumps(report["summary"], ensure_ascii=False, indent=2))
    print(f"Wrote report: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
