# GameDB



## Getting started

To make it easy for you to get started with GitLab, here's a list of recommended next steps.

Already a pro? Just edit this README.md and make it your own. Want to make it easy? [Use the template at the bottom](#editing-this-readme)!

## Add your files

- [ ] [Create](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#create-a-file) or [upload](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#upload-a-file) files
- [ ] [Add files using the command line](https://docs.gitlab.com/ee/gitlab-basics/add-file.html#add-a-file-using-the-command-line) or push an existing Git repository with the following command:

```
cd existing_repo
git remote add origin https://git.nanofo.com/danyileremenko/gamedb.git
git branch -M main
git push -uf origin main
```

# Setup the project

To run project you should have at least python 3.10.

1) Create venv
python -m venv/venv

Activate venv:
    a)Linux/mac:
        source venv/bin/activate
    b) Windows
        venv\Scripts\activate

Exit:
deactivate


2) Next we need to install all libraries:   
`pip install -r requirements.txt`


So far so good. Now we wont to create our .env file.

Here is the latest .env_example.
You can just copy and paste your values.

# .env_example_file
MAIL_SENDER="380673172158vv@gmail.com"
MAIL_PASSWORD="mvppfuncuhdzwyzu"

DB_NAME="db_name"
DB_HOST="127.0.0.1"
DB_USER="db_user"
DB_PASSWORD="password"

SECRET_KEY="hello_secret"

ROOT_USERNAME='root_username'
ROOT_PASSWORD='password'
BASE_URL='http://127.0.0.1:8000'


# Congratulations!

Now you can run server:
from  root dir write:  
``uvicorn server:app``