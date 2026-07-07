Ansys LS-DYNA est un programme d'éléments finis à usage général capable de simuler des problèmes complexes du monde réel. Il est hautement optimisé pour des performances exceptionnelles sur CPU et est largement utilisé dans diverses industries, notamment l'automobile, l'aérospatiale, la défense et la fabrication, pour analyser des événements à grande vitesse et de courte durée tels que les crash tests, les drop tests (tests de chute), les impacts et les explosions.

Les ingénieurs et les chercheurs s'appuient sur LS-DYNA pour prototyper et valider virtuellement des systèmes, réduisant ainsi le besoin d'essais physiques coûteux. Le logiciel prend en charge des modèles de matériaux avancés et est réputé pour sa stabilité dans la gestion des déformations hautement non linéaires et des interactions fluide-structure.

## Licence

Afin de lancer une simulation LS-DYNA sur Qarnot, vous devez accorder à Qarnot l'accès à votre licence. Pour plus de détails, veuillez contacter notre équipe à l'adresse <a href="mailto:support-compute@qarnot-computing.com" target="_blank">support-compute@qarnot-computing.com</a>.

À partir de ce point, nous supposerons que votre configuration de licence avec nous est déjà complète.

## Versions

Les versions d'Ansys LS-DYNA disponibles sur Qarnot sont présentées dans notre <a href="https://qarnot.com/logiciels/ansys-ls-dyna-qarnot" target="_blank">catalogue</a>.

Si une autre version vous intéresse, veuillez nous envoyer un e-mail à l'adresse <a href="mailto:support-compute@qarnot-computing.com" target="_blank">support-compute@qarnot-computing.com</a>.

## Lancer une tâche sur Qarnot

Pour lancer une tâche sur Qarnot, il existe deux manières :
- Via notre interface web <a href="https://app.qarnot.com/my-simulations" target="_blank">HPC</a>
- À l'aide d'un script, en utilisant un SDK

La suite de cet article de blog concerne le lancement grâce à des scripts Python, pour toujours plus d'automatisations et de rapidité.

## Prérequis

Avant de lancer un calcul avec le Python SDK, quelques étapes sont nécessaires :
- <a href="https://app.qarnot.com/register" target="_blank">Créer un compte</a>
- Récupérer votre <a href="https://app.qarnot.com/settings/access-token" target="_blank">jeton d'authentification API</a>
- <a href="https://doc.tasq.qarnot.com/documentation/sdk-python/installation.html" target="_blank">Installer le Python SDK de Qarnot</a>
- Connaître votre profil Qarnot, par exemple `ls-dyna-qarnot-vnc-wan`

> **Note** : en plus du Python SDK, Qarnot propose également des SDKs pour <a href="https://doc.tasq.qarnot.com/documentation/sdk-csharp/" target="_blank">C#</a> et <a href="https://doc.tasq.qarnot.com/documentation/sdk-nodejs/" target="_blank">Node.js</a>, ainsi qu'une ligne de commande (<a href="https://doc.tasq.qarnot.com/documentation/cli/man/ManIndex.html" target="_blank">CLI</a>).

## Cas test

Voici un exemple de la façon d'exécuter un cas d'usage LS-DYNA sur la plateforme. Cela suppose que :

- Vous avez accès à une licence LS-DYNA.
- Votre cas d'usage inclut un fichier de maillage/d'entrée (par exemple, `EXP_SC_DROP.key`) dans un dossier de votre répertoire de travail.

Dans ce tutoriel, nous utiliserons un dossier nommé `dyna_drop_test/`. Placez vos fichiers de simulation `.key` dans ce dossier.

Une fois cela fait, la structure de vos fichiers devrait ressembler à ceci :

<pre>
.
├── dyna_drop_test/
│   └── EXP_SC_DROP.key
└── run-lsdyna-test.py
</pre>

## Lancer un cas test autonome

Une fois que tout est configuré, vous pouvez exécuter le script `run-lsdyna-test.py` ci-dessous. Dans ce script, vous pouvez :
- Remplacer `MY_SECRET_TOKEN` par votre jeton d'authentification réel.
- Sélectionner le répertoire que vous souhaitez synchroniser avec votre bucket.
- Modifier les paramètres d'exécution de la commande (`LSDYNA_CMD`). Par exemple :
  - Mode SMP : `lsdyna_sp.e i=input.k ncpu=1 memory=1200M`
  - Mode MPP : `mpiexec -np 1 lsdyna_sp_mpp.e i=input.k memory=1200M`

Une fois que tout est configuré, utilisez le script ci-dessous pour lancer le calcul sur Qarnot.

<div class="wf-code-card"
     data-url="https://cdn.jsdelivr.net/gh/qarnot/blog-samples@main/ls-dyna/run-lsdyna-test.py"
     data-filename="run-lsdyna-test.py"
     data-language="python"
     data-linenumbers="true"
     data-maxheight="65vh"
     data-fontsize="13px"
     data-download="true"
     data-copy="true"></div>

Pour lancer ce script, exécutez simplement `python3 run-lsdyna-test.py` dans votre terminal.

> **Bon à savoir :** ce script intègre également la connectivité VNC. Si le VNC est activé, il attend que la tâche commence son exécution et affiche un lien direct de connexion par navigateur pour accéder au bureau web interactif.

## Résultats

Vous devriez maintenant avoir un dossier `dyna_drop_test_out` dans votre répertoire de travail sur votre ordinateur et le même dossier de sortie sur l'application <a href="https://app.qarnot.com/my-simulations" target="_blank">HPC</a> contenant tous les fichiers de sortie.

Vos résultats seront stockés dans votre bucket de sortie et peuvent être récupérés de trois manières :
- Via la plateforme web : télécharger directement depuis la section Bucket.
- Comme fait dans le script Python : à l'aide de la fonction <a href="https://doc.tasq.qarnot.com/documentation/sdk-python/api/compute/task.html#qarnot.task.Task.download_results" target="_blank">download_results</a>.
- Ou via l'une des <a href="https://qarnot.com/documentation/manage-data-dedicated-ui" target="_blank">applications opensource de gestion de bucket S3</a>.

Pour une grande quantité de fichiers ou plus de 5 Go de données, il est conseillé d'utiliser rclone (Linux) ou Cyberduck (Windows). Ce sont deux <a href="https://qarnot.com/documentation/manage-data-dedicated-ui" target="_blank">applications opensource de gestion de bucket S3</a>.
