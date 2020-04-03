# script to clear BACON history 
This script will clear the BACON history in art_relations.youtube_channel_video_status table for provided youtube video IDs

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
python clear-bacon-history.py
```

### Steps for execution
1. Place all files in a directory
2. Rename the .env.shadow to .env 
3. Update the art_relations database credentials in .env file
4. Update youtube_video_id's in the sql_create query
5. Change the tablename in the CREATE TABLE section according to the ticket no in the sql_create query 
5. Run the script python clear-bacon-history.py
