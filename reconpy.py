#!/usr/bin/env python3

"""
reconpy — Fast & Clean Recon Pipeline
My first real cybersecurity portfolio project
Author: cHarKe4iHeR | Dec 2025
"""

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

# External tools this script expects to find on your system
REQUIRED_TOOLS = ["subfinder", "assetfinder", "httpx", "nuclei"]


def check_tools() -> None:
    missing = [t for t in REQUIRED_TOOLS if shutil.which(t) is None]
    if missing:
        print(f"[!] Missing required tools: {', '.join(missing)}")
        print("    sudo apt install subfinder assetfinder nuclei")
        print("    Please install from github.com/projectdiscovery/httpx/cmd/httpx@latest before running this script.")
        sys.exit(1)


def run(cmd: str) -> None:
    print(f"[+] {cmd}")
    result = subprocess.run(
        cmd,
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    # 0 = success, 2 or 130 often mean Ctrl+C / user interrupt
    if result.returncode not in (0, 2, 130):
        print(f"[!] Command failed with code: {result.returncode}")


def main() -> None:
    # ----- argument parsing -----
    parser = argparse.ArgumentParser(description="Simple recon tool wrapper.")
    parser.add_argument("domain", help="Target domain (e.g. tesla.com)")
    args = parser.parse_args()

    domain = args.domain

    # ----- output folder setup -----
    # Example: output/tesla.com/
    out = Path("output") / domain
    out.mkdir(parents=True, exist_ok=True)
    results_path = out.resolve()

    print(f"[*] Saving results to {results_path}\n")

    # Change working directory so files land inside output/<domain>/
    os.chdir(out)

    # ----- check external tools exist -----
    check_tools()

    # ----- 1. Subdomain enumeration -----
    run(f"subfinder -d {domain} -silent -o subfinder.txt")
    run(f"assetfinder --subs-only {domain} >> all.txt")

    # ----- 2. Alive check + deduplication -----
    # Takes subfinder + assetfinder results, sorts/uniqs them,
    # then passes into httpx to check which hosts are alive.
    run(
        "cat all.txt subfinder.txt 2>/dev/null | "
        "sort -u | "
        "httpx -sc -title -timeout 10 -random-agent -o alive.txt"
    )

    # ----- 3. Fast vulnerability scan with nuclei -----
    run(
        "nuclei -l alive.txt "
        "-severity critical,high "
        "-t http/cves/,http/exposed-panels/,http/technologies/ "
        "-c 30 -rl 30 -timeout 20 -silent "
        "-o nuclei.txt || true"
    )

    print(f"\nFinished: Results in {results_path}")


if __name__ == "__main__":
    main()
