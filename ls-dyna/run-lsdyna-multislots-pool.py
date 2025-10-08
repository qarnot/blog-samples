"""Script to run an LS-DYNA pool on Qarnot cloud"""

import qarnot
from qarnot.pool import MultiSlotsSettings
from qarnot.scheduling_type import OnDemandScheduling, ReservedScheduling

import os

# =============================== Setup Variables =============================== #
# To change
CLIENT_TOKEN="MY_SECRET_TOKEN"                 # To retrieve on tasq.qarnot.com/settings/access-token
CLIENT_TOKEN=os.getenv("QARNOT_TOKEN")         # Using an env variable
PROFILE="YOUR_PROFILE"                         # Example : 'ls-dyna-multislots-qarnot-vnc'

# Change the following if needed
VNC_PASSWORD = ""                              # Password for the VNC server. Must be less than 8 chars.
NB_INSTANCE_POOL = 1                           # Number of instances to be started for your pool.
SLOTS = 2                                      # Maximum number of tasks to be run on your pool.
ANSYS_VERSION="2025R1"                         # LS-DYNA 14.1 -> 2025R2
POOL_NAME=f'RUN Pool - LS-DYNA - {ANSYS_VERSION}' 

# =============================================================================== #
# =============================================================================== #

# Create a connection, from which all other objects will be derived
conn = qarnot.connection.Connection(client_token=CLIENT_TOKEN)

# Print available profiles with you account
print([profile for profile in conn.profiles_names() if 'dyna' in profile])

# Create pool
pool = conn.create_pool(POOL_NAME, PROFILE, NB_INSTANCE_POOL)

# IMAGE
pool.constants['DOCKER_TAG'] = ANSYS_VERSION

# MULTI SLOTS SETTINGS
## 
pool.multi_slots_settings = MultiSlotsSettings(SLOTS)
pool.constants['SLOTS']= str(SLOTS)

# Optional parameters
# VNC - set to true to enable desktop visualization
pool.constants["VNC"] = "true"
# VNC_PASSWORD - Password for the VNC server. Must be less than 8 chars (additional ones will be ignored).
# If none, a random one will be assigned and log in task's stdout.
pool.constants["VNC_PASSWORD"] = VNC_PASSWORD

# Scheduling type
# task.scheduling_type=OnDemandScheduling()
# task.scheduling_type=ReservedScheduling() # If your company has reserved nodes

# Settings to copy from simulation directory (/share) to bucket linked directory (/job).
##  /job  is the dir where buckets are downloaded at start and uploaded to your bucket by the snapshots.
## /share is the dir where the simulation is executing. Fastest disk and shared directories between nodes.
pool.constants['LOCAL_FILES_COPY_FEATURE'] = "true"       # Set to true to upload periodically from the /share folder
pool.constants['LOCAL_FILES_COPY_INTERVAL_SEC'] = "1800"  # Set the upload interval in seconds
pool.constants['LOCAL_FILES_COPY_REGEX'] = ""             # Filters the files to upload, leave empty to upload everything


pool.submit()

print(f"Pool UUID to create tasks on : \n{pool.uuid}")

# ============= Optional =============
# Print VNC web link - password 
LAST_STATE = ''
VNC_UP = False
while not VNC_UP:
    if pool.state != LAST_STATE:
        LAST_STATE = pool.state
        print(f"** {LAST_STATE}")

    # Wait for the pool to be FullyExecuting
    if pool.state == 'FullyExecuting':
        # If the ssh connexion was not done yet and the list active_forward is available (len!=0)
        forward_list = pool.status.running_instances_info.per_running_instance_info[0].active_forward
        if not VNC_UP and len(forward_list) != 0:
            for forward in forward_list:
                forward_host = forward.forwarder_host
                if forward_host != "gateway.qarnotservices.com":
                    print(f"Desktop link : https://{forward_host}/vnc.html?password={VNC_PASSWORD}\n")
                    VNC_UP = True

    # Display errors on failure
    if pool.state == 'Failure':
        print(f"** Errors: {pool.errors[0]}")
        VNC_UP = True
