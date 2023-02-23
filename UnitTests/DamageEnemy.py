import requests
from Routes.battle import damage_enemy

def test_damage():
    data = {
        "enemy_id": "63acdf61d0c2668b1336d319",
        "damage": 50
    }
    headers = {
        'Content-Length': str(data.__sizeof__()),
        'Content-type': 'application/x-www-form-urlencoded',
        'Accept': '*/*',
        'Connection': 'keep-alive'
    }

    print(requests.post('http://127.0.0.1:5000/battle/damage_enemy', data=data, headers=headers, verify=False).text)

if __name__ == '__main__':
    test_damage()
