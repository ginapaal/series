# Codecool Series DB
A system to help you store your favourite TV shows. 

## The story
This is a basic practice session to go through the basics of WEB technologies with python backend, postgres and some code on front-end.

A dumb wireframe is provided in the `design.html` file with will help you mix'n'match elements without lot of styling work.

## Setup

1. Clone this repo
2. Open a terminal in the root folder of the cloned repository. After that run this command:
    ```
    sudo pip3 install -r requirements.txt
    ```
3. Fill out the `setenv.sh.template` with your details and rename it to `setenv.sh`
4. Source the `setenv.sh` file in the command line with **one** of the following commands:
    - *`source setenv.sh`*
    - *`. setenv.sh`*
5. Run the `data_inserter.py` file:
    ```
    python3 data_inserter.py
    ``` 
6. Run the server with: *`python3 main.py`*
7. After you stop the server run: *`deactivate`* in the command line to clean up the variables used

## Database

![Relational model](data/db_schema/relational_model.png?raw=true "Relational model")
