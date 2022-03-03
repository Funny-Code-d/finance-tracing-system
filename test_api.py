import requests

res = requests.get("http://funny-code.ru/api/token/v1/user/settings/?params=test")
print(res.json())
# for item in res.json():
#     print(f"ID: {item['user_id']}")
#     print(f"First name: {item['first_name']}")
#     print(f"Last_name: {item['last_name']}")
# for item in res.text:
#     print(f"ID: {item['user_id']}")
#     print(f"First name: {item['first_name']}")
#     print(f"Last_name: {item['last_name']}")

# for item in res.text:
#     print("---")
#     print(item)