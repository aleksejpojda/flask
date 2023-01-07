import requests

interface = 'GigabitEthernet0/1'
data = {"10.1.77.2_10.1.77.2_data.yml": { "interfaces": {
    'GigabitEthernet0/1': {
    "description": "Cisco-880-ZAI",
    "mode": "access",
    "portfast": "edge",
    "vlan_access": 105,
    "vlan_native": None,
    "vlan_trunk": None,
    "vlan_voice": None
    }
    }
    }
}

req = requests.post('http://127.0.0.1:5000/api/data/10.1.77.2_10.1.77.2_data.yml/GigabitEthernet0_1', json=data)
req_get = requests.get('http://127.0.0.1:5000/api/errors/10.43.255.109_new_data.yml')
print(req_get.content)