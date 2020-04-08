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
run the script by running following command providing the list of youtube_video_id as given below:
```
python clear-bacon-history.py BQPxgsLX2PM Gx_8z-IufPg
```

### Steps for execution
1. Place all files in a directory
2. Rename the .env.shadow to .env
3. Update the art_relations database credentials and ticket no in .env file
6. Run the script python clear-bacon-history.py id1 id2
