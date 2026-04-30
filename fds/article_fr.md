Fire Dynamics Simulator, ou FDS, est un logiciel open source de mécanique des fluides numérique dédié à la simulation de la propagation du feu et de la fumée. Il s’appuie sur une approche LES adaptée aux écoulements à faible vitesse avec transport thermique et il est généralement utilisé avec Smokeview pour la visualisation des résultats.

Sur Qarnot, FDS peut être lancé via l’interface web ou à l’aide de scripts Python basés sur le SDK. Dans cet article, nous allons :
- présenter un script simple pour un lancement en batch
- présenter un script plus détaillé en batch
- puis un script pour lancer une tâche avec un bureau à distance

## Licence

FDS étant open source, il n’y a pas de gestion de licence à mettre en place pour exécuter un cas standard sur Qarnot.

## Versions

Les versions FDS présentées par Qarnot sont récapitulées dans notre article <a href="https://qarnot.com/logiciels/fds-qarnot" target="_blank">Fire Dynamics Simulator sur Qarnot Cloud</a>.

Dans les exemples ci-dessous, les scripts utilisent `6.10.1`. Si une autre version vous intéresse, il suffit d’adapter la valeur `DOCKER_TAG` dans le script en fonction des versions disponibles.

## Lancer une tâche sur Qarnot

Pour lancer une tâche sur Qarnot, il existe deux manières :
- Via notre interface web <a href="https://app.qarnot.com/my-simulations" target="_blank">HPC</a>
- À l’aide d’un script, en utilisant un SDK

Pour lancer une tâche depuis notre interface web, vous pouvez suivre ce <a href="https://app.supademo.com/demo/cmnsvu34a4669cr4jpur5ffcn?preview=true&step=1" target="_blank">tutoriel pas à pas</a>.

<div style="position: relative; box-sizing: content-box; max-height: 80vh; max-height: 80svh; width: 100%; aspect-ratio: 1.81; padding: 40px 0 40px 0;">
  <iframe src="https://app.supademo.com/embed/cmnsvu34a4669cr4jpur5ffcn?embed_v=2&utm_source=embed" loading="lazy" title="How to start an FDS simulation on Qarnot" allow="clipboard-write" frameborder="0" webkitallowfullscreen="true" mozallowfullscreen="true" allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe>
</div>

La suite de cet article concerne le lancement grâce à des scripts Python, pour toujours plus d’automatisation et de rapidité.

## Prérequis

Avant de lancer un calcul avec le SDK Python, quelques étapes sont nécessaires :
- <a href="https://app.qarnot.com/register" target="_blank">Créer un compte</a>
- Récupérer votre <a href="https://app.qarnot.com/settings/access-token" target="_blank">jeton d’authentification API</a>
- <a href="https://doc.tasq.qarnot.com/documentation/sdk-python/installation.html" target="_blank">Installer le SDK Python de Qarnot</a>

> **Note :** en plus du SDK Python, Qarnot propose également des SDKs pour <a href="https://doc.tasq.qarnot.com/documentation/sdk-csharp/" target="_blank">C#</a> et <a href="https://doc.tasq.qarnot.com/documentation/sdk-nodejs/" target="_blank">Node.js</a>, ainsi qu'une ligne de commande (<a href="https://doc.tasq.qarnot.com/documentation/cli/man/ManIndex.html" target="_blank">CLI</a>).

## Cas test

Voici un exemple de la façon d’exécuter un cas d’usage FDS sur la plateforme. Cela suppose que :

- Votre cas d’usage inclut un dossier de calcul complet dans votre répertoire de travail.
- Le cas contient un fichier `.fds` prêt à être lancé.

Dans les exemples ci-dessous, nous utilisons le cas `temple/`.
Si nécessaire, vous pouvez télécharger directement le fichier de l’exemple : <a href="https://27028395.fs1.hubspotusercontent-eu1.net/hubfs/27028395/%5BMARCOM%5D%20Blog%20site%20HPC/temple_16_MPI_PROC_bf9e47311b.fds" target="_blank">temple_16_MPI_PROC.fds</a>. Ce cas est déjà découpé pour `16` rangs MPI.

Une fois cela fait, la structure de vos fichiers devrait ressembler à ceci :

<pre>
.
├── temple/
│   └── temple_16_MPI_PROC.fds
├── run_fds_batch.py
├── run_fds_batch_advanced.py
└── run_fds_vnc.py
</pre>

## Lancer le cas test

Une fois que tout est configuré, il est temps d’exécuter le script `run_fds_batch.py` ci-dessous. Dans ce script, il faut :
- Remplacer `MY_SECRET_TOKEN` par votre jeton d’authentification réel
- Sélectionner le répertoire que vous souhaitez synchroniser avec votre bucket
- Adapter la version de FDS si nécessaire

Une fois que tout est prêt, utilisez le script `run_fds_batch.py` ci-dessous pour lancer le calcul sur Qarnot.

<div class="wf-code-card"
     data-url="https://cdn.jsdelivr.net/gh/qarnot/blog-samples@main/fds/run_fds_batch.py"
     data-filename="run_fds_batch.py"
     data-language="python"
     data-linenumbers="true"
     data-maxheight="65vh"
     data-fontsize="13px"
     data-download="true"
     data-copy="true"></div>

Vous savez désormais lancer une tâche FDS en batch sur Qarnot.

## Script batch avancé

Le script présenté ci-dessous permet d’aller plus loin sur le choix des machines. Il documente des exemples mono noeud allant de `8c` à `96c`

<div class="wf-code-card"
     data-url="https://cdn.jsdelivr.net/gh/qarnot/blog-samples@main/fds/run_fds_batch_advanced.py"
     data-filename="run_fds_batch_advanced.py"
     data-language="python"
     data-linenumbers="true"
     data-maxheight="65vh"
     data-fontsize="13px"
     data-download="true"
     data-copy="true"></div>

## Lancer une tâche FDS avec un bureau à distance

Voici un exemple de la façon d’exécuter un cas d’usage FDS avec un bureau à distance d'activé sur la plateforme.

Le profil utilisé ici est `fds-vnc` ou `fds-non-cluster-vnc-ssh` pour accéder à des CPUs de moins de 28 cœurs. 

<div class="wf-code-card"
     data-url="https://cdn.jsdelivr.net/gh/qarnot/blog-samples@main/fds/run_fds_vnc.py"
     data-filename="run_fds_vnc.py"
     data-language="python"
     data-linenumbers="true"
     data-maxheight="65vh"
     data-fontsize="13px"
     data-download="true"
     data-copy="true"></div>

Pour lancer le calcul sur Qarnot, copiez le code ci-dessus dans un script Python dans votre répertoire de travail. Assurez-vous d’avoir copié votre jeton d’authentification dans le script, à la place de `MY_SECRET_TOKEN`.

Ensuite, vous pouvez exécuter `python3 run_fds_vnc.py`.

Une fois connecté, vous pouvez lancer manuellement votre cas avec la commande suivante :

> `cd /share/ && mpiexec -np 16 fds temple_16_MPI_PROC.fds`

## Résultats

Vous devriez maintenant avoir un dossier `temple-out` dans votre répertoire de travail sur votre ordinateur après un lancement batch simple, ou `temple-advanced-out` si vous utilisez le script avancé. Le même bucket de sortie est également disponible sur l’app <a href="https://app.qarnot.com/my-simulations" target="_blank">HPC</a> avec tous les fichiers générés par la simulation.

Vous pouvez visualiser directement sur l’app <a href="https://app.qarnot.com/my-simulations" target="_blank">HPC</a> certains fichiers de logs générés par la simulation qui se trouvent dans votre bucket de sortie.

Vos résultats seront stockés dans le bucket de sortie défini dans le script et peuvent être récupérés de trois manières :
- Via la plateforme web : téléchargement direct depuis la section Bucket
- Comme dans le script Python : à l’aide de la fonction <a href="https://doc.tasq.qarnot.com/documentation/sdk-python/api/compute/task.html#qarnot.task.Task.download_results" target="_blank">download_results</a>
- Ou via l'une des <a href="https://qarnot.com/documentation/manage-data-dedicated-ui" target="_blank">applications opensource de gestion de bucket S3</a>

Pour une grande quantité de fichiers ou plus de 5gb de données, il est conseillé d’utiliser rclone (Linux) ou Cyberduck (Windows). Ce sont deux <a href="https://qarnot.com/documentation/manage-data-dedicated-ui" target="_blank">applications open source de gestion de bucket S3</a>.

Le cas produit également un fichier `IMP_TEMPLE.smv` que vous pouvez ouvrir avec <a href="https://github.com/firemodels/smv" target="_blank">Smokeview</a> pour la visualisation.

> `smokeview IMP_TEMPLE.smv`
