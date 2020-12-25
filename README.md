# Farbophon_Server

# Installation

Follow the instruction to set up a local server

Clone the repository:
```
git clone https://github.com/chronoB/Farbophon_Server/
```

Create the folder/files needed for the server to work.
This can also be made by hand in the explore or finder.

These are the terminal commands:
```bash
# go into the cloned directory
cd Farbophon_Server

# create folder and the file for the database
mkdir db
touch db/farbophon.db

# create folder and file for the configuration of the server
mkdir instance
touch instance/config.py
```

Now we have to edit the configuration of the server. Just copy this into your configuration file.
> ⚠️ For Windows use `db\\farbophon`
```python
# file: instance/config.py

import os

# Get the Path to the project root to use it for the database uri later on
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = PROJECT_ROOT[:PROJECT_ROOT.find('instance')]


# the key that is used to store the flask session
SECRET_KEY = "SecretKey"
# the URI to the database. if you used a different path for the creation of the database you have to change it here.
SQLALCHEMY_DATABASE_URI = "sqlite:///" + \
    os.path.join(PROJECT_ROOT, 'db/farbophon.db')
```

For your local server the SECRET_KEY variable can be some random string. In production you want to use a real secret key. You can generate one with the following command.

---
> ⚠️
All python commands could be python3 on your system.
---


```bash
python -c "import os; print(os.urandom(24).hex())"

# output:
~
❯ python -c "import os; print(os.urandom(24).hex())"
c406411ca6ed46c4d41da3817473fa2863e4ba18b0b180a3
```

Afterwards you want to install the necessary dependencies with pip.
I would recommend to do that in a virtual environment that keeps this projects dependencies seperate from other python projects.
I use venv to do that:
```bash
# this will initiate a virtual environment in the venv folder
python -m venv venv


# Now we activate the virtual environment for this terminal session
#Windows:
venv/Scripts/activate

# Unix/Mac:
source venv/bin/activate
```

Now we can install the dependencies

```bash
pip install -r requirements.txt
```

Afterwards you can start the server. Make sure you activated your venv if you use one.
```bash
python app.py
```

## Development

---

If you want to change something in the implemenation I would recommend you using pre-commit.

```bash
pip install pre-commit

pre-commit install
```

This way everytime you commit a file pre-commit will format and lint your code.

You can manually trigger pre-commit with the following command:
```bash
pre-commit run --all-files
```
