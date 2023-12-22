# Maintain iTunes Music Collection

Scripts for playing around with my music collection

## Using the services standalone

Services shall be able to execute standalone

### PostgreSQL

Pull PostgreSQL official image and start container, initially creating a database **music**.

    docker pull postgres:alpine

Details at: https://hub.docker.com/_/postgres

### cronpg

Script **cronpg.py**, parsing **iTunes Music Library.xml** and tracking the content in database. 

Git clone/fork this repository, and create a **.env** file with following environment variables.

    ITUNES_MUSIC_DIR=your iTunes music directory
    ITUNES_LIBRARY_FILE=iTunes Music Library.xml
    POSTGRES_PASSWORD=your password
    POSTGRES_DB=music
    POSTGRES_HOST=your host ip address

When using the scripts from within a virtual machine iTunes music directory has to be mounted first.

Change directory to **cronpg** and setup python3 virtual environment.

    python3 -m venv .venv
    source .venv/bin/activate

Change dirctory to **app** and run script.

    python3 cronpg.py

### backend

Change directory to **backend** and setup python3 virtual environment.

    python3 -m venv .venv
    source .venv/bin/activate

Start **uvicorn** server.

    uvicorn app.main:app --reload --workers 1 --host 0.0.0.0 --port 8000
    