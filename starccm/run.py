"""Script to run a STAR-CCM sample computation on Qarnot cloud"""

import qarnot
from qarnot.scheduling_type import OnDemandScheduling

# =============================== Setup Variables =============================== #
# To change
CLIENT_TOKEN="MY_SECRET_TOKEN"
PROFILE="YOUR_PROFILE"

# If needed
TASK_NAME='RUN SAMPLE - STARCCM'
STARCCM_VERSION="19.04.009"
NB_INSTANCES = 1
STARCCM_CMD="starccm+ -power -batch run cylindre_complet_extrusion_both_demi_DP_reconstruit_init_c4056f43d7.sim"

# Optional - Multi node simulation
# NB_INSTANCES = 2
# STARCCM_CMD="starccm+ -power -batch -mpi openmpi -mpiflags \"--mca btl ^openib,tcp --mca pml ucx --mca osc ucx\" -machinefile /job/mpihosts run cylindre_complet_extrusion_both_demi_DP_reconstruit_init_c4056f43d7.sim"

# =============================================================================== #

# Create a connection, from which all other objects will be derived
conn = qarnot.connection.Connection(client_token=CLIENT_TOKEN)

# Create task
task = conn.create_task(TASK_NAME, PROFILE, NB_INSTANCES)

# Create the input bucket and synchronize with a local folder
input_bucket = conn.create_bucket('starccm-in')
input_bucket.sync_directory('input')
task.resources.append(input_bucket)

# Create a result bucket and attach it to the task
output_bucket = conn.create_bucket('starccm-out')
task.results = output_bucket

# Configure task parameters
task.constants['STARCCM_CMD'] = STARCCM_CMD
task.constants['DOCKER_TAG'] = STARCCM_VERSION

# Optional parameters
# Number of processes per node in the mpihost file, e.g. "26" out of 28 cores.
# task.constants['SETUP_CLUSTER_NB_SLOTS'] = "26"

# Define interval time in seconds when your simulation will be saved to your bucket.
# task.snapshot(900)

# OnDemand setup
# task.scheduling_type=OnDemandScheduling()

task.submit()

# ---------- Optional ----------

OUTPUT_DIR="cylindre-out"

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
        task.download_results(OUTPUT_DIR, True)
        SSH_TUNNELING_DONE = True

    # Display errors on failure
    if task.state == 'Failure':
        print(f"** Errors: {task.errors[0]}")
        SSH_TUNNELING_DONE = True