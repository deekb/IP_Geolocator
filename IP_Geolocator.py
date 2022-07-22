#!/bin/python3
import json
import socket
from urllib.request import urlopen
URL = "http://ip-api.com/json/"

def helpMenu():
    return("Usage: [OPTIONS]... [IP Address(V4/V6)]...\n" + \
           "Options:\n" + \
           "\tAll\t\tPrint all data about the address\n" + \
           "\tCity\t\tPrint the city of the address\n" + \
           "\tZIP\t\tPrint the ZIP code of the address\n" + \
           "\tISP\t\tPrint the Internet Service Provider(ISP) of the address\n" + \
           "\tCountry\t\tPrint the country of an address\n" + \
           "\tRegion\t\tPrint the region of an address\n" + \
           "\tTime Zone\tPrint the time zone of an address\n" + \
           "IP Address(V4/V6):\n" + \
           "\t\"~\"\t\tDenotes your global ip address")

def app():
    while True:
        ip = input("Command (\"?\" for help): ").lower()
        if ip == "?":
            print(helpMenu())
            continue
        elif "~" in ip:
            ip = ip.replace("~", urlopen("https://api.ipify.org/").read().decode())
        
        shownFields = []
        if "all" not in ip:
            if "city" in ip:
                shownFields.append(["\tCity: ", "city"])
                ip = ip.replace("city", "")
            if "zip" in ip:
                shownFields.append(["\tZIP code: ", "zip"])
                ip = ip.replace("zip", "")
            if "isp" in ip:
                shownFields.append(["\tISP: ", "isp"])
                ip = ip.replace("isp", "")
            if "country" in ip:
                shownFields.append(["\tCountry: ", "country"])
                ip = ip.replace("country", "")
            if "region" in ip:
                shownFields.append(["\tRegion: ", "regionName"])
                ip = ip.replace("region", "")
            if "time zone" in ip:
                shownFields.append(["\tTime Zone: ", "timezone"])
                ip = ip.replace("time zone", "")
                
        else:
            shownFields = [["\tCity: ", "city"], ["\tZIP Code: ", "zip"], ["\tISP: ", "isp"], ["\tCountry: ", "country"], ["\tRegion: ", "regionName"], ["\tTime Zone: ", "timezone"]]
            ip = ip.replace("all", "")
        
        
        ip = ip.strip()
        ip = "".join([char for char in ip if char in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ".", ":"]])


        try:
            response = urlopen(URL + ip)
            data = response.read()
            values = json.loads(data)
        except:
            print(f"Retrieving data for IP: {ip} failed, ensure you have a good internet connection")
            continue
        if values['status'] == "success":
            
            if shownFields:
                print("Data dump for IP: " + values['query'])
                for pair in shownFields:
                    print(pair[0] + values[pair[1]])
            else:
                print("No valid options specified")
        else:
            print(f"Retrieving data for IP: {ip} failed, ensure your IP is valid")
if __name__ == "__main__":
    print("\033[92m\033[1mStarting App...\033[94m")
    app()
