#!/bin/bash 

wget https://dl.google.com/cloudsql/cloud_sql_proxy.linux.386
mv cloud_sql_proxy.linux.386 cloud_sql_proxy
chmod +x cloud_sql_proxy
./cloud_sql_proxy -instances=cedar-amulet-234921:us-central1:postgres-civic-tech -credential_file=$CREDENTIALS