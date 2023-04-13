import requests

# Андрей

# data = {'login': 'test_login1',
#         'password': 'test_password',
#         'first_name': 'Nikola',
#         'last_name': 'Lenivetc'}
#
# response = requests.post('http://127.0.0.1/auth/sign-up', json=data)
#
# data_login = {'login': 'test_login1',
#               'password': 'test_password'}
# response1 = requests.get('http://127.0.0.1/auth/sign-in', json=data_login)
# #
# data_desc = {'id': 'c9d58c5e-47d8-40f1-8c10-2cac341d345b'}
# response = requests.get('http://127.0.0.1/auth/get-user-description', cookies=response1.cookies, json=data_desc)
#
# data_change = {'id': 'c9d58c5e-47d8-40f1-8c10-2cac341d345b',
#                'role': 'superUser'}
# response = requests.get('http://127.0.0.1/auth/change-role', cookies=response1.cookies, json=data_change)


# print(response.text)
# print('-----------------------------')
# print(response.cookies)




# Вова

# data = {'login': 'test_login1',
#         'password': 'test_password',
#         'first_name': 'Nikola',
#         'last_name': 'Lenivetc'}

# response = requests.post('http://127.0.0.1/auth/sign-up', json=data)


data_login = {'login': 'test_login1',
              'password': 'test_password'}
response1 = requests.get('http://127.0.0.1/auth/sign-in', json=data_login)

# print(response1.cookies)

data_desc = {'id': '061b2a67-8a44-40f0-beb2-a668781281ba'}
response = requests.get('http://127.0.0.1/auth/get-user-description', cookies=response1.cookies, json=data_desc)

# data_change = {'id': 'd5660506-56ec-4583-92eb-15ecfec321b4',
#                'role': 'admin'}
# response = requests.get('http://127.0.0.1/auth/change-role', cookies=response1.cookies, json=data_change)


print(response.text)
# print('-----------------------------')
# print(response.cookies)