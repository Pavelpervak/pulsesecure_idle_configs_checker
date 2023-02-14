"""
Resource policies - XPATH

non-parent type:

:::Web:::
saml-access-acl,saml-sso,custom-headers,cross-domain-access-policies,proxy-policy
protocol,encodings,saml-external-apps-sso.
All VPN tunneling policies.

"""

WEB_ROOT = './/web-policies'
WEB_ACL = './/web-acls/web-acl'
WEB_SSO_BASIC_NTLM = './/sso-basic-ntlms/sso-basic-ntlm-kerberos'
WEB_SSO_POST = './/sso-posts/sso-post'
WEB_SSO_HEADERS = './/sso-headers/sso-header'
WEB_CACHING_ACL = './/caching-acls/caching-acl'
WEB_JAVA_ACL = './/java-acls/java-acl'
WEB_CODESIGNING_ACL = './/codesigning-acls/codesigning-acl'
WEB_SELECTIVE_REWRITE = './/selective-rewrites/selective-rewrite'
WEB_COMPRESS_ACL = './/compression-acls/compression-acl'
WEB_LAUNCHJSAM = './/launchjsam-acls/launchjsam-acl'
WEB_CLIENTAUTH = './/client-authentications/client-authentication'

WEB_SAML_ACCESS = './/saml-accesses/saml-access'
WEB_SAML_SSO = './/saml-ssos/saml-sso'
WEB_CUSTOM_HEADER = './/custom-headers/custom-header'
WEB_CROSS_DOMAIN_ACL = './/cross-domain-access-policies/cross-domain-access-policy'
WEB_PROXY_POLICY = './/proxy-policies/proxy-policy'
WEB_PROTOCOL = './/protocols/protocol'
WEB_ENCODING = './/encodings/encoding'
WEB_SAML_EXTERNAL = './/saml-external-apps-ssos/saml-external-apps-sso'

WEB_POLICIES_HEADERS = ["ROLE", "WEB_ACL", "SSO_BASIC_NTLM", "SSO_POST", "SSO_HEADERS",
    "CACHING_ACL", "JAVA_ACL", "CODESIGNING_ACL", "SELECTIVE_REWRITE",
    "COMPRESS_ACL", "LAUNCH_JSAM", "CLIENT_AUTHENTICATION", "SAML_ACL",
    "SAML_SSO", "CUSTOM_HEADERS", "CROSS_DOMAIN_ACL", "PROXY_POLICY",
    "PROTOCOL", "ENCODING", "SAML_EXTERNAL_SSO"]

FILE_ROOT = './/file-policies'
FILE_WIN_ACL = './/file-win-acl'
FILE_WIN_SSO_ACL = './/file-win-sso-acl'
FILE_WIN_COMPRESS_ACL = './/file-win-compression-acl'

FILE_POLICIES_HEADERS = ["ROLE", "WIN_ACL", "WIN_SSO_ACL", "WIN_COMPRESS_ACL"]

SAM_ROOT = './/sam-policies'
SAM_ACL = './/sam-acl'

SAM_POLICIES_HEADERS = ["ROLE", "SAM_ACL"]

TERM_SERV_ROOT = './/terminal-services-policies'
TERM_SERV_ACL = './/terminal-services-acl'

TERMSERV_POLICIES_HEADERS = ["ROLE", "TERM_SERV_ACL"]

HTML5_ROOT = './/html5-access-policies'
HTML5_ACL = './/html5-access-acl'

HTML5_POLICIES_HEADERS = ["ROLE", "HTML5_ACL"]

NC_ROOT = './/network-connect-policies'
NC_ACL = './/network-connect-acl'
NC_CONNPROF = './/network-connect-global-connection-profile'
NC_STUNNEL = './/network-connect-split-tunneling-network'
NC_BWIDTH = './/network-connect-bandwidth-policy'
NC_NODE_CONNPROF = './/network-connect-connection-profile'

NC_POLICIES_HEADERS = ["ROLE", "VPN_ACL", "VPN_CONNPROFILE", "VPN_SPLIT_TUNNEL",
"VPN_BANDWIDTH", "VPN_NODE_CONNPROFILE"]
