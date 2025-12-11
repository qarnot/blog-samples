"""
Script to launch a simple StarCCM task on Qarnot's platform
"""

import qarnot
import os

from dotenv import load_dotenv
load_dotenv()

# =============================== SETUP VARIABLES =============================== #

# =============================== Mandatory Variables =============================== #

CLIENT_TOKEN=os.getenv("QARNOT_TOKEN")         # If your token is in a .env. You can also execute, in your terminal, 'export QARNOT_TOKEN='your_token''.
PROFILE="YOUR_PROFILE"                         # Example : 'starccm-qarnot'

NB_INSTANCES = 2                               # Number of instances in your cluster.

DIR_TO_SYNC = 'starccm_cylindre_test'          # Name for your model's directory with your .sim model
INPUT_BUCKET_NAME =  f"{DIR_TO_SYNC}-in"    
OUTPUT_BUCKET_NAME = f"{DIR_TO_SYNC}-out"
TASK_NAME = f"RUN test StarCCM - {DIR_TO_SYNC}" 

STARCCM_CMD = f"starccm+ -np 26*{NB_INSTANCES} -batch cylindre_complet_extrusion_both_demi_DP_reconstruit_init.sim" 

# =============================== TASK CONFIGURATION =============================== #

# Create a connection, from which all other objects will be derived
conn = qarnot.connection.Connection(client_token=CLIENT_TOKEN)

# Create task
task = conn.create_task(TASK_NAME, PROFILE, NB_INSTANCES)

# Create the input bucket and synchronize with a local folder
# If needed, you can put the absolute path to your model`s directory instead of DIR_TO_SYNC
input_bucket = conn.create_bucket(INPUT_BUCKET_NAME)
input_bucket.sync_directory(DIR_TO_SYNC)     
task.resources.append(input_bucket)

# Create a result bucket and attach it to the task
output_bucket = conn.create_bucket(OUTPUT_BUCKET_NAME)
task.results = output_bucket

# Specify StarCCM CMD
task.constants["STARCCM_CMD"] = STARCCM_CMD

# Submitting task
task.submit()
print('Submitting task on Qarnot. You can monitor the task on the online platform. Results will be downloaded when task reach Success.')

# =============================== MONITORING AND RESULTS =============================== #

# The following will download result to the OUTPUT_BUCKET_NAME directory
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
