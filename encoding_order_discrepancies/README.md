# Encoding Order Discrepancies Script
This script finds the discrepancies between the two databases and sends a message to a slack channel.

### Installation
```
python3 -m venv env
```
```
source env/bin/activate
```
```
pip install -r requirements.txt
```
```
cp .env.shadow .env
```

### Running the script
```
python slack-notification.py
```
### Steps to create incoming-webhook
1. Go to apps inside slack
2. Go to app directory
3. search "Incoming WebHooks"
4. Click on "add to slack"
5. Select a channel
6. Click on "add Incoming WebHook Integration"
7. Copy the "WebHookURL" and paste in .env file

### Steps for execution
1. Create a new directory.
2. Insert all the files inside this directory.
3. Update the database credentials, slack webhook url and channel-name in .env file.
4. Install the dependencies.
5. Run the script.
