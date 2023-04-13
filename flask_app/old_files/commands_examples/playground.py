import requests

# data = {'login': 'test_login1',
#         'password': 'test_password',
#         'first_name': 'Nikola',
#         'last_name': 'Lenivetc'}
#
# response = requests.post('http://127.0.0.1/sign-up', json=data)

# data = {'login': 'test_login1',
#         'password': 'test_password'}
#
# response = requests.post('http://127.0.0.1/sign-in', json=data)

# response = requests.post('http://127.0.0.1/get-user-description', cookies=cookies)

data_login = {'login': 'test_login1',
              'password': 'test_password'}
response1 = requests.get('http://127.0.0.1/sign-in', json=data_login)

data_desc = {'id': 'b76a8f76-60c1-4130-868c-a3cc215a9edf'}
response = requests.get('http://127.0.0.1/get-user-description', cookies=response1.cookies, json=data_desc)

print(response.text)
print(response.cookies)


# print(response.text)
# print(response.cookies)