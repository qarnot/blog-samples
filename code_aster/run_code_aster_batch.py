import qarnot
from qarnot.scheduling_type import OnDemandScheduling, FlexScheduling, ReservedScheduling
import os

from dotenv import load_dotenv
load_dotenv()

# =============================== Setup Variables =============================== #

# =============================== Mandatory Variables =============================== #
CLIENT_TOKEN="MY_SECRET_TOKEN"                 # To retrieve on your HPC or Tasq account
CLIENT_TOKEN=os.getenv("QARNOT_TOKEN")         # Or, Using an env variable
PROFILE="code-aster"                           # Qarnot profile to use. Use "code-aster" to not have interenet acces and no ssh connectivity.

NB_INSTANCES = 1                               # Number of instances in your cluster.
CODE_ASTER_VERSION="16.7"                      # Code_Aster version

DIR_TO_SYNC = 'etudepoutre2D'                  # Exact name for your model's directory.
INPUT_BUCKET_NAME =  f"{DIR_TO_SYNC}-in"    
OUTPUT_BUCKET_NAME = f"{DIR_TO_SYNC}-out"
TASK_NAME = f"RUN test Code_Aster - {DIR_TO_SYNC}" 

CA_EXPORT_FILE = "etudepoutre2D.export"        # Your Code_Aster .export file. 

INSTANCE_TYPE = 'xeon'                         # "xeon" is the default choice. Otherwise, put "epyc".
if INSTANCE_TYPE == 'xeon':
    SETUP_CLUSTER_NB_SLOTS = 26                # Number of processes per node in the mpihost file. "26" is optimal for xeon.
    instance_type="28c-128g-intel-dual-xeon2680v4-ssd"
elif INSTANCE_TYPE == 'epyc':
    SETUP_CLUSTER_NB_SLOTS = 94                # Number of processes per node in the mpihost file. "94" is optimal for xeon.       
    instance_type = "96c-512g-amd-epyc9654-ssd"

# =============================== Optional Variables =============================== #
#OUTPUT_FILTER = r"(?i).*\.txt$"               # Optional : Regex filter to select which outputfiles you want to keep. Here, an example with .txt
#SYNC_FILTER = OUTPUT_FILTER                   # Optional : Regex filter to select which files are copied during your snapshots

POST_PROCESSING_CMD = ""                       # Optional : Post processing command, ran after simulation if not empty.

# =============================== TASK CONFIGURATION =============================== #

# =============================== Mandatory Configuration =============================== #

# Create a connection, from which all other objects will be derived
conn = qarnot.connection.Connection(client_token=CLIENT_TOKEN)

# Print available profiles with you account
print([profile for profile in conn.profiles_names() if 'code-aster' in profile])

# Create task
task = conn.create_task(TASK_NAME, PROFILE, NB_INSTANCES)

# Create the input bucket and synchronize with a local folder
input_bucket = conn.create_bucket(INPUT_BUCKET_NAME)
input_bucket.sync_directory(DIR_TO_SYNC)
task.resources.append(input_bucket)

# Create a result bucket and attach it to the task
output_bucket = conn.create_bucket(OUTPUT_BUCKET_NAME)
task.results = output_bucket

# Required settings
task.constants["CA_EXPORT_FILE"] = CA_EXPORT_FILE
task.constants['DOCKER_TAG'] = CODE_ASTER_VERSION
task.constants["SETUP_CLUSTER_NB_SLOTS"] = SETUP_CLUSTER_NB_SLOTS
task.hardware_constraints = [qarnot.hardware_constraint.SpecificHardware(instance_type)]

# Scheduling type
task.scheduling_type=OnDemandScheduling()
# task.scheduling_type=FlexScheduling()
# task.scheduling_type=ReservedScheduling()               # If your company has reserved nodes
# task.targeted_reserved_machine_key = instance_type      # Uncomment if your company has reserved nodes

# =============================== Optional Configuration =============================== #

#task.snapshot(1800)                                     # Define interval time in seconds when /job will be saved to your bucket.
#task.snapshots_whitelist  = SYNC_FILTER
#task.results_whitelist  = OUTPUT_FILTER

#task.constants['POST_PROCESSING_CMD'] = POST_PROCESSING_CMD

# Settings to copy from simulation directory (/share) to bucket linked directory (/job).
##  /job  is the dir where buckets are downloaded at start and uploaded to your bucket by the snapshots.
## /share is the dir where the simulation is executing. Fastest disk and shared directories between nodes.

#task.constants['LOCAL_FILES_COPY_FEATURE'] = "true"       # Set to true to upload periodically from the /share folder
#task.constants['LOCAL_FILES_COPY_INTERVAL_SEC'] = "1800"  # Set the upload interval in seconds
#task.constants['LOCAL_FILES_COPY_REGEX'] = ""             # Filters the files to upload, leave empty to upload everything

# =============================== LAUNCH YOUR TASK ! =============================== #

# You are ready to submit your task!
print('Submitting task on Qarnot')
task.submit()

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