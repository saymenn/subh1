# subh1
A simple scripte that I built to automate program subscription on hackerone

# how it works:
- The script will fetch every public and private program you can access from hackerone's restAPI, the send a Graphql query for reach of the fetched programs. Note currently it only subscribes to bounty programs, if you're willing to subscribe to VDPs just remove the offers_bounties condition.

# requirements:
- The script needs a valid h1 username, api_key, __Host-session cookie and h1_device_id cookie in order to work. Upon providing those just run the script and it will issue a subscription request to every private or public bounty program
