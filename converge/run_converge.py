"""
Script to launch a simple Converge task on Qarnot's platform
"""

import qarnot

# =============================== SETUP VARIABLES =============================== #

# =============================== Mandatory Variables =============================== #

CLIENT_TOKEN="YOUR_QARNOT_TOKEN"                   # You can also insert your token in a .env, export it in your terminal or use the .conf file directly. 
PROFILE="YOUR_PROFILE"                             # Example : 'converge-qarnot'

NB_INSTANCES = 1                                   # Number of instances in your cluster. We will set it for "one xeon" instance here.

MODEL_NAME = 'SI8_engine_intake_flowbench_2_mm_steady_RANS' # Name for your model's directory inside 'input_converge'
INPUT_BUCKET_NAME =  "CONVERGE-in"    
OUTPUT_BUCKET_NAME = "CONVERGE-out"
TASK_NAME = "RUN test - CONVERGE" 

# =============================== TASK CONFIGURATION =============================== #

# Create a connection, from which all other objects will be derived
conn = qarnot.connection.Connection(client_token=CLIENT_TOKEN)

# Create task
task = conn.create_task(TASK_NAME, PROFILE, NB_INSTANCES)

# Create the input bucket and synchronize with a local folder
# If needed, you can put the absolute path to your model`s directory instead the second INPUT_BUCKET_NAME
input_bucket = conn.create_bucket(INPUT_BUCKET_NAME)
input_bucket.sync_directory(MODEL_NAME)     
task.resources.append(input_bucket)

# Create a result bucket and attach it to the task
output_bucket = conn.create_bucket(OUTPUT_BUCKET_NAME)
task.results = output_bucket

# Specify Converge constants
task.constants['CONVERGE_INPUT_DIRECTORY_NAME'] = MODEL_NAME
task.constants['NB_PROCESSES'] = 26

# Submitting task
task.submit()
print('Submitting task on Qarnot')

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
