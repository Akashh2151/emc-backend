# emc-backend

Step 1: Setting Up a Virtual Environment
Before you begin, it's a good practice to create a virtual environment for your project. This will help isolate your project's dependencies from the system-wide Python packages.

1  Open your terminal and navigate to your project directory.
2  Run the following commands to create and activate a virtual environment:

# On Windows
python -m venv venv
venv\Scripts\activate

..

# On macOS and Linux
python -m venv venv
source venv/bin/activate

Step 2: Installing Required Dependencies
Now, you can install the required dependencies using pip. Make sure your virtual environment is activated:

pip install Flask==2.0.3 gunicorn==20.0.4 wfastcgi==3.0.0 pymongo==4.5.0 Werkzeug==2.0.2

Step 3: Creating Your Flask Application
Next, you'll need to create a Flask application for your Auto Pilot project. Here's a basic structure for your Flask app:

# flaskapp.py
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'Auto Pilot Project'

if __name__ == '__main__':
    app.run()


Step 4: Running Your Flask App Locally
You can now run your Flask app locally to make sure everything is set up correctly. In your terminal, execute the following command:

python flaskapp.py

