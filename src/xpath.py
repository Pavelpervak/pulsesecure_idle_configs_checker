"""
XPATH for config objects.

:::Conventions used:::

ROOT -> Used for validating the presence of the XML tree
MISC -> Optional config objects that might affect the result.

"""

AUTH_SERVERS_ROOT = './/auth-servers'
AUTH_SERVERS = './/auth-server/name'

SIGNIN_ROOT = './/access-urls'
# SIGNIN_USER_URLS = './/user/../url-pattern'
# SIGNIN_USER_STATUS = './/user/../enabled'
SIGNIN_USER_REALMS = './/access-url/user/realms'
# SIGNIN_ADMIN_URLS = './/admin/../url-pattern'
# SIGNIN_ADMIN_STATUS = './/admin/../enabled'
SIGNIN_ADMIN_REALMS = './/access-url/admin/realms'

USER_REALMS_ROOT = './/user-realms'
USER_REALMS = './/user-realms/realm/name'
USER_REALMS_AUTHSERVER = './/user-realms/realm/authentication-server'
USER_REALMS_DIRSERVER = './/user-realms/realm/directory-server'
USER_REALMS_ACCSERVER = './/user-realms/realm/accounting-server'
USER_REALMS_SECAUTHSERVER = './/user-realms/realm/secondary-authentication-settings/name'
USER_REALMS_RMAP = './/user-realms/realm/role-mapping-rules/rule/roles'

ADMIN_REALMS_ROOT = './/admin-realms'
ADMIN_REALMS = './/admin-realms/realm/name'
ADMIN_REALMS_AUTHSERVER = './/admin-realms/realm/authentication-server'
ADMIN_REALMS_DIRSERVER = './/admin-realms/realm/directory-server'
ADMIN_REALMS_ACCSERVER = './/admin-realms/realm/accounting-server'
ADMIN_REALMS_SECAUTHSERVER = './/admin-realms/realm/secondary-authentication-settings/name'
ADMIN_REALMS_RMAP = './/admin-realms/realm/role-mapping-rules/rule/roles'

USER_ROLES_ROOT = './/user-roles'
USER_ROLES = './/user-role/name'

ADMIN_ROLES_ROOT = './/admin-roles'
ADMIN_ROLES = './/admin-role/name'

MISC_AOA_ROOT = './/authorization-only-policies'
MISC_AOA_ROLES = './/authorization-only-policy/role-option'

MISC_IKEV2_ROOT = './/ike-options'
MISC_IKEV2_PORTREALM = './/ike-options/port-realm-mappings/port-realm/realm'
MISC_IKEV2_PROTOREALM = './/ike-options/realm-protocol-mappings/realm-protocol/realm'
MISC_IKEV2_REALMS = 'ikev2_realms'
