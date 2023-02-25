import csv
import random
import string
import json
from pprint import pprint
from ctfd import CTFD, log

def get_random_password(len = 20):
    return ''.join(random.choice(string.ascii_letters + string.digits) for i in range(len))

def _inc(c):
    c[0] += 1
    return c

def get_users():
    users = []
    with open(file_name, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            users.append(row)
    return_users = {}
    for i in range(1, len(users)):
        c = [num_members]
        try:
            return_users[users[i][0].strip().title()] = {
                "password": get_random_password(),
                "members": {
                    f"{j.strip().title()}" : {
                            "password" : get_random_password(),
                            "email" : users[i][_inc(c)[0]].strip().replace(' ', '')
                    } for j in users[i][1:num_members + 1] if j != ''
                },
            }
        except:
            pass

    for team in return_users.keys():
        for user in return_users[team]['members'].keys():
            if return_users[team]['members'][user]['email'] == '':
                return_users[team]['members'][user]['email'] = f"{user.lower().replace(' ', '.')}@{default_email_domain}"
                
    return return_users

if __name__ == "__main__":

    # Read from config file
    with open("config.json", "r") as f:
        config = json.load(f)
        TOKEN = config["TOKEN"]
        URL = config["URL"]
        default_email_domain = config["DEFAULT_EMAIL_DOMAIN"]
        num_members = config["NUM_MEMBERS"]
        file_name = config["IN_FILE"]
        out_file = config["OUT_FILE"]

    if TOKEN == "":
        print("Please enter a valid token in config.json")
        exit(1)

    ctfd = CTFD(URL, TOKEN)
    users = get_users()
    for i in users:
        with open(out_file, "a") as f:
            writer = csv.writer(f)
            data = [i, users[i]["password"]]
            j = 0
            for name, fields in users[i]['members'].items():
                data.append(f"{name}:{fields['password']}")
                j += 1
            
            if j < num_members:
                for _ in range(num_members - j):
                    data.append("")
            
            for user in users[i]['members'].values():
                data.append(user['email'])
            writer.writerow(data)

        log(f"Current team: {i} ==> {users[i]['members'].keys()}\n")
        try:
            team_id = -1
            if not ctfd.is_team(team_name = i):
                print(f"Registering team: {i}", end = '')
                team_id = ctfd.create_team(i, users[i]["password"])
                print(f" [OK] [ID: {team_id}]")

            if team_id == -1:
                team_id = ctfd.get_team_id(team_name = i)

            for name, fields in users[i]['members'].items():
                if not ctfd.is_user(user_name=name):
                    print(f"===> Registering user: {name}", end = '')
                    user_id = ctfd.create_user(name, fields["password"], fields['email'], team_id)
                    print(f" [OK] [ID: {user_id}]")
        except:
            continue
