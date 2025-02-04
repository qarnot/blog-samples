#!/usr/bin/env python3

# Import the Qarnot SDK
import qarnot
import os

# Create a connection, from which all other objects will be derived
# Enter client token here

conn = qarnot.connection.Connection(client_token="MY_SECRET_TOKEN")

# -------------------------------------------------------------------------- #
NB_NODES = 2
OPENFOAM_VERSION = "v2412"
# -------------------------------------------------------------------------- #

# Create a task
task = conn.create_task("OpenFOAM Tests","openfoam",NB_NODES)

# Create the input bucket and synchronize with a local folder
# Insert a local folder directory
input_bucket = conn.retrieve_or_create_bucket("openfoam-article-in")
input_bucket.sync_directory("motorbike")

# Attach the bucket to the task
task.resources.append(input_bucket)

# Create a result bucket and attach it to the task
task.results = conn.create_bucket("openfoam-article-out")

# Openfoam contants
task.constants['RUN_SCRIPT'] = "Allrun" # Path of your run script inside the input bucket
task.constants['DOCKER_TAG'] = OPENFOAM_VERSION

# Optional, do not set if script is at the root of your input bucket
# task.constants['OPENFOAM_INPUT_DIRECTORY_NAME'] = 'motorbike'

# Optional, define interval time in seconds when your simulation will be saved to your bucket.
# task.snapshot(600)

# Submit the task
task.submit()
