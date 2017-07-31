#!/usr/bin/bash

deactivate() {
    unset MY_PSQL_DBNAME
    unset MY_PSQL_USER
    unset MY_PSQL_HOST
    unset MY_PSQL_PASSWORD
    unset TRAKT_API_KEY
    # uncomment the next line if you want to run your flask server in debug mode
    unset FLASK_DEBUG
    unset -f deactivate
}

# insert your database name, username (role), host ip and password
# you can find the API key in the Canvas assignment description
MY_PSQL_DBNAME="series"
MY_PSQL_USER="gina"
MY_PSQL_HOST="localhost"
MY_PSQL_PASSWORD="thebest"
TRAKT_API_KEY="8ff15ce86611f31cd1253c5e6d2c2232bf5e7db500476b31c81f1dded88c7a37"

export MY_PSQL_DBNAME
export MY_PSQL_USER
export MY_PSQL_HOST
export MY_PSQL_PASSWORD
export TRAKT_API_KEY

# uncomment the next two lines if you want to run your flask server in debug mode
FLASK_DEBUG="1"
export FLASK_DEBUG