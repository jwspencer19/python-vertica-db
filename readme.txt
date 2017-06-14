This folder contains a set of Python scripts to read, write, and delete data
from a Vertica database.

These scripts are useful when wanting to copy a subset of data from an existing
Vertica database and writing to another Vertica database. This includes reading
from one schema and writing to a different schema.

Each Python script: readdb.py, writedb.py, and deletedb.py contains its own
Yaml input file that specifies the Vertica database, schema, and tables. Edit
these Yaml input files to specify your requirements:
-read.yaml
-write.yaml
-delete.yaml

To read from a Vertica database, and store the data for each table, execute:
$ python readdb.py

To write data to a set of Vertica database tables, execute:
$ python writedb.py

To delete data from a set of Vertica database tables, execute:
$ python deletedb.py


To build a Docker image that contains Python and the two libraries needed to
run these Python scripts:
$ docker build -t my_python_vertica .

To save the Docker image to a tar file that can be loaded on a separate system:
$ docker save -o my_python_vertica.tar my_python_vertica

To load the Docker image on a separate system to then later start the container
$ docker load --input my_python_vertica.tar


To start the container based on the Docker image and mount an external folder
to store the data created and/or read by the scripts, which will ensure the
data is persisted after the Docker container is closed:
$ docker run -v /opt/output:/output -it my_python_vertica bash

From the bash shell created within the Docker container
-edit the yaml input files for your particular requirements
-run the Python scripts listed above for read, write, delete.

