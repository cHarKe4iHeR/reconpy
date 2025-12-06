# reconpy

A simple, fast reconnaissance pipeline written in Python

## What it does
- Enumerates subdomains using **subfinder** + **assetfinder**
- Checks which ones are alive with status codes and page titles (**httpx**)
- Runs a quick critical/high-severity scan (**nuclei**)
- Saves everything neatly into `output/<domain>/`

## Requirements
Built and tested on Kali Linux.
Any system with the tools below:


```bash
sudo apt install subfinder assetfinder nuclei
go install github.com/projectdiscovery/httpx/cmd/httpx@latest
```
--------------------------------------------------------------------------

## How to run commands
# 1. Clone the repo
git clone https://github.com/cHarKe4iHeR/reconpy.git
cd reconpy

# 2. Make the script executable
chmod +x reconpy.py

# 3. Run it on any domain
./reconpy.py tesla.com

---------------------------------------------------------------------------

## Example output (tesla.com)
[*] Saving results to /home/kali/reconpy/output/tesla.com

[+] subfinder -d tesla.com -silent -o subfinder.txt
[+] assetfinder --subs-only tesla.com >> all.txt
[+] cat all.txt subfinder.txt 2>/dev/null | sort -u | httpx -sc -title -timeout 10 -random-agent -o alive.txt
[+] nuclei -l alive.txt -severity critical,high -t http/cves/,http/exposed-panels/,http/technologies/ -c 30 -rl 30 -timeout 20 -silent -o nuclei.txt || true

Finished: Results in /home/kali/reconpy/output/tesla.com

----------------------------------------------------------------------------

## Files created

    subfinder.txt — raw subdomains from subfinder
    all.txt       — combined + deduplicated list
    alive.txt     — live hosts with status + titles
    nuclei.txt    — any critical/high findings (empty = clean)

## Notes

    Tested on fresh Kali 2025.3 VM
    Still learning — pull requests & feedback very welcome

Thanks for checking it out!
