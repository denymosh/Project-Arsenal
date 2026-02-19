#!/usr/bin/env python3
import argparse
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("ticker")
    parser.add_argument("--top", type=int, default=3)
    args = parser.parse_args()

    base = PROJECT_ROOT / "reports" / args.ticker.upper() / "originals"
    if not base.exists():
        raise SystemExit(f"not found: {base}")

    files = sorted(base.glob("*.pdf"), key=lambda p: p.stat().st_mtime, reverse=True)[: args.top]
    for p in files:
        print(p)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
