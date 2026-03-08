# run.py

import os

from app import create_app
os.environ['FLASK_CONFIG'] = 'development'
os.environ['FLASK_APP'] = 'run.py'

config_name = os.getenv('FLASK_CONFIG')
app = create_app(config_name)

if __name__ == '__main__':
    app.run()