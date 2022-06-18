import requests


class RequestManager:
    def __init__(self, url):
        self.url = url

    def send_request(self, method, path, headers, payload={}, files=[]):
        method = method.upper()
        path = path.strip()

        if path[0] == '/':
            path = path[1:]

        res = requests.request(
            method=method,
            url=f'{self.url}{path}',
            headers=headers,
            data=payload,
            files=files
        )

        return res
