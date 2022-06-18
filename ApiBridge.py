import json

from RequestManager import RequestManager


class ApiBridge:
    def __init__(self, request_manager: RequestManager, auth_token: str):
        self.requests = request_manager
        self.headers = {
            "Authorization": f'Token {auth_token}',
            # "Content-Type": "application/json"
        }

    def get_meals(self):
        data = self.requests.send_request(
            method="GET",
            path='/api/meal/meals/',
            headers=self.headers
        ).text

        return json.loads(data)

    def upload_image(self, meal_id: int, image_path: str):
        data = self.requests.send_request(
            method="POST",
            path=f'/api/meal/meals/{meal_id}/upload-image/',
            headers=self.headers,
            files=[
                ('image', ('myimage.jpg', open(
                    image_path, 'rb'), 'image/jpeg'))
            ]
        ).text

        return json.loads(data)
