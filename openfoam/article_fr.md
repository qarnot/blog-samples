OpenFOAM est un logiciel open source de mécanique des fluides numérique largement utilisé pour simuler des écoulements, des transferts thermiques et d’autres phénomènes physiques. Il s’appuie sur une grande bibliothèque de solveurs et d’utilitaires, ce qui en fait un environnement particulièrement flexible pour exécuter des cas CFD sur des ressources HPC.

Sur Qarnot, OpenFOAM peut être lancé via l’interface web ou à l’aide de scripts Python basés sur le SDK. Dans cet article, nous allons :
- présenter un script simple pour un lancement en batch
- présenter un script plus détaillé en batch
- puis un script pour lancer une tâche avec connexion SSH

## Licence

OpenFOAM étant open source, il n’y a pas de gestion de licence à mettre en place pour exécuter un cas standard sur Qarnot.

## Versions

Les versions d’OpenFOAM disponibles sur Qarnot sont présentées dans notre <a href="https://qarnot.com/logiciels/openfoam-qarnot" target="_blank">catalogue</a>.

Dans les exemples ci-dessous, les scripts utilisent `v2412`. Si une autre version vous intéresse, il suffit d’adapter la valeur `DOCKER_TAG` dans le script en fonction des versions disponibles.

## Lancer une tâche sur Qarnot

Pour lancer une tâche sur Qarnot, il existe deux manières :
- Via notre interface web <a href="https://app.qarnot.com/my-simulations" target="_blank">HPC</a>
- À l’aide d’un script, en utilisant un SDK

Pour lancer une tâche OpenFOAM depuis notre interface web, vous pouvez suivre ce <a href="https://app.supademo.com/demo/cmc33707602ae090i7h3chpy5" target="_blank">tutoriel pas à pas</a>.

<div style="position: relative; box-sizing: content-box; max-height: 80vh; max-height: 80svh; width: 100%; aspect-ratio: 1.81; padding: 40px 0 40px 0;">
  <iframe src="https://app.supademo.com/embed/cmc33707602ae090i7h3chpy5?embed_v=2&utm_source=embed" loading="lazy" title="How to start an OpenFOAM simulation on Qarnot" allow="clipboard-write" frameborder="0" webkitallowfullscreen="true" mozallowfullscreen="true" allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe>
</div>

Pour monitorer une tâche sur la plateforme HPC, vous pouvez également consulter ce <a href="https://app.supademo.com/demo/cmawil0f96jybho3r4h0ki18n" target="_blank">tutoriel dédié</a>.

<div style="position: relative; box-sizing: content-box; max-height: 80vh; max-height: 80svh; width: 100%; aspect-ratio: 1.81; padding: 40px 0 40px 0;">
  <iframe src="https://app.supademo.com/embed/cmawil0f96jybho3r4h0ki18n?embed_v=2&utm_source=embed" loading="lazy" title="How to monitor an OpenFOAM task on Qarnot" allow="clipboard-write" frameborder="0" webkitallowfullscreen="true" mozallowfullscreen="true" allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe>
</div>

La suite de cet article concerne le lancement grâce à des scripts Python, pour toujours plus d’automatisation et de rapidité.

## Prérequis

Avant de lancer un calcul avec le SDK Python, quelques étapes sont nécessaires :
- <a href="https://app.qarnot.com/register" target="_blank">Créer un compte</a>
- Récupérer votre <a href="https://app.qarnot.com/settings/access-token" target="_blank">jeton d’authentification API</a>
- <a href="https://doc.tasq.qarnot.com/documentation/sdk-python/installation.html" target="_blank">Installer le SDK Python de Qarnot</a>
- Connaître votre profil Qarnot, par exemple `openfoam` pour le batch et `openfoam-ssh` pour un accès SSH

> **Note** : en plus du SDK Python, Qarnot propose également des SDKs pour <a href="https://doc.tasq.qarnot.com/documentation/sdk-csharp/" target="_blank">C#</a> et <a href="https://doc.tasq.qarnot.com/documentation/sdk-nodejs/" target="_blank">Node.js</a>, ainsi qu'une ligne de commande (<a href="https://doc.tasq.qarnot.com/documentation/cli/man/ManIndex.html" target="_blank">CLI</a>).

## Cas test

Voici un exemple de la façon d’exécuter un cas d’usage OpenFOAM sur la plateforme. Cela suppose que :

- Votre cas d’usage inclut un dossier de calcul complet dans votre répertoire de travail.
- Le cas contient un script `Allrun` servant de point d’entrée au lancement.

Dans les exemples ci-dessous, nous utilisons le cas `motorbike/`.
Si nécessaire, vous pouvez télécharger directement l’exemple : <a href="https://communication.qarnot.com/hubfs/%5BMARCOM%5D%20Blog%20site%20HPC/motorbike.zip"target="_blank">motorbike.zip</a>

Une fois cela fait, la structure de vos fichiers devrait ressembler à ceci :

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

## Lancer le cas test

Une fois que tout est configuré, il est temps d’exécuter le script `run_openfoam_batch.py` ci-dessous. Dans ce script, il faut :
- Remplacer `MY_SECRET_TOKEN` par votre jeton d’authentification réel
- Sélectionner le répertoire que vous souhaitez synchroniser avec votre bucket
- Adapter la version d’OpenFOAM si nécessaire

Une fois que tout est prêt, utilisez le script `run_openfoam_batch.py` ci-dessous pour lancer le calcul sur Qarnot.

<div class="wf-code-card"
     data-url="https://cdn.jsdelivr.net/gh/qarnot/blog-samples@main/openfoam/run_openfoam_batch.py"
     data-filename="run_openfoam_batch.py"
     data-language="python"
     data-linenumbers="true"
     data-maxheight="65vh"
     data-fontsize="13px"
     data-download="true"
     data-copy="true"></div>

Vous savez désormais lancer une tâche OpenFOAM en batch sur Qarnot.

## Script batch avancé

Le script présenté ci-dessous permet d’explorer des topologies plus avancées, notamment un nœud AMD `96c` ou une configuration `2x28c` en multi-nœud.

<div class="wf-code-card"
     data-url="https://cdn.jsdelivr.net/gh/qarnot/blog-samples@main/openfoam/run_openfoam_batch_advanced.py"
     data-filename="run_openfoam_batch_advanced.py"
     data-language="python"
     data-linenumbers="true"
     data-maxheight="65vh"
     data-fontsize="13px"
     data-download="true"
     data-copy="true"></div>

## Lancer une tâche OpenFOAM avec la connectivité SSH activée

Voici un exemple de la façon d’exécuter un cas d’usage OpenFOAM avec SSH activé sur la plateforme. Vous aurez besoin d’une clé publique SSH (vous pouvez en créer une en suivant ce <a href="https://qarnot.com/documentation/use-ssh" target="_blank">tutoriel</a>).

<div class="wf-code-card"
     data-url="https://cdn.jsdelivr.net/gh/qarnot/blog-samples@main/openfoam/run_openfoam_ssh.py"
     data-filename="run_openfoam_ssh.py"
     data-language="python"
     data-linenumbers="true"
     data-maxheight="65vh"
     data-fontsize="13px"
     data-download="true"
     data-copy="true"></div>

Pour lancer le calcul sur Qarnot, copiez le code ci-dessus dans un script Python dans votre répertoire de travail. Assurez-vous d’avoir :

- Copié votre jeton d’authentification dans le script, à la place de `MY_SECRET_TOKEN`
- Copié votre clé publique SSH dans `DOCKER_SSH`

Ensuite, vous pouvez exécuter `python3 run_openfoam_ssh.py`.

> **Note :** le profil utilisé doit être votre profil SSH dédié, par exemple `openfoam-ssh`.

Une fois connecté au nœud maître, vous pouvez lancer manuellement votre cas avec la commande suivante :

> `cd /share/motorbike && bash Allrun`

## Résultats

Vous devriez maintenant avoir un dossier `motorbike-out` dans votre répertoire de travail sur votre ordinateur après un lancement batch simple, ou `motorbike-advanced-out` si vous utilisez le script avancé. Le même bucket de sortie est également disponible sur l’app <a href="https://app.qarnot.com/my-simulations" target="_blank">HPC</a> avec tous les fichiers générés par la simulation.

Vous pouvez visualiser directement sur l’app <a href="https://app.qarnot.com/my-simulations" target="_blank">HPC</a> certaines images et certains fichiers de logs générés par la simulation qui se trouvent dans votre bucket de sortie.

Vos résultats seront stockés dans le bucket de sortie défini dans le script et peuvent être récupérés de trois manières :
- Via la plateforme web : téléchargement direct depuis la section Bucket
- Comme dans le script Python : à l’aide de la fonction <a href="https://doc.tasq.qarnot.com/documentation/sdk-python/api/compute/task.html#qarnot.task.Task.download_results" target="_blank">download_results</a>
- Ou via l'une des <a href="https://qarnot.com/documentation/manage-data-dedicated-ui" target="_blank">applications opensource de gestion de bucket S3</a>

Pour une grande quantité de fichiers ou plus de 5gb de données, il est conseillé d’utiliser rclone (linux) ou cyberduck (windows). Ce sont deux <a href="https://qarnot.com/documentation/manage-data-dedicated-ui" target="_blank">applications opensource de gestion de bucket S3</a>.
