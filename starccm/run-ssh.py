"""Script to run a STAR-CCM sample with SSH connectivity on Qarnot cloud"""

import qarnot
from qarnot.scheduling_type import OnDemandScheduling

# =============================== Setup Variables =============================== #
# To change
CLIENT_TOKEN="<MY_SECRET_TOKEN>"
PROFIL="<YOUR_SSH_PROFILE>"
SSH_PUBLIC_KEY=""

# If needed
TASK_NAME='RUN SAMPLE - STARCCM'
STARCCM_VERSION="19.04.009"
NB_INSTANCES = 1
STARCCM_CMD="starccm+ -power -batch run cylindre_complet_extrusion_both_demi_DP_reconstruit_init.sim"

# Optional - Multi node simulation
# NB_INSTANCES = 2
# STARCCM_CMD="starccm+ -power -batch -mpi openmpi -mpiflags \"--mca btl ^openib,tcp --mca pml ucx --mca osc ucx\" -machinefile /job/mpihosts run cylindre_complet_extrusion_both_demi_DP_reconstruit_init.sim"

# =============================================================================== #

# Create a connection, from which all other objects will be derived
conn = qarnot.connection.Connection(client_token=CLIENT_TOKEN)

# Create task
task = conn.create_task(TASK_NAME, PROFIL, NB_INSTANCES)

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
task.constants['DOCKER_SSH'] = SSH_PUBLIC_KEY

# Optional parameters
# Set to 'true' to keep cluster alive once your simulation is done.
task.constants['NO_EXIT'] = "false" 

# Number of processes per node in the mpihost file, e.g. "26" out of 28 cores.
task.constants['SETUP_CLUSTER_NB_SLOTS'] = "26"

# Define interval time in seconds when your simulation will be saved to your bucket.
# task.snapshot(900)

# OnDemand setup
# task.scheduling_type=OnDemandScheduling()

task.submit()

