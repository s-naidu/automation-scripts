# Encoding Order Discrepancies Script
This script finds the discrepancies between the two databases and sends a message to a slack channel.

#Installation
```
py -3 -m venv env
env\Scripts\activate
pip install snowflake-connector-python == 2.2.2
pip install pandas == 1.0.1
pip install requests == 2.23.0
```

#Running the script
```
py slack-notification.py
```

#Steps for execution
1. Create a new directory.
2. Insert the script and key inside that directory.
3. Update the database credentials, passphrase for the key, slack webhook url and channel-name in the script.
4. Install the dependencies.
5. Run the script.
