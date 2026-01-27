#!/usr/bin/env python3
"""
Script to launch a Fluent mpi test task on Qarnot's platform
"""

# Import the Qarnot SDK
import qarnot

# Create a connection
conn = qarnot.connection.Connection(client_token='MY_SECRET_TOKEN')

# Create a task
task = conn.create_task('ansys-fluent mpitest', 'ansys-fluent-e-corp', 2)

# Fluent command based on this template : 'fluent 3ddp -t56 -i run.jou'
task.constants['FLUENT_CMD'] = "fluent 3ddp -mpitest -t56"

# Fluent tag version
task.constants["DOCKER_TAG"] = "2025R2"

# Submit the task to the API
task.submit()
