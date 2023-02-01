import os
import datetime
from mega import Mega

print(""" ______            ___  ____              __       _        __       
|_   _ \          |_  ||_  _|            [  |     (_)      [  |      
  | |_) | _   __    | |_/ /   ,--.  .--.  | |--.  __  .--.  | |--.   
  |  __'.[ \ [  ]   |  __'.  `'_\ :( (`\] | .-. |[  |( (`\] | .-. |  
 _| |__) |\ '/ /   _| |  \ \_// | |,`'.'. | | | | | | `'.'. | | | |  
|_______[\_:  /   |____||____\'-;__[\__) )___]|__|___|\__) )___]|__] 
         \__.'                                                       """)

backup_destination="/location/to/store/backup"

backup_files = [i for i in os.listdir(backup_destination) if i.endswith(".tar.gz.gpg")]
backup_files.sort(key=lambda x: os.path.getctime(os.path.join(backup_destination, x)))

days_to = 7
for backup_file in backup_files[:-days_to]:
    os.remove(os.path.join(backup_destination, backup_file))

print("backup report:")
extension = ".tar.gz.gpg"
print("Upload? or show report")
choice = input("1 = upload, 2 = show report: ")
if choice == "1":
    mega = Mega()
    m = mega.login("email", "password")
    path = "/backup/location"
    for i in os.listdir(path):
        if i.endswith(".gpg"):
            folder = m.find("Folder_name")[0]
        try:
            m.upload(i, folder)
        except Exception as e:
            print(f"Error uploading file: {e}")

elif choice == "2":   
    if any(file.endswith(extension) for file in os.listdir(backup_destination)):
        for backup_file in backup_files:
            print("- {} ({})".format(backup_file, datetime.datetime.fromtimestamp(os.path.getctime(os.path.join(backup_destination, backup_file))).strftime("%Y-%m-%d %H:%M:%S")))
    else:
        print("Backup doesn't exist")
else:
    print("Invalid choice")
