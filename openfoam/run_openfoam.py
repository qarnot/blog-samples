"""
Script to launch a simple Openfoam task on Qarnot's platform
"""

import qarnot
import os

from dotenv import load_dotenv
load_dotenv()

# =============================== SETUP VARIABLES =============================== #

# =============================== Mandatory Variables =============================== #

CLIENT_TOKEN=os.getenv("QARNOT_TOKEN")         # If your token is in a .env. You can also execute, in your terminal, 'export QARNOT_TOKEN='your_token''.
PROFILE="openfoam"                        

NB_INSTANCES = 2                               # Number of instances in your cluster.

DIR_TO_SYNC = 'motorbike'                      # Name for your model's directory
INPUT_BUCKET_NAME =  f"{DIR_TO_SYNC}-in"    
OUTPUT_BUCKET_NAME = f"{DIR_TO_SYNC}-out"
TASK_NAME = f"RUN test Openfoam - {DIR_TO_SYNC}" 

OPENFOAM_CMD = "Allrun"           
# =============================== TASK CONFIGURATION =============================== #

# Create a connection, from which all other objects will be derived
conn = qarnot.connection.Connection(client_token=CLIENT_TOKEN)

# Create task
task = conn.create_task(TASK_NAME, PROFILE, NB_INSTANCES)

# Create the input bucket and synchronize with a local folder
input_bucket = conn.create_bucket(INPUT_BUCKET_NAME)
input_bucket.sync_directory(DIR_TO_SYNC)  # Replace with absolute path to your folder if needed
task.resources.append(input_bucket)

# Create a result bucket and attach it to the task
output_bucket = conn.create_bucket(OUTPUT_BUCKET_NAME)
task.results = output_bucket

# Specify Run script CMD, version, number of cores per node, etc. 
task.constants['RUN_SCRIPT'] = OPENFOAM_CMD

# Submitting task
print('Submitting and running task on Qarnot. You can go to the online platform for more interactive task monitoring. Otherwise, the results will be downloaded automatically once the task reaches Success.')
task.submit()

# =============================== MONITORING AND RESULTS =============================== #

# Download results when "Success" state is reached
SUCCESS = False
while not SUCCESS:
    # Wait for the task to be FullyExecuting
    if task.state == 'Success':
      print('Task reached Success. Downloading Results.')
      task.download_results(OUTPUT_BUCKET_NAME, True)
      SUCCESS = True