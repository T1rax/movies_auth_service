import requests

data = {'login': 'test_login10',
        'password': 'test_password',
        'first_name': 'Nikola',
        'last_name': 'Lenivetc'}

response = requests.post('http://127.0.0.1/sign-up', json=data)

print(response.text)
print(response.cookies)