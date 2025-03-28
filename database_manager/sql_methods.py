from sql_lite.sql_lite import SqlLite
import os
import json



# files paths
src_path = 'C:/AndroRPA'
assets_path = 'C:/AndroRPA/assets'
cache_path = 'C:/AndroRPA/cache'
apps_path = 'C:/AndroRPA/apps'
data_path = 'C:/AndroRPA/data'
exec_path = '/exec_files'
platform_tools_path = 'C:/AndroRPA/platform-tools'

database_path = os.path.join(data_path, 'temp_data.db')
database = SqlLite(database_path)




# settings methods
def update_setting(setting_name, value):
    try:
        query = f"UPDATE settings SET value='{value}' WHERE name='{setting_name}'"
        database.execute_query(query)
        print(f"Setting '{setting_name}' updated successfully to '{value}'")
    except Exception as e:
        print(f"An error occurred: {e}")


def get_setting(setting_name):
      try:
          query = f"SELECT value FROM settings WHERE name='{setting_name}'"
          result = database.fetch_query(query)
          return result[0][0] if result else None
      except Exception as e:
          print(f"An error occurred: {e}")

# credentials methods
def update_credentials(email, password):
    try:
        query = f"UPDATE credentials SET password='{password}', email='{email}'"
        database.execute_query(query)
        print(f"Credentials for '{email}' updated successfully")
    except Exception as e:
        print(f"An error occurred: {e}")


def get_credentials():
    """try:
        query = "SELECT * FROM credentials"
        result = database.fetch_query(query)
        if result:
            result = result[0]
            email = result[0]
            password = result[1]
            return {'email': email, 'password': password}
        else:
            return None

    except Exception as e:
        print(f"An error occurred: {e}")"""

    # charged json data
    try:
        with open(f'{data_path}/token.json', 'r', encoding='utf-8') as file:
            data_ = json.load(file)
        return data_
    except Exception as e:
        print(f'Error in get credentials: {e}')


# user credentials methods
def update_user(username, email, plan, expired_date):
    try:
        query = f"UPDATE user SET email='{email}', plan='{plan}', expired_date='{expired_date}', username='{username}'"
        database.execute_query(query)
        print(f"User credentials for '{username}' or '{email}' updated successfully")
    except Exception as e:
        print(f"An error occurred: {e}")


def get_user_data():
    try:
        query = "SELECT * FROM user"
        result = database.fetch_query(query)
        if result:
            result = result[0]
            email = result[0]
            username = result[1]
            plan = result[2]
            expired_date = result[3]
            return {'username': username, 'email': email, 'plan': plan, 'expired_date': expired_date}
    except Exception as e:
        print(f"An error occurred: {e}")


# proxy records methods --------------------------------
def add_proxy_record(ip, port, username, password):
    try:
        query = f"INSERT INTO proxy_records (ip, port, username, password) VALUES ('{ip}', {port}, '{username}', '{password}')"
        database.execute_query(query)
        print(f"Proxy record added successfully")
    except Exception as e:
        print(f"An error occurred: {e}")

def clear_all_proxy_records():
    try:
        query = "DELETE FROM proxy_records"
        database.execute_query(query)
        print("All proxy records cleared successfully")
    except Exception as e:
        print(f"An error occurred: {e}")

def get_all_proxy_records():
    try:
        query = "SELECT * FROM proxy_records"
        result = database.fetch_query(query)
        if result:
            return result
        else:
            return None
    except Exception as e:
        print(f"An error occurred: {e}")

def check_proxy_if_proxy_in_records(ip):
    try:
        query = f"SELECT * FROM proxy_records WHERE ip='{ip}'"
        result = database.fetch_query(query)
        if result:
            return True
        else:
            return False
    except Exception as e:
        print(f"An error occurred: {e}")

# ----------------------------------------------

if __name__ == "__main__":
    # Example usage
    pass
    #update_setting('artists_file', 'text.ee')
    #print(get_setting('tracks_file'))

    #update_credentials('new_email@example.com', 'new_password')
    #print(get_credentials())

    #update_user('new_username', 'new_email@example.com', 'premium', '2022-12-31')
    #print(get_user_data())
