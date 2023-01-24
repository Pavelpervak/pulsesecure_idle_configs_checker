
## Pulse Secure VPN Idle Config Parser

Python Script to parse Idle configurations from Pulse Secure VPN server's XML export file.


## Features

- Console output support with categorization.
- Saves the results to CSV file in current working directory.
- Uses the default Python's [XML ElementTree API](https://docs.python.org/3/library/xml.etree.elementtree.html) for parsing _(no third-party library dependencies)_

## Prerequisites

- Python 3.x _(Standlone or Windows Store version)_
- XML export file from Pulse Secure VPN.

_Download XML export from VPN server admin GUI by navigating to Maintenance >> Import/Export >> Export XML >> Select All >> Export_


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
