"""Main file for ICE Idle Config"""

import logging
import os
import sys
import argparse
from time import strftime
from csv import DictWriter
from src import ICSIdleConfig, ICSRSPolicy, ICSRSProfile


# Console Logging handler.

logger = logging.getLogger('ICS_Idle_Config')
logger.setLevel(logging.INFO)

consoleHandler = logging.StreamHandler(sys.stdout)
console_formatter = logging.Formatter(
    "%(asctime)s - CONSOLE - %(levelname)s - %(message)s"
)
# Removed log params %(name)s - (%(filename)s):(%(lineno)d) for better readability.
consoleHandler.setFormatter(console_formatter)
logger.addHandler(consoleHandler)

class RayParser(argparse.ArgumentParser):
    """Args Parser Class"""
    def error(self, message: str) -> None:
        print()
        sys.stderr.write(f'***Argument Error*** {message}\n')
        print()
        self.print_help()
        input()
        sys.exit(2)

argparser = RayParser(
    prog="ics_idle_config.py",
    description="Script to check ICS Idle configurations.",
    epilog="(C) Author -> Ray A.")

optargs = argparser.add_mutually_exclusive_group(required=False)
optargs.add_argument(
    '--disable-console-output',
    action="store_true",
    help="Disables console output",
    default=False,
    dest="console_output")

optargs.add_argument(
    '--disable-csv-report',
    action="store_true",
    help="Disables all CSV reports generation - Idle config, Idle resource policies & profiles.",
    default=False,
    dest="csv_report")

argparser.add_argument(
    'file',
    metavar="XML_EXPORT_FILE",
    action="store",
    help="Path to XML export file")

args = argparser.parse_args() # Init the argsparser.

timestr = strftime("%d-%m-%Y-%H%M%S")

def pprint(data):
    """Unpacks the items and print it"""
    for item_ in data:
        print(item_)

config = ICSIdleConfig(args.file)

# Calling the pipeline method.

print()
config.idle_configs() # Executes all Idle config methods & resource policy parser.
print()

def results_dir() -> None:
    """Results directory creator"""

    if 'results' not in os.listdir():
        os.mkdir('results')
    os.mkdir(fr"results\{timestr}")
    os.mkdir(fr"results\{timestr}\resource_policies")

def console_output() -> None:
    """Enables the Console output"""
    print("****** TOTAL CONFIGS ******")
    print()

    logger.info("Total Admin Realms - %d\n", len(config.total_admin_realms))
    logger.info("Total User Realms - %d\n", len(config.total_user_realms))
    logger.info(
    "Total Authentication servers - %d\n", len(config.total_auth_servers))
    logger.info("Total Admin Roles - %d\n", len(config.total_admin_roles))
    logger.info("Total User Roles - %d\n", len(config.total_user_roles))

    print()
    print("****** MISC CONFIGS ******")
    print()

    logger.info("AOA Role mappings - %d\n", len(config.aoa_roles))
    logger.info("IKEv2 Realm mappings - %d\n", len(config.ikev2_realms))

    print()
    print("****** IDLE CONFIGS ******")
    print()

    logger.info("Idle Admin realms - %d\n", len(config.idle_admin_realms))
    pprint(config.idle_admin_realms)
    print()

    logger.info("Idle User realms - %d\n", len(config.idle_user_realms))
    pprint(config.idle_user_realms)
    print()

    logger.info("Idle Admin sign-in urls - %d\n", len(config.idle_admin_urls))
    pprint(config.idle_admin_urls)
    print()

    logger.info("Idle User sign-in urls - %d\n", len(config.idle_user_urls))
    pprint(config.idle_user_urls)
    print()

    logger.info("Idle Admin sign-in realms - %d\n", len(config.idle_signin_admin_realm))
    pprint(config.idle_signin_admin_realm)
    print()

    logger.info("Idle User sign-in realms - %d\n", len(config.idle_signin_user_realm))
    pprint(config.idle_signin_user_realm)
    print()

    logger.info("Idle Authentication servers - %d\n",
            len(config.idle_auth_servers))
    pprint(config.idle_auth_servers)
    print()

    logger.info("Idle Admin roles - %d\n", len(config.idle_admin_roles))
    pprint(config.idle_admin_roles)
    print()

    logger.info("Idle User roles - %d\n", len(config.idle_user_roles))
    pprint(config.idle_user_roles)
    print()

def csv_report() -> None:
    """Enables CSV report"""
    max_len = max(
        len(config.idle_auth_servers),
        len(config.idle_user_realms),
        len(config.idle_user_roles),
        len(config.idle_admin_realms),
        len(config.idle_admin_roles),
        len(config.idle_user_urls),
        len(config.idle_admin_urls),
        len(config.idle_signin_user_realm),
        len(config.idle_signin_admin_realm)
    )

    def fill_entries(data_list: list):
        """Fill entries of the list with NULL as padding"""
        if len(data_list) < max_len:
            diff = max_len - len(data_list)
            length = len(data_list)
            for item_ in range(diff):
                data_list.insert((length+item_), " ")
            return data_list
        return data_list

    iauth_servers = fill_entries(list(config.idle_auth_servers))
    iuser_realms = fill_entries(list(config.idle_user_realms))
    iuser_roles = fill_entries(list(config.idle_user_roles))
    iuser_urls = fill_entries(list(config.idle_user_urls))
    iadmin_urls = fill_entries(list(config.idle_admin_urls))
    iadmin_realms = fill_entries(list(config.idle_admin_realms))
    iadmin_roles = fill_entries(list(config.idle_admin_roles))
    iuser_signin = fill_entries(list(config.idle_signin_user_realm))
    iadmin_signin = fill_entries(list(config.idle_signin_admin_realm))

    with open(
        fr"results\{timestr}\idle_config_report.csv", mode='w', encoding='utf-8', newline=''
    ) as file_handle:
        headers = ["IDLE_AUTH_SERVERS", "IDLE_USER_REALMS",
                "IDLE_USER_ROLES", "IDLE_ADMIN_REALMS", "IDLE_ADMIN_ROLES",
                "IDLE_USER_URLS", "IDLE_ADMIN_URLS", "IDLE_SIGNIN_USER_REALMS",
                "IDLE_SIGNIN_ADMIN_REALMS"]
        write_output = DictWriter(file_handle, dialect='excel', fieldnames=headers)
        write_output.writeheader()

        for item in range(max_len):

            write_output.writerow(
                {
                    headers[0]: iauth_servers[item],
                    headers[1]: iuser_realms[item],
                    headers[2]: iuser_roles[item],
                    headers[3]: iadmin_realms[item],
                    headers[4]: iadmin_roles[item],
                    headers[5]: iuser_urls[item],
                    headers[6]: iadmin_urls[item],
                    headers[7]: iuser_signin[item],
                    headers[8]: iadmin_signin[item]
                }
            )
    print()

def rs_policy_parser() -> None:
    """Pipeline for all CSV write operations"""

    logger.info("Parsing Resource policy dependencies.")

    rs_policy = ICSRSPolicy(args.file, config.idle_user_roles)
    rs_policy.rs_policies()

    rs_policy.write_web_policies(fr"results\{timestr}\resource_policies\web_policy.csv")
    rs_policy.write_file_policies(fr"results\{timestr}\resource_policies\file_policy.csv")
    rs_policy.write_sam_policies(fr"results\{timestr}\resource_policies\sam_policy.csv")
    rs_policy.write_termsrv_policies(fr"results\{timestr}\resource_policies\termsrv_policy.csv")
    rs_policy.write_html5_policies(fr"results\{timestr}\resource_policies\html5_policy.csv")
    rs_policy.write_vpntunnel_policies(fr"results\{timestr}\resource_policies\vpn_policy.csv")

    print()

def rs_profile_parser() -> None:
    """Pipeline for RS profiles"""

    logger.info("Parsing Idle Resource Profiles.")

    rs_profile = ICSRSProfile(args.file)
    rs_profile.rs_profiles()

    max_len = max(
        len(rs_profile.web_profiles_),
        len(rs_profile.file_profiles_),
        len(rs_profile.sam_profiles_capp_),
        len(rs_profile.sam_profiles_dest_),
        len(rs_profile.termsrv_profiles_),
        len(rs_profile.html5_profiles_),
        len(rs_profile.vdi_profiles_)
    )

    def fill_entries(data_list: list):
        """Fill entries of the list with NULL as padding"""
        if len(data_list) < max_len:
            diff = max_len - len(data_list)
            length = len(data_list)
            for item_ in range(diff):
                data_list.insert((length+item_), " ")
            return data_list
        return data_list

    eweb_profiles = fill_entries(rs_profile.web_profiles_)
    efile_profiles = fill_entries(rs_profile.file_profiles_)
    esam_profiles_capp = fill_entries(rs_profile.sam_profiles_capp_)
    esam_profiles_dest = fill_entries(rs_profile.sam_profiles_dest_)
    eterm_profiles = fill_entries(rs_profile.termsrv_profiles_)
    evdi_profiles = fill_entries(rs_profile.vdi_profiles_)
    ehtml5_profiles = fill_entries(rs_profile.html5_profiles_)

    with open(
            fr"results\{timestr}\idle_resource_profiles.csv", mode='w', encoding='utf-8', newline=''
        ) as file_handle:
        headers = ["WEB_PROFILES", "FILE_PROFILES", "SAM_CLIENT_APPS", "SAM_DESTS",
        "TERMSERV_PROFILES", "VDI_PROFILES", "HTML5_PROFILES"]
        write_output = DictWriter(file_handle, dialect='excel', fieldnames=headers)
        write_output.writeheader()

        for item in range(max_len):

            write_output.writerow(
                {
                    headers[0]: eweb_profiles[item],
                    headers[1]: efile_profiles[item],
                    headers[2]: esam_profiles_capp[item],
                    headers[3]: esam_profiles_dest[item],
                    headers[4]: eterm_profiles[item],
                    headers[5]: evdi_profiles[item],
                    headers[6]: ehtml5_profiles[item]
                })
    print()


# Output control flow.

if args.csv_report:
    console_output() # User opted to disable csv_report

elif args.console_output:
    results_dir()
    csv_report() # User opted to disable console output.
    rs_policy_parser()
    rs_profile_parser()
    logger.info("Reports saved under 'results' folder (created under current working directory).\n")

else: # Default will execute all methods.
    console_output()
    results_dir()
    csv_report()
    rs_policy_parser()
    rs_profile_parser()
    logger.info("Reports saved under 'results' folder (created under current working directory).\n")
