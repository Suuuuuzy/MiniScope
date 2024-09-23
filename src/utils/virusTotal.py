import requests

def get_passive_dns(domain, api_key):
    url = 'https://www.virustotal.com/vtapi/v2/domain/report'
    params = {
        'apikey': api_key,
        'domain': domain
    }

    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        # return data
        if 'resolutions' in data:
            return data['resolutions']
        else:
            print(f'No passive DNS data available for this domain: {domain}.')
            return None
    else:
        print(f'Error: {response.status_code}')
        return None

# Replace with your VirusTotal API key and the domain you want to query
api_key = '1a1dd4dad9427edcbbed9eace9993018f473ffd4ee4629521f8dc0c68c1892a2'
domain = 'wxardm.weixin.qq.com'

resolutions = get_passive_dns(domain, api_key)
# print(resolutions)
if resolutions:
    for resolution in resolutions:
        print(f"IP Address: {resolution['ip_address']}, Last Resolved: {resolution['last_resolved']}")
