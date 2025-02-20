import requests
import json

session = requests.Session()
### registering a test user
resp = session.post(
    "http://localhost:9999/User/register",
    json={
        "username": "avatar_test",
        "password": "super secret",
        "email": "avatar_test@example.com",
    },
)

### login
print("login")
resp = session.post(
    "http://localhost:9999/Session/login",
    json={
        "username": "avatar_test",
        "password": "super secret",
    },
)
img_counter = 0
print("uploading image")
resp = session.post(
    "http://localhost:9999/Image",
    files={f"upload_file_{img_counter}.png": open("./example_image.png", "rb")},
)
img_counter = 1
resp = session.post(
    "http://localhost:9999/Image",
    files={f"upload_file_{img_counter}.png": open("./example_image2.png", "rb")},
)
print(resp.text)

# get avatar
user_resp = session.get("http://localhost:9999/Image")
print(user_resp.json())
