STAR-CCM+ est un logiciel de simulation multiphysique largement utilisé pour les études de mécanique des fluides numérique, de transfert thermique et, plus largement, pour l’analyse de systèmes complexes en ingénierie. Il permet d’exécuter des calculs robustes aussi bien en batch qu’en mode interactif sur des ressources de calcul haute performance.

Sur Qarnot, STAR-CCM+ peut être lancé via l’interface web ou à l’aide de scripts Python basés sur le SDK. Dans cet article, nous allons :
- présenter un script simple pour un lancement en batch
- présenter un script plus détaillé en batch
- puis un script pour lancer une tâche avec connexion SSH

## Licence

Afin de lancer une simulation STAR-CCM+ sur Qarnot, vous devez accorder à Qarnot l’accès à votre licence. Pour plus de détails, veuillez contacter notre équipe à l’adresse <a href="mailto:support-compute@qarnot-computing.com" target="_blank">support-compute@qarnot-computing.com</a>.

À partir de ce point, nous supposerons que votre configuration de licence avec nous est déjà complète.

## Versions

Les versions de STAR-CCM+ disponibles sur Qarnot sont présentées dans notre <a href="https://qarnot.com/logiciels/starccm-qarnot" target="_blank">catalogue</a>.

Si une autre version vous intéresse, veuillez nous envoyer un e-mail à <a href="mailto:support-compute@qarnot-computing.com" target="_blank">support-compute@qarnot-computing.com</a>.

## Lancer une tâche sur Qarnot

Pour lancer une tâche sur Qarnot, il existe deux manières :
- Via notre interface web <a href="https://app.qarnot.com/my-simulations" target="_blank">HPC</a>
- À l’aide d’un script, en utilisant un SDK

Pour lancer une tâche depuis notre interface web, vous pouvez suivre ce <a href="https://app.supademo.com/demo/cmdfq02do1rg46n9n60b4xcmt?utm_source=link" target="_blank">tutoriel pas à pas</a>.

<div style="position: relative; box-sizing: content-box; max-height: 80vh; max-height: 80svh; width: 100%; aspect-ratio: 1.81; padding: 40px 0 40px 0;">
  <iframe src="https://app.supademo.com/embed/cmdfq02do1rg46n9n60b4xcmt?embed_v=2&utm_source=embed" loading="lazy" title="How to start a STAR-CCM+ simulation on Qarnot" allow="clipboard-write" frameborder="0" webkitallowfullscreen="true" mozallowfullscreen="true" allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe>
</div>

Si vous souhaitez plutôt visualiser votre session avec un remote desktop, vous pouvez également consulter ce <a href="https://app.supademo.com/demo/cmeu0wtk95zglv9kqbysic0ix?utm_source=link" target="_blank">tutoriel dédié</a>.

<div style="position: relative; box-sizing: content-box; max-height: 80vh; max-height: 80svh; width: 100%; aspect-ratio: 1.81; padding: 40px 0 40px 0;">
  <iframe src="https://app.supademo.com/embed/cmeu0wtk95zglv9kqbysic0ix?embed_v=2&utm_source=embed" loading="lazy" title="How to visualize a STAR-CCM+ simulation with remote desktop on Qarnot" allow="clipboard-write" frameborder="0" webkitallowfullscreen="true" mozallowfullscreen="true" allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe>
</div>

La suite de cet article concerne le lancement grâce à des scripts Python, pour toujours plus d’automatisation et de rapidité.

## Prérequis

Avant de lancer un calcul avec le SDK Python, quelques étapes sont nécessaires :
- <a href="https://app.qarnot.com/register" target="_blank">Créer un compte</a>
- Récupérer votre <a href="https://app.qarnot.com/settings/access-token" target="_blank">jeton d’authentification API</a>
- <a href="https://doc.tasq.qarnot.com/documentation/sdk-python/installation.html" target="_blank">Installer le SDK Python de Qarnot</a>
- Connaître votre profil Qarnot, par exemple `starccm-qarnot` pour le batch et `starccm-qarnot-ssh` pour un accès SSH

> **Note** : en plus du SDK Python, Qarnot propose également des SDKs pour <a href="https://doc.tasq.qarnot.com/documentation/sdk-csharp/" target="_blank">C#</a> et <a href="https://doc.tasq.qarnot.com/documentation/sdk-nodejs/" target="_blank">Node.js</a>, ainsi qu'une ligne de commande (<a href="https://doc.tasq.qarnot.com/documentation/cli/man/ManIndex.html" target="_blank">CLI</a>).

## Cas test

Voici un exemple de la façon d’exécuter un cas d’usage STAR-CCM+ sur la plateforme. Cela suppose que :

- Vous avez accès à une licence.
- Votre cas d’usage inclut un fichier `.sim` dans un dossier de votre répertoire de travail.

Dans les exemples ci-dessous, nous utilisons le fichier `cylindre_complet_extrusion_both_demi_DP_reconstruit_init.sim` placé dans un répertoire `cylindre/`.
Si nécessaire, vous pouvez télécharger directement le fichier de l’exemple : <a href="https://communication.qarnot.com/hubfs/%5BMARCOM%5D%20Blog%20site%20HPC/cylindre_complet_extrusion_both_demi_DP_reconstruit_init_c4056f43d7.sim" target="_blank">cylindre_complet_extrusion_both_demi_DP_reconstruit_init.sim</a>

Une fois cela fait, la structure de vos fichiers devrait ressembler à ceci :

<pre>
.
├── cylindre/
│   └── cylindre_complet_extrusion_both_demi_DP_reconstruit_init.sim
├── run_starccm_batch.py
├── run_starccm_batch_advanced.py
└── run_starccm_ssh.py
</pre>

## Lancer le cas test

Une fois que tout est configuré, il est temps d’exécuter le script `run_starccm_batch.py` ci-dessous. Dans ce script, il faut :
- Remplacer `MY_SECRET_TOKEN` par votre jeton d’authentification réel
- Sélectionner le répertoire que vous souhaitez synchroniser avec votre bucket
- Adapter la version de STAR-CCM+ si nécessaire

Une fois que tout est prêt, utilisez le script `run_starccm_batch.py` ci-dessous pour lancer le calcul sur Qarnot.

<div class="wf-code-card"
     data-url="https://cdn.jsdelivr.net/gh/qarnot/blog-samples@main/starccm/run_starccm_batch.py"
     data-filename="run_starccm_batch.py"
     data-language="python"
     data-linenumbers="true"
     data-maxheight="65vh"
     data-fontsize="13px"
     data-download="true"
     data-copy="true"></div>

Vous savez désormais lancer une tâche STAR-CCM+ en batch sur Qarnot.

## Script batch avancé

Le script présenté ci-dessous permet d’explorer des topologies plus avancées, notamment un nœud AMD `96c` ou une configuration `2x28c` en multi-nœud.

<div class="wf-code-card"
     data-url="https://cdn.jsdelivr.net/gh/qarnot/blog-samples@main/starccm/run_starccm_batch_advanced.py"
     data-filename="run_starccm_batch_advanced.py"
     data-language="python"
     data-linenumbers="true"
     data-maxheight="65vh"
     data-fontsize="13px"
     data-download="true"
     data-copy="true"></div>

## Lancer une tâche STAR-CCM+ avec la connectivité SSH activée

Voici un exemple de la façon d’exécuter un cas d’usage STAR-CCM+ avec SSH activé sur la plateforme. Vous aurez besoin d’une clé publique SSH (vous pouvez en créer une en suivant ce <a href="https://qarnot.com/documentation/use-ssh" target="_blank">tutoriel</a>).

<div class="wf-code-card"
     data-url="https://cdn.jsdelivr.net/gh/qarnot/blog-samples@main/starccm/run_starccm_ssh.py"
     data-filename="run_starccm_ssh.py"
     data-language="python"
     data-linenumbers="true"
     data-maxheight="65vh"
     data-fontsize="13px"
     data-download="true"
     data-copy="true"></div>

Pour lancer le calcul sur Qarnot, copiez le code ci-dessus dans un script Python dans votre répertoire de travail. Assurez-vous d’avoir :

- Copié votre jeton d’authentification dans le script, à la place de `MY_SECRET_TOKEN`
- Copié votre clé publique SSH dans `DOCKER_SSH`

Ensuite, vous pouvez exécuter `python3 run_starccm_ssh.py`.

> **Note :** le profil utilisé doit être votre profil SSH dédié, par exemple `starccm-qarnot-ssh`.

Une fois connecté au nœud maître, vous pouvez lancer une simulation STAR-CCM+ sur votre cluster avec l’une des commandes suivantes :

> `starccm+ -power -batch run cylindre_complet_extrusion_both_demi_DP_reconstruit_init.sim`

> `starccm+ -power -batch -mpi openmpi -mpiflags "--mca btl ^openib,tcp --mca pml ucx --mca osc ucx" -machinefile /job/mpihosts run cylindre_complet_extrusion_both_demi_DP_reconstruit_init.sim`

Où `-mpi openmpi`, `-mpiflags ...` et `-machinefile /job/mpihosts` sont les paramètres nécessaires pour une simulation multi-nœud.

## Résultats

Vous devriez maintenant avoir un dossier `cylindre-out` dans votre répertoire de travail sur votre ordinateur après un lancement batch simple, ou `cylindre-advanced-out` si vous utilisez le script avancé. Le même bucket de sortie est également disponible sur l’app <a href="https://app.qarnot.com/my-simulations" target="_blank">HPC</a> avec tous les fichiers générés par la simulation.

Vous pouvez visualiser directement sur l’app <a href="https://app.qarnot.com/my-simulations" target="_blank">HPC</a> certaines images et certains fichiers de logs générés par la simulation qui se trouvent dans votre bucket de sortie.

Vos résultats seront stockés dans le bucket de sortie défini dans le script et peuvent être récupérés de trois manières :
- Via la plateforme web : téléchargement direct depuis la section Bucket
- Comme dans le script Python : à l’aide de la fonction <a href="https://doc.tasq.qarnot.com/documentation/sdk-python/api/compute/task.html#qarnot.task.Task.download_results" target="_blank">download_results</a>
- Ou via l'une des <a href="https://qarnot.com/documentation/manage-data-dedicated-ui" target="_blank">applications opensource de gestion de bucket S3</a>

Pour une grande quantité de fichiers ou plus de 5gb de données, il est conseillé d’utiliser rclone (linux) ou cyberduck (windows). Ce sont deux <a href="https://qarnot.com/documentation/manage-data-dedicated-ui" target="_blank">applications opensource de gestion de bucket S3</a>.
