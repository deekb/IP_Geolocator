#!/bin/python3
import json
from rich import print
from rich.panel import Panel
from urllib.request import urlopen
import requests
import argparse
import os

GEOLOCATION_API_URL = "http://ip-api.com/json/"
INTERNET_CHECK_URL = "http://www.google.com"
INTERNET_CHECK_TIMEOUT_SECONDS = 3
INSTALLED = os.path.dirname(os.path.abspath(
    __file__)) == os.path.join(os.path.sep, "usr", "bin")

if INSTALLED:
    print(Panel.fit("[cyan]Installed"))


def main():
    while True:
        query = input("Command: ").lower()

        shownFields = []
        if "all" not in query:
            for _ in ["city", "zip", "isp", "country", "region", "timezone"]:
                if _ in query:
                    shownFields.append(_)
                    query = query.replace(_, "")

        else:
            shownFields = [
                "city",
                "zip",
                "isp",
                "country",
                "region",
                "timezone"]
            query = query.replace("all", "")

        query = query.strip()
        query = "".join([_ for _ in query if _ in [
            "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ".", ":"]])

        try:
            response = urlopen(GEOLOCATION_API_URL + query)
            data = response.read()
            values = json.loads(data)
        except (requests.ConnectionError, requests.Timeout):
            print(
                f"Retrieving geodata for: {query} failed, could not connect to host")
            continue
        if values["status"] == "success":

            if shownFields:
                print("Geodata for: " + values["query"])
                for field in shownFields:
                    print("\t" + field.title() + ": " + values[field])
            else:
                print("No valid options specified")
        else:
            print(f"Retrieving data for: {query} failed, invalid IP")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Get data about IP addresses.')

    parser.add_argument('--city', action='store_true',
                        help='Print the city of the address')
    parser.add_argument('--zip', action='store_true',
                        help='Print the ZIP code of the address')
    parser.add_argument('--isp', action='store_true',
                        help='Print the Internet Service Provider(ISP) of the address')
    parser.add_argument('--country', action='store_true',
                        help='Print the country of the address')
    parser.add_argument('--region', action='store_true',
                        help='Print the region of the address')
    parser.add_argument('--timezone', action='store_true',
                        help='Print the time zone of the address')
    parser.add_argument('--install', action='store_true',
                        help='install this script to your /usr/bin directory (Unix only)')
    parser.add_argument('IP', type=str, nargs='?',
                        help='An IP address (V4/V6)')
    args = parser.parse_args()

    print("City: ", args.city)
    if args.install:
        print(Panel.fit("[green bold]Installing"))
        print(
            f"copy \"{os.path.abspath(__file__)}\" to /usr/bin/{os.path.splitext(os.path.basename(__file__))[0]}")
    try:
        request = requests.get(
            INTERNET_CHECK_URL,
            timeout=INTERNET_CHECK_TIMEOUT_SECONDS)
        print(Panel.fit("[green bold]Starting App..."))
    except (requests.ConnectionError, requests.Timeout) as exception:
        print(Panel.fit("[red bold]No internet connection."))
        quit()
    try:
        main()
    except KeyboardInterrupt:
        print()
        print(Panel.fit("[red bold]Goodbye"))
