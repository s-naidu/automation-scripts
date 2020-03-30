# Encoding Order Discrepancies Script
This script finds the discrepancies between art_relations.encoding_order_detail and direct_delivery.encoding_queue_detail  and sends an alert message to a slack channel so respective person can take action on it.

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
1. Go to "Apps" inside the slack-app
2. Click on "App Directory"
3. Search "Incoming WebHooks"
4. Click on "Add to Slack"
5. Select a channel
6. Click on "add Integration"
7. Copy the "WebHookURL" and paste in .env file

### Steps for execution
1. Place all files in a directory
2. Rename the .env.shadow to .env 
3. Update the Snowflake credentials, Slack configs, Slack bot-name in .env file
4. Run the script python slack-notification.py
