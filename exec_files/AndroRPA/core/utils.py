import uiautomator2
import os
import requests
import shutil
import zipfile
import winreg

from setuptools.archive_util import unpack_zipfile


#
# os methods
def download(url, directory):
    try:
        filename = url.split('/')[-1]
        complete_file_path = os.path.join(directory, filename)

        resp = requests.get(url)
        resp.raise_for_status()

        with open(complete_file_path, 'wb') as f:
            f.write(resp.content)
            print(f"Downloaded {filename} to {directory}")
            return True

    except requests.exceptions.RequestException as e:
        print(f"Error downloading {url}: {e}")
    except OSError as e:
        print(f"Error writing to {directory}: {e}")

def delete_file(filename):
    try:
        os.remove(filename)
        print(f"Deleted {filename}")
        return True
    except OSError as e:
        print(f"Error deleting {filename}: {e}")

def delete_directory(directory):
    try:
        shutil.rmtree(directory)
        print(f"Deleted directory {directory}")
        return True
    except OSError as e:
        print(f"Error deleting {directory}: {e}")

def unzip_file(file, directory):
    try:
        with zipfile.ZipFile(file, 'r') as zip_ref:
            zip_ref.extractall(directory)
            print(f"Extracted {file} to {directory}")
            return True
    except zipfile.BadZipfile as e:
        print(f"Error extracting {file}: {e}")

def add_environment_value(name, value):
    try:
        key_env = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment", 0, winreg.KEY_READ)
        current_value, _ = winreg.QueryValueEx(key_env, name)
        winreg.CloseKey(key_env)

        if value in str(current_value).split(';'):
            print(f"{name} already set to {value}")
            return True

        new_value = f"{current_value};{value}"

        key_env = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment", 0, winreg.KEY_WRITE)
        winreg.SetValueEx(key_env, name, 0, winreg.REG_SZ, new_value)
        winreg.CloseKey(key_env)

        print(f"Added {name} to environment variable with value {value}")
        return True

    except Exception as e:
        print(f"Error adding {name} to environment variable: {e}")



if __name__ == "__main__":
    #download('https://gp2.liteapks.com/Facebook%20Lite/Facebook%20Lite-451.0.0.0.4.apk', '.')
    unpack_zipfile('platform-tools-latest-windows.zip', 'C:/')



