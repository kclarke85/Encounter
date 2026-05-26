import geoip2.database

def get_location_from_ip(ip_address, database_path='GeoLite2-City.mmdb'):
    try:
        with geoip2.database.Reader(database_path) as reader:
            response = reader.city(ip_address)

            country = response.country.name
            region = response.subdivisions.most_specific.name if response.subdivisions else None
            city = response.city.name
            postal_code = response.postal.code
            latitude = response.location.latitude
            longitude = response.location.longitude
            isp = None # GeoLite2 doesn't directly provide ISP

            print(f"IP: {ip_address}")
            print(f"Country: {country}")
            print(f"Region: {region}")
            print(f"City: {city}")
            print(f"Postal Code: {postal_code}")
            print(f"Latitude: {latitude}, Longitude: {longitude}")
            print("-" * 30)

    except geoip2.errors.AddressNotFoundError:
        print(f"Location not found for IP: {ip_address}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
# Use a known public IP address (replace with your visitor's IP)
# For testing, you can use a sample IP or your own public IP.
# You'd typically get visitor IPs from your web server logs (e.g., Apache, Nginx, or Flask/Django request objects)

# Example IP addresses:
# A general IP (may resolve to a general region)
get_location_from_ip('8.8.8.8')

# An example IP that might route through a data center (like a known Microsoft Azure IP, for illustrative purposes)
# Note: Specific data center IPs change and might not always resolve to the exact physical location publicly.
# This is just for demonstration of what you'd feed the function.
get_location_from_ip('40.78.149.8') # This might resolve to a Microsoft Azure datacenter location

# A local IP (will raise AddressNotFoundError)
# get_location_from_ip('192.168.1.1')