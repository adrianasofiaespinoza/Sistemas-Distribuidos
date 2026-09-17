import subprocess
import json

commands = [
    ("A1_default", "nslookup yachaytech.edu.ec"),
    ("A1_google", "nslookup yachaytech.edu.ec 8.8.8.8"),
    ("A2_default", "nslookup 8.8.8.8"),
    ("A2_cloudflare", "nslookup 8.8.8.8 1.1.1.1"),
    ("A3_cloudflare", "nslookup hpc.cedia.edu.ec 1.1.1.1"),
    ("A4_mx", "nslookup -type=mx yachaytech.edu.ec 8.8.8.8"),
    ("A5_ns", "nslookup -type=ns yachaytech.edu.ec 8.8.8.8"),
    ("A6_soa", "nslookup -type=soa yachaytech.edu.ec 8.8.8.8"),
    ("A7_cname", "nslookup -type=cname www.microsoft.com 8.8.8.8"),
    ("A8_debug", "nslookup -debug yachaytech.edu.ec 8.8.8.8"),
    ("A9_nonexistent", "nslookup nonexistdomain12345.com 8.8.8.8")
]

results = {}

print("=== EXECUTING PART A: NSLOOKUP COMMANDS (WITH PUBLIC DNS BACKUP) ===")
for key, cmd in commands:
    print(f"\n--- Running {key}: {cmd} ---")
    try:
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=15)
        out = res.stdout + res.stderr
        results[key] = {
            "cmd": cmd,
            "output": out.strip(),
            "returncode": res.returncode
        }
        print(out.strip())
    except Exception as e:
        results[key] = {
            "cmd": cmd,
            "output": str(e),
            "returncode": -1
        }
        print(f"Error executing {cmd}: {e}")

with open(r"c:\Users\User\Desktop\8vo\Sistemas-Distribuidos\Sistemas-Distribuidos\Workshop4\nslookup_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print("\nSaved comprehensive nslookup results to nslookup_results.json")
