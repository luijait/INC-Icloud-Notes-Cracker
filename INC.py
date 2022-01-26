import sqlite3
import sys, os, platform
hashes = ''
def developer(): #My portfolio
    print("https://luijait.es")

def menu(): #Menu, Banner from: http://www.patorjk.com/software/taag/#p=display&f=Varsity&t=INC
    print ('''
_____  ____  _____   ______  
|_   _||_   \|_   _|.' ___  | 
  | |    |   \ | | / .'   \_| 
  | |    | |\ \| | | |        
 _| |_  _| |_\   |_\ `.___.'\ 
|_____||_____|\____|`.____ .' 
                              
                          

    [+] 1. Autoextract database
    [+] 2. Set database path manually 
    [+] 3. Only Crack Hash
    [+] 4. Developer Portfolio
    [+] 5. Exit


    
    WARNING: Option 1 only works on Mac OS, full access disk terminal app required
    ''') 

def check_os():
    if platform.system() == 'Darwin':
        db = autoextractdb()
    else:
        print ('You arent in a Mac')
    return db
#To properly work this func use mac
def autoextractdb():
    db = '~/Library/Group Containers/group.com.apple.notes/NoteStore.sqlite'
    return db
#Print extract hashes from db
def show_pass(hashes):
    cmd = ('cat {}'.format(hashes))
    os.system(cmd)
#Save output hash from sql query to the file
def save(format, *args):
    sys.stdout = open('hashes.txt','w')
    sys.stdout.write(format % args)
    sys.stdout.close
    sys.stdout = sys.__stdout__ #You need this to can print again
def extract_hash(db):
    #Remove hashes file to overwrite that
    os.system('rm -rf hashes.txt')
    
    start_con = sqlite3.connect(db)
    #To execute query in sqlite database
    querier = start_con.cursor()
    try:
        #Execute query to get the hashes
        bytes_hashes = querier.execute('SELECT Z_PK,ZCRYPTOITERATIONCOUNT,ZCRYPTOSALT,ZCRYPTOWRAPPEDKEY FROM ZICCLOUDSYNCINGOBJECT WHERE ZISPASSWORDPROTECTED=1')
        for bytes_hash in bytes_hashes:
            #Save all db hashes into hashes.txt
            save('$ASN$*%d*%d*%s*%s\n',bytes_hash[0],bytes_hash[1],bytes_hash[2].hex(),bytes_hash[3].hex())
    except sqlite3.DatabaseError:
        pass
    #Ignore Database Errors like corrupted file

def passwordcracker(dicc,hashes):
    if hashes and dicc: #Option 3
        cracker = ('hashcat -m 16200 -a 0 {} {}').format(hashes,dicc)
    else: # Option 1,2
        cracker = ('hashcat -m 16200 -a 0 hashes.txt {}'.format(dicc))
    os.system(cracker)

if __name__ == "__main__":
    while True:
        try:
        
            menu()
            ans = int(input('[+]Choose an Option:> '))
            if ans == 1:
                db = check_os()
            elif ans == 2:
                db = input('[+]Database:> ')
            elif ans == 3:
                hashes = input('[+]Hashes to crack:> ')
                dicc = input('[+]Password Dictionary:> ')
                passwordcracker(dicc,hashes)
                break    
            elif ans == 4:
                developer()
            elif ans == 5:
                print ("Finishing.... Thanks and remember star repository")
                sys.exit()
            else:
                print ("Pls select a valid option")
            try:
                extract_hash(db)
            except sqlite3.OperationalError:
                print ("[!] Database Not found")
                break
            if os.stat('hashes.txt').st_size == 0:
                print("[!]Unable to extract any hash")
            else:
                show_pass('hashes.txt')
                print('[+]Want to crack password? (Y/N): ')
                next_step = input()
                if (next_step == 'Y') or (next_step == 'y'):
                    print("[+]Password diccionary:> ")
                    dicc = input()
                    passwordcracker(dicc,hashes)
                else:
                    print ('[+] Finishing...')
                    sys.exit()
        except:
            sys.exit() 