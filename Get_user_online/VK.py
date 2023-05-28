import vk_api


def get_user_friends_online(api_vk, user_id):
    friends_list = api_vk.friends.get(user_id=user_id, fields='online')
    friends_count = friends_list['count']

    with open(r"friends_list.txt", "w") as file:
        count_output = f'Количество друзей: {friends_count}\n'
        file.write(count_output + '\n\n')
        for friend in friends_list['items']:
            output = f"{friend['first_name']} {friend['last_name']} : online={friend['online']}"
            print(output)
            file.write(output + '\n')
        print('\n' + count_output)


def main():
    with open('token.txt') as file:
        access_token = file.readline()  # access token
    target_id = int(input('ID пользователя: '))

    api_vk = vk_api.VkApi(token=access_token).get_api()
    get_user_friends_online(api_vk, target_id)


if __name__ == '__main__':
    main()
