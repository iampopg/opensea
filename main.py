import requests, platform, os , sys
from colorama import init, Fore
from concurrent.futures import ThreadPoolExecutor
from fake_useragent import UserAgent

init(autoreset=True)
red = Fore.RED
black = Fore.BLACK
yellow = Fore.YELLOW
green = Fore.GREEN
blue = Fore.BLUE
white = Fore.WHITE


def send_graphql_request(email,save):
    ua = UserAgent()
    # usa = ua.random
    # print(usa)

    headers = {
        'Host': 'opensea.io',
        'Cookie': '__os_session=eyJpZCI6IjZiYmE1NjFiLWJjM2ItNDBjYS04ZDE0LTQ4ODA0YzYwNDNhMiJ9; __os_session.sig=1Z0BJrvTcpGO0R742ufh5WuQh5gMQ_Lwn1hCTJbY8Ec; device_id=%22022b6ded-c5b7-4479-bf16-e570e7f525e4%22; AMP_ddd6ece4d5=JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjIwMjJiNmRlZC1jNWI3LTQ0NzktYmYxNi1lNTcwZTdmNTI1ZTQlMjIlMkMlMjJ1c2VySWQlMjIlM0ElMjIweDU3MWQyYzMxMzgzMTQ1ZDlmNDBhM2E1OWFmMjBiYTFkZmY0ZjQ0MzglMjIlMkMlMjJzZXNzaW9uSWQlMjIlM0ExNzE0OTQ0NzQzMTA2JTJDJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJsYXN0RXZlbnRUaW1lJTIyJTNBMTcxNDk0NDc3NDk5MyUyQyUyMmxhc3RFdmVudElkJTIyJTNBMjQlN0Q=; AMP_MKTG_ddd6ece4d5=JTdCJTIycmVmZXJyZXIlMjIlM0ElMjJodHRwcyUzQSUyRiUyRnd3dy5nb29nbGUuY29tJTJGJTIyJTJDJTIycmVmZXJyaW5nX2RvbWFpbiUyMiUzQSUyMnd3dy5nb29nbGUuY29tJTIyJTdE; _gcl_au=1.1.1920310981.1714865964; _ga_9VSBF2K4BX=GS1.1.1714944775.3.0.1714944775.0.0.0; _ga=GA1.1.1171226826.1714865964; cf_clearance=Q63lQ87wlJ5p2mV5yyjYCEi1G160eSIjNzyBsG2FU4I-1714944764-1.0.1.1-puKh79rNcLM1xZpeKDTtiDDsWkAHbjPt4vkfyiSNoyKlUH6P55KZMw8UEjJu93foqbSz5t1WjYHZbHGxO83VsA; _gid=GA1.2.1450338548.1714865967; opensea_logged_out=true; new_account_table_view_asset_card_variant=undefined; __cf_bm=p6eYE5mhKdPsfbOGTDUdEsXuAc2ev_kg.NXsl0hUsN0-1714944737-1.0.1.1-OxnMQwoa71w6kPqrBEycRgNNU7ppw_HKWKmM5lMPH4_pdeQZ9cHmHlFzuMXL1sTqtj49CKsleYrFldn1qc16jg; _cfuvid=yFHiM9I935nH1eyPSgPHHUZCJx2NwEZI4P.ZIqLX880-1714944737334-0.0.1.1-604800000; ext-os-wallet={%22installedWallets%22:[]%2C%22theme%22:%22dark%22%2C%22deviceId%22:%22022b6ded-c5b7-4479-bf16-e570e7f525e4%22}; _dd_s=rum=0&expire=1714945674653; _gat_gtag_UA_111688253_1=1; _gat_UA-111688253-1=1; _uetsid=8be2a6100a6f11efbd0fb95fed52ab70; _uetvid=8be288b00a6f11efb2c697f9202d888a',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://opensea.io/',
        'X-Build-Id': 'ebc1d17c1947abaddc0f970a0e368661509005ae',
        'X-App-Id': 'opensea-web',
        'X-Signed-Query': 'e16bad42ac64bc3ccb80abc30b11b5769f7f6b67849d7f8313a79299b5362853',
        'Content-Type': 'application/json',
        'Content-Length': '185',
        'Origin': 'https://opensea.io',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Te': 'trailers',
    }

    payload = {
        "id": "OSLoginQuery",
        "query": "query OSLoginQuery(\n  $email: Email!\n) {\n  accountHelpers {\n    hasEmbeddedWallet(email: $email)\n  }\n}\n",
        "variables": {"email": email}
    }
    
    try:
        response = requests.post('https://opensea.io/__api/graphql/', headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        result= response.json()
        # print(result)
        has_embedded_wallet = result.get('data', {}).get('accountHelpers', {}).get('hasEmbeddedWallet', None)
        # print(has_embedded_wallet)
        if has_embedded_wallet == True:
            print(green + f"REGISTERED----> {yellow}{email}")
            with open("result/"+save+'_Registered.txt', 'a') as valid_file:
                        valid_file.write(email + '\n')
        
        elif has_embedded_wallet == False:
            print(red + f"UNREGISTERED--> {yellow}{email}")
            with open("result/"+save+'_NotRegistered.txt', 'a') as valid_file:
                        valid_file.write(email + '\n')
        else:
            print("Please report this to @iampopg")
            print(response.text)
        
    except Exception as e:
        print(f"Error: {e}")
        return None

# response = send_graphql_request("sawdyk2@gmail.com")
if platform.system() == 'Windows':
    os.system('cls')
elif platform.system() == 'Linux':
    os.system('clear')

print()
print(f""" {green}OpenSea Email Checker v1
                            {white}Coded by Pop(G)
                            {red}telegram: https://t.me/iampopg
                            
        """)
print()

#creating result folder if not exist
if not os.path.exists("result"):
    os.makedirs('result')

path_to_email = input(blue + f"Please enter Path to Email List (e.g., email.txt): {white}")
try:
    save = input(f"Enter name to SAVE the output: {white}")
    speed = int(input("Enter Speed limit(between 1-10 only): "))
    
    print()
    with open(path_to_email, 'r') as read:
        emails = read.readlines()
        with ThreadPoolExecutor(max_workers=speed) as executor:
                    executor.map(lambda email: send_graphql_request(email.strip(), save), emails)
        # for email in emails:
        #     request_code(email.strip(), save)
        print()
        input(f"Registed and Non_Registed has been saved to {green}'{save}'{white} inside RESULT folder")
except FileNotFoundError:
    print(f"{red}Unable to locate file name '{path_to_email}'")
    if not path_to_email.endswith(".txt"):
        print()
        input(yellow + "Please make sure you include .txt if it has (Press enter to continue)")