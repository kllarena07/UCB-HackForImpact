# How to Run This App

All the commands given should be run in the terminal. Commands will also be UNIX -- so they won't work on Windows

Additionally, this assumes that you have Python and Node.js installed on your system

## Clone the Repo

```
git clone https://github.com/kllarena07/UCB-HackForImpact.git
```

## Install Python Requirements

From the root directory:

```
1. cd backend
2. python3 -m venv venv
3. source venv/bin/activate
4. pip install -r requirements.txt
5. deactivate
```

## Install NPM Requirements

From the root directory:

```
1. cd frontend
2. npm run install
```

## Running the App

### Running the Flask server

In order for the Flask server to run, you will need 2 things:

1. An OpenAI API Key
2. An AssemblyAI API Key

When you have these, export them as an environment variable using:

```
1. cd backend
2. export OAI_API_KEY="YOUR-OPENAI-API-KEY-HERE"
3. export AAI_API_KEY="YOUR-ASSEMBLYAI-API-KEY-HERE"
```

Once this is done, proceed by running these commands in the backend directory:

```
1. source venv/bin/activate
2. python server.py
```

The Flask server should now be running

### Running the Express.js server

In a seperate terminal and in the root directory:

```
1. cd frontend
2. node server.js
```

## Finishing Steps

Once the above steps are complete, connect to localhost:3000 in your web browser and use the app
