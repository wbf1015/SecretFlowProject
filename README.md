# SecretFlowProject

Our project is in project

## What is the purpose of each file?

sql.sql : you need to run it on mysql with a serectflow db to init the enviroment

db.py : you need to change the config with your own environmrnt and use the getUser() to get the init message of username and password

corn.py : Init the secretflow`s config with some specific protocol

demo.py : When you want to change the properties of the environment (in this project, it probably means changing the key-value in a dictionary), you need to call its function

web.py : A very simple front-end that will call functions from the demo as external time response

