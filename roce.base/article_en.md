`roce.base` is a Qarnot-provided base image for HPC applications that need MPI and RoCE networking. `roce_wrapper` is the runtime entry point inside that image: it prepares the cluster, generates the MPI hostfile, manages shared storage, and runs your pre-simulation, simulation, and post-simulation commands.

This article shows how to build your own child image on top of the Qarnot-provided `roce.base` image, push it to Qarnot Container Registry, and launch it with the Python SDK. If you do not already have access to the base image repository and tag, ask Qarnot to provide them before starting.

## Task lifecycle powered by `roce.base`: stay focused on your simulation software
Qarnot's internal scripts orchestrate the entire application lifecycle.

It follows a structured lifecycle:

1. **Cluster initialization**
   - checking environment variables;
   - SSH configuration;
   - hostfile generation;
   - MPI configuration;
   - NFS or Lustre detection;
   - optional VNC activation;
   - working directory preparation.

2. **Loading the software wrapper**
   - software-specific configuration;
   - adding environment variables;
   - license configuration;
   - optional activation of a log parser;

3. **Simulation execution**
   - pre-simulation command;
   - main simulation command;
   - post-simulation command;
   - optional maximum execution time management.

4. **Synchronization and finalization**
   - final copy of results;
   - stopping synchronization scripts;
   - stopping monitoring scripts;
   - log analysis to detect soft errors;
   - returning a consistent error code.

## Access to the base image

The `roce.base` parent image is provided directly by Qarnot. If you do not already have the exact repository and tag for your project, please contact your Qarnot account team or <a href="mailto:support-compute@qarnot-computing.com" target="_blank">support-compute@qarnot-computing.com</a>.

This public article assumes that you already have access to that private parent image and focuses on the customer-side steps: build a child image, push it to Qarnot Container Registry, and launch it with `roce_wrapper`.

## Launching a task on Qarnot

Common ways to launch a task on Qarnot are:
- Via the web interface <a href="https://tasq.qarnot.com/tasks" target="_blank">Tasq</a>
- With a script, for example with the Python SDK

For a custom image built from `roce.base`, the Python SDK is generally the most practical option, so the rest of this article uses it.

> **Note:** In addition to the Python SDK, Qarnot also provides SDKs for <a href="https://doc.tasq.qarnot.com/documentation/sdk-csharp/" target="_blank">C#</a> and <a href="https://doc.tasq.qarnot.com/documentation/sdk-nodejs/" target="_blank">Node.js</a>, as well as a Command Line Interface (<a href="https://doc.tasq.qarnot.com/documentation/cli/man/ManIndex.html" target="_blank">CLI</a>).


## Prerequisites

Before launching the sample, make sure you have:
- A Qarnot account: <a href="https://app.qarnot.com/register" target="_blank">create an account</a>
- An API token: <a href="https://app.qarnot.com/settings/access-token" target="_blank">retrieve it here</a>
- The Qarnot Python SDK installed: <a href="https://doc.tasq.qarnot.com/documentation/sdk-python/installation.html" target="_blank">installation guide</a>
- Docker installed on your local machine
- Qarnot Container Registry activated from <a href="https://app.qarnot.com/settings/access-token" target="_blank">the access token page</a>
- A Container Registry Key available from <a href="https://app.qarnot.com/settings/access-token" target="_blank">the same page</a> after registry activation
- Access to one of the RoCE Docker cluster profiles: `docker-cluster-roce-vnc`, `docker-cluster-roce`, or `docker-cluster-roce-ssh`
- Access to the Qarnot-provided `roce.base` parent image repository and tag

## Qarnot runtime model and lifecycle commands

### Qarnot runtime conventions
This sample relies on a few Qarnot-specific runtime conventions:

- A task is launched on a Qarnot cluster profile such as `docker-cluster-roce`, `docker-cluster-roce-ssh`, or `docker-cluster-roce-vnc`.
- Your custom image is a child image built on top of the Qarnot-provided `roce.base` parent image.
- Inside the container, `roce_wrapper` is the Qarnot runtime entry point. It prepares the cluster and executes the simulation lifecycle.
- The file `/opt/qarnot/wrapper` is your software-specific hook. It is loaded by `roce_wrapper` to expose environment variables, version checks, licenses, or setup logic.
- `/share` is the fast shared runtime directory used by the simulation across the cluster nodes.
- `/job` is the bucket-backed directory used for input and output synchronization.
- In the Python SDK, `task.constants[...]` are exposed to the runtime as environment variables consumed by `roce_wrapper` and your wrapper logic.

In practice, this means the sample uploads inputs to the input bucket, runs the simulation from `/share`, and synchronizes selected files back through `/job` to the output bucket.

### Passing simulation lifecycle commands
The simulation lifecycle commands are then passed through environment variables:

- `PRE_SIMULATION_COMMAND`;
- `SIMULATION_COMMAND`;
- `POST_SIMULATION_COMMAND`.

#### Conceptual Example

```bash
PRE_SIMULATION_COMMAND="echo Preparing case"
SIMULATION_COMMAND="mpirun --hostfile /share/qhost ./my_solver"
POST_SIMULATION_COMMAND="tar -czf results.tar.gz output/"
```

## Test case

To keep the sample reusable for any customer software, this test case uses a minimal MPI connectivity demo instead of a solver-specific case.

The sample files are:

<pre>
roce.base/
├── Dockerfile
├── mpi_test/
│   └── run_mpi_demo.sh
├── wrapper.sh
├── run_roce_base_advanced.py
└── run_roce_base_batch.py
</pre>

The Python scripts synchronize the local `mpi_test/` directory to the input bucket and launch the task on Qarnot. The image installs a `wrapper.sh` as `/opt/qarnot/wrapper`.

## Build your custom image

The `Dockerfile` below extends the Qarnot-provided base image, copies the MPI demo script into the image, and installs `/opt/qarnot/wrapper`, the customer-specific software wrapper. 

> **Roce.base version**: Replace the parent image placeholder `<qarnot-provided-roce-base-image>:<tag-provided-by-qarnot>` with the private value shared by Qarnot.

<div class="wf-code-card"
     data-url="https://cdn.jsdelivr.net/gh/qarnot/blog-samples@main/roce.base/Dockerfile"
     data-filename="Dockerfile"
     data-language="dockerfile"
     data-linenumbers="true"
     data-maxheight="65vh"
     data-fontsize="13px"
     data-download="true"
     data-copy="true"></div>

### Software wrapper

The wrapper below exposes a few demo environment variables, publishes this version assertion, writes an `/etc/profile.d` snippet, and makes sure `/share/run_mpi_demo.sh` exists before the simulation lifecycle starts.

> **Note:** `/opt/qarnot/wrapper` is loaded automatically, so it should contain a real `main()` function and explicitly call it.

<div class="wf-code-card"
     data-url="https://cdn.jsdelivr.net/gh/qarnot/blog-samples@main/roce.base/wrapper.sh"
     data-filename="wrapper.sh"
     data-language="bash"
     data-linenumbers="true"
     data-maxheight="65vh"
     data-fontsize="13px"
     data-download="true"
     data-copy="true"></div>

This wrapper also declares a software version assertion. `DOCKER_BUILD_SOFT_VERSION` is the build-time value stored in the image, and `QARNOT_GET_SOFT_VERSION` is the runtime command exported by the wrapper to retrieve the same version.

For this `mpirun` / OpenMPI demo, both values are pinned to `5.0.9`. The wrapper normalizes the first line of `mpirun --version` so that `QARNOT_GET_SOFT_VERSION` returns only `5.0.9`.

> **Note:** To ignore this feature, use a static placeholder `1.0.0` as `DOCKER_BUILD_SOFT_VERSION` in the Dockerfile

### MPI demo script

The MPI demo script uses `mpirun --hostfile /share/qhost ...`, writes its files directly to `/share/`, and also prints the `mpihosts` resource file pointed to by `SETUP_CLUSTER_MPIHOST_FILENAME` (usually `/job/mpihosts`).

For example:

```text
cat mpihosts
10.200.2.1 slots=26
10.200.2.2 slots=26
```

This means the cluster exposes `26` MPI slots per node. In the demo, `SETUP_CLUSTER_NB_SLOTS=26` is the number of slots per node and `QARNOT_INSTANCE_COUNT=2` is the number of nodes, so the script can explain that `26 x 2 = 52` MPI slots are available in total.

<div class="wf-code-card"
     data-url="https://cdn.jsdelivr.net/gh/qarnot/blog-samples@main/roce.base/mpi_test/run_mpi_demo.sh"
     data-filename="mpi_test/run_mpi_demo.sh"
     data-language="bash"
     data-linenumbers="true"
     data-maxheight="65vh"
     data-fontsize="13px"
     data-download="true"
     data-copy="true"></div>

## Push your image to Qarnot Container Registry

Before pushing your image, you can review:
- <a href="https://qarnot.com/documentation-tasq/pushing-container-images" target="_blank">Pushing container images to Qarnot Containers Registry</a>
- <a href="https://qarnot.com/documentation-tasq/container-stored-qarnot-container-registry" target="_blank">Using a container stored in Qarnot Container Registry in Tasq</a>

From the directory containing the `Dockerfile`, use the following commands:

> `docker login --username <your_qarnot_email> https://containers.qarnot.com`

> `docker build -t containers.qarnot.com/<registry_id>/roce-base-demo:<customer-image-tag> .`

> `docker push containers.qarnot.com/<registry_id>/roce-base-demo:<customer-image-tag>`


## Launching the test case
The minimal script below uses the `docker-cluster-roce` profile, it:
- launches a `2`-node cluster. Default nodes are 28 cores Intel Xeon, see the advanced script to use 96 cores. 
- synchronizes the local `mpi_test/` directory into the input bucket `roce-base-demo-in`
- sets up a periodic copy of the files written at the root of `/share` into `/job` and uploads them to the output bucket `roce-base-demo-out` through task snapshots.

It stops right after `submit()`, so it stays close to the shortest possible `roce_wrapper` launcher.

<div class="wf-code-card"
     data-url="https://cdn.jsdelivr.net/gh/qarnot/blog-samples@main/roce.base/run_roce_base_batch.py"
     data-filename="run_roce_base_batch.py"
     data-language="python"
     data-linenumbers="true"
     data-maxheight="65vh"
     data-fontsize="13px"
     data-download="true"
     data-copy="true"></div>

## Advanced launcher features

The advanced example below keeps the same image, input bucket, and output bucket names, but adds state monitoring, log capture, and a few commonly useful options. It also shows an optional commented `download_results` call at the end instead of forcing a local download.

<div class="wf-code-card"
     data-url="https://cdn.jsdelivr.net/gh/qarnot/blog-samples@main/roce.base/run_roce_base_advanced.py"
     data-filename="run_roce_base_advanced.py"
     data-language="python"
     data-linenumbers="true"
     data-maxheight="65vh"
     data-fontsize="13px"
     data-download="true"
     data-copy="true"></div>

This advanced script highlights:
- `/share/qhost`: the generated MPI hostfile used by the demo script
- `SETUP_CLUSTER_NB_SLOTS` and `QARNOT_INSTANCE_COUNT`: the demo uses them together to explain how many MPI slots are available per node and in the full cluster
- `mpihosts` / `SETUP_CLUSTER_MPIHOST_FILENAME`: the source resource file that lists the allocated nodes and their slot count
- `QARNOT_MPI_ARGS`: a convenient place to expose MPI options
- `USE_SIMULATION_MAXIMUM_EXECUTION_TIME` and `SIMULATION_MAXIMUM_EXECUTION_TIME`: a global timeout for the full execution lifecycle
- `SOFT_ERROR_LOGS_STR`: log-based failure detection for applications that can return `0` even after a functional failure
- `LOCAL_FILES_COPY_INTERVAL_SEC` and `LOCAL_FILES_COPY_REGEX`: periodic synchronization settings for the files you want to keep from `/share`
- `DOCKER_SSH`, `USE_VNC`, and `USE_KEEP_RUNNING_AFTER_SIMULATION`: optional debugging features when you need to inspect a live cluster

By default, the advanced sample uses the `docker-cluster-roce` profile. If you need SSH access instead, switch to `docker-cluster-roce-ssh` and set `DOCKER_SSH` with your public key. 

If you need virtual desktop access, switch to `docker-cluster-roce-vnc`, set `USE_VNC` to `true`, and set a `VNC_PASSWORD`.

## Results

Both sample scripts synchronize files from the root of `/share` to the output bucket `roce-base-demo-out`. The batch sample stops after submission, while the advanced sample can monitor the task and optionally call `download_results` once the simulation reaches the `Success` state.

When you inspect the output bucket or download its contents manually, expect files such as `mpi-demo.log`, `mpi-demo.stdout.log`, `mpi-ranks.txt`, `mpihosts.txt`, `qhost.txt`, `summary.txt`, and `post_simulation.log`.

The same files are also visible from the <a href="https://tasq.qarnot.com/tasks" target="_blank">Tasq app</a>. You can retrieve them from the Python SDK with <a href="https://doc.tasq.qarnot.com/documentation/sdk-python/api/compute/task.html#qarnot.task.Task.download_results" target="_blank">download_results</a>, or manage the bucket with S3-compatible tools such as <a href="https://qarnot.com/documentation/manage-data-dedicated-ui" target="_blank">rclone or Cyberduck</a>.

---

## Applications Available in `roce.base`

The `roce.base` image contains several useful components for building and running HPC workflows.

Examples of applications available in `/opt`:

### OpenMPI

OpenMPI is the MPI implementation used by default to run distributed programs in parallel.

Usage example:

```bash
mpirun -np 4 ./my_mpi_program
```

### IntelMPI

IntelMPI can also be used, but the default `roce.base` configuration is OpenMPI-oriented.

To use IntelMPI, the MPI configuration must be adapted through the provided variables, especially `MPI_PROVIDER`, and the options specific to the software being used must be validated.

### VNC

The image includes a VNC server that provides access to a graphical interface inside the container.

This makes it possible, in particular, to use graphical applications such as ParaView or certain pre/post-processing tools.

VNC access can be enabled with the following variable:

```bash
USE_VNC=true
```

### SSH

Nodes can be accessed via SSH if a public key is provided to the task.

The nodes are also preconfigured to communicate with each other via SSH, which is required for some MPI workflows.
