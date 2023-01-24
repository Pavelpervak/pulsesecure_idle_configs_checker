# pulsesecure_idle_configs
Python Script to fetch unused/idle configurations from Pulse Connect Secure XML export.


Fetch the idle configurations present in Pulse/Ivanti Connect Secure appliances using the XML export backup file.

Syntax -> python3 or python ics_idle_config.py "path-to-xml-backup.xml" [optional-arugments]

Optional arguments:

--disable-console-output -> Disables the console output but saves a .csv file in the cwd.
--disable-csv-report -> Disables the csv report creation but prints the console output with results.
