import requests
from os import environ
from getpass import getuser, getpass


def getCookies():
    session = "53616c7465645f5f1112922560209ba2bc1cf24b1353c0b06638a408f47cd0992af83c26b6ba7a67dc8a0fff3bde48b8cb4d03dfab4a932ddb8421010d49b78b"
    return {"session": session}


def getProxies():
    proxies = {}
    for key in environ:
        if "proxy" in key or "PROXY" in key:
            prot, _, proxy = key.partition("_")
            proxies[prot.lower()] = environ[key]
    return proxies


def load_input(year: int, day: int):
    url = f"https://adventofcode.com/{year}/day/{day}/input"
    cookies = getCookies()
    proxies = getProxies()
    print(f"Reading [{url}]")
    for key, value in proxies.items():
        print(f" With proxy: [{key}: {value}]")
    content = ""
    while content == "":
        r = requests.get(url, cookies=cookies, proxies=proxies)
        if r.status_code == 200:
            content = r.text
            print(f"{len(content)} characters read.")
        elif r.status_code == 407:
            print("Uh, oh. Proxy authentication needed!")
            username = getuser()
            password = getpass(prompt=f"Password for [{username}]:")
            newProxies = dict()
            for key, value in proxies.items():
                newProxies[key] = f"{key.lower()}://{username}:{password}@{value}"
            proxies = newProxies
        else:
            r.raise_for_status()
    return content
