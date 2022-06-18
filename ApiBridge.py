import json

from RequestManager import RequestManager

class ApiBridge:
    def __init__(self, request_manager: RequestManager, auth_token: str):
        self.requests = request_manager
        self.headers = {
            "Authorization": f'Token {auth_token}',
            "Content-Type": "application/json"
        }

    def get_meals(self):
        data = self.requests.send_request(
            method="GET",
            path='/api/meal/meals/',
            headers={}
        ).text

        return json.loads(data)
