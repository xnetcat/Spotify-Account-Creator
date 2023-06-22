"""
This is the main file for the project
"""

import asyncio
import json
import re
from random import choice, choices, randint, shuffle
from string import ascii_lowercase, digits
from threading import Thread
from typing import Any, Dict, List, Optional
from uuid import uuid4

import httpx
from faker import Faker

# ------------------------------ OPTIONS ------------------------------ #
MAX_RETRIES = 2
TIMEOUT = 30
BATCH_SIZE = 200
THREADS = 4
DELAY = 3
RUN_INFINITELY = False
USE_HOST_IP = False
USE_PROXIES = True
PROXY_URLS = [
    "http://proxysearcher.sourceforge.net/Proxy%20List.php?type=http",
    "http://worm.rip/http.txt",
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http",
    "https://openproxy.space/list/http",
    "https://openproxylist.xyz/http.txt",
    "https://proxyspace.pro/http.txt",
    "https://proxyspace.pro/https.txt",
    "https://raw.githubusercontent.com/B4RC0DE-TM/proxy-list/main/HTTP.txt",
    "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
    "https://raw.githubusercontent.com/hendrikbgr/Free-Proxy-Repo/master/proxy_list.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-http.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-https.txt",
    "https://raw.githubusercontent.com/mertguvencli/http-proxy-list/main/proxy-list/data.txt",
    "https://raw.githubusercontent.com/mmpx12/proxy-list/master/http.txt",
    "https://raw.githubusercontent.com/mmpx12/proxy-list/master/https.txt",
    "https://raw.githubusercontent.com/proxy4parsing/proxy-list/main/http.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt",
    "https://raw.githubusercontent.com/RX4096/proxy-list/main/online/http.txt",
    "https://raw.githubusercontent.com/RX4096/proxy-list/main/online/https.txt",
    "https://raw.githubusercontent.com/saschazesiger/Free-Proxies/master/proxies/http.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/https.txt",
    "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt",
    "https://rootjazz.com/proxies/proxies.txt",
    "https://sheesh.rip/http.txt",
    "https://www.freeproxychecker.com/result/http_proxies.txt",
    "https://www.proxy-list.download/api/v1/get?type=http",
    "https://www.proxy-list.download/api/v1/get?type=https",
    "https://www.proxyscan.io/download?type=http",
    "https://www.sslproxies.org/",
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&"
    "timeout=10000&country=all&ssl=all&anonymity=all",
    "https://spys.me/proxy.txt",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
]
# --------------------------------------------------------------------- #

FAKER = Faker()
CHARACTERS = ascii_lowercase + digits
EMAIL_PROVIDERS = [
    "@gmail.com",
    "@yahoo.com",
    "@outlook.com",
    "@hotmail.com",
    "@protonmail.com",
]
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/114.0.0.0 Safari/537.36"
)
CLIENT_VERSION = "1.2.15.316.g8a504b70"
SPOTIFY_APP_VERSION = "8.8.46.529"
ACCEPT_LANGUAGE = "pl-PL,pl;q=0.9"
SEC_CH_UA = '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"'


async def send_request(
    session: httpx.AsyncClient,
    url: str,
    post: bool,
    json_data: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None,
    data: Any = None,
    max_retries: int = MAX_RETRIES,
) -> Optional[httpx.Response]:
    """Send request."""

    retries = 0
    while retries < max_retries:
        try:
            await asyncio.sleep(DELAY)
            if post:
                response = await session.post(
                    url, json=json_data, headers=headers, data=data
                )
            else:
                response = await session.get(url, headers=headers)

            print(response.text)

            if response.status_code == 200:
                return response
        except Exception:  # pylint: disable=broad-except
            pass

        retries += 1

    return None


async def create_account(
    session: httpx.AsyncClient,
) -> None:
    """Create account."""

    username: str = FAKER.name()
    mail: str = "".join(choices(CHARACTERS, k=20)) + choice(EMAIL_PROVIDERS)
    password: str = FAKER.password(length=10)

    day = str(randint(1, 28))
    month = str(randint(1, 12))

    if int(month) < 10:
        month = "0" + month
    if int(day) < 10:
        day = "0" + day

    birthday: str = "-".join([str(randint(1998, 2004)), month, day])

    client_id = str(uuid4())
    payload = {
        "account_details": {
            "birthdate": birthday,
            "consent_flags": {
                "eula_agreed": True,
                "send_email": False,
                "third_party_email": False,
            },
            "display_name": username,
            "email_and_password_identifier": {"email": mail, "password": password},
            "gender": randint(1, 2),
        },
        "callback_uri": "https://auth-callback.spotify.com/r/android/music/signup",
        "client_info": {
            "api_key": "142b583129b2df829de3656f9eb484e6",
            "app_version": "v2",
            "capabilities": [1],
            "installation_id": client_id,
            "platform": "Android-ARM",
        },
        "tracking": {
            "creation_flow": "",
            "creation_point": "client_mobile",
            "referrer": "",
        },
    }

    headers3 = {
        "accept": "*/*",
        "accept-encoding": "gzip",
        "app-platform": "Android",
        "connection": "Keep-Alive",
        "Origin": "https://www.spotify.com",
        "host": "spclient.wg.spotify.com",
        "spotify-app-version": SPOTIFY_APP_VERSION,
        "user-agent": f"Spotify/{SPOTIFY_APP_VERSION} Android/25 (SM-G988N)",
        "content-length": str(len(json.dumps(payload))),
        "x-client-id": str(client_id).replace("-", ""),
    }

    response = await send_request(
        session=session,
        post=True,
        url="https://spclient.wg.spotify.com/signup/public/v2/account/create",
        headers=headers3,
        json_data=payload,
    )

    if response and "success" in response.text:
        print(f"Created account: {mail}:{password} with token: ")

        save_accounts(
            {
                "username": username,
                "mail": mail,
                "password": password,
            }
        )

    await session.aclose()

    return None


def load_proxies() -> List[str]:
    """Load proxies from the internet."""

    proxies_list = []
    for url in PROXY_URLS:
        response = httpx.get(url)
        proxies_list.extend(re.findall(r"[0-9]+(?:\.[0-9]+){3}\:[0-9]+", response.text))

    proxies_list = list(set(proxies_list))

    return proxies_list


async def create_accounts(
    clients: List[httpx.AsyncClient],
) -> List[httpx.AsyncClient]:
    """Create accounts."""

    tasks = (create_account(client) for client in clients)

    results = await asyncio.gather(*tasks)

    results = [result for result in results if result is not None]
    clients = [result["client"] for result in results]

    return clients


def split_list(input_list, number_of_chunks):
    """
    Split a list into a given number of chunks
    """

    avg = len(input_list) / float(number_of_chunks)
    new_list = []
    last = 0.0

    while last < len(input_list):
        new_list.append(input_list[int(last) : int(last + avg)])
        last += avg

    return new_list


def save_accounts(account: Dict[str, Any]):
    """
    Save accounts to a file
    """

    with open("accounts.txt", "a+", encoding="utf-8") as accounts_file:
        accounts_file.write(
            f"{account['username']} - {account['mail']}:"
            f"{account['password']} - {account['token']}\n"
        )


async def main(all_proxies: Optional[List[str]] = None):
    """
    Main function
    """

    if all_proxies is None:
        all_proxies = load_proxies()

    shuffle(all_proxies)

    print(f"Loaded {len(all_proxies)} proxies.")

    proxies_lists = split_list(all_proxies, len(all_proxies) / BATCH_SIZE)
    for sproxies in proxies_lists:
        clients = [
            httpx.AsyncClient(timeout=TIMEOUT, proxies=proxy)
            for proxy in sproxies  # type: ignore
        ]

        # First run to get working proxies
        valid_clients = await create_accounts(clients)

        while True:
            if len(valid_clients) == 0:
                break

            print(f"Running again, with {len(valid_clients)} working clients.")
            valid_clients = await create_accounts(valid_clients)


def start():
    """
    Start the program
    """

    # Load proxies from the internet
    proxies = [f"http://{proxy}" for proxy in load_proxies()]

    # Load proxies from file
    with open("proxies.txt", "r", encoding="utf-8") as file:
        proxies.extend(
            [f"http://{proxy}" for proxy in file.read().splitlines() if proxy]
        )

    proxies = list(set(proxies))

    if USE_HOST_IP:
        asyncio.run(create_account(httpx.AsyncClient(timeout=TIMEOUT)))

    if USE_PROXIES:
        if THREADS == 1:
            asyncio.run(main(proxies))
        else:
            threads = []
            for index, proxy_split in enumerate(split_list(proxies, THREADS)):
                thread = Thread(
                    target=asyncio.run, args=(main(proxy_split),), name=f"thread-{index}"
                )

                threads.append(thread)

            for thread in threads:
                thread.start()

            for thread in threads:
                thread.join()


if __name__ == "__main__":
    if RUN_INFINITELY:
        while True:
            start()
    else:
        start()
