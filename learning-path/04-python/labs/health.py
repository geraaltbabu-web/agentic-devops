"""HTTP health check for operators. No secrets."""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request


def check(url: str, timeout: float) -> dict:
    req = urllib.request.Request(url, method="HEAD")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return {"ok": True, "url": url, "status": resp.status}
    except urllib.error.HTTPError as exc:
        return {"ok": 200 <= exc.code < 400, "url": url, "status": exc.code}
    except (urllib.error.URLError, TimeoutError) as exc:
        return {"ok": False, "url": url, "error": type(exc).__name__}


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--url", default="https://example.com")
    p.add_argument("--timeout", type=float, default=8)
    p.add_argument("--json", action="store_true")
    args = p.parse_args(argv)
    result = check(args.url, args.timeout)
    if args.json:
        print(json.dumps(result))
    else:
        print(result)
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
