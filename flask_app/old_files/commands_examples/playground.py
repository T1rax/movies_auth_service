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
#
# response = requests.post('http://127.0.0.1/auth/sign-up', json=data)


data_login = {'login': 'test_login1',
              'password': 'test_password'}
response1 = requests.get('http://127.0.0.1/auth/sign-in', json=data_login)

# print(response1.cookies)

# data_desc = {'id': 'b14723fd-8751-45ce-ae63-22aee5a09efc'}
# response = requests.get('http://127.0.0.1/auth/get-user-description', cookies=response1.cookies, json=data_desc)

data_change = {'id': 'b14723fd-8751-45ce-ae63-22aee5a09efc',
               'role': 'premiumUser',
               'action_type': 'delete'} # delete/add
response = requests.get('http://127.0.0.1/auth/change-role', cookies=response1.cookies, json=data_change)


print(response.text)
# print('-----------------------------')
# print(response.cookies)