import ldap
import sys
import LDAP_ADMIN_DN
def try_ldap_bind(ldap_host, admin_pass):
    try:
        ldap_conn = ldap.initialize(ldap_host)
    except ldap.SERVER_DOWN:
        print("Can't contact LDAP server")
        exit(4)
    try:
        ldap_conn.simple_bind_s(LDAP_ADMIN_DN, admin_pass)
    except (ldap.INVALID_CREDENTIALS):
        print("This password is incorrect")
        sys.exit(3)
    print("YOUR IN")
