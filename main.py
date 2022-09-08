#!/bin/python3
from shutil import copyfile
from time import time
from json import loads
from urllib.request import urlopen
from requests import get as requests_get
from requests import ConnectionError, Timeout
from argparse import ArgumentParser
from os import _exit
from os import path, name, geteuid, environ
start_time = time()

GEOLOCATION_API_URL = "http://ip-api.com/json/"
INTERNET_CHECK_URL = "http://www.google.com"
INTERNET_CHECK_TIMEOUT_SECONDS = 3
INSTALLED = (path.dirname(path.abspath(__file__)) == path.join(path.sep, "usr", "bin"))
ON_WINDOWS = (name == "nt")
IS_ROOT = (not geteuid())
DEBUG = ("DEBUG" in environ)

if DEBUG:
    print("Debug mode is activated")
    print(f"GEOLOCATION_API_URL: {GEOLOCATION_API_URL}")
    print(f"INTERNET_CHECK_URL: {INTERNET_CHECK_URL}")
    print(f"INTERNET_CHECK_TIMEOUT_SECONDS: {INTERNET_CHECK_TIMEOUT_SECONDS}")
    print("if you do not wish to see this message then run \"unset DEBUG\" in bash")


# Just for simplicity, this allows to use exit() with no args
def exit(exit_code: int = 0) -> None:
    _exit(exit_code)


def has_internet(url_to_check: str = "http://www.google.com", timeout_seconds: int = 3) -> bool:
    """
    param url_to_check: which website to attempt to connect to
    param timeout_seconds: the time before the program gives up (seconds)
    return: whether the program connected within the timeout or not
    """
    try:
        requests_get(url_to_check, timeout=timeout_seconds)
        return True
    except ConnectionError or Timeout:
        return False


def main() -> None:
    try:
        response = urlopen(GEOLOCATION_API_URL + IP)
        data = response.read()
        values = loads(data)
    except (ConnectionError or Timeout):
        print(
            f"Retrieving geodata for: {IP} failed, could not connect to host")
        values = None
        exit()
    if values["status"] == "success":
        print(f"Requested geodata for: {values['query']}:")
        for field in shownFields:
            print(f"\t{field.title()}: {values[field]}")
    else:
        print(f"Retrieving data for: {IP} failed, invalid IP")
        exit()


if __name__ == "__main__":
    print(f"Took {round(time() - start_time, 6)} seconds")
    parser = ArgumentParser(description='Get data about IP addresses.')

    parser.add_argument('--city', action='store_true', help='Print the city of the address')
    parser.add_argument('--zip', action='store_true', help='Print the ZIP code of the address')
    parser.add_argument('--isp', action='store_true', help='Print the Internet Service Provider(ISP) of the address')
    parser.add_argument('--country', action='store_true', help='Print the country of the address')
    parser.add_argument('--region', action='store_true', help='Print the region of the address')
    parser.add_argument('--timezone', action='store_true', help='Print the time zone of the address')
    parser.add_argument('--all', action='store_true', help='Print all data about the address')
    parser.add_argument('--install', action='store_true', help='install this script to your /usr/bin directory ('
                                                               'Unix/MacOS only)')
    parser.add_argument('IP', type=str, nargs='?', help='An IP address (V4/V6)')
    args = parser.parse_args()

    if args.IP:
        IP = args.IP
    else:
        IP = ""
    shownFields = []
    if args.all or True not in [args.city, args.zip, args.isp, args.country, args.region, args.timezone]:
        shownFields = ["city", "zip", "isp", "country", "region", "timezone"]
    else:
        if args.city:
            shownFields.append("city")
        if args.zip:
            shownFields.append("zip")
        if args.isp:
            shownFields.append("isp")
        if args.country:
            shownFields.append("country")
        if args.region:
            shownFields.append("region")
        if args.timezone:
            shownFields.append("timezone")

    if args.install:
        if ON_WINDOWS:
            print("Running on Windows, installation is unavailable")
        else:
            if not IS_ROOT:
                print("Not running as root, can't install!")
            else:
                print("Installing")
                print(f"copy {path.abspath(__file__)} to /usr/bin/ip-geolocator")
                copyfile(path.abspath(__file__), path.join(path.sep, "usr", "bin", "ip-geolocator"))
    if has_internet(INTERNET_CHECK_URL, INTERNET_CHECK_TIMEOUT_SECONDS):
        print("Making request...")
    else:
        print("This operation requires an internet connection")
        exit()
    try:
        main()
    except KeyboardInterrupt:
        print()
        print("KeyboardInterrupt")
