from . import conector

class UsersRepository(object):
    def __init__(self):
        self.ldap_users_base = 'ou=People,dc=sergio,dc=gonzalonazareno,dc=org'
        self.conn = conector.LdapConector.initialize_ldap_connection()

    def _ldap_query(self):
        filter_pattern = '(objectclass=person)'
        attr_list = ['uid', 'gidNumber', 'uidNumber']
        self.conn.search(self.ldap_users_base, filter_pattern, attributes=attr_list)
        return self.conn.entries

    def get_admins(self):
        users = self._ldap_query()
        admin_users = []
        for user in users:
            if user.gidNumber.value == 2050:
                admin_users.append(user.uid.value)
        return admin_users

    def get_users(self):
        users = self._ldap_query()
        # user types
        common_users = []
        premium_users = []

        for user in users:
            if user.gidNumber.value == 2000:
                common_users.append(user.uid.value)
            elif user.gidNumber.value == 2001:
                premium_users.append(user.uid.value)
        return common_users, premium_users

    def get_uidNumber_for_user(self):
        users = self._ldap_query()
        uidNumber_list = []
        for user in users:
            uidNumber_list.append(user.uidNumber.value)
        uidNumber_list.sort()
        last_uid = uidNumber_list[-1] + 1
        return int(last_uid)

    def get_pwhash_for_user(self, textplain_passwd):
        # Only needed for that
        from passlib.hash import ldap_salted_sha1
        password_hash = ldap_salted_sha1.encrypt(textplain_passwd)
        return password_hash

    def create_user(self, ldap_auth_user_password, user):
        # App user
        auth_conn = conector.LdapConector.rebind_to_ldap_auth_connection(self.conn, ldap_auth_user_password)
        # That comma is really important
        user_dn = 'uid=' + user['uid'] + ',' + self.ldap_users_base
        auth_conn.add(user_dn, user['objectclass'], user['user_attributes'])
        auth_conn.unbind()


    def delete_user(self, ldap_auth_user_password, user):
        auth_conn = conector.LdapConector.rebind_to_ldap_auth_connection(self.conn, ldap_auth_user_password)
        # That comma is really important
        user_dn = 'uid=' + user + ',' + self.ldap_users_base
        auth_conn.delete(user_dn)
        auth_conn.unbind()

    # def get_premium_users():
    #     common_users, premium_users, admin_users = self.get_users()
    #     if username in
    #     is_admin = conn.search('dc=sergio,dc=gonzalonazareno,dc=org', '(&(uid={})(gidNumber={}))'.format(username, admin_gid))
    #     is_premium = conn.search('dc=sergio,dc=gonzalonazareno,dc=org', '(&(uid={})(gidNumber={}))'.format(username, premium_gid))
