# Blog Samples

This repository contains code samples used in articles published on the [Qarnot blog](https://qarnot.com/blog).

Each folder is associated with a blog article to make it easier to follow along and understand the use cases.


## Repository Structure

Under each `software/` directory, you will generally find the following scripts:

1. `run_{software}.py`  
   Basic task launching example.

2. `run_{software}_batch.py`  
   Example to run tasks in **batch mode**.

3. `run_{software}_ssh.py`  
   Example to run a task in **SSH mode**.

All scripts are launched using the Qarnot **Python SDK**. For more detailed options and advanced usage, refer to the Python SDK documentation:
- **Python SDK**  
  https://doc.tasq.qarnot.com/documentation/sdk-python/


## Other Available SDKs and Tools

Qarnot also provides SDKs and tools in other languages:

- **C# SDK**  
  https://doc.tasq.qarnot.com/documentation/sdk-csharp/

- **Node.js SDK**  
  https://doc.tasq.qarnot.com/documentation/sdk-nodejs/

- **CLI (Command Line Interface)**  
  https://doc.tasq.qarnot.com/documentation/cli/man/ManIndex.html



<div class="wf-code-card"
     data-url="https://cdn.jsdelivr.net/gh/qarnot/blog-samples@main/altair/run_altair.py"
     data-filename="run_altair.py"
     data-language="python"
     data-linenumbers="true"
     data-maxheight="65vh"
     data-fontsize="13px"
     data-download="true"
     data-copy="true"></div>


<iframe
  class="supademo-iframe"
  src="https://app.supademo.com/embed/cmi31rhyd1tpfqnb9259mrtp8?embed_v=2&utm_source=embed"
  loading="lazy"
  title="[Tasq] Altair Hyperworks suite"
  allow="clipboard-write"
  frameborder="0"
  webkitallowfullscreen="true"
  mozallowfullscreen="true"
  allowfullscreen
></iframe>


<div style="position: relative; box-sizing: content-box; max-height: 80vh; max-height: 80svh; width: 100%; aspect-ratio: 1.99; padding: 40px 0 40px 0;">
  <iframe src="https://app.supademo.com/embed/cmjitxqs3377c3zz2qabr05xk?embed_v=2&utm_source=embed" loading="lazy" title="Configure and Launch Code_Aster Simulations on Qarnot" allow="clipboard-write" frameborder="0" webkitallowfullscreen="true" mozallowfullscreen="true" allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe>
</div>