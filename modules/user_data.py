import psycopg2

from modules.utils import Config as cfg


class GetUserToken:
    def __init__(self, user_id):
        connection = psycopg2.connect(
            user=cfg().database_user,
            password=cfg().database_password,
            host=cfg().database_host,
            database=cfg().database_name,
        )

        cursor = connection.cursor()
        try:
            cursor.execute(
                """SELECT token FROM access_tokens WHERE access_tokens.user_id != %s;""",
                [user_id])

            select_data = cursor.fetchone()
            self.token = select_data[0]

        except (Exception, psycopg2.Error) as error:
            print("ERROR! SharedRooms module", flush=True)
            print(error, flush=True)
        finally:
            if connection:
                cursor.close()
                connection.close()
