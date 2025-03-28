import random

from sql_lite.sql_lite import SqlLite
import os


database_path = os.path.join('c:/AndroRPA/data', 'temp_data.db')
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
    try:
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
        print(f"An error occurred: {e}")


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


# accounts methods
def add_account(email, password, state='inactive'):
    try:
        query = f"INSERT INTO accounts (email, password, state) VALUES ('{email}', '{password}', '{state}')"
        database.execute_query(query)
        print(f"Account '{email}' added successfully")
    except Exception as e:
        print(f"An error occurred: {e}")

def get_account(email):
    try:
        query = f"SELECT * FROM accounts WHERE email='{email}'"
        result = database.fetch_query(query)
        if result:
            result = result[0]
            email = result[0]
            password = result[1]
            state = result[2]
            return {'email': email, 'password': password,'state': state}
    except Exception as e:
        print(f"An error occurred: {e}")

def get_all_accounts_by_state(state='inactive'):
    try:
        query = f"SELECT * FROM accounts WHERE state='{state}'"
        result = database.fetch_query(query)
        if result:
            accounts = []
            result = result
            for account in result:
                email = account[0]
                password = account[1]
                state = account[2]
                accounts.append({'email': email, 'password': password,'state': state})

            return accounts
    except Exception as e:
        print(f"An error occurred: {e}")

def update_account(email, state='inactive'):
    try:
        query = f"UPDATE accounts SET state='{state}' WHERE email='{email}'"
        database.execute_query(query)
        print(f"Account '{email}' state updated successfully to '{state}'")

    except Exception as e:
        print(f"An error occurred: {e}")


def clear_account_table():
    try:
        query = "DELETE FROM accounts"
        database.execute_query(query)
        print("Account table cleared successfully")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Example usage
    pass
    #update_setting('artists_file', 'text.ee')
    #print(get_setting('tracks_file'))

    #update_credentials('new_email@example.com', 'new_password')
    #print(get_credentials())

    #update_user('new_username', 'new_email@example.com', 'premium', '2022-12-31')
    #print(get_user_data())

    # ----------------
    #add_account('new_email@exdample.com', 'new_password')
    #print(get_account('new_email@example.com'))

    print(random.choice(get_all_accounts_by_state('inactive')))

    #update_account('new_email@example.com', password='new_password_updated', state='bad')
    #clear_account_table()
