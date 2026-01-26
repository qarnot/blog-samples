#!/usr/bin/env python3
"""
Script to run a ansys-mechanical sample computation on Qarnot cloud
"""

import qarnot
from qarnot.scheduling_type import OnDemandScheduling

import os

# =============================== Setup Variables =============================== #
# ================================ CHANGE NEEDED ================================ #
CLIENT_TOKEN=os.getenv("QARNOT_TOKEN")         # If your token is in a .env. You can also execute, in your terminal, 'export QARNOT_TOKEN='your_token''.
CLIENT_TOKEN="MY_SECRET_TOKEN"                 # To comment or change
PROFILE="ansys-mechanical-e-corp"              # Example : 'ansys-mechanical-qarnot'

# =============================================================================== #
DIR_TO_SYNC = "v8"                       # This is the local directory that will be uploaded to you input bucket
INPUT_BUCKET_NAME =  f"{DIR_TO_SYNC}-in"
OUTPUT_BUCKET_NAME = f"{DIR_TO_SYNC}-out"
TASK_NAME = f"RUN test Ansys Mechanical - {DIR_TO_SYNC}" 

VERSION="2025R2-beta"                          # Ansys Mechanical Version
NB_INSTANCES = 1                               # Number of instances in your cluster.
MECHANICAL_CMD = f"mapdl -b -i V24direct-1.dat -np 26"

# =============================================================================== #

# Create a connection, from which all other objects will be derived
conn = qarnot.connection.Connection(client_token=CLIENT_TOKEN)

# Print available profiles with you account
print([profile for profile in conn.profiles_names() if 'ansys-mechanical' in profile])

# Create task
task = conn.create_task(TASK_NAME, PROFILE, NB_INSTANCES)

# Create the input bucket and synchronize with a local folder
input_bucket = conn.create_bucket(INPUT_BUCKET_NAME)
input_bucket.sync_directory(DIR_TO_SYNC)
task.resources.append(input_bucket)

# Create a result bucket and attach it to the task
output_bucket = conn.create_bucket(OUTPUT_BUCKET_NAME)
task.results = output_bucket

# Ansys mechanical version
task.constants['DOCKER_TAG'] = VERSION

# CMD - To use with mapdl
task.constants["MECHANICAL_CMD"] = MECHANICAL_CMD

# Optional parameters
# Number of processes per node in the mpihost file, e.g. "26" out of 28 cores.
task.constants['SETUP_CLUSTER_NB_SLOTS'] = "26"

# Scheduling type
task.scheduling_type=OnDemandScheduling()

# =============================== LAUNCH YOUR TASK ! ================================== #

# Submitting task
task.submit()
print('Task submitted on Qarnot')

# =============================== MONITORING AND RESULTS =============================== #

# The following will download result to the OUTPUT_BUCKET_NAME dir
# It will also print the state of the task to your console
LAST_STATE = ''
TASK_ENDED = False
while not TASK_ENDED:
    if task.state != LAST_STATE:
        LAST_STATE = task.state
        print(f"** {LAST_STATE}")

    # Wait for the task to be FullyExecuting
    if task.state == 'Success':
        print(f"** {LAST_STATE}")
        task.download_results(OUTPUT_BUCKET_NAME, True)
        TASK_ENDED = True

    # Display errors on failure
    if task.state == 'Failure':
        print(f"** Errors: {task.errors[0]}")
        TASK_ENDED = True