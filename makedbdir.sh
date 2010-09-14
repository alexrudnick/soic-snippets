#!/bin/bash

# Create the database directory and set its permissions so that it'll work on
# Ubuntu with Apache.

mkdir -p db
./db.py
sudo chgrp -R www-data db
sudo chmod -R ug+rwx db
