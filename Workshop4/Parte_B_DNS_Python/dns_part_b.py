"""
Part B: DNS resolution using dnspython
Workshop 4 - Sistemas Distribuidos
"""

import dns.resolver
import dns.reversename
import json

def run_dnspython_tests():
    # Configure custom resolver using Google DNS (8.8.8.8) and Cloudflare (1.1.1.1)
    custom_resolver = dns.resolver.Resolver(configure=False)
    custom_resolver.nameservers = ['8.8.8.8', '1.1.1.1']

    cloudflare_resolver = dns.resolver.Resolver(configure=False)
    cloudflare_resolver.nameservers = ['1.1.1.1']

    results = {}

    print("==========================================================")
    print(" PART B: DNS LOOKUPS USING DNSPYTHON")
    print("==========================================================")

    # 1: Basic Domain Lookup
    print("\n--- B1: Basic Domain Lookup (yachaytech.edu.ec) ---")
    try:
        answers = custom_resolver.resolve('yachaytech.edu.ec', 'A')
        ips = [rdata.to_text() for rdata in answers]
        print(f"IP address of yachaytech.edu.ec: {ips}")
        results["B1"] = {"domain": "yachaytech.edu.ec", "type": "A", "result": ips}
    except Exception as e:
        print(f"Error B1: {e}")
        results["B1"] = {"error": str(e)}

    # 2: Reverse Lookup (IP to Domain Name)
    print("\n--- B2: Reverse Lookup (8.8.8.8) ---")
    try:
        rev_name = dns.reversename.from_address("8.8.8.8")
        answers = custom_resolver.resolve(rev_name, "PTR")
        domains = [rdata.to_text() for rdata in answers]
        print(f"Domain associated with 8.8.8.8: {domains}")
        results["B2"] = {"ip": "8.8.8.8", "type": "PTR", "result": domains}
    except Exception as e:
        print(f"Error B2: {e}")
        results["B2"] = {"error": str(e)}

    # 3: Query Specific DNS Server (Cloudflare 1.1.1.1)
    print("\n--- B3: Query Specific DNS Server (hpc.cedia.edu.ec via Cloudflare 1.1.1.1) ---")
    try:
        answers = cloudflare_resolver.resolve('hpc.cedia.edu.ec', 'A')
        ips = [rdata.to_text() for rdata in answers]
        print(f"IP of hpc.cedia.edu.ec via 1.1.1.1: {ips}")
        results["B3"] = {"domain": "hpc.cedia.edu.ec", "dns_server": "1.1.1.1", "result": ips}
    except Exception as e:
        print(f"Error B3: {e}")
        results["B3"] = {"error": str(e)}

    # 4: Retrieve MX Records
    print("\n--- B4: Retrieve MX Records (yachaytech.edu.ec) ---")
    try:
        answers = custom_resolver.resolve('yachaytech.edu.ec', 'MX')
        mx_records = [{"preference": rdata.preference, "exchange": rdata.exchange.to_text()} for rdata in answers]
        for mx in mx_records:
            print(f"MX Server: {mx['exchange']} (Preference: {mx['preference']})")
        results["B4"] = {"domain": "yachaytech.edu.ec", "type": "MX", "result": mx_records}
    except Exception as e:
        print(f"Error B4: {e}")
        results["B4"] = {"error": str(e)}

    # 5: Retrieve NS Records
    print("\n--- B5: Retrieve NS Records (yachaytech.edu.ec) ---")
    try:
        answers = custom_resolver.resolve('yachaytech.edu.ec', 'NS')
        ns_servers = [rdata.to_text() for rdata in answers]
        for ns in ns_servers:
            print(f"Name Server: {ns}")
        results["B5"] = {"domain": "yachaytech.edu.ec", "type": "NS", "result": ns_servers}
    except Exception as e:
        print(f"Error B5: {e}")
        results["B5"] = {"error": str(e)}

    # 6: Query Start of Authority (SOA) Record
    print("\n--- B6: Query SOA Record (yachaytech.edu.ec) ---")
    try:
        answers = custom_resolver.resolve('yachaytech.edu.ec', 'SOA')
        soa_data = []
        for rdata in answers:
            info = {
                "mname": rdata.mname.to_text(),
                "rname": rdata.rname.to_text(),
                "serial": rdata.serial,
                "refresh": rdata.refresh,
                "retry": rdata.retry,
                "expire": rdata.expire,
                "minimum": rdata.minimum
            }
            soa_data.append(info)
            print(f"SOA MName (Primary NS): {info['mname']}")
            print(f"SOA RName (Admin Email): {info['rname']}")
            print(f"Serial: {info['serial']}, Refresh: {info['refresh']}, Retry: {info['retry']}, Expire: {info['expire']}, Min TTL: {info['minimum']}")
        results["B6"] = {"domain": "yachaytech.edu.ec", "type": "SOA", "result": soa_data}
    except Exception as e:
        print(f"Error B6: {e}")
        results["B6"] = {"error": str(e)}

    # 7: Query for Canonical Name (CNAME)
    print("\n--- B7: Query CNAME (www.microsoft.com) ---")
    try:
        answers = custom_resolver.resolve('www.microsoft.com', 'CNAME')
        cnames = [rdata.to_text() for rdata in answers]
        print(f"CNAME for www.microsoft.com: {cnames}")
        results["B7"] = {"domain": "www.microsoft.com", "type": "CNAME", "result": cnames}
    except Exception as e:
        print(f"Error B7: {e}")
        results["B7"] = {"error": str(e)}

    # 8: Debug Mode Simulation (Detailed Query Details using dnspython wire format/response packet)
    print("\n--- B8: Debug Mode (yachaytech.edu.ec wire protocol response details) ---")
    try:
        query_msg = dns.message.make_query('yachaytech.edu.ec', dns.rdatatype.A)
        response_msg = dns.query.udp(query_msg, '8.8.8.8', timeout=5)
        debug_info = {
            "opcode": dns.opcode.to_text(response_msg.opcode()),
            "rcode": dns.rcode.to_text(response_msg.rcode()),
            "id": response_msg.id,
            "flags": dns.flags.to_text(response_msg.flags),
            "question_count": len(response_msg.question),
            "answer_count": len(response_msg.answer),
            "authority_count": len(response_msg.authority),
            "additional_count": len(response_msg.additional),
            "raw_response_text": str(response_msg)
        }
        print("Detailed DNS Wire Message Response:")
        print(str(response_msg))
        results["B8"] = {"domain": "yachaytech.edu.ec", "debug_details": debug_info}
    except Exception as e:
        print(f"Error B8: {e}")
        results["B8"] = {"error": str(e)}

    # 9: Query a Non-Existent Domain
    print("\n--- B9: Query Non-Existent Domain (nonexistdomain12345.com) ---")
    try:
        answers = custom_resolver.resolve('nonexistdomain12345.com', 'A')
        print(f"Result: {[rdata.to_text() for rdata in answers]}")
    except dns.resolver.NXDOMAIN as e:
        print(f"Caught expected NXDOMAIN Exception: {e}")
        results["B9"] = {"domain": "nonexistdomain12345.com", "status": "NXDOMAIN", "message": "Domain does not exist"}
    except Exception as e:
        print(f"Error B9: {e}")
        results["B9"] = {"error": str(e)}

    with open(r"c:\Users\User\Desktop\8vo\Sistemas-Distribuidos\Sistemas-Distribuidos\Workshop4\dnspython_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print("\nSaved dnspython results to dnspython_results.json")

if __name__ == "__main__":
    run_dnspython_tests()
