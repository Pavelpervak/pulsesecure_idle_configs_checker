"""Main file for ICE Idle Config"""

import logging
import os
import sys
import argparse
from time import strftime
from csv import DictWriter
from src.config import ICSIdleConfig


# Console Logging handler.

logger = logging.getLogger('ICS_Idle_Config')
logger.setLevel(logging.INFO)

consoleHandler = logging.StreamHandler(sys.stdout)
console_formatter = logging.Formatter(
    "%(asctime)s - CONSOLE -%(levelname)s -  %(name)s - (%(filename)s):(%(lineno)d) - %(message)s"
)
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
    epilog="(C) Author -> Ray A."
    )

optargs = argparser.add_mutually_exclusive_group(required=False)
optargs.add_argument(
    '--disable-console-output',
    action="store_true",
    help="Disables console output",
    default=False,
    dest="console_output")

optargs.add_argument(
    '--disable-csv_report',
    action="store_true",
    help="Disables CSV report generation",
    default=False,
    dest="csv_report"
)

argparser.add_argument(
    'file',
    metavar="XML_EXPORT_FILE",
    action="store",
    help="Path to XML export file",
)

args = argparser.parse_args() # Init the argsparser.

def pprint(data):
    """Unpacks the items and print it"""
    for item_ in data:
        print(item_)

config = ICSIdleConfig(args.file)

# Calling the pipeline method.

print()
config.idle_configs()  # Executes all Idle config methods.
print()

def console_output():
    """Enables the Console output"""
    print("****** TOTAL CONFIGS ******")
    print()

    logger.info("Total Admin Realms %d\n", len(config.total_admin_realms))
    logger.info("Total User Realms %d\n", len(config.total_user_realms))
    logger.info(
    "Total Authentication servers %d\n", len(config.total_auth_servers))
    logger.info("Total Admin Roles %d\n", len(config.total_admin_roles))
    logger.info("Total User Roles %d\n", len(config.total_user_roles))

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

def csv_report():
    """Enables CSV report"""
    max_len = max(
        len(config.idle_auth_servers), len(
            config.idle_user_realms), len(config.idle_user_roles),
        len(config.idle_admin_realms), len(config.idle_admin_roles)
    )


    def fill_entries(data_list: list):
        """Fill entries of the list with NULL"""
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
    iadmin_realms = fill_entries(list(config.idle_admin_realms))
    iadmin_roles = fill_entries(list(config.idle_admin_roles))

    if 'results' not in os.listdir():
        os.mkdir('results')

    timestr = strftime("%d-%m-%Y-%H%M%S")

    with open(
        f"results\\idle_config_report[{timestr}].csv", mode='w', encoding='utf-8', newline=''
    ) as file_handle:
        headers = ["IDLE_AUTH_SERVERS", "IDLE_USER_REALMS",
                "IDLE_USER_ROLES", "IDLE_ADMIN_REALMS", "IDLE_ADMIN_ROLES"]
        write_output = DictWriter(file_handle, dialect='excel', fieldnames=headers)
        write_output.writeheader()

        for item in range(max_len):

            write_output.writerow(
                {
                    headers[0]: iauth_servers[item],
                    headers[1]: iuser_realms[item],
                    headers[2]: iuser_roles[item],
                    headers[3]: iadmin_realms[item],
                    headers[4]: iadmin_roles[item]
                }
            )

    logger.info("Idle Config Report Saved under 'results' folder (created under current working directory).\n")


# Output control flow.

if args.csv_report:
    console_output() # User opted to disable csv_report
elif args.console_output:
    csv_report() # User opted to disable console output.
else: # Default will execute both.
    console_output()
    csv_report()
