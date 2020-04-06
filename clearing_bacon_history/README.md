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
python clear-bacon-history.py id1,id2,id3,id4,....,idn
```

### Steps for execution
1. Place all files in a directory
2. Rename the .env.shadow to .env
3. Update the art_relations database credentials and ticket no in .env file
4. Copy all the youtube_video_id and format it in a single line where id's are separated by comma
5. Copy the formated string and paste it while running the script
6. Run the script python clear-bacon-history.py id1,id2,id3,id4,id5,....,idn
