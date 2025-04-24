#!/usr/bin/env python
"""Script to run an FDS sample computation on Qarnot cloud"""

import qarnot
from qarnot.scheduling_type import OnDemandScheduling

# =============================== Setup Variables =============================== #
# To change
CLIENT_TOKEN="YOUR_SECRET_TOKEN"
SSH_PUBLIC_KEY="YOUR_SSH_PUBLIC_KEY"

# If needed
TASK_NAME=f"RUN SAMPLE FDS VNC"
FDS_VERSION="6.7.9"
NB_INSTANCES=1
NO_EXIT="false"
# =============================================================================== #

# Create a connection, from which all other objects will be derived
conn = qarnot.connection.Connection(client_token=CLIENT_TOKEN)

# Create a task
task = conn.create_task(TASK_NAME, "fds-vnc-ssh", NB_INSTANCES)

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
task.constants['DOCKER_SSH'] = SSH_PUBLIC_KEY

# Set to 'true' to keep cluster alive once your simulation is done.
task.constants['NO_EXIT'] = NO_EXIT 

# Number of processes per node in the mpihost file, e.g. "26" out of 28 cores.
# task.constants['SETUP_CLUSTER_NB_SLOTS'] = "26"

# Define interval time in seconds when your simulation will be saved to your bucket.
task.snapshot(900)

# OnDemand setup
# task.scheduling_type=OnDemandScheduling()

task.submit()