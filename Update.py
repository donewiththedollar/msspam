import requests as req
import json as js
import threading as thr
import time as tm
import random as rnd
import logging as lg

user_input = input("Enter number: ")

lg.basicConfig(
    filename='activity.log', 
    filemode='a', 
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
    except Exception as e:
        lg.error(f"Error fetching proxies from main URL: {str(e)}")
    
    secondary_url = "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt"
    try:
        res = req.get(secondary_url, timeout=5)
        if res.status_code == 200:
            proxy_list = res.text.splitlines()
            return proxy_list
    except Exception as e:
        lg.error(f"Error fetching proxies from secondary URL: {str(e)}")
    
    return []

def send_request(prx):
    hdr = {  # Your headers here }
    data = {  # Your data here }

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
        lg.error(result)

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
