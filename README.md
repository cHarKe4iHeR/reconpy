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

**Everything you need to run reconpy.py on any Linux system (Kali, Ubuntu, Debian, Arch, etc.)**

|#|Dependency|How to install (copy-paste)|Why it’s needed|
|---|---|---|---|
|1|**Python 3.8+**|sudo apt install -y python3 python3-pip|Runs the script|
|2|**Go (Golang) 1.21+**|sudo apt install -y golang-go|Required to install httpx (and future tools)|
|3|**subfinder**|sudo apt install -y subfinder|Passive subdomain enumeration|
|4|**assetfinder**|sudo apt install -y assetfinder|Second passive subdomain source|
|5|**httpx (ProjectDiscovery)**|go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest sudo cp ~/go/bin/httpx /usr/local/bin/|Alive host checking + titles (the Go version is mandatory)|
|6|**nuclei + templates**|sudo apt install -y nuclei nuclei -update-templates|Vulnerability scanner|
|7|**PATH fix for Go binaries** (once forever)|echo 'export PATH=$PATH:$HOME/go/bin' >> ~/.bashrc source ~/.bashrc|Makes httpx (and future Go tools) available everywhere|

**7 commands total.**

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
