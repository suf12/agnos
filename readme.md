# Platform Agnostic Script
The purpose of this script is perform the following functions regardless of what OS it runs on.
* Create a text file containing the word 'Hello'. File location is passed in as an argument.
* Ping an IP address (default to 3 times).
* Run either test.sh or test.bat depending on the OS.
* Log output to a file.

## Usage
This script was tested with Python 3.8.2+, backwards compatibility is not guaranteed. To execute the script, run the following:
`python agnos.py -a <ip address> -p <path to generated text file> [-f <name of generated text file>]`
>you can run `python agnos.py --help` to view options again

## Assumptions
This script assumes the following:

1. `python --version` will return a 3.x version. If not you might need to run `python3 agnos.py` to call the script.
2. `agnos.py` is executable.
3. The current user has permission to execute `agnos.py`.
4. ICMP is not blocked.
5. `--path` is required. Should only be the path of the text file.
7. `--address` is required. Sends only 3 ICMP packets before stopping.
8. The test script exists in PATH

## Updates
Some updates to consider in a later version of this script:
1. in general
    * Return values for class functions
    * Make `-f` and `-a` optional when invoking program directly
    * Add `-v` with debug levels to increase verbosity
    * Add `-q` to supress STDOUT logging
    * Change log file to either overwrite upon existing file on program execution or timestamp log file name
    * Add an option to specify path/name of log file
2. ping_addr()
    * Check if ICMP is blocked by firewall
    * Add an option to change number of ICMP packets sent
3. run_script()
    * Check if test.(sh|bat) is executable
    * Check if the current user has permission to run test.(sh|bat)
    * Add an option to pass the test script path and/or name as an argument
    * Spawn another thread for executing test script
    * Use which/where/command/type to determine if test script exists in system path
