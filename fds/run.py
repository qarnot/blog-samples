#!/usr/bin/env python
"""Script to run an FDS sample computation on Qarnot cloud"""

import qarnot
from qarnot.scheduling_type import OnDemandScheduling

# =============================== Setup Variables =============================== #
# To change
CLIENT_TOKEN="YOUR_SECRET_TOKEN"

# If needed
TASK_NAME=f"RUN SAMPLE FDS"
FDS_VERSION="6.7.9"
NB_INSTANCES=1

# =============================================================================== #

# Create a connection, from which all other objects will be derived
conn = qarnot.connection.Connection(client_token=CLIENT_TOKEN)

# Create a task
task = conn.create_task(TASK_NAME, "fds", NB_INSTANCES)

# Create the input bucket and synchronize with a local folder
input_bucket = conn.create_bucket('fds-temple')
input_bucket.sync_directory('temple')
task.resources.append(input_bucket)

# Create a result bucket and attach it to the task
output_bucket = conn.create_bucket(f'fds-temple-out')
task.results = output_bucket

# Configure task parameters
task.constants["DOCKER_TAG"] = FDS_VERSION
task.constants["FDS_CMD"] = "mpiexec -np 16 fds temple_16_MPI_PROC.fds"

# Number of processes per node in the mpihost file, e.g. "26" out of 28 cores.
# task.constants['SETUP_CLUSTER_NB_SLOTS'] = "26"

# Define interval time in seconds when your simulation will be saved to your bucket.
task.snapshot(900)

# OnDemand setup
# task.scheduling_type=OnDemandScheduling()

# ---------- Optional ----------
OUTPUT_DIR="temple-out"
task.submit()

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