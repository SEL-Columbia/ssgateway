#!/bin/bash
# A script to sync your local gateway database with the remove db
# Ivan Willig 13 June 2011
TIME=$(date +%y%m%d)
DB_NAME="gateway"
echo "Syncing your local database with the remove databae on gateways.sharedsolar.org"
echo "IMPORTANT; this will destory your exisiting databaes"

echo "Making temp folder"
mkdir temp

echo "Downloading zip file"
pushd temp
scp root@gateway.sharedsolar.org:/var/lib/postgresql/backups/gateway.$TIME.sql.zip .
unzip gateway.$TIME.sql.zip 

echo "Droping old database"
dropdb $DB_NAME

echo "Creating new database"
createdb $DB_NAME

echo "Loading new data into databae"
psql -d $DB_NAME -f var/lib/postgresql/backups/gateway.$TIME.sql

echo "Removing tmp folder"
pushd ..
rm -rf temp


