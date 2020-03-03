# automation-scripts
This script is used to verify the performer_name data in a csv file with the performer_name data in the database.
# Steps for execution
1. create a new directory.
2. insert the script and the csv file which will be used for comparision.(please note:- if you have excel file first convert it to csv then insert)
3. open script and insert correct database credentials.
4. open command prompt from this directory.
5. type ```py scriptname.py``` to execute the script.
6. enter the no of performers. (please note:- if your file contains single performer and single header enter 1. if your file contains more than 1 header even if you have only 1 performer enter any number which is greater than 1 but less than or equal to 9) 
7. two new excel sheets will be created after the execution in the same directory one will contain the track id's which did not match with database data and other one will contain the track id's which contain no data in the database. 
