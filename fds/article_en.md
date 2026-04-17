Fire Dynamics Simulator, or FDS, is an open-source Computational Fluid Dynamics software dedicated to simulating fire and smoke propagation. It relies on a LES approach suited to low-speed flows with heat transfer and is generally used together with Smokeview for result visualization.

On Qarnot, FDS can be launched via the web interface or with Python scripts based on the SDK. In this article, we will:
- present a simple script for batch launching
- present a more detailed batch script
- and then a script to launch a task with a remote desktop

## Licensing

Since FDS is open source, there is no license setup required to run a standard case on Qarnot.

## Versions

The FDS versions presented by Qarnot are summarized in our article <a href="https://qarnot.com/en/software/fds-qarnot" target="_blank">Fire Dynamics Simulator on Qarnot Cloud</a>.

In the examples below, the scripts use `6.10.1`. If you need another version, simply adapt the `DOCKER_TAG` value in the script according to the available versions.

## Launching a task on Qarnot

There are two ways to launch a task on Qarnot:
- Via our web interface <a href="https://app.qarnot.com/my-simulations" target="_blank">HPC</a>
- Using a script with an SDK

To launch a task via the web interface, you can follow this <a href="https://app.supademo.com/demo/cmnsvu34a4669cr4jpur5ffcn?utm_source=link" target="_blank">step-by-step tutorial</a>.

<div style="position: relative; box-sizing: content-box; max-height: 80vh; max-height: 80svh; width: 100%; aspect-ratio: 1.81; padding: 40px 0 40px 0;">
  <iframe src="https://app.supademo.com/embed/cmnsvu34a4669cr4jpur5ffcn?embed_v=2&utm_source=embed" loading="lazy" title="How to start an FDS simulation on Qarnot" allow="clipboard-write" frameborder="0" webkitallowfullscreen="true" mozallowfullscreen="true" allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe>
</div>

The rest of this blog post focuses on launching with Python scripts for increased automation and speed.

## Prerequisites

Before launching a calculation with the Python SDK, a few steps are required:
- <a href="https://app.qarnot.com/register" target="_blank">Create an account</a>
- Retrieve your <a href="https://app.qarnot.com/settings/access-token" target="_blank">API authentication token</a>
- <a href="https://doc.tasq.qarnot.com/documentation/sdk-python/installation.html" target="_blank">Install the Qarnot Python SDK</a>

> **Note**: In addition to the Python SDK, Qarnot also provides SDKs for <a href="https://doc.tasq.qarnot.com/documentation/sdk-csharp/" target="_blank">C#</a> and <a href="https://doc.tasq.qarnot.com/documentation/sdk-nodejs/" target="_blank">Node.js</a>, as well as a Command Line Interface (<a href="https://doc.tasq.qarnot.com/documentation/cli/man/ManIndex.html" target="_blank">CLI</a>).

## Test case

Here is an example of how to run an FDS use case on the platform. This assumes that:

- Your use case includes a complete case folder in your working directory.
- The case contains a `.fds` file ready to be launched.

In the examples below, we use the `temple/` case.
If needed, you can directly download the example file here: <a href="https://27028395.fs1.hubspotusercontent-eu1.net/hubfs/27028395/%5BMARCOM%5D%20Blog%20site%20HPC/temple_16_MPI_PROC_bf9e47311b.fds" target="_blank">temple_16_MPI_PROC.fds</a>. This case is already partitioned for `16` MPI ranks.

Once done, your file structure should look like this:

<pre>
.
├── temple/
│   └── temple_16_MPI_PROC.fds
├── run_fds_batch.py
├── run_fds_batch_advanced.py
└── run_fds_vnc.py
</pre>

## Launching the test case

Once everything is configured, it is time to run the `run_fds_batch.py` script below. In this script, you need to:
- Replace `MY_SECRET_TOKEN` with your actual authentication token
- Select the directory you want to synchronize with your bucket
- Adjust the FDS version if needed

Once everything is ready, use the `run_fds_batch.py` script below to launch the calculation on Qarnot.

<div class="wf-code-card"
     data-url="https://cdn.jsdelivr.net/gh/qarnot/blog-samples@main/fds/run_fds_batch.py"
     data-filename="run_fds_batch.py"
     data-language="python"
     data-linenumbers="true"
     data-maxheight="65vh"
     data-fontsize="13px"
     data-download="true"
     data-copy="true"></div>

You now know how to launch an FDS batch task on Qarnot!

## Advanced batch script

The script shown below allows you to go further in choosing machine types. It includes single-node examples ranging from `8c` to `96c`.

<div class="wf-code-card"
     data-url="https://cdn.jsdelivr.net/gh/qarnot/blog-samples@main/fds/run_fds_batch_advanced.py"
     data-filename="run_fds_batch_advanced.py"
     data-language="python"
     data-linenumbers="true"
     data-maxheight="65vh"
     data-fontsize="13px"
     data-download="true"
     data-copy="true"></div>

## Launching an FDS task with a remote desktop

Here is an example of how to run an FDS use case with a remote desktop enabled on the platform.

The profile used here is `fds-vnc`, or `fds-non-cluster-vnc-ssh` to use CPUs of less than 28 cores. 

<div class="wf-code-card"
     data-url="https://cdn.jsdelivr.net/gh/qarnot/blog-samples@main/fds/run_fds_vnc.py"
     data-filename="run_fds_vnc.py"
     data-language="python"
     data-linenumbers="true"
     data-maxheight="65vh"
     data-fontsize="13px"
     data-download="true"
     data-copy="true"></div>

To launch the calculation on Qarnot, copy the code above into a Python script in your working directory. Make sure you have copied your authentication token into the script, replacing `MY_SECRET_TOKEN`.

Then you can run `python3 run_fds_vnc.py`.

Once connected, you can manually launch your case with the following command:

> `cd /share/ && mpiexec -np 16 fds temple_16_MPI_PROC.fds`

## Results

You should now have a `temple-out` folder in your local working directory after a simple batch launch, or a `temple-advanced-out` folder if you use the advanced script. The same output bucket is also available on the <a href="https://app.qarnot.com/my-simulations" target="_blank">HPC app</a> with all files generated by the simulation.

You can directly view certain log files generated by the simulation in your output bucket via the <a href="https://app.qarnot.com/my-simulations" target="_blank">HPC app</a>.

Your results will be stored in the output bucket defined in the script and can be retrieved in three ways:
- Via the web platform: download directly from the Bucket section
- As shown in the Python script: using the <a href="https://doc.tasq.qarnot.com/documentation/sdk-python/api/compute/task.html#qarnot.task.Task.download_results" target="_blank">download_results</a> function
- Or via one of the <a href="https://qarnot.com/documentation/manage-data-dedicated-ui" target="_blank">open-source S3 bucket management applications</a>

For a large number of files or more than 5GB of data, we recommend using rclone (Linux) or Cyberduck (Windows). Both are <a href="https://qarnot.com/documentation/manage-data-dedicated-ui" target="_blank">open-source S3 bucket management tools</a>.

The case also produces an `IMP_TEMPLE.smv` file that you can open with <a href="https://github.com/firemodels/smv" target="_blank">Smokeview</a> for visualization.

> `smokeview IMP_TEMPLE.smv`
