import requests
from prettytable import PrettyTable

with open('token.txt') as file:
    TOKEN = file.readline()


def get_user_info(user_id):
    params = {
        'access_token': TOKEN,
        'user_id': user_id,
        'v': 5.131
    }
    req = requests.get("https://api.vk.com/method/users.get?", params=params).json()
    info = req["response"][0]
    return info


def get_friends(user_id):
    friends_req = requests.get("https://api.vk.com/method/friends.get?",
                               params={
                                   'access_token': TOKEN,
                                   'user_id': user_id,
                                   'v': 5.131
                               }).json()['response']
    print_table(friends_req)


def print_table(req_info):
    table = PrettyTable()
    table.field_names = ["Name", "ID"]
    for item in req_info["items"]:
        info = get_user_info(item)
        name = f"{info['first_name']} {info['last_name']}"
        if info['is_closed']:
            table.add_row([name, info['id']])
        print(info['id'], info['first_name'], info['last_name'])
    print(table)


def main():
    user_id = input("Enter user id: ")
    get_friends(user_id)


if __name__ == '__main__':
    main()
