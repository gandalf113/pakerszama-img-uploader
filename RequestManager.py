import requests


class RequestManager:
    def __init__(self, url):
        self.url = url

    def send_request(self, method, path, headers, payload={}):
        method = method.upper()
        path = path.strip()

        if method == 'GET':
            callback = requests.get
        elif method == 'POST':
            callback = requests.post
        elif method == 'PATCH':
            callback = requests.patch
        elif method == 'PUT':
            callback = requests.put
        elif method == 'DELETE':
            callback = requests.delete
        else:
            raise Exception(f'Method "{method}" not recognized.')

        if path[0] == '/':
            path = path[1:]

        if method in ['POST', 'PUT', 'PATCH']:
            res = callback(
                f'{self.url}{path}',
                data=payload,
                headers=headers
            )
        else:
            res = callback(f'{self.url}{path}')

        return res
