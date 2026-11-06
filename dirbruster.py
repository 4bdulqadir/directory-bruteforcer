import argparse
import time
import requests
from concurrent.futures import ThreadPoolExecutor

# In codes ka matlab hai ke cheez maujood hai
INTERESTING = {200, 301, 302, 403}

parser = argparse.ArgumentParser(description="Directory Bruteforcer")
parser.add_argument("-u", "--url", required=True, help="Target URL")
parser.add_argument("-w", "--wordlist", default="wordlist.txt", help="Wordlist file")
parser.add_argument("-t", "--threads", type=int, default=5, help="Number of threads")
parser.add_argument("-o", "--output", help="Save results to a file")
args = parser.parse_args()

target = args.url.rstrip("/")

# Safety check
print("Only scan systems you own or have written permission to test.")
if input("Type yes to continue: ").strip().lower() != "yes":
    raise SystemExit("Aborted.")

with open(args.wordlist) as f:
    words = f.read().split()

try:
    requests.get(target, timeout=5)
except requests.RequestException:
    print("[ERROR] Cannot reach", target)
    raise SystemExit(1)


def check(word):
    url = target + "/" + word
    try:
        response = requests.get(url, timeout=5, allow_redirects=False)
    except requests.RequestException:
        return None
    if response.status_code in INTERESTING:
        line = f"[{response.status_code}] {url}"
        print(line)
        return line
    return None


print("Scanning", target)
start = time.time()

with ThreadPoolExecutor(max_workers=args.threads) as executor:
    results = list(executor.map(check, words))

found = sorted(r for r in results if r)
print("Scan complete in", round(time.time() - start, 2), "seconds")
print("Total found:", len(found))

if args.output:
    with open(args.output, "w") as f:
        f.write("\n".join(found) + "\n")
    print("Results saved to", args.output)