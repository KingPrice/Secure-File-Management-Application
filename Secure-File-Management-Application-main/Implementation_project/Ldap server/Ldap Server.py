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

    #CSV File Loading

import csv
users_to_import = []
with open('file.csv' , 'rb') as users_csv_file:
    users_reader = csv.reader(users_csv_file)
    for row in users_reader:
        user = {
            'username' : row[0],
            'password' : row[1],
            'firstname' : row[2],
            'lastname' : row[3],
            'group' : row[4],
            'shell' : row[5],
            'hosts' : row[6],
        }
        users_to_import.append(user)

    #User Creation on LDAP server

def create_user(user, admin_pass):
    dn = 'uid=' + user['username'] + ',' + LDAP_BASE_DN
    fullname = user['firstname'] + ' ' + user['username']
    home_dir = HOME_BASE + '/' + user['username']
    gid = find_gid(user['group'])
    lastchange = int(math.floor(time() / 86400))

entry = []
entry.extend([
    ('objectClass', ["person", "organizationalPerson", "inetOrgPerson", "posixAccount", "top", "shadowAccount", "hostObject"])
    ('uid', user['username']),
    ('cn', fullname),
    ('givenname', user['firstname']),
    ('sn', user['lastname']),
    ('mail', user['email']),
    ('uidNumber', str(user['uid'])),
    ('gidNumber', str(gid)),
    ('loginShell', user['shell']),
    ('homeDirectory', home_dir),
    ('shadowMax', "99999"),
    ('shadowWarning', "7"),
    ('shadowLastChange', str(lastchange)),
    ('userPassword', user['password'])
])
if (len(user['hosts'])):
    entry.append( ('host', user['hosts']) )

ldap_conn = ldap.initialize(LDAP_HOST)
ldap_conn.simple_bind_s(LDAP_ADMIN_DN, admin_pass)

try:
    ldap_conn.add_s(dn, entry)
finally:
    ldap_conn.unbind_s()

