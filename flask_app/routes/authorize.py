

def authorize_user(jwt_token):

    response = {'msg': 'User authorized',
                'first_name': jwt_token.get('first_name'),
                'last_name': jwt_token.get('last_name'),
                'roles': jwt_token.get('roles'),}
    
    return response



# {'fresh': False, 
#  'iat': 1681068544, 
#  'jti': 'ad116f93-4f70-4c96-ab59-f19589585339', 
#  'type': 'access', 
#  'userid': 'example_user', 
#  'nbf': 1681068544, 
#  'csrf': '420eda8c-8eda-4ae5-9b92-446840555d3b', 
#  'exp': 1681072144, 
#  'roles': ['basicRole', 'premiumUser'], 
#  'first_name': 'Ivan', 
#  'last_name': 'Ivanov'}