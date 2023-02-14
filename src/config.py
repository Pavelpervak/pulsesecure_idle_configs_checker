""" ICS Idle Config Parser """

from .parser import ICSXMLParser, Optional
from .xpath_ic import *
from .logger import LOGGER, logger


class ICSIdleConfig(ICSXMLParser):
    """ICS Idle Config Parser Class"""

    def __init__(self, xml_file) -> None:
        self.log_object = None
        self.results = {}
        super().__init__(xml_file)


    def idle_configs(self):
        """Pipeline method to run all Idle config fetching methods"""
        self.auth_servers()
        self.admin_realms()
        self.user_realms()
        self.signin_urls()
        self.user_roles()
        self.admin_roles()
        self.misc_aoa_roles()
        self.misc_ikev2_realms()


    def get_value(
        self,
        root_element: str,
        element_path: str,
        allow_dups: bool = False,
        invalid_values: Optional[list] = None) -> None:
        """Gets the element value"""

        if self.check_tree(root_element):
            logger.info(LOGGER[self.log_object]['success'])
            self.results[element_path] = self.parse_element(
                element_path,
                allow_dups=allow_dups,
                invalid_values=invalid_values)
        else:
            self.results[element_path] = set()
            logger.warning(LOGGER[self.log_object]['fail'])


    def get_values(
        self,
        root_element: str,
        element_path: list,
        allow_dups: bool = False,
        invalid_values: Optional[list] = None) -> None:
        """Get element values from multiple paths"""

        if isinstance(element_path, list):
            if self.check_tree(root_element):
                logger.info(LOGGER[self.log_object]['success'])
                for elem in element_path:
                    self.results[elem] = self.parse_element(
                        elem,
                        allow_dups=allow_dups,
                        invalid_values=invalid_values)
            else:
                for elem in element_path:
                    self.results[elem] = set()
                logger.warning(LOGGER[self.log_object]['fail'])


    def auth_servers(self) -> None:
        """Parse Total Auth Servers"""

        self.log_object = self.auth_servers.__name__
        self.get_value(
            root_element=AUTH_SERVERS_ROOT,
            element_path=AUTH_SERVERS
        )

    @property
    def total_auth_servers(self) -> set:
        """Get Total Auth Servers"""
        return self.results[AUTH_SERVERS]


    def signin_urls(self) -> None:
        """Parse user & admin realms from signin_policies"""

        self.log_object = self.signin_urls.__name__
        elements = [SIGNIN_USER_REALMS, SIGNIN_ADMIN_REALMS]
        self.get_values(
            root_element=SIGNIN_ROOT,
            element_path=elements
        )
        self.signin_status()


    def signin_status(self):
        """Getting the Sign-in URLs mapping - enabled and disabled status"""

        user_signin_disabled_dict = self.parse_element_dict(
            './/access-urls/access-url',
            'url-pattern',
            'user/realms',
            check_tree='user',
            check_key='enabled',
            check_value='false')

        self.results["user_signin_disabled"] = user_signin_disabled_dict

        user_signin_enabled_dict = self.parse_element_dict(
            './/access-urls/access-url',
            'url-pattern',
            'user/realms',
            check_tree='user',
            check_key='enabled',
            check_value='true')

        self.results["user_signin_enabled"] = user_signin_enabled_dict

        admin_signin_disabled_dict = self.parse_element_dict(
            './/access-urls/access-url',
            'url-pattern',
            'admin/realms',
            check_tree='admin',
            check_key='enabled',
            check_value='false')

        self.results["admin_signin_disabled"] = admin_signin_disabled_dict

        admin_signin_enabled_dict = self.parse_element_dict(
            './/access-urls/access-url',
            'url-pattern',
            'admin/realms',
            check_tree='admin',
            check_key='enabled',
            check_value='true')

        self.results["admin_signin_enabled"] = admin_signin_enabled_dict

    # Finding the idle-signing URLs

        self.results["used_urls_user"] = self.used_signin_realms(
            enabled_url=user_signin_enabled_dict,
            disabled_url=user_signin_disabled_dict
        )

        self.results["used_urls_admin"] = self.used_signin_realms(
            enabled_url=admin_signin_enabled_dict,
            disabled_url=admin_signin_disabled_dict
        )


    def used_signin_realms(self, enabled_url: dict, disabled_url: dict) -> set:
        """Used SignIn URLs
        Returns the signin URL which has idle user realm thats not mapped any other active signin URL
        """

        enabled_set = set().union(*enabled_url.values())
        # Optimized version of user_signin_url method.
        used_urls = set()
        for disable_url,disable_realm in disabled_url.items():
            disable_realm: set
            if len(disable_realm) == 1:
                if disable_realm.issubset(enabled_set):
                    used_urls.add(disable_url)
                    continue
            else:
                for _realm in disable_realm:
                    if _realm in enabled_set:
                        used_urls.add(disable_url)
                        continue
        return used_urls

    @property
    def idle_user_urls(self) -> set:
        """Unused disabled signin URL - User"""
        return sorted(set(list(self.results["user_signin_disabled"])).difference(self.results["used_urls_user"]))

    @property
    def idle_admin_urls(self) -> set:
        """Unused disabled signin URL - Admin"""
        return sorted(set(list(self.results["admin_signin_disabled"])).difference(self.results["used_urls_admin"]))

    @property
    def idle_signin_user_realm(self) -> set:
        """Ununsed user realm mapped to disabled signin URL"""
        return sorted(set().union(*self.results["user_signin_disabled"].values()).difference(
            set().union(*self.results["user_signin_enabled"].values())
        ))

    @property
    def idle_signin_admin_realm(self) -> set:
        """Ununsed admin realm mapped to disabled signin URL"""
        return sorted(set().union(*self.results["admin_signin_disabled"].values()).difference(
            set().union(*self.results["admin_signin_enabled"].values())
        ))


    def user_realms(self) -> None:
        """Parse elements present under user realms section"""

        self.log_object = self.user_realms.__name__
        elements = [
            USER_REALMS,
            USER_REALMS_AUTHSERVER,
            USER_REALMS_SECAUTHSERVER,
            USER_REALMS_DIRSERVER,
            USER_REALMS_ACCSERVER,
            USER_REALMS_RMAP
        ]
        self.get_values(
            root_element=USER_REALMS_ROOT,
            element_path=elements
        )

    @property
    def total_user_realms(self) -> set:
        """Total user realms from realms data"""
        return self.results[USER_REALMS]


    def admin_realms(self) -> None:
        """Parse elements present under Admin realms section"""

        self.log_object = self.admin_realms.__name__
        elements = [
            ADMIN_REALMS,
            ADMIN_REALMS_AUTHSERVER,
            ADMIN_REALMS_SECAUTHSERVER,
            ADMIN_REALMS_DIRSERVER,
            ADMIN_REALMS_ACCSERVER,
            ADMIN_REALMS_RMAP
        ]
        self.get_values(
            root_element=ADMIN_REALMS_ROOT,
            element_path=elements
        )

    @property
    def total_admin_realms(self) -> set:
        """Total Admin realms from realms data"""
        return self.results[ADMIN_REALMS]


    def user_roles(self) -> None:
        """Parse total user roles from roles data"""

        self.log_object = self.user_roles.__name__

        self.get_value(
            root_element=USER_ROLES_ROOT,
            element_path=USER_ROLES,
            invalid_values=['Outlook Anywhere User Role',]
        )

    @property
    def total_user_roles(self) -> set:
        """Get total user role from results dict"""
        return self.results[USER_ROLES]


    def admin_roles(self) -> None:
        """Parse total admin roles from roles data"""

        self.log_object = self.admin_roles.__name__

        self.get_value(
            root_element=ADMIN_ROLES_ROOT,
            element_path=ADMIN_ROLES,
            invalid_values=['.Read-Only Administrators', '.Administrators', ]
        )

    @property
    def total_admin_roles(self) -> set:
        """Get total user role from results dict"""
        return self.results[ADMIN_ROLES]


    def misc_aoa_roles(self) -> None:
        """MISC: AOA Roles"""

        if self.check_tree(MISC_AOA_ROOT):
            logger.info("SUCCESS: (misc)Authorization-Only policy data found.")

            if self.check_tree(MISC_AOA_ROLES):
                logger.info(
                    "SUCCESS: (misc)Authorization-Only policy role mapping found.")
                self.results[MISC_AOA_ROLES] = self.parse_element(
                    MISC_AOA_ROLES)
            else:
                self.results[MISC_AOA_ROLES] = set()
        else:
            self.results[MISC_AOA_ROLES] = set()
            logger.warning(
                "ERROR: (misc)Authorization-Only policy data not found.\
                Roles data might be inaccurate!"
            )

    @property
    def aoa_roles(self) -> set:
        """Gets the AOA roles from result"""
        return self.results[MISC_AOA_ROLES]


    def misc_ikev2_realms(self) -> None:
        """MISC: IKEv2 realms"""

        if self.check_tree(MISC_IKEV2_ROOT):
            logger.info("SUCCESS: (misc)IKEv2 config data found.")

            if self.check_tree(MISC_IKEV2_PORTREALM):
                logger.info("SUCCESS: (misc)IKEv2 Port realm mapping found.")
                self.results[MISC_IKEV2_PORTREALM] = self.parse_element(
                    MISC_IKEV2_PORTREALM)
            else:
                self.results[MISC_IKEV2_PORTREALM] = set()

            if self.check_tree(MISC_IKEV2_PROTOREALM):
                logger.info(
                    "SUCCESS: (misc)IKEv2 Protocol realm mapping found.")
                self.results[MISC_IKEV2_PROTOREALM] = self.parse_element(
                    MISC_IKEV2_PROTOREALM)
            else:
                self.results[MISC_IKEV2_PROTOREALM] = set()

            self.results[MISC_IKEV2_REALMS] = self.results[MISC_IKEV2_PORTREALM].union(
                self.results[MISC_IKEV2_PROTOREALM]
            )  # Union them to get all realms.

        else:
            logger.warning(
                "ERROR: (misc)IKEv2 Config data not found. Realms data might be inaccurate!")
            self.results[MISC_IKEV2_REALMS] = set()

    @property
    def ikev2_realms(self) -> set:
        """IKEv2 Realms configured"""
        return self.results[MISC_IKEV2_REALMS]


    @property
    def idle_user_realms(self) -> set:
        """Idle User realms"""
        return sorted(self.total_user_realms.difference(
            self.results[SIGNIN_USER_REALMS],
            self.results[MISC_IKEV2_REALMS]
        ))

    @property
    def idle_admin_realms(self) -> set:
        """Idle Admin realms"""
        return sorted(self.total_admin_realms.difference(
            self.results[SIGNIN_ADMIN_REALMS]
        ))

    @property
    def idle_auth_servers(self) -> set:
        """Idle Auth Servers"""
        return sorted(self.total_auth_servers.difference(
            self.results[USER_REALMS_AUTHSERVER],
            self.results[USER_REALMS_SECAUTHSERVER],
            self.results[USER_REALMS_DIRSERVER],
            self.results[USER_REALMS_ACCSERVER],
            self.results[ADMIN_REALMS_AUTHSERVER],
            self.results[ADMIN_REALMS_SECAUTHSERVER],
            self.results[ADMIN_REALMS_DIRSERVER],
            self.results[ADMIN_REALMS_ACCSERVER]
        ))

    @property
    def idle_user_roles(self) -> set:
        """Idle User roles"""
        return sorted(self.total_user_roles.difference(
            self.results[USER_REALMS_RMAP],
            self.results[MISC_AOA_ROLES]
        ))

    @property
    def idle_admin_roles(self) -> set:
        """Idle Admin roles"""
        return sorted(self.total_admin_roles.difference(
            self.results[ADMIN_REALMS_RMAP]
        ))
