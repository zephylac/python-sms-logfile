import os
import re
import sms
import sqlite3
import time

class data:
    """Class defining data :
    - date of the logfile
    - ban list
    - kick list
    - slap list
    """


    def __init__(self,date,ban,kick,slap):
        self.date = date
        self.ban  = ban
        self.kick = kick
        self.slap = slap

        
conn = sqlite3.connect('log.db')
conn.text_factory = str
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS logfiles(name text)''')

array = []
for filename in os.listdir('.'):
    root, ext = os.path.splitext(filename)
    if root.startswith('L') and ext == '.log' :
        cursor.execute('SELECT * FROM logfiles WHERE name=?', (filename,))
        #test if logfile has been treated
        value = cursor.fetchone()
        if not value or value[0] != filename :
            # DATE FOR SMS
            date = re.findall(r'L(.*).log', filename)
            if date[0] != (time.strftime("%Y%m%d")) :
                #add logfile to treated list
                cursor.execute('''INSERT INTO logfiles(name) VALUES (?)''',(filename,))
                ban = []
                kick = []
                slap = []
                with open(filename) as origin_file:
                    for line in origin_file:
                        #searching for kick
                        if(re.findall(r'kicked|banned|slapped', line)) :
                            test = re.sub('"','',line)
                            test = test.partition(']')[2]
                            test = re.sub('<.*?>|reason','',test)
                            if(re.findall(r'banned', test)) :
                                ban.append(test)
                            if(re.findall(r'kicked', test)) :
                                kick.append(test)
                            if(re.findall(r'slapped', test)) :
                                slap.append(test)

                array.append(data(date,ban,kick,slap))

#sms.send(test)
conn.commit()
conn.close();   
