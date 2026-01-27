Ansys Fluent est un puissant logiciel de mécanique des fluides numérique (CFD) qui simule l'écoulement des fluides, le transfert de chaleur et d'autres phénomènes connexes. Il est largement utilisé dans divers secteurs, notamment l'aérospatial, l'automobile, l'énergie et l'ingénierie environnementale.

Les chercheurs, ingénieurs et concepteurs s'appuient sur Fluent pour analyser le comportement complexe des fluides, optimiser les conceptions et améliorer les performances. Le logiciel utilise des méthodes numériques pour résoudre les équations aux dérivées partielles qui régissent l'écoulement des fluides, fournissant des prédictions et des analyses précises pour des applications réelles.

## Licence

Afin de lancer une simulation Fluent sur Qarnot, vous devez accorder à Qarnot l'accès à votre licence. Pour plus de détails, veuillez contacter notre équipe à l'adresse <a href="mailto:support-compute@qarnot-computing.com" target="_blank">support-compute@qarnot-computing.com</a>.

À partir de ce point, nous supposerons que votre configuration de licence avec nous est déjà complète.

## Versions

Les versions d’Ansys Fluent disponibles sur Qarnot sont présentées dans notre <a href="https://qarnot.com/logiciels/ansys-fluent-qarnot" target="_blank">catalogue</a>.

Si une autre version vous intéresse, veuillez nous envoyer un e-mail à <a href="mailto:support-compute@qarnot-computing.com" target="_blank">support-compute@qarnot-computing.com</a>.

## Lancer une tâche sur Qarnot

Pour lancer une tâche sur qarnot, il existe deux manières :
- Via notre interface web <a href="https://app.qarnot.com/my-simulations" target="_blank">HPC</a>
- À l’aide d’un script, en utilisant un SDK

Pour lancer une tâche en clique bouton depuis notre interface web, vous pouvez utiliser ce <a href="https://app.supademo.com/demo/cmdpsrrgz2skb9f96zxlzrzdf?utm_source=link" target="_blank">tutoriel pas à pas</a>.

<div style="position: relative; box-sizing: content-box; max-height: 80vh; max-height: 80svh; width: 100%; aspect-ratio: 1.81; padding: 40px 0 40px 0;">
  <iframe src="https://app.supademo.com/embed/cmdpsrrgz2skb9f96zxlzrzdf?embed_v=2&utm_source=embed" loading="lazy" title="How to start an Ansys Fluent simulation on Qarnot" allow="clipboard-write" frameborder="0" webkitallowfullscreen="true" mozallowfullscreen="true" allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe>
</div>

La suite de cet article de blog concerne le lancement grâce à des scripts Python, pour toujours plus d’automatisations et de rapidité.

## Prérequis

Avant de lancer un calcul avec le Python SDK, quelques étapes sont nécessaires :
- <a href="https://tasq.qarnot.com/register" target="_blank">Créer un compte</a>
- Récupérer votre <a href="https://tasq.qarnot.com/settings/access-token" target="_blank">jeton d'authentification API</a>
- <a href="https://doc.tasq.qarnot.com/documentation/sdk-python/installation.html" target="_blank">Installer le Python SDK de Qarnot</a>
- Connaître votre profil Qarnot, par exemple `ansys-fluent-e-corp` et `ansys-fluent-e-corp-vnc`

> **Note** : en plus du Python SDK, Qarnot propose également des SDKs pour <a href="https://doc.tasq.qarnot.com/documentation/sdk-csharp/" target="_blank">C#</a> et <a href="https://doc.tasq.qarnot.com/documentation/sdk-nodejs/" target="_blank">Node.js</a>, ainsi qu'une ligne de commande (<a href="https://doc.tasq.qarnot.com/documentation/cli/man/ManIndex.html" target="_blank">CLI</a>).

## Lancer un test MPI

Le test MPI d'Ansys-Fluent peut s'exécuter sans licence. Pour démarrer un test MPI sur Qarnot, copiez le code suivant dans un script Python. Assurez-vous d'avoir copié votre jeton d'authentification (à <a href="http://tasq.qarnot.com/settings/access-token" target="_blank">récupérer ici</a>) dans le script à la place de `MY_SECRET_TOKEN` pour pouvoir lancer la tâche sur Qarnot.

<div class="wf-code-card"
     data-url="https://cdn.jsdelivr.net/gh/qarnot/blog-samples@main/ansys-fluent/run_ansys-fluent_mpi-test.py"
     data-filename="run_ansys-fluent_mpi-test.py"
     data-language="python"
     data-linenumbers="true"
     data-maxheight="65vh"
     data-fontsize="13px"
     data-download="true"
     data-copy="true"></div>

> **Bon à savoir :** lorsque vous créez une tâche avec conn.create_task, vous devez spécifier son nom, le profil que vous souhaitez utiliser et, dans le cas d'un cluster, le nombre d'instances que vous souhaitez exécuter.

## Cas test

Voici un exemple de la façon d'exécuter un cas d'usage Ansys-Fluent sur la plateforme. Cela suppose que :

- Vous avez accès à une licence.
- Votre cas d'usage inclut des données et un fichier .jou dans un dossier de votre répertoire de travail.

Si nécessaire, voici le cas d'usage générique <a href="https://pages.qarnot.com/hubfs/%5BMARCOM%5D%20Blog%20site%20HPC/aircraft_wing_14m.zip" target="_blank">aircraft_wing_14m</a>. Vous pouvez le télécharger et l'extraire dans un répertoire `aircraft/`.

Une fois cela fait, la structure de vos fichiers devrait ressembler à ceci :

<pre>
.
├── aircraft/
│   ├── run.jou
│   ├── aircraft_wing_14m.cas
│   └── aircraft_wing_14m.dat
└── run-ansys-fluent.py
</pre>

## Lancer le cas test

Une fois que tout est configuré, il est temps d'exécuter le script `run-ansys-fluent.py` ci-dessous. Dans ce script, vous pouvez :
- Remplacez `MY_SECRET_TOKEN` par votre jeton d'authentification réel.
- Sélectionner le répertoire que vous souhaitez synchroniser avec votre bucket.
- Modifier la FLUENT_CMD si necessaire.

Une fois que tout est configuré, utilisez le script `run-ansys-fluent.py` ci-dessous pour lancer le calcul sur Qarnot.

<div class="wf-code-card"
     data-url="https://cdn.jsdelivr.net/gh/qarnot/blog-samples@main/ansys-fluent/run_ansys-fluent.py"
     data-filename="run-ansys-fluent.py"
     data-language="python"
     data-linenumbers="true"
     data-maxheight="65vh"
     data-fontsize="13px"
     data-download="true"
     data-copy="true"></div>


Vous savez désormais lancer une tâche ansys-fluent sur Qarnot !

## Script pour lancement en batch

Le script présenté ci-dessous vous permet d’explorer les fonctionnalités plus avancées de la plateforme pour un lancement en batch.

<div class="wf-code-card"
     data-url="https://cdn.jsdelivr.net/gh/qarnot/blog-samples@main/ansys-fluent/run_ansys-fluent_batch.py"
     data-filename="run_fluent_batch.py"
     data-language="python"
     data-linenumbers="true"
     data-maxheight="65vh"
     data-fontsize="13px"
     data-download="true"
     data-copy="true"></div>

## Lancer une tâche Fluent avec la connectivité SSH activée

Voici un exemple de la façon d'exécuter un cas d'usage Ansys-Fluent avec SSH activé sur la plateforme. Vous aurez besoin d'une clé publique SSH (vous pouvez en créer une en suivant ce <a href="https://qarnot.com/documentation/use-ssh" target="_blank">tutoriel</a>)

<div class="wf-code-card"
     data-url="https://cdn.jsdelivr.net/gh/qarnot/blog-samples@main/ansys-fluent/run_ansys-fluent_ssh.py"
     data-filename="run_fluent_ssh.py"
     data-language="python"
     data-linenumbers="true"
     data-maxheight="65vh"
     data-fontsize="13px"
     data-download="true"
     data-copy="true"></div>

Pour lancer le calcul sur Qarnot, copiez le code ci-dessus dans un script Python dans votre répertoire de travail. Assurez-vous d'avoir :

- Copié votre jeton d'authentification dans le script (à la place de MY_SECRET_TOKEN)
- Copié votre clé SSH dans `DOCKER_SSH`

Et maintenant, vous pouvez exécuter python3 run_fluent_ssh.py.

> **Note :** Le profil utilisé a changé, il s'agit désormais d'`ansys-fluent-ssh`.

Une fois connecté au nœud maître, vous pouvez lancer une simulation sur votre cluster avec cette commande :

> `fluent 3ddp -g mpi=openmpi -pinfiniband -cnf=/job/mpihosts -i run.jou`

Où mpi=openmpi -pinfiniband -cnf=/job/mpihosts sont les paramètres MPI nécessaires pour une simulation sur plus d'un nœud.

## Résultats

Vous devriez maintenant avoir un dossier `aircraft-out` dans votre répertoire de travail sur votre ordinateur et le même `aircraft-out` sur l’app <a href="https://app.qarnot.com/my-simulations" target="_blank">HPC</a> contenant tous les fichiers de sortie.

Vous pouvez visualiser directement sur l’app <a href="https://app.qarnot.com/my-simulations" target="_blank">HPC</a> certaines images et fichiers de logs générés par la simulation qui se trouvent dans votre bucket de sortie.

Vos résultats seront stockés dans le bucket `aircraft-out` et peuvent être récupérés de trois manières :
- Via la plateforme web : télécharger directement depuis la section Bucket.
- Comme fait dans le script Python : à l’aide de la fonction <a href="https://doc.tasq.qarnot.com/documentation/sdk-python/api/compute/task.html#qarnot.task.Task.download_results" target="_blank">download_results</a>.
- Ou via l'une des <a href="https://qarnot.com/documentation/manage-data-dedicated-ui" target="_blank">applications opensource de gestion de bucket S3</a>.

Pour une grande quantité de fichiers ou plus de 5gb de données, il est conseillé d’utiliser rclone (linux) ou cyberduck (windows). Ce sont deux <a href="https://qarnot.com/documentation/manage-data-dedicated-ui" target="_blank">applications opensource de gestion de bucket S3</a>.