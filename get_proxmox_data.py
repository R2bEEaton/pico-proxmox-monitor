import urequests as requests
import ujson as json

# Proxmox API credentials
PROXMOX_HOST = "https://192.168.1.228:8006" # change to your proxmox IP address
API_TOKEN = "xxx@xxx!xxx=xx-xxxx-xxx" # change to your proxmox API token

# Function to make requests to the Proxmox API
def proxmox_get(endpoint):
    url = f"{PROXMOX_HOST}/api2/json{endpoint}"
    headers = {
        'Authorization': f'PVEAPIToken={API_TOKEN}',
        'Accept': 'application/json',
    }
    
    try:
        # Make the GET request to the API
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Request failed: {e}")
        return None

# Get usage statistics for a specific node
def get_node_usage(node_name):
    endpoint = f"/nodes/{node_name}/status"
    data = proxmox_get(endpoint)
    if data is not None:
        return {"cpu": data['data']['cpu'], "memory": data['data']['memory']['used'] / data['data']['memory']['total'], "storage": data['data']['rootfs']['used'] / data['data']['rootfs']['total']}
    return {"cpu": -1, "memory": -1, "storage": -1}


if __name__ == '__main__':
    print(get_node_usage('proxmox'))
