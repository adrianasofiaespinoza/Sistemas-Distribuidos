"""
Part C: LDAP Installation, Setup, Search, and Python Authentication
Workshop 4 - Sistemas Distribuidos
"""

import json
from ldap3 import Server, Connection, MOCK_SYNC, ALL, ALL_ATTRIBUTES

def run_ldap_part_c():
    print("==========================================================")
    print(" PART C: LDAP SERVER EMULATION & AUTHENTICATION")
    print("==========================================================")

    # 1. Initialize LDAP Server Mock with directory schema
    server = Server('ldap://localhost:389', get_info=ALL)
    
    # Create Connection with Mock Strategy
    conn = Connection(
        server,
        user='cn=admin,dc=example,dc=com',
        password='adminpassword',
        client_strategy=MOCK_SYNC
    )
    conn.bind()

    # Define base domain entry
    conn.strategy.add_entry(
        'dc=example,dc=com',
        {
            'objectClass': ['top', 'dcObject', 'organization'],
            'o': 'Example Inc.',
            'dc': 'example'
        }
    )

    # Step 4: Add base structure from base.ldif
    print("\n--- Step 4: Adding basic LDAP structure (base.ldif) ---")
    conn.strategy.add_entry(
        'ou=People,dc=example,dc=com',
        {
            'objectClass': ['top', 'organizationalUnit'],
            'ou': 'People'
        }
    )
    conn.strategy.add_entry(
        'ou=Groups,dc=example,dc=com',
        {
            'objectClass': ['top', 'organizationalUnit'],
            'ou': 'Groups'
        }
    )
    print("Added: ou=People,dc=example,dc=com")
    print("Added: ou=Groups,dc=example,dc=com")

    # Step 5: Add user from user.ldif
    print("\n--- Step 5: Adding user to directory (user.ldif) ---")
    conn.strategy.add_entry(
        'uid=francisco,ou=People,dc=example,dc=com',
        {
            'objectClass': ['top', 'person', 'organizationalPerson', 'inetOrgPerson'],
            'uid': 'francisco',
            'sn': 'Hidrobo',
            'cn': 'Francisco Hidrobo',
            'userPassword': 'password'
        }
    )
    print("Added User: uid=francisco,ou=People,dc=example,dc=com")

    # Step 3 & 6: Verify and search LDAP entries (ldapsearch -x -LLL -b dc=example,dc=com)
    print("\n--- Step 3 & 6: LDAP Search (ldapsearch -x -LLL -b \"dc=example,dc=com\" \"uid=francisco\") ---")
    search_success = conn.search(
        search_base='dc=example,dc=com',
        search_filter='(uid=francisco)',
        attributes=ALL_ATTRIBUTES
    )
    
    search_results = []
    if search_success:
        for entry in conn.entries:
            print(f"\nDN: {entry.entry_dn}")
            print(f"Attributes: {entry.entry_attributes_as_dict}")
            search_results.append({
                "dn": entry.entry_dn,
                "attributes": {k: [str(v) for v in vals] for k, vals in entry.entry_attributes_as_dict.items()}
            })

    # Step 7: Python LDAP Authentication Simulation
    print("\n--- Step 7: Python LDAP Authentication Simulation ---")
    
    def authenticate_user(user_dn, password):
        # Query LDAP directory for user DN
        search_ok = conn.search(
            search_base='dc=example,dc=com',
            search_filter=f'(entryDN={user_dn})',
            attributes=['userPassword']
        )
        
        if not search_ok or len(conn.entries) == 0:
            # Fallback search if entryDN filter is not supported by mock
            conn.search(
                search_base='dc=example,dc=com',
                search_filter='(objectClass=inetOrgPerson)',
                attributes=['userPassword']
            )
        
        target_entry = None
        for entry in conn.entries:
            if entry.entry_dn.lower() == user_dn.lower():
                target_entry = entry
                break

        if target_entry is None:
            print(f"[AUTH FAILED] User '{user_dn}' does not exist in LDAP directory.")
            return False

        stored_pw = target_entry.userPassword[0] if target_entry.userPassword else None
        if stored_pw == password:
            print(f"[AUTH SUCCESS] User '{user_dn}' authenticated successfully!")
            return True
        else:
            print(f"[AUTH FAILED] Invalid password for '{user_dn}'.")
            return False

    # Test 1: Valid Credentials
    print("\nTesting Valid Credentials (uid=francisco, password=password):")
    auth1 = authenticate_user('uid=francisco,ou=People,dc=example,dc=com', 'password')

    # Test 2: Invalid Password
    print("\nTesting Invalid Password (uid=francisco, password=wrongpass):")
    auth2 = authenticate_user('uid=francisco,ou=People,dc=example,dc=com', 'wrongpass')

    # Test 3: Non-existent User
    print("\nTesting Non-existent User (uid=nonexistent, password=password):")
    auth3 = authenticate_user('uid=nonexistent,ou=People,dc=example,dc=com', 'password')

    output_data = {
        "search_results": search_results,
        "auth_test_valid": auth1,
        "auth_test_invalid_pass": auth2,
        "auth_test_nonexistent": auth3
    }

    with open(r"c:\Users\User\Desktop\8vo\Sistemas-Distribuidos\Sistemas-Distribuidos\Workshop4\ldap_results.json", "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    print("\nSaved LDAP test results to ldap_results.json")

if __name__ == "__main__":
    run_ldap_part_c()
