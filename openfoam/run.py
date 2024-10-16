#!/usr/bin/env python3

# Import the Qarnot SDK
import qarnot
import os

# Create a connection, from which all other objects will be derived
# Enter client token here

conn = qarnot.connection.Connection(client_token="MY_SECRET_TOKEN")

# -------------------------------------------------------------------------- #
NB_NODES = 2
# -------------------------------------------------------------------------- #

# Create a task
task = conn.create_task("OpenFOAM Tests",
                        "openfoam", NB_NODES)


# Create the input bucket and synchronize with a local folder
# Insert a local folder directory
input_bucket = conn.retrieve_or_create_bucket("openfoam-in")
input_bucket.sync_directory("input")

# Attach the bucket to the task
task.resources.append(input_bucket)

# Create a result bucket and attach it to the task
task.results = conn.create_bucket("openfoam-out")

task.constants['OPENFOAM_INPUT_DIRECTORY_NAME'] = 'MOTORBIKE-v2106'
task.constants['RUN_SCRIPT'] = "MOTORBIKE-v2106/Allrun"
task.constants['DOCKER_TAG'] = "v2106"

# Define checkpoint
task.snapshot(60)

# Submit the task
task.submit()
