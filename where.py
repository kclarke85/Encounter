import requests

ip = "99.135.106.243"

def get_ip_location(ip):
    response = requests.get(f"http://ip-api.com/json/{ip}")
    data = response.json()
    if data["status"] == "success":
        print(f"IP: {ip}")
        print(f"City: {data.get('city')}")
        print(f"Region: {data.get('regionName')}")
        print(f"Country: {data.get('country')}")
        print(f"Coordinates: {data.get('lat')}, {data.get('lon')}")
        print(f"ISP: {data.get('isp')}")
    else:
        print("Could not fetch location info.")

get_ip_location(ip)
