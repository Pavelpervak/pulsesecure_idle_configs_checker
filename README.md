
## Pulse Secure VPN Idle Config Checker

Python Script to check Idle configurations in Pulse Secure VPN servers using the XML export/backup file.

---

## Features

- Console output support with categorization.
- Saves the result to a CSV file (timestamped csv files stored under "results" folder - created automatically under cwd) - uses the [CSV API](https://docs.python.org/3/library/csv.html) from python standard library.
- Uses the [XML ElementTree API](https://docs.python.org/3/library/xml.etree.elementtree.html) from python standard library for parsing operations.
- No third-party library dependencies.
- Direct/Live interaction with VPN server is not required as the parsing is done offline.
---
## Supported Operations

_Identifies the following idle configuration items and logic used to identify them_

- **Authentication Servers** (Not mapped to any user/admin realms as primary, secondary, directory, accounting server).
- **User & Admin Realms** (Not mapped to any signin URL(s) policy).
- **User & Admin Roles** (Not mapped to any realm(s) role mapping rules).
- **SignIn URLs** (In disabled state and not holding user/admin realm(s) that's active on any other active/enabled signin URLs).
- **User & Admin realms mapped to disabled SignIn URLs** (user/admin realms not mapped to any other active/enabled signin URLs).
- **User Roles - Resource Policies dependency report** (CSV report that shows resource policy dependency for idle user roles).
- **Resource Profiles** (resource profiles not mapped to any user roles).
```diff
+ It's recommended to run the script again after clearing up all IDLE USER ROLES
+ as clearing some roles might orphan some resource profiles.
```


---
## Prerequisites

- Python 3.x _(Standlone or Windows Store version)_ | _Created & Tested using Python 3.9_
- XML export file from Pulse Secure VPN Server.

_Download XML export from VPN server admin GUI by navigating to **Maintenance >> Import/Export >> Export XML >> Select All >> Export**_

```diff
- Excluding ESAP & Pulse Client package during XML export will reduce size of the backup file.
+ Recommended for faster parsing :)
ESAP - Under XML Import/Export > collapse Endpoint Security tree > ESAP Version > select None.
Client package - Under XML Import/Export > collapse Pulse Secure Versions/Ivanti Secure Access Client tree > Pulse Secure Versions > None.
```
---

## Usage

```
ics_idle_config.py [-h] [--disable-console-output | --disable-csv_report] XML_EXPORT_FILE

Script to check ICS Idle configurations.

positional arguments:
  XML_EXPORT_FILE       Path to XML export file

optional arguments:
  -h, --help            show this help message and exit
  --disable-console-output
                        Disables console output
  --disable-csv_report  Disables CSV report generation
```
---

## Example

_(Use `python` if `python3` doesn't work)_

#### Default - `Enables both console output & CSV report.`
```
> python3 ics_idle_config.py "C:\Users\<USER>\Downloads\ive-export.xml"
```

#### Disable Console output - `saves the output to CSV file`
```
> python3 ics_idle_config.py "C:\Users\<USER>\Downloads\ive-export.xml" --disable-console-output
```

#### Disable CSV report - `prints the output to console.`
```
> python3 ics_idle_config.py "C:\Users\<USER>\Downloads\ive-export.xml" --disable-csv-report
```

#### Invalid Operation - Cannot have both --disable flags set.
###### _*disable flags are mutually exclusive_
```
> python3 ics_idle_config.py "C:\Users\<USER>\Downloads\ive-export.xml" --disable-console-output --disable-csv-report
```

## Work-In-Progress

- Option to generate XML delete config file for identified idle config objects.
