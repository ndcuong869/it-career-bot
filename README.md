# IT Career Bot - A Personalized Career Counseling Chatbot
IT Career Bot is a project for desmontrating how to build a personalized chatbot based on context-aware knowledge base.

# Installation
## Environment requirement
1. Virtual environment
  * We use Anaconda (https://www.anaconda.com/) to create an isolated virtual environment for interpreting and executing Python scripts. It also provides many modules and libraries to enable a flexible approach when programming chatbot functions.

2. Flask (https://flask.palletsprojects.com)
  * A Python web framework allows create production in a short time without considering the low level of web programming. 

## How to run the chatbot application?
* Step 1. Execute Rasa component by using the below command:
```
rasa run --enable-api --cors "*" --port 5005 --debug --credentials credentials.yml
```
* Step 2. Running Rasa action server to serve single actions for each request from dialog management
```
rasa run actions
```

* Step 3: Running the Flask server to handle user requests
```
flask run
```
