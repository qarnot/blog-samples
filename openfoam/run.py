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
task.snapshot(900)

# Optionnal, blacklist processor directories with regex
task.snapshot_blacklist = r"processor\d+" # Set snapshots blacklist
task.results_blacklist = r"processor\d+" # Set results blacklist

# Optionnal, whitelist only log. files with regex
# task.snapshot_whitelist = r"log\..*" # Set snapshots whitelist
# task.results_whitelist = r"log\..*" # Set results whitelist

# OnDemand setup
# task.scheduling_type=OnDemandScheduling()

# Submit the task
task.submit()

# # ---------- Optional ----------
OUTPUT_DIR="motorbike-out"
# The following will download result to the OUTPUT_DIR 
# It will also print the state of the task to your console
LAST_STATE = ''
SSH_TUNNELING_DONE = False
while not SSH_TUNNELING_DONE:
    if task.state != LAST_STATE:
        LAST_STATE = task.state
        print(f"** {LAST_STATE}")

    # Wait for the task to be FullyExecuting
    if task.state == 'Success':
        print(f"** {LAST_STATE}")
        task.download_results(OUTPUT_DIR, True)
        SSH_TUNNELING_DONE = True

    # Display errors on failure
    if task.state == 'Failure':
        print(f"** Errors: {task.errors[0]}")
        SSH_TUNNELING_DONE = True

