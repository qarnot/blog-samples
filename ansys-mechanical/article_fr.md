ANSYS Mechanical est une suite logicielle de simulation numérique multidisciplinaire basée sur la méthode des éléments finis (MEF), conçue pour l'analyse statique, dynamique et thermique de structures et de composants. Elle s'impose comme une référence pour l'évaluation de la résistance, de la durabilité, de la cinématique et du comportement thermique des systèmes d'ingénierie.

Le logiciel est largement utilisé dans des secteurs comme l'aérospatial, l'automobile, l'énergie et l'électronique pour valider les prototypes virtuellement et réduire le besoin d'essais physiques coûteux, accélérant ainsi le cycle de conception et de développement. Il offre également une intégration poussée avec d'autres outils de la suite ANSYS, permettant des simulations complexes couplées (mécanique-fluide, thermique-structurel, etc.).

## Licence

Pour lancer une simulation Ansys Mechanical sur Qarnot, vous devez nous autoriser à accéder à votre licence. Pour plus de détails, veuillez contacter notre équipe via <a href="mailto:support-compute@qarnot-computing.com" target="_blank">support-compute@qarnot-computing.com</a>.

Nous supposerons, à partir de maintenant, que votre configuration de licence avec nous est déjà terminée.

## Versions

Les versions d’Ansys Mechanical disponibles sur Qarnot sont présentées dans notre <a href="https://qarnot.com/logiciels/ansys-mechanical-qarnot" target="_blank">catalogue</a>.

Si une autre version vous intéresse, veuillez nous envoyer un e-mail à <a href="mailto:support-compute@qarnot-computing.com" target="_blank">support-compute@qarnot-computing.com</a>.

## Lancer une tâche sur Qarnot

Pour lancer une tâche sur qarnot, il existe deux manières :
- Via notre interface web <a href="https://app.qarnot.com/my-simulations" target="_blank">HPC</a>
- À l’aide d’un script, en utilisant un SDK

La suite de cet article de blog concerne le lancement grâce à des scripts Python, pour toujours plus d’automatisations et de rapidité.

## Prérequis

Avant de lancer un calcul avec le Python SDK, quelques étapes sont nécessaires :
- <a href="https://app.qarnot.com/register" target="_blank">Créer un compte</a>
- Récupérer votre <a href="https://app.qarnot.com/settings/access-token" target="_blank">jeton d'authentification API</a>
- <a href="https://doc.tasq.qarnot.com/documentation/sdk-python/installation.html" target="_blank">Installer le Python SDK de Qarnot</a>
- Connaître votre profil Qarnot, par exemple `ansys-mechanical-e-corp` et `ansys-mechanical-e-corp-vnc`

**Note** : en plus du Python SDK, Qarnot propose également des SDKs pour <a href="https://doc.tasq.qarnot.com/documentation/sdk-csharp/" target="_blank">C#</a> et <a href="https://doc.tasq.qarnot.com/documentation/sdk-nodejs/" target="_blank">Node.js</a>, ainsi qu'une ligne de commande (<a href="https://doc.tasq.qarnot.com/documentation/cli/man/ManIndex.html" target="_blank">CLI</a>).

## Cas test

Ce cas test vous montrera comment lancer le modèle de bench officiel v8. Vous aurez besoin des fichiers <a href="https://27028395.fs1.hubspotusercontent-eu1.net/hubfs/27028395/%5BMARCOM%5D%20Blog%20site%20HPC/ansys-mecha/V24direct-1.dat" target="_blank">V24direct-1.dat</a> et <a href="https://27028395.fs1.hubspotusercontent-eu1.net/hubfs/27028395/%5BMARCOM%5D%20Blog%20site%20HPC/ansys-mecha/V24direct-1geom.db" target="_blank">V24direct-1geom.db</a> provenant du <a href="https://ansyshelp.ansys.com/public/account/secured?returnurl=/Views/Secured/corp/v242/en/wb_vm/wbvt-vm-mech-wb.html" target="_blank">site d’Ansys</a>.

Une fois les fichiers téléchargés, placez-les dans un répertoire nommé `v8-in`.

## Lancer le cas test

Une fois que tout est configuré, utilisez le script `run-ansys-mechanical.py` ci-dessous pour lancer le calcul sur Qarnot.

Pour lancer le calcul sur Qarnot, enregistrez le code ci-dessus en tant que script Python dans votre répertoire de travail. Avant de l'exécuter, assurez-vous de mettre à jour les constantes suivantes au début du script :
- Remplacez `MY_SECRET_TOKEN` par votre jeton d'authentification réel. À <a href="http://app.qarnot.com/settings/access-token" target="_blank">récupérer ici</a>.

<pre>
.
├── v8-in/
│   ├── V24direct-1.dat
│   ├── V24direct-1geom.db
└── run-ansys-mechanical.py
</pre>

<div class="wf-code-card"
     data-url="https://cdn.jsdelivr.net/gh/qarnot/blog-samples@main/ansys-mechanical/run-ansys-mechanical.py"
     data-filename="run-ansys-mechanical.py"
     data-language="python"
     data-linenumbers="true"
     data-maxheight="65vh"
     data-fontsize="13px"
     data-download="true"
     data-copy="true"></div>

Pour lancer ce script, exécutez simplement `python3 run-ansys-mechanical.py` dans votre terminal.

Vous savez désormais lancer une tâche ansys-mechanical sur Qarnot !

## Script pour lancement en batch - avancé

Le script présenté ci-dessous vous permet d’explorer les fonctionnalités plus avancées de la plateforme pour un lancement en batch.

<div class="wf-code-card"
     data-url="https://cdn.jsdelivr.net/gh/qarnot/blog-samples@main/ansys-mechanical/run-ansys-mechanical_batch.py"
     data-filename="run-ansys-mechanical_batch.py"
     data-language="python"
     data-linenumbers="true"
     data-maxheight="65vh"
     data-fontsize="13px"
     data-download="true"
     data-copy="true"></div>

## Résultats

Vous devriez maintenant avoir un dossier `v8-out` dans votre répertoire de travail sur votre ordinateur et le même `v8-out` sur l’app <a href="https://app.qarnot.com/my-simulations" target="_blank">HPC</a> contenant tous les fichiers de sortie.

Vous pouvez visualiser directement sur l’app <a href="https://app.qarnot.com/my-simulations" target="_blank">HPC</a> certaines images et fichiers de logs générés par la simulation qui se trouvent dans votre bucket de sortie.

Vos résultats seront stockés dans le bucket `v8-out` et peuvent être récupérés de trois manières :
- Via la plateforme web : télécharger directement depuis la section Bucket.
- Comme fait dans le script Python : à l’aide de la fonction <a href="https://doc.tasq.qarnot.com/documentation/sdk-python/api/compute/task.html#qarnot.task.Task.download_results" target="_blank">download_results</a>.
- Ou via l'une des <a href="https://qarnot.com/documentation/manage-your-data-with-a-dedicated-ui" target="_blank">applications opensource de gestion de bucket S3</a>.

Pour une grande quantité de fichiers ou plus de 5gb de données, il est conseillé d’utiliser rclone (linux) ou cyberduck (windows). Ce sont deux <a href="https://qarnot.com/documentation/manage-your-data-with-a-dedicated-ui" target="_blank">applications opensource de gestion de bucket S3</a>.