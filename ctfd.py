import requests

def log(*args, **kwargs):
    with open("log.txt", "a") as f:
        print(*args, **kwargs, file=f)

class CTFD:

    def __init__(self, url, token):
        self.URL = url
        self.headers = {
            "Authorization": f"Token {token}",
            "Content-Type": "application/json"
        }

    ''' Validation methods '''
    def is_team(self, team_name : str = None, team_id : int = None):
        r = requests.get(f"{self.self.URL}/teams", headers=self.headers)
        log(r.json())
        for i in r.json()['data']:
            if i['name'] == team_name or i['id'] == team_id:
                return True
        return False

    def is_user(self, user_name : str = None, user_id : int = None):
        r = requests.get(f"{self.URL}/users", headers=self.headers)
        for i in r.json()['data']:
            if i['name'] == user_name or i['id'] == user_id:
                return True
        return False

    def get_team_id(self, team_name : str):
        r = requests.get(f"{self.URL}/teams", headers=self.headers)
        for i in r.json()['data']:
            if i['name'] == team_name:
                return i['id']
        return -1

    def get_user_id(self, user_name):
        r = requests.get(f"{self.URL}/users", headers=self.headers)
        for i in r.json()['data']:
            if i['name'] == user_name:
                return i['id']
        return -1

    ''' Team methods '''
    def create_team(self, team_name, password) -> int:
        r = requests.post(f"{self.URL}/teams", headers=self.headers, json={
            "name": team_name,
            "password": password
        })
        log(f"[DEBUG] create_team: {r.json()}")
        return r.json()['data']['id']

    ''' User methods '''
    def create_user(self, user_name, password, email, team_id):
        r = requests.post(f"{self.URL}/users", headers=self.headers, json={
            "name": user_name,
            "password": password,
            "email": email,
            "team_id": team_id
        })
        log(f"[DEBUG] create_user: {r.json()}")

        uid = r.json()['data']['id']
        log(f"[DEBUG] ==> Adding to team: {uid} -> {team_id}")
        r = requests.post(f"{self.URL}/teams/{team_id}/members", headers=self.headers, json={"user_id": uid})
        log(f"[DEBUG] ==> {r.json()}")
        return uid