import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

username = ""
api_key = ""

def fetch_programs(username, secret):
    if username and secret:
        programs = []
        h1_api = "https://api.hackerone.com/v1/hackers/programs"
        params = {"page[number]":1, "page[size]": 100}
        try:
            while True:
                fetched_data = requests.get(h1_api, verify = False, timeout = 20, auth=(username, secret), params=params)
                if fetched_data.status_code == 200:
                    parsed_data = json.loads(fetched_data.content)
                    if parsed_data['data']:
                        for program in parsed_data['data']:
                            if program['attributes']['offers_bounties']:
                                programs.append(program['attributes']['handle'])
                            else:
                                continue
                        params['page[number]'] +=1
                    else:
                        break
                else:
                    print(f"[-] Couldn't reach the api or the credentials are wrong: {fetched_data.status_code}")
        except Exception as err:
            print(f"[-] Something went wrong: {err}")
        return programs



def subscribe():
    fetched_programs = fetch_programs(username, api_key)
    for program in fetched_programs:
        program = program.strip()
        try:
            while True:
                url = "https://hackerone.com/graphql"
                cookies = {
                    "h1_device_id": "",
                    "__Host-session": "",
                }
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
                    "Content-Type": "application/json",
                    "X-Csrf-Token": ""
                }
                graphql_query = {
                    "operationName":"UpdateSubscription",
                    "variables":{
                        "handle":f"{program}",
                        "product_area":"team_profile",
                        "product_feature":"overview"},
                    "query":"mutation UpdateSubscription($handle: String!) {\n  toggleTeamUpdatesSubscription(input: {handle: $handle}) {\n    was_successful\n    team {\n      id\n      policy_setting {\n        id\n        subscribed\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"
                    }
                response = requests.post(url, verify=False, json=graphql_query, headers=headers, timeout=20, cookies=cookies)
                if response.status_code == 200:
                    json_response = response.json()
                    is_sub = json_response.get('data', {}).get('toggleTeamUpdatesSubscription', {}).get('team', {}).get('policy_setting', {}).get('subscribed')
                    if is_sub == True:
                        print(f"[+] You have subscribed to {program}")
                        break
                    else:
                        print(f"[-] Failed to subscribe to {program} retrying now")

        except Exception as err:
            print(err)

subscribe()