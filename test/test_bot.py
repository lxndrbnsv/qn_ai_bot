import datetime
import json
import sys
import asyncio

import requests
from nio import AsyncClient, MatrixRoom, RoomMessageText, SyncResponse

from modules.utils import Config as cfg
from modules.user_data import GetUserToken


# sys.stdout = open("./test_bot.log", "w")
# sys.stderr = open("./test_bot.log", "w")


start_time = int(str(round(datetime.datetime.now().timestamp(), 3)).replace(".", ""))


async def send_room_message(message, room_id):
    url = (
        f"https://test.matrix.mybusines.app/_matrix/client/r0/rooms/"
        f"{room_id}/send/m.room.message?access_token={GetUserToken(cfg().bot_id).token}"
    )
    headers = {"headers": "Content-type: application/json"}
    data = {"msgtype": "m.text", "body": message}
    print("Message data: ", data)
    r = requests.post(url=url, headers=headers, json=data)
    return json.loads(r.text)


async def get_ai_response(message, sender):
    url = f"https://qaim.me/userapi/ai/{cfg().api_key}/"
    payload = dict(
        data=json.dumps(dict(
            q=message,
            ai=cfg().ai_id,
            client_id=sender,
            lng="en",
        ),
            ensure_ascii=False
        )
    )

    r = requests.post(url, data=payload)
    print("Response results: ", r, r.text)
    try:
        return json.loads(r.text)[1]
    except IndexError:
        pass


async def message_handler(room: MatrixRoom, event: RoomMessageText) -> None:
    print(
        f"Message received in room {room.display_name}\n"
        f"{room.user_name(event.sender)} | {event.body}"
    )
    if event.sender != cfg().bot_id:
        event_server_timestamp = event.server_timestamp
        if event_server_timestamp >= start_time:
            print("--- --- ---")
            print(
                "Current timestamp: ",
                round(
                    datetime.datetime.now().timestamp(),
                    3
                )
            )
            print("Event: ", event.server_timestamp)
            print("Start: ", start_time)
            print(event)

            print("--- --- ---")
            sender_id = event.sender
            msg_body = event.body

            ai_response = await get_ai_response(msg_body, sender_id)
            await send_room_message(ai_response, room.room_id)


async def main() -> None:
    client = AsyncClient(
        "https://test.matrix.mybusines.app", cfg().bot_id
    )
    client.add_event_callback(message_handler, RoomMessageText)

    print(await client.login(cfg().bot_password))

    await client.sync_forever(timeout=30000)  # milliseconds


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())

