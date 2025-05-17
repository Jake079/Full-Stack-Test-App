# Light-weight note-taking app using Flask

Create, read, update, and delete notes. 
User registration & authentication + Password hashing.

- Backend: **Flask**
- Database: **SQLAlchemy**
- Template rendering: **Jinja2** 
- Auth & security: **Werkzeug**

![web demo](Website/Static/img/demo.png)


To run the app, first set up your secret key as environment variable: 
> export SECRET_KEY='your_secret_key_here' #Bash/Zsh

> set SECRET_KEY='your_secret_key_here' #Command Prompt

> $env:SECRET_KEY = 'your_secret_key_here' #PowerShell

Once the key is set, simply run: 
> python main.py