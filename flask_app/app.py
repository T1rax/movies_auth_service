import sys
sys.path.insert(0, '/home/tirax/movies_auth_service')

from flask import Flask
from database.db import init_db

app = Flask(__name__)


# Test pages
@app.route('/')
async def main_page():
    return 'Hello, World!'    

# Account authorization routes
from routes.authorize import authorize_user

@app.route('/authorize')
async def authorize():
    return authorize_user()

@app.route('/logout')
async def logout():
    return 'Hello, World! logout'

@app.route('/sign-in')
async def sign_in():
    return 'Hello, World! sign-in'

@app.route('/sign-up')
async def sign_up():
    return 'Hello, World! sign-up'

# Token-related routes
# from routes. import
@app.route('/refresh')
async def refresh():
    return 'Hello, World! refresh'

# Roles routes
# from routes. import
@app.route('/change-role')
async def change_role():
    return 'Hello, World! change-role'

# Support routes
# from routes. import
@app.route('/get-user-description')
async def get_user_description():
    return 'Hello, World! get-user-description'

@app.route('/sign-in-history')
async def sign_in_history():
    return 'Hello, World! sign-in-history'


def main():
    init_db(app)
    app.run()


if __name__ == '__main__':
    main() 