import ldap

ldapconn = ldap.initialize('ldap://localhost')

ID = ""

cn = input("Enter username here:  ")
User = 'cn='+ cn + ',cn=SysUsers,dc=ImpDemo,dc=com'
PW = input("Enter password: ")

ldapconn.simple_bind_s(User, PW)
cn = 'cn=' + cn

UID = ldapconn.search_s("dc=ImpDemo,dc=com", ldap.SCOPE_SUBTREE, cn, ['uidNumber'])
UID = str(UID)
for n in UID:
    if n.isdecimal():
        ID = ID + n
print(ID)
