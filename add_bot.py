import sys
import json
import time
import traceback

import psycopg2
import requests

from modules.utils import Config as cfg
from modules.user_data import GetUserToken, GetTokenHolder


# sys.stdout = open("./add_bot.log", "w")
# sys.stderr = open("./add_bot.log", "w")


def get_users():
    users = []
    connection = psycopg2.connect(
        user=cfg().database_user,
        password=cfg().database_password,
        host=cfg().database_host,
        database=cfg().database_name,
    )

    cursor = connection.cursor()
    try:
        cursor.execute(
            """SELECT name FROM users WHERE name != %s;""",
            [cfg().bot_id])

        select_data = cursor.fetchall()
        for s in select_data:
            users.append(s[0])

    except (Exception, psycopg2.Error) as error:
        print("ERROR! SharedRooms module", flush=True)
        print(error, flush=True)
    finally:
        if connection:
            cursor.close()
            connection.close()

    return users


def create_room(user_to_invite):
    url = f"{cfg().matrix_api_url}/_matrix/client/r0/createRoom"
    room_creator_token = bot_token
    print("Token: ", room_creator_token)
    headers = {
        "headers": "Content-type: application/json",
        "Authorization": "Bearer " + room_creator_token
    }
    data = {
        "preset": "trusted_private_chat",
        "invite": [user_to_invite],
        "is_direct": True
    }
    r = requests.post(url=url, headers=headers, json=data)
    print(data, flush=True)
    print(json.loads(r.text), flush=True)
    try:
        return json.loads(r.text)["room_id"]
    except KeyError:
        print(json.loads(r.text))
        return None


def send_hello_message(room_id):
    hello_message = "I am artificial intelligence." \
                    " You can communicate with me on any topic," \
                    " ask any questions and use me as a personal assistant!\n\n" \
                    "Я искусственный интеллект. Вы можете общаться со мной на любую тему," \
                    " задавать любые вопросы и использовать меня как личного помощника!\n\n" \
                    "Ben yapay zekayım. Benimle her konuda iletişim kurabilir, " \
                    "soru sorabilir ve beni kişisel asistan olarak kullanabilirsiniz!\n\n" \
                    "Soy inteligencia artificial. ¡Puedes comunicarte conmigo sobre cualquier tema," \
                    " hacer cualquier pregunta y usarme como asistente personal!\n\n" \
                    "Ich bin künstliche Intelligenz. " \
                    "Sie können mit mir zu jedem Thema kommunizieren," \
                    " Fragen stellen und mich als persönlichen Assistenten nutzen!"

    url = (
        f"{cfg().matrix_api_url}/_matrix/client/r0/rooms/"
        f"{room_id}/send/m.room.message?access_token={bot_token}"
    )
    headers = {"headers": "Content-type: application/json"}
    data = {"msgtype": "m.direct", "body": hello_message}
    r = requests.post(url=url, headers=headers, json=data)


def login_as_user(user_id, admin_token):
    url = f"{cfg().matrix_api_url}/_synapse/admin/v1/users/{user_id}/login"
    auth_header = {"Authorization": f"Bearer {admin_token}"}
    response = requests.post(url, headers=auth_header)
    return json.loads(response.text)["access_token"]


def join_via_invite(room, token):
    url = (
        f"{cfg().matrix_api_url}/_matrix/client/r0/"
        f"rooms/{room}/join?access_token={token}"
    )
    headers = {"headers": "Content-type: application/json"}
    data = {"is_direct": True}
    r = requests.post(url=url, headers=headers, json=data)
    return json.loads(r.text)



def login():
    bot_id = cfg().bot_id
    login_url = f"{cfg().matrix_api_url}/_matrix/client/r0/login"
    data = dict(
        type="m.login.password",
        identifier=dict(
            type="m.id.user",
            user=bot_id
        ),
        password=cfg().bot_password,
        initial_device_display_name="QN API"
    )
    r = requests.post(login_url, json=data)

    return json.loads(r.text)["access_token"]



def generate_users_bl():
    users = []
    connection = psycopg2.connect(
        user=cfg().database_user,
        password=cfg().database_password,
        host=cfg().database_host,
        database=cfg().database_name,
    )

    cursor = connection.cursor()
    try:
        cursor.execute(
            """SELECT other_user_id FROM users_who_share_private_rooms WHERE user_id = %s;""",
            [cfg().bot_id])

        select_data = cursor.fetchall()
        for s in select_data:
            if s[0] not in users:
                users.append(s[0])

    except (Exception, psycopg2.Error) as error:
        print("ERROR! SharedRooms module", flush=True)
        print(error, flush=True)
    finally:
        if connection:
            cursor.close()
            connection.close()

    return users

# USERS_BL = [
#     "@qn18:m.mybusines.app",
#     "@qn1037668:m.mybusines.app,"
#     "@qn1043177:m.mybusines.app",
#     "@qn1041178:m.mybusines.app",
#     "@qn1043178:m.mybusines.app",
#     "@qn1036770:m.mybusines.app",
#     "@qn1043176:m.mybusines.app",
#     "@qn1043179:m.mybusines.app",
#     "@qn20444:m.mybusines.app",
#     "@qn1042402:m.mybusines.app"
# ]
# USERS_BL = []
USERS_BL = generate_users_bl()

if __name__ == '__main__':
    for u in USERS_BL:
        print(u)
    # bot_token = login()
    # all_users = get_users()
    # for u in all_users:
    #     try:
    #         if u not in USERS_BL:
    #             room_id = create_room(u)
    #             send_hello_message(room_id)
    #
    #             time.sleep(1)
    #
    #             user_token = login_as_user(u, bot_token)
    #             if user_token is not None:
    #                 if room_id is not None:
    #                     join_via_invite(
    #                         room=room_id,
    #                         token=user_token
    #                     )
    #                 else:
    #                     print(room_id)
    #             else:
    #                 print("Token is None!\n", "User: ", u)
    #     except Exception:
    #         traceback.print_exc()
    #         with open("unable_to_add.txt", "a+") as error_file:
    #             error_file.write(
    #                 f"{u}\n"
    #             )
