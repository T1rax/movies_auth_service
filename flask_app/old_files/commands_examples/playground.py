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


# cookies = {'access_token_cookie': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY4MTIzNzI5MiwianRpIjoiNjY2NWQ1NWItMDU1Ni00MDA5LTgyY2QtMTdmOWUyZDg3M2U5IiwidHlwZSI6ImFjY2VzcyIsInVzZXJpZCI6ImI3NmE4Zjc2LTYwYzEtNDEzMC04NjhjLWEzY2MyMTVhOWVkZiIsIm5iZiI6MTY4MTIzNzI5MiwiY3NyZiI6ImI4MDVlZmU0LWYzZmItNDUyYi04OTNkLWQ2ZmM3MWM1MjdjMSIsImV4cCI6MTY4MTI0MDg5Miwicm9sZXMiOlsiYmFzaWNSb2xlIiwicHJlbWl1bVVzZXIiXSwiZmlyc3RfbmFtZSI6Ikl2YW4iLCJsYXN0X25hbWUiOiJJdmFub3YifQ.bHA47HLfN_Wa-D6rn1WIkC8qZc3NflowIIS_qrWJ6lA',
#            'refresh_token_cookie': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY4MTIzNzI5MiwianRpIjoiNWNhZGZjMmItYjU0Ny00NzJmLWI0ZWMtY2FiZmE3OWYwNGU4IiwidHlwZSI6InJlZnJlc2giLCJ1c2VyaWQiOiJiNzZhOGY3Ni02MGMxLTQxMzAtODY4Yy1hM2NjMjE1YTllZGYiLCJuYmYiOjE2ODEyMzcyOTIsImNzcmYiOiJjODUxYmY0OS1jOTg4LTQwMDktYTQ1Zi03NzllMDkyMDllMzciLCJleHAiOjE2ODM4MjkyOTIsInJvbGVzIjpbImJhc2ljUm9sZSIsInByZW1pdW1Vc2VyIl0sImZpcnN0X25hbWUiOiJJdmFuIiwibGFzdF9uYW1lIjoiSXZhbm92In0.jGoPpQ_LqCgujAvIrgKZr1YU-UQaYzCseoeTcIk8SmE',
#            'csrf_access_token': 'b805efe4-f3fb-452b-893d-d6fc71c527c1',
#            'csrf_refresh_token': 'c851bf49-c988-4009-a45f-779e09209e37',
#            }
#
# response = requests.post('http://127.0.0.1/get-user-description', cookies=cookies)

print(response.text)
print(response.cookies)