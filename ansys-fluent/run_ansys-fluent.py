#!/usr/bin/env python3
"""
Script to launch a simple Fluent task on Qarnot's platform
"""

import qarnot
from qarnot.scheduling_type import OnDemandScheduling

import os

# =============================== SETUP VARIABLES =============================== #
# ================================ CHANGE NEEDED ================================ #

CLIENT_TOKEN=os.getenv("QARNOT_TOKEN")         # If your token is in a .env. You can also execute, in your terminal, 'export QARNOT_TOKEN='your_token''.
CLIENT_TOKEN="MY_SECRET_TOKEN"                 # To comment or change
PROFILE="ansys-fluent-e-corp"                  # Set to your profile 

# =============================================================================== #
DIR_TO_SYNC = 'aircraft'                       # Name for your model's directory
INPUT_BUCKET_NAME =  f"{DIR_TO_SYNC}-in"    
OUTPUT_BUCKET_NAME = f"{DIR_TO_SYNC}-out"
TASK_NAME = f"RUN case - {DIR_TO_SYNC}" 

FLUENT_VERSION = "2025R2"
NB_INSTANCES = 2                               # Number of instances in your cluster. Xeon 28cores are the default instances.
FLUENT_CMD = "fluent -g 3ddp -t56 -i run.jou"  # t56 to use 2*26 cores out of the 2*28 available.        
# =============================== TASK CONFIGURATION =============================== #

# Create a connection
conn = qarnot.connection.Connection(client_token=CLIENT_TOKEN)

# Create a task
task = conn.create_task(TASK_NAME, PROFILE, NB_INSTANCES)

# Create the input bucket and synchronize with a local folder
input_bucket = conn.create_bucket(INPUT_BUCKET_NAME)
input_bucket.sync_directory(DIR_TO_SYNC)  # Replace with absolute path to your folder if needed
task.resources.append(input_bucket)

# Create a result bucket and attach it to the task
output_bucket = conn.create_bucket(OUTPUT_BUCKET_NAME)
task.results = output_bucket

# Fluent Command
task.constants['FLUENT_CMD'] = FLUENT_CMD
task.constants["DOCKER_TAG"] = FLUENT_VERSION

# Scheduling type
task.scheduling_type=OnDemandScheduling()

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