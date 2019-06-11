#!/bin/bash
wget https://dl.google.com/cloudsql/cloud_sql_proxy.linux.386
mv cloud_sql_proxy.linux.386 cloud_sql_proxy
chmod +x cloud_sql_proxy
./cloud_sql_proxy -instances=postgres-civic-tech=tcp:5432 -credential_file=$GSP