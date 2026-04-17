STAR-CCM+ Design Manager permet d’orchestrer automatiquement des campagnes d’exploration de design, de DOE ou d’optimisation à partir d’un projet unique. Concrètement, on décrit l’étude dans un fichier `.dmprj`, puis Design Manager lance et pilote les simulations nécessaires en s’appuyant sur une simulation de référence.

Dans notre cas, le projet est `industrialExhaust_optimization.dmprj` et il s’appuie sur la simulation de référence `industrialExhaust_referenceSimulation.sim`, tous deux rangés dans le dossier `exhaust_opti/`. Le lancement en batch signifie que tout se fait sans interface graphique : le projet est soumis, exécuté et suivi automatiquement depuis un script Python.

Dans cet article, nous allons :
- faire un panorama rapide des licences utiles à connaître ;
- clarifier les différences entre features, unités de consommation et modes Design Manager ;
- comparer les principaux modes de licensing côté Design Manager ;
- puis montrer comment lancer techniquement l’étude sur Qarnot avec `-preallocpower`.

## Licences : accès sur Qarnot

Pour lancer une étude STAR-CCM+ Design Manager sur Qarnot, vous devez nous autoriser à accéder à votre serveur de licences. Pour plus de détails, contactez notre équipe à l’adresse <a href="mailto:support-compute@qarnot-computing.com" target="_blank">support-compute@qarnot-computing.com</a>.

Nous supposerons ici que cette configuration est déjà prête.

Les repères ci-dessous s’appuient sur la documentation Siemens <a href="https://docs.sw.siemens.com/documentation/external/PL20250327063586548/en-US/userManual/starccmp_userguide_html/STARCCMP/GUID-7873A15A-2776-4096-8AE3-142F2B7A3BA5.html" target="_blank">Design Manager Licensing</a>.

## Licences : l’essentiel avant de lancer 
Avant de rentrer dans le détail des licences, fixons d’abord le vocabulaire Design Manager :

- une **simulation de référence** est le fichier `.sim` de départ ;
- un **design** est une simulation individuelle générée à partir de cette référence ;
- une **étude** est l’ensemble des designs pilotés par Design Manager.

> Autrement dit, `1 design = 1 simulation`, tandis qu’`1 étude = un ensemble de simulations`.

### Trois notions à ne pas confondre

#### 1. Les features ou licences produit

- `ccmpsuite` : licence STAR-CCM+ historique de type "suite", utilisée pour ouvrir une session et exécuter des calculs selon les droits disponibles dans votre portefeuille.
- `ccmppower` : licence de session utilisée avec le modèle Power Licensing.
- `innovatesuite` : feature requise pour certaines études avancées comme `DOE`, `Optimization` ou `Robustness and Reliability`.
- `In-cylinder` : feature supplémentaire nécessaire si la simulation de référence utilise ce module de physique.

> Ce sont elles qui autorisent l’usage de certaines fonctions ou de certains modèles de licensing.

#### 2. Les unités de consommation de calcul

- `powerpre` : consommation orientée pré/post-traitement, utile notamment pour lire ou mettre à jour la simulation de référence.
- `power` : unité de consommation de calcul dans le modèle Power Licensing.
- `PoD` : Power on Demand ; ce n’est pas une licence distincte, mais un mode de consommation à la demande des ressources Power.
- `DOEtoken` : unité de consommation de calcul historiquement utilisée par Design Manager.

#### 3. Les postes de dépense

La consommation solver d’un design se décrit avec :
- une composante `Session` ;
- une composante `Core` ;
- puis `X` composantes `Parallel` selon le nombre de processeurs utilisés.

Le point qui prête le plus à confusion est souvent celui-ci : `core` et `parallel` ne sont pas des licences produit au même titre que `ccmpsuite` ou `ccmppower`.

Ils peuvent être satisfaits différemment en fonction des modes Design Manager.

## Les 3 modes côté Design Manager

### 1. Mode par défaut

En mode par défaut, le serveur Design Manager prend une licence de session et la partage avec les designs qu’il lance. Design Manager n’immobilise donc qu’une seule `ccmpsuite`

Le détail exact des composantes `Core` et `Session` dépend ensuite de votre portefeuille de licences et des priorités de consommation configurées sur votre environnement. Dans de nombreux cas, les consommations de calcul associées aux designs s’appuient en priorité sur des `DOEtoken`, avec des possibilités de repli selon les autres options disponibles.

> Le flag `-nosuite` permet de forcer l’utilisation de `DOEtoken` pour ces consommations, ce qui peut être utile si vous souhaitez éviter d’immobiliser des `ccmpsuite`.

Plus d'informations dans la documentation Siemens <a href="https://docs.sw.siemens.com/documentation/external/PL20250327063586548/en-US/userManual/starccmp_userguide_html/STARCCMP/GUID-7873A15A-2776-4096-8AE3-142F2B7A3BA5.html" target="_blank">Design Manager Licensing</a>.

### 2. General Job Submission avec `-dmnoshare`

> Le mode **General Job Submission** s’active avec `-dmnoshare`.

Dans ce mode, Design Manager ne partage pas de licence de session avec les designs. Chaque design démarre donc comme une simulation STAR-CCM+ plus classique, avec son propre schéma de licensing côté solveur.

Dit autrement, si votre objectif principal est d’économiser des sessions, ce n’est pas le meilleur choix.

Son intérêt est ailleurs :

- vous voulez lancer les designs en `ccmppower`,
- vous utilisez du `PoD`,
- vous ne voulez pas dépendre du mécanisme de partage entre le serveur Design Manager et les designs.

En pratique, `General Job Submission` est donc surtout un mode de flexibilité et de compatibilité avec votre stratégie de licensing, pas un mode d’optimisation systématique de la consommation.

> Vous souhaitez l’utiliser sur Qarnot ? Contactez-nous pour un accompagnement personnalisé à cette adresse : <a href="mailto:support-compute@qarnot-computing.com" target="_blank">support-compute@qarnot-computing.com</a>.

### 3. Pre-Allocation avec `-preallocpower`

> Dans les scripts de cet article, nous utilisons `-preallocpower`.

Ce mode signifie que Design Manager réserve à l’avance les ressources de licensing nécessaires avant de lancer les designs, depuis un seul pool de licences.

> Un pool de licences désigne ici un ensemble de ressources de licensing. Il est possible d'avoir plusieurs pool sur un meme serveur, ou bien plusieurs serveurs redondants pour un même pool.

Ce comportement est utile lorsque vous cherchez :

- un comportement plus prévisible côté licences ;
- une validation anticipée de la disponibilité des ressources ;
- une gestion centralisée du licensing au niveau du serveur Design Manager.

Autrement dit, on préfère vérifier en amont que l’étude pourra partir dans de bonnes conditions, plutôt que de démarrer des designs puis d’échouer plus tard faute de ressources disponibles.

Dans cet exemple, nous utiliserons le mode Pre-Allocation qui est le plus simple à mettre ne oeuvre sur Qarnot. 

## Implémentation technique sur Qarnot

Le lancement batch passe par `starlaunch jobmanager`, qui pilote l’étude Design Manager et délègue aux simulations STAR-CCM+ la résolution proprement dite.

Dans les exemples ci-dessous, les scripts utilisent STAR-CCM+ `20.04.008`. Si vous souhaitez changer de version, adaptez simplement `DOCKER_TAG` dans le script en fonction des versions disponibles dans le <a href="https://qarnot.com/logiciels/starccm-qarnot" target="_blank">catalogue logiciel Qarnot</a>.

Avant de lancer un calcul avec le SDK Python, quelques étapes sont nécessaires :

- <a href="https://app.qarnot.com/register" target="_blank">Créer un compte</a>
- Récupérer votre <a href="https://app.qarnot.com/settings/access-token" target="_blank">jeton d’authentification API</a>
- <a href="https://doc.tasq.qarnot.com/documentation/sdk-python/installation.html" target="_blank">Installer le SDK Python de Qarnot</a>
- Connaître votre profil Qarnot, par exemple `starccm-qarnot`

### Cas d'exemple

Si nécessaire, vous pouvez télécharger directement les deux fichiers de l’exemple :

- <a href="https://communication.qarnot.com/hubfs/%5BMARCOM%5D%20Blog%20site%20HPC/starccm_DM/industrialExhaust_optimization.dmprj" target="_blank">industrialExhaust_optimization.dmprj</a>
- <a href="https://communication.qarnot.com/hubfs/%5BMARCOM%5D%20Blog%20site%20HPC/starccm_DM/industrialExhaust_referenceSimulation.sim" target="_blank">industrialExhaust_referenceSimulation.sim</a>

La structure de travail attendue est la suivante :

<pre>
.
├── starccm_DM/
│   ├── exhaust_opti/
│   │   ├── industrialExhaust_optimization.dmprj
│   │   └── industrialExhaust_referenceSimulation.sim
│   ├── run_starccm_dm_batch.py
│   └── run_starccm_dm_batch_advanced.py
</pre>

Le fichier `.dmprj` décrit l’étude Design Manager. Le fichier `.sim` est la simulation de référence sur laquelle l’étude s’appuie pour créer et exécuter les différents designs.

### Comprendre la commande batch

Pour le script simple sur un seul serveur, la commande utile est de la forme :

> starlaunch jobmanager --command "starccm+ -batch industrialExhaust_optimization.dmprj -preallocpower -passtodesign -power -licpath $CDLMD_LICENSE_FILE -mpi openmpi -np 26" --slots 0 --resourcefile /job/mpihosts

Voici le rôle des principaux éléments :

- `starlaunch jobmanager` : lance le gestionnaire Design Manager qui orchestre l’étude et distribue les designs.
- `--command` : fournit la commande STAR-CCM+ que le job manager va exécuter pour les designs.
- `starccm+ -batch industrialExhaust_optimization.dmprj` : ouvre le projet Design Manager sans interface graphique.
- `-preallocpower` : active le mode Pre-Allocation côté licences.
- `-passtodesign` : transmet les options d’exécution et de licence aux simulations générées par Design Manager.
- `-power` : demande l’utilisation du mode Power Licensing dans les runs solver.
- `-licpath $CDLMD_LICENSE_FILE` : indique où trouver le serveur de licences.
- `-mpi openmpi` : sélectionne l’implémentation MPI utilisée pour le calcul parallèle.
- `-np 26` : fixe le nombre total de processus MPI.
- `--slots 0` : laisse le job manager s’appuyer sur le fichier de ressources fourni.
- `--resourcefile /job/mpihosts` : donne au job manager la liste des ressources allouées au job.

Dans le script avancé, vous pouvez ensuite monter à `-np 94` sur une machine `96c`, en gardant quelques cœurs libres pour le système et les communications MPI.

## Scripts

### Script simple sur un serveur

Le premier script est volontairement allégé. Il vise un lancement simple sur un seul serveur en `OnDemandScheduling`, avec `26` cœurs utilisés sur `28` pour laisser un peu de marge au système et aux communications.

<div class="wf-code-card"
     data-url="https://cdn.jsdelivr.net/gh/qarnot/blog-samples@main/starccm_DM/run_starccm_dm_batch.py"
     data-filename="run_starccm_dm_batch.py"
     data-language="python"
     data-linenumbers="true"
     data-maxheight="65vh"
     data-fontsize="13px"
     data-download="true"
     data-copy="true"></div>

### Script batch avancé

Le second script reprend la même logique avec davantage d’options et de commentaires. On y utilise ici un processeur EPYC `96c` en mono-nœud.

<div class="wf-code-card"
     data-url="https://cdn.jsdelivr.net/gh/qarnot/blog-samples@main/starccm_DM/run_starccm_dm_batch_advanced.py"
     data-filename="run_starccm_dm_batch_advanced.py"
     data-language="python"
     data-linenumbers="true"
     data-maxheight="65vh"
     data-fontsize="13px"
     data-download="true"
     data-copy="true"></div>

## Résultats

Vous devriez maintenant avoir un dossier `industrial-exhaust-opti-out` dans votre répertoire de travail si vous utilisez le script simple, ou `industrial-exhaust-opti-advanced-out` si vous utilisez le script avancé. Le même bucket de sortie est également disponible sur l’app <a href="https://app.qarnot.com/my-simulations" target="_blank">HPC</a> avec tous les fichiers générés par l’étude.

Vous pouvez visualiser directement sur l’app <a href="https://app.qarnot.com/my-simulations" target="_blank">HPC</a> certaines images et certains fichiers de logs générés par la simulation qui se trouvent dans votre bucket de sortie.

Vos résultats seront stockés dans le bucket de sortie défini dans le script et peuvent être récupérés de trois manières :

- via la plateforme web, avec téléchargement direct depuis la section Bucket ;
- comme dans le script Python, à l’aide de la fonction <a href="https://doc.tasq.qarnot.com/documentation/sdk-python/api/compute/task.html#qarnot.task.Task.download_results" target="_blank">download_results</a> ;
- via l'une des <a href="https://qarnot.com/documentation/manage-data-dedicated-ui" target="_blank">applications opensource de gestion de bucket S3</a>.

Pour une grande quantité de fichiers ou plus de `5 GB` de données, il est conseillé d’utiliser `rclone` sous Linux ou `Cyberduck` sous Windows.
