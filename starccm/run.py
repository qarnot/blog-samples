"""Script to run a STAR-CCM sample computation on Qarnot cloud"""

import qarnot

# =============================== Setup Variables =============================== #
# Change the following if needed

CLIENT_TOKEN="<<<YOUR_PRIVATE_TOKEN>>>"
NB_INSTANCES = 2
TASK_NAME='RUN SAMPLE - STARCCM'

STARCCM_LICENSE_PORT='<<<YOUR_LICENSE_PORT>>>'
STARCCM_LICENSE_IP='<<<YOUR_LICENSE_IP>>>'

STARCCM_CMD="starccm+ -power -batch run -mpi openmpi4 -machinefile /job/mpihosts cylindre_complet_extrusion_both_demi_DP_reconstruit_init.sim"

# =============================================================================== #

# Create a connection, from which all other objects will be derived
conn = qarnot.Connection(client_token=CLIENT_TOKEN)

# Create task
task = conn.create_task(TASK_NAME, 'starccm', NB_INSTANCES)

# Create the input bucket and synchronize with a local folder
input_bucket = conn.create_bucket('starccm-in')
input_bucket.sync_directory('input')
task.resources.append(input_bucket)

# Create a result bucket and attach it to the task
output_bucket = conn.create_bucket('starccm-out')
task.results = output_bucket

# Configure task parameters
task.constants['STARCCM_LICENSE_IP'] = STARCCM_LICENSE_IP
task.constants['STARCCM_LICENSE_PORT'] = STARCCM_LICENSE_PORT
task.constants['STARCCM_CMD'] = STARCCM_CMD

task.constants['SETUP_CLUSTER_MPIHOST_STYLE'] = "colon" # Starccm requires a secial style for mpihost file

task.submit()
