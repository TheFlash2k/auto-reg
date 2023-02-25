# auto-reg
An automated script that takes a list of users and registers them on the CTFD platform


Usage:
```
python3 main.py
```

## How to use?
In order to use this, we need to firstly generate an `ACCESS TOKEN` from the Users page. Then, we will have to modify `config.json`. Once done, the script will validate the inputs and then make the requests to add the users.


## Format:
The `.csv` format that should be passed to it is as following:
```
TEAM_NAME | USER_1_USERNAME | USER_N_USERNAME | USER_1_EMAIL | USER_N_EMAIL
```

Ensure that Team names aren't the same, otherwise the script will break. Logs are also maintained to check for error manually.
