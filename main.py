#!/bin/python3
import json
from rich.console import Console
from rich import print
from urllib.request import urlopen

GEOLOCATION_API = "http://ip-api.com/json/"


def get_host_ip():
    return urlopen("https://api.ipify.org/").read().decode()


def help_menu():
    return ("Usage: [OPTIONS]... [IP Address(V4/V6)]\n" +
            "Options:\n" +
            "\tAll\t\tPrint all data about the address\n" +
            "\tCity\t\tPrint the city of the address\n" +
            "\tZIP\t\tPrint the ZIP code of the address\n" +
            "\tISP\t\tPrint the Internet Service Provider(ISP) of the address\n" +
            "\tCountry\t\tPrint the country of an address\n" +
            "\tRegion\t\tPrint the region of an address\n" +
            "\tTime Zone\tPrint the time zone of an address\n" +
            "IP Address(V4/V6):\n")


def app():
    while True:
        query = input("Command (\"?\" for help): ").lower()
        if query == "?":
            console = Console(highlight=False)
            console.print(help_menu())
            continue

        shown_fields = []
        if "all" not in query:
            if "city" in query:
                shown_fields.append(["\tCity: ", "city"])
                query = query.replace("city", "")
            if "zip" in query:
                shown_fields.append(["\tZIP code: ", "zip"])
                query = query.replace("zip", "")
            if "isp" in query:
                shown_fields.append(["\tISP: ", "isp"])
                query = query.replace("isp", "")
            if "country" in query:
                shown_fields.append(["\tCountry: ", "country"])
                query = query.replace("country", "")
            if "region" in query:
                shown_fields.append(["\tRegion: ", "regionName"])
                query = query.replace("region", "")
            if "time zone" in query:
                shown_fields.append(["\tTime Zone: ", "timezone"])
                query = query.replace("time zone", "")

        else:
            shown_fields = [
                ["\tCity: ", "city"],
                ["\tZIP Code: ", "zip"],
                ["\tISP: ", "isp"],
                ["\tCountry: ", "country"],
                ["\tRegion: ", "regionName"],
                ["\tTime Zone: ", "timezone"]]
            query = query.replace("all", "")

        query = query.strip()
        query = "".join([_ for _ in query if _ in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ".", ":"]])

        try:
            response = urlopen(GEOLOCATION_API + query)
            data = response.read()
            values = json.loads(data)
            print(values)
        except BaseException:
            print(
                f"Retrieving data for IP: {ip} failed, ensure you have a good internet connection")
            continue
        if values["status"] == "success":

            if shown_fields:
                print("Geodata for: " + values["query"])
                for pair in shown_fields:
                    print(pair[0] + values[pair[1]])
            else:
                print("No valid options specified")
        else:
            print(
                f"Retrieving data for IP: {query} failed, ensure your IP is valid")


if __name__ == "__main__":
    print("[green bold]Starting App...[/green bold]")
    app()
