import requests

# Андрей

# data = {'login': 'test_login1',
#         'password': 'test_password',
#         'first_name': 'Nikola',
#         'last_name': 'Lenivetc'}
#
# response = requests.post('http://127.0.0.1/sign-up', json=data)
#
# data_login = {'login': 'test_login1',
#               'password': 'test_password'}
# response1 = requests.get('http://127.0.0.1/sign-in', json=data_login)
# #
# data_desc = {'id': 'c9d58c5e-47d8-40f1-8c10-2cac341d345b'}
# response = requests.get('http://127.0.0.1/get-user-description', cookies=response1.cookies, json=data_desc)
#
# data_change = {'id': 'c9d58c5e-47d8-40f1-8c10-2cac341d345b',
#                'role': 'superUser'}
# response = requests.get('http://127.0.0.1/change-role', cookies=response1.cookies, json=data_change)


# print(response.text)
# print('-----------------------------')
# print(response.cookies)




# Вова

data_login = {'login': 'test_login12',
              'password': 'test_password'}
response1 = requests.get('http://127.0.0.1/sign-in', json=data_login)

# print(response1.cookies)

# data_desc = {'id': 'd5660506-56ec-4583-92eb-15ecfec321b4'}
# response = requests.get('http://127.0.0.1/get-user-description', cookies=response1.cookies, json=data_desc)

data_change = {'id': 'd5660506-56ec-4583-92eb-15ecfec321b4',
               'role': 'premiumUser'}
response = requests.get('http://127.0.0.1/change-role', cookies=response1.cookies, json=data_change)


print(response.text)
# print('-----------------------------')
# print(response.cookies)