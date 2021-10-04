import sys
import json
import time

import psycopg2
import requests

from modules.utils import Config as cfg
from modules.user_data import GetUserToken


sys.stdout = open("./add_bot.log", "w")
sys.stderr = open("./add_bot.log", "w")


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
    url = f"https://{cfg().matrix_api_url}/_matrix/client/r0/createRoom"
    room_creator_token = GetUserToken(cfg().bot_id).token
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
        f"https://{cfg().matrix_api_url}/_matrix/client/r0/rooms/"
        f"{room_id}/send/m.room.message?access_token={GetUserToken(cfg().bot_id).token}"
    )
    headers = {"headers": "Content-type: application/json"}
    data = {"msgtype": "m.direct", "body": hello_message}
    r = requests.post(url=url, headers=headers, json=data)


def login_as_user(user_id, admin_token):
    url = f"https://{cfg().matrix_api_url}/_synapse/admin/v1/users/{user_id}/login"
    auth_header = {"Authorization": f"Bearer {admin_token}"}
    response = requests.post(url, headers=auth_header)
    return json.loads(response.text)["access_token"]


def join_via_invite(room, token):
    url = (
        f"https://{cfg().matrix_api_url}/_matrix/client/r0/"
        f"rooms/{room}/join?access_token={token}"
    )
    headers = {"headers": "Content-type: application/json"}
    data = {"is_direct": True}
    r = requests.post(url=url, headers=headers, json=data)
    return json.loads(r.text)


if __name__ == '__main__':
    all_users = get_users()
    for u in all_users:
        room_id = create_room(u)
        send_hello_message(room_id)

        time.sleep(1)

        user_token = login_as_user(u, cfg().admin_token)
        if user_token is not None:
            if room_id is not None:
                join_via_invite(
                    room=room_id,
                    token=user_token
                )
            else:
                print(room_id)
        else:
            print("Token is None!\n", "User: ", u)
