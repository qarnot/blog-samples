OpenFOAM is a widely used open-source Computational Fluid Dynamics software for simulating flows, heat transfer, and other physical phenomena. It relies on a large library of solvers and utilities, which makes it a particularly flexible environment for running CFD cases on HPC resources.

On Qarnot, OpenFOAM can be launched via the web interface or with Python scripts based on the SDK. In this article, we will:
- present a simple script for batch launching
- present a more detailed batch script
- and then a script to launch a task with SSH connectivity

## Licensing

Since OpenFOAM is open source, there is no license setup required to run a standard case on Qarnot.

## Versions

The versions of OpenFOAM available on Qarnot are listed in our <a href="https://qarnot.com/en/software/openfoam-qarnot" target="_blank">catalogue</a>.

In the examples below, the scripts use `v2412`. If you need another version, simply adapt the `DOCKER_TAG` value in the script according to the available versions.

## Launching a task on Qarnot

There are two ways to launch a task on Qarnot:
- Via our web interface <a href="https://app.qarnot.com/my-simulations" target="_blank">HPC</a>
- Using a script with an SDK

To launch an OpenFOAM task from our web interface, you can follow this <a href="https://app.supademo.com/demo/cmc33707602ae090i7h3chpy5" target="_blank">step-by-step tutorial</a>.

<div style="position: relative; box-sizing: content-box; max-height: 80vh; max-height: 80svh; width: 100%; aspect-ratio: 1.81; padding: 40px 0 40px 0;">
  <iframe src="https://app.supademo.com/embed/cmc33707602ae090i7h3chpy5?embed_v=2&utm_source=embed" loading="lazy" title="How to start an OpenFOAM simulation on Qarnot" allow="clipboard-write" frameborder="0" webkitallowfullscreen="true" mozallowfullscreen="true" allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe>
</div>

To monitor a task on the HPC platform, you can also follow this <a href="https://app.supademo.com/demo/cmawil0f96jybho3r4h0ki18n" target="_blank">dedicated tutorial</a>.

<div style="position: relative; box-sizing: content-box; max-height: 80vh; max-height: 80svh; width: 100%; aspect-ratio: 1.81; padding: 40px 0 40px 0;">
  <iframe src="https://app.supademo.com/embed/cmawil0f96jybho3r4h0ki18n?embed_v=2&utm_source=embed" loading="lazy" title="How to monitor an OpenFOAM task on Qarnot" allow="clipboard-write" frameborder="0" webkitallowfullscreen="true" mozallowfullscreen="true" allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe>
</div>

The rest of this blog post focuses on launching with Python scripts for increased automation and speed.

## Prerequisites

Before launching a calculation with the Python SDK, a few steps are required:
- <a href="https://app.qarnot.com/register" target="_blank">Create an account</a>
- Retrieve your <a href="https://app.qarnot.com/settings/access-token" target="_blank">API authentication token</a>
- <a href="https://doc.tasq.qarnot.com/documentation/sdk-python/installation.html" target="_blank">Install the Qarnot Python SDK</a>
- Know your Qarnot profile, for example `openfoam` for batch mode and `openfoam-ssh` for SSH access

> **Note**: In addition to the Python SDK, Qarnot also provides SDKs for <a href="https://doc.tasq.qarnot.com/documentation/sdk-csharp/" target="_blank">C#</a> and <a href="https://doc.tasq.qarnot.com/documentation/sdk-nodejs/" target="_blank">Node.js</a>, as well as a Command Line Interface (<a href="https://doc.tasq.qarnot.com/documentation/cli/man/ManIndex.html" target="_blank">CLI</a>).

## Test case

Here is an example of how to run an OpenFOAM use case on the platform. This assumes that:

- Your use case includes a complete case directory in your working directory.
- The case contains an `Allrun` script used as the entry point for launching.

In the examples below, we use the `motorbike/` case.
If needed, you can directly download the example here: <a href="https://communication.qarnot.com/hubfs/%5BMARCOM%5D%20Blog%20site%20HPC/motorbike.zip"target="_blank">motorbike.zip</a>

Once done, your file structure should look like this:

<pre>
.
├── motorbike/
│   ├── Allrun
│   ├── Allclean
│   ├── 0.orig/
│   ├── constant/
│   └── system/
├── run_openfoam_batch.py
├── run_openfoam_batch_advanced.py
└── run_openfoam_ssh.py
</pre>

## Launching the test case

Once everything is configured, it is time to run the `run_openfoam_batch.py` script below. In this script, you need to:
- Replace `MY_SECRET_TOKEN` with your actual authentication token
- Select the directory you want to synchronize with your bucket
- Adjust the OpenFOAM version if needed

Once everything is ready, use the `run_openfoam_batch.py` script below to launch the calculation on Qarnot.

<div class="wf-code-card"
     data-url="https://cdn.jsdelivr.net/gh/qarnot/blog-samples@main/openfoam/run_openfoam_batch.py"
     data-filename="run_openfoam_batch.py"
     data-language="python"
     data-linenumbers="true"
     data-maxheight="65vh"
     data-fontsize="13px"
     data-download="true"
     data-copy="true"></div>

You now know how to launch an OpenFOAM batch task on Qarnot!

## Advanced batch script

The script below allows you to explore more advanced topologies, especially a `96c` AMD node or a `2x28c` multi-node configuration.

<div class="wf-code-card"
     data-url="https://cdn.jsdelivr.net/gh/qarnot/blog-samples@main/openfoam/run_openfoam_batch_advanced.py"
     data-filename="run_openfoam_batch_advanced.py"
     data-language="python"
     data-linenumbers="true"
     data-maxheight="65vh"
     data-fontsize="13px"
     data-download="true"
     data-copy="true"></div>

## Launching an OpenFOAM task with SSH connectivity enabled

Here is an example of how to run an OpenFOAM use case with SSH enabled on the platform. You will need an SSH public key (you can create one following this <a href="https://qarnot.com/documentation/use-ssh" target="_blank">tutorial</a>).

<div class="wf-code-card"
     data-url="https://cdn.jsdelivr.net/gh/qarnot/blog-samples@main/openfoam/run_openfoam_ssh.py"
     data-filename="run_openfoam_ssh.py"
     data-language="python"
     data-linenumbers="true"
     data-maxheight="65vh"
     data-fontsize="13px"
     data-download="true"
     data-copy="true"></div>

To launch the calculation on Qarnot, copy the code above into a Python script in your working directory. Make sure you have:

- Copied your authentication token into the script, replacing `MY_SECRET_TOKEN`
- Copied your SSH public key into `DOCKER_SSH`

Then you can run `python3 run_openfoam_ssh.py`.

> **Note:** the profile used must be your dedicated SSH profile, for example `openfoam-ssh`.

Once connected to the master node, you can manually launch your case with the following command:

> `cd /share/motorbike && bash Allrun`

## Results

You should now have a `motorbike-out` folder in your local working directory after a simple batch launch, or a `motorbike-advanced-out` folder if you use the advanced script. The same output bucket is also available on the <a href="https://app.qarnot.com/my-simulations" target="_blank">HPC app</a> with all files generated by the simulation.

You can directly view certain images and log files generated by the simulation in your output bucket via the <a href="https://app.qarnot.com/my-simulations" target="_blank">HPC app</a>.

Your results will be stored in the output bucket defined in the script and can be retrieved in three ways:
- Via the web platform: download directly from the Bucket section
- As shown in the Python script: using the <a href="https://doc.tasq.qarnot.com/documentation/sdk-python/api/compute/task.html#qarnot.task.Task.download_results" target="_blank">download_results</a> function
- Or via one of the <a href="https://qarnot.com/documentation/manage-data-dedicated-ui" target="_blank">open-source S3 bucket management applications</a>

For a large number of files or more than 5GB of data, we recommend using rclone (Linux) or Cyberduck (Windows). Both are <a href="https://qarnot.com/documentation/manage-data-dedicated-ui" target="_blank">open-source S3 management tools</a>.
