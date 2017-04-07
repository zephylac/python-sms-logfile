import os
import re
import sms
import sqlite3


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
            print filename
            # DATE FOR SMS
            date = re.findall(r'L(.*).log', filename)
            #add logfile to treated list
            cursor.execute('''INSERT INTO logfiles(name) VALUES (?)''',(filename,))
            with open(filename) as origin_file:
                for line in origin_file:
                    #searching for kick
                    if(re.findall(r'kicked|banned|slapped', line)) :
                        test = re.sub('"','',line)
                        test = test.partition(']')[2]
                        test = re.sub('<.*?>|reason','',test)
                        array.append(test)
                        print test
                print "\n\n"
#sms.send(test)
conn.commit()
conn.close();
