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
# response1 = requests.post('http://127.0.0.1/auth/sign-in', json=data_login)
# #
# data_desc = {'id': '10dd44fb-ff6d-4b20-80be-b72ecebc3603'}
# response = requests.get('http://127.0.0.1/auth/get-user-description', cookies=response1.cookies, json=data_desc)
#
# data_change = {'id': 'c9d58c5e-47d8-40f1-8c10-2cac341d345b',
#                'role': 'superUser'}
# response = requests.get('http://127.0.0.1/auth/change-role', cookies=response1.cookies, json=data_change)

# data_history = {'id': '10dd44fb-ff6d-4b20-80be-b72ecebc3603',
#                 'page': 1,
#                 'per_page': 10}
# response = requests.get('http://127.0.0.1/auth/sign-in-history', cookies=response1.cookies, json=data_history)

# print(response.text)
# print('-----------------------------')
# print(response.cookies)




# Вова

data = {'login': 'test_login3',
        'password': 'test_password',
        'first_name': 'Nikola',
        'last_name': 'Lenivetc'}

# response = requests.post('http://127.0.0.1/auth/sign-up', json=data)


data_login = {'login': 'test_login3',
              'password': 'test_password'}
response = requests.post('http://127.0.0.1/auth/sign-in', json=data_login)

# data_desc = {'id': '10dd44fb-ff6d-4b20-80be-b72ecebc3603'}
# response = requests.get('http://127.0.0.1/auth/get-user-description', cookies=response1.cookies, json=data_desc)

# data_change = {'id': '070eace9-ec49-44ff-8423-96e7faacaccd',
#                'role': 'premiumUser',
#                'action_type': 'add'} # delete/add
# response = requests.get('http://127.0.0.1/auth/change-role', cookies=response1.cookies, json=data_change)

# data_history = {'id': '070eace9-ec49-44ff-8423-96e7faacaccd'}
# response = requests.get('http://127.0.0.1/auth/sign-in-history', cookies=response1.cookies, json=data_history)

# data_login = {'login': 'admin',
#               'password': '123qwe'}
# response1 = requests.get('http://127.0.0.1/auth/sign-in', json=data_login)
#
#
print(response.text)
print('-----------------------------')
print(response.cookies)