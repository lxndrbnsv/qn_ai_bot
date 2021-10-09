import traceback

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
                """SELECT token FROM access_tokens WHERE user_id = %s;""",
                [user_id])

            select_data = cursor.fetchone()
            if select_data is not None:
                self.token = select_data[0]
            else:
                self.token = None

        except (Exception, psycopg2.Error) as error:
            traceback.print_exc()
            print(error, flush=True)
        finally:
            if connection:
                cursor.close()
                connection.close()


class GetTokenHolder:
    def __init__(self, token):
        connection = psycopg2.connect(
            user=cfg().database_user,
            password=cfg().database_password,
            host=cfg().database_host,
            database=cfg().database_name,
        )

        cursor = connection.cursor()
        try:
            cursor.execute(
                """SELECT user_id FROM access_tokens WHERE token = %s;""",
                [token])

            select_data = cursor.fetchone()
            if select_data is not None:
                self.user = select_data[0]
            else:
                self.user = None

        except (Exception, psycopg2.Error) as error:
            traceback.print_exc()
            print(error, flush=True)
        finally:
            if connection:
                cursor.close()
                connection.close()
