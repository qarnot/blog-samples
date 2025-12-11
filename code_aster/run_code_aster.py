"""
Script to launch a simple code-aster task on Qarnot's platform
"""

import qarnot
from qarnot.scheduling_type import OnDemandScheduling
import os

# =============================== Setup Variables =============================== #

CLIENT_TOKEN=os.getenv("QARNOT_TOKEN")         # If your token is in a .env. You can also execute, in your terminal, 'export QARNOT_TOKEN='your_token''.
PROFILE="code-aster"                           # Qarnot profile to use. Use "code-aster" to not have interenet acces and no ssh connectivity.

NB_INSTANCES = 1                               # Number of instances in your cluster.
CODE_ASTER_VERSION="16.7"                      # Code_Aster version

DIR_TO_SYNC = 'etudepoutre2D'                  # Exact name for your model's directory.
INPUT_BUCKET_NAME =  f"{DIR_TO_SYNC}-in"    
OUTPUT_BUCKET_NAME = f"{DIR_TO_SYNC}-out"
TASK_NAME = f"RUN test Code_Aster - {DIR_TO_SYNC}" 

CA_EXPORT_FILE = "etudepoutre2D.export"        # Your Code_Aster .export file. 

# =============================== Lauching a Task =============================== #

# Create a connection, from which all other objects will be derived
conn = qarnot.connection.Connection(client_token=CLIENT_TOKEN)

# Create task
task = conn.create_task(TASK_NAME, PROFILE, NB_INSTANCES)

# Create the input bucket and synchronize with a local folder
input_bucket = conn.retrieve_or_create_bucket(INPUT_BUCKET_NAME)
input_bucket.sync_directory(DIR_TO_SYNC)
task.resources.append(input_bucket)

# Create a result bucket and attach it to the task
output_bucket = conn.create_bucket(OUTPUT_BUCKET_NAME)
task.results = output_bucket

# Required settings
task.constants["CA_EXPORT_FILE"] = CA_EXPORT_FILE
task.constants['DOCKER_TAG'] = CODE_ASTER_VERSION
task.constants["SETUP_CLUSTER_NB_SLOTS"] = "26"   # Number of processes per node in the mpihost file. "26" is optimal for xeon.
task.hardware_constraints = [qarnot.hardware_constraint.SpecificHardware("28c-128g-intel-dual-xeon2680v4-ssd")]

# Scheduling type
task.scheduling_type=OnDemandScheduling()

# You are ready to submit your task!
print('Submitting task on Qarnot')
task.submit()
