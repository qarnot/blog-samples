"""
Script to launch a simple Altair task on Qarnot's platform
"""

import qarnot
import os

from dotenv import load_dotenv
load_dotenv()

# =============================== SETUP VARIABLES =============================== #

# =============================== Mandatory Variables =============================== #

CLIENT_TOKEN=os.getenv("QARNOT_TOKEN")         # If your token is in a .env. You can also execute, in your terminal, 'export QARNOT_TOKEN='your_token''.
PROFILE="YOUR_PROFILE"                         # Example : 'altair-hyperworks-qarnot-vnc-wan'
#ALM_HHWU_TOKEN='YOUR_ALM_HHWU_TOKEN'          # If your licence is hosted on Altair-One 

NB_INSTANCES = 1                               # Number of instances in your cluster.
ALTAIR_VERSION="2024.1"                        # Altair Hyperwork 2024.1 
                        
DIR_TO_SYNC = 'altair_block_test'              # Exact name for your model's directory containg your .rad (Radioss) or .fem (Optistruct) model
INPUT_BUCKET_NAME =  f"{DIR_TO_SYNC}-in"    
OUTPUT_BUCKET_NAME = f"{DIR_TO_SYNC}-out"
TASK_NAME = f"RUN test Altair - {DIR_TO_SYNC}" 

INSTANCE_TYPE = 'xeon'                         # xeon is the default choice. Otherwise, put 'epyc'.
SETUP_CLUSTER_NB_SLOTS = 26                    

ALTAIR_CMD = f"optistruct -nt {SETUP_CLUSTER_NB_SLOTS} -out block.fem" # Your Altair Hyperworks CMD, depending on your solver

# =============================== TASK CONFIGURATION =============================== #

# Create a connection, from which all other objects will be derived
conn = qarnot.connection.Connection(client_token=CLIENT_TOKEN)

# Create task
task = conn.create_task(TASK_NAME, PROFILE, NB_INSTANCES)

# Insert your Altair One token to access your licence, if applicable
#task.constants['ALM_HHWU_TOKEN'] = ALM_HHWU_TOKEN

# Create the input bucket and synchronize with a local folder
input_bucket = conn.create_bucket(INPUT_BUCKET_NAME)
input_bucket.sync_directory(DIR_TO_SYNC)
task.resources.append(input_bucket)

# Create a result bucket and attach it to the task
output_bucket = conn.create_bucket(OUTPUT_BUCKET_NAME)
task.results = output_bucket

# Specify Altair CMD, version, number of cores per node, etc. 
## Historically, at Qarnot, the Altair Hyperworks Suite was named "Altair Mechanical" at Qarnot. We kept the variable value, but don't worry - It is Altair Hyperworks!
task.constants["ALTAIR_MECHA_CMD"] = ALTAIR_CMD
task.constants['DOCKER_TAG'] = ALTAIR_VERSION

# Submitting task
task.submit()
print('Submitting task on Qarnot')

# =============================== MONITORING AND RESULTS =============================== #

# The following will download results to the OUTPUT_BUCKET_NAME directory
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

