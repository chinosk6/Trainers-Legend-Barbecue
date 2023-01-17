import json

import requests
from .user_config import user_config


def get_userinfo(token: str):
    api = user_config.api_endpoint
    return requests.request("GET", f"{api}/api/get_userinfo", headers={"token": token}).text


def get_server_all_files():
    api = user_config.api_endpoint
    token = user_config.token
    return requests.request("GET", f"{api}/api/get_all_files", headers={"token": token}).text


def get_file(file_name: str, file_hash: str):
    api = user_config.api_endpoint
    token = user_config.token
    return requests.request("GET", f"{api}/file/get", headers={"token": token}, params={
        "filename": file_name,
        "hash": file_hash
    })


def upload_file(file_name: str, file_full_path: str, description: str):
    api = user_config.api_endpoint
    token = user_config.token
    url = f"{api}/api/post_file"
    payload = {'filename': file_name,
               'description': description}
    files = [
        ('file', (
            file_name,
            open(file_full_path, 'rb'),
            'text/plain'))
    ]
    headers = {
        'token': token
    }
    return requests.request("POST", url, headers=headers, data=payload, files=files)


def delete_file(filename: str):
    api = user_config.api_endpoint
    token = user_config.token
    url = f"{api}/api/delete_file"
    headers = {
        'token': token
    }
    return requests.request("DELETE", url, headers=headers, params={"filename": filename})


def update_token(new_token=None):
    api = user_config.api_endpoint
    token = user_config.token
    try:
        url = f"{api}/api/update_token"
        headers = {
            'token': token,
        }
        if new_token:
            params = {"new_token": new_token}
            headers["new_token"] = new_token
        else:
            params = None
        response = requests.request("GET", url, params=params, headers=headers)

        data = json.loads(response.text)
        if data.get("success", False):
            n_token = data.get("data", None)
            if n_token is None:
                return None
            user_config.token = n_token
            user_config.save_config()
            return n_token
    except BaseException:
        pass
    return None
