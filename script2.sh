#!/bin/bash

source_files="/files/to/backup"
backup_destination="/location/to/store/backup"
file_name="backup-$(date +%Y-%m-%d).tar.gz"
backup_path="$backup_destination/$file_name"

read -p "Choose Encrypt or Decrypt: " choice

for option in $choice; do
    if [ "$option" = "Encrypt" ];
    then
    if [ -e "${backup_destination}"/"${file_name}" ];
    then
        echo "Backup already exist"
        exit 0
    else
        echo "Backup doesn't already exist"
        tar -czf "$backup_path" --absolute-names $source_files
        gpg --symmetric --cipher-algo AES256 "$backup_path"
        rm "$backup_path"
        echo "Encrypted backup has been created"
        exit 0
    fi
elif [ "$option" = "Decrypt" ];
then
    gpg --decrypt "$backup_path.gpg" | tar -xzf - -C /location/to/store/backup
    tar -xzf "$backup_path" 2> /dev/null
    rm "$backup_path.gpg"
    echo "Files have been decryped"
    exit 0

else
    echo "Invalid Operation"
    exit 0
fi
done 
