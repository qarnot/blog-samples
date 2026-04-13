STAR-CCM+ Design Manager permet d’orchestrer automatiquement des campagnes d’exploration de design, de DOE ou d’optimisation à partir d’un projet unique. Concrètement, on décrit l’étude dans un fichier `.dmprj`, puis Design Manager lance et pilote les simulations nécessaires en s’appuyant sur une simulation de référence.

Dans notre cas, le projet est `industrialExhaust_optimization.dmprj` et il s’appuie sur la simulation de référence `industrialExhaust_referenceSimulation.sim`, tous deux rangés dans le dossier `exhaust_opti/`. Le lancement en batch signifie que tout se fait sans interface graphique : le projet est soumis, exécuté et suivi automatiquement depuis un script Python.

Dans cet article, nous allons :
- faire un panorama rapide des licences utiles à connaître ;
- clarifier les licences nécessaires à chaque étape, les schémas Design Manager et les options de commande ;
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

### Ce que cela change au moment de lancer

Avant de lancer une étude Design Manager, il faut surtout savoir à quel moment chaque ressource de licence peut être utilisée. Cela permet d’anticiper les blocages les plus courants : impossible de lire la simulation de référence, étude avancée non autorisée, designs qui ne démarrent pas faute de ressources solver disponibles.

#### 1. Licences nécessaires selon l’étape Design Manager

- **Lecture ou mise à jour de la simulation de référence** : Design Manager a besoin d’une licence valide :
  - `1 ccmpsuite`, `1 ccmppower` ou `10 powerpre` est nécessaire
- **Configuration de l’étude** : pas de licence spécifique
- **Analyse ou lancement d’études avancées** comme `Optimization`, `DOE` ou `Robustness and Reliability` :
  - `1 innovatesuite` est nécessaire
- **Exécution solver des designs** : chaque design doit disposer des ressources solver nécessaires selon le mode Design Manager choisi et les options de commande :
  - `X DOEtoken`, `1 ccmppower` ou `PoD` Power on Demand
- **Simulation avec fonctionnalités `In-cylinder`** :
  - 1 licence `In-cylinder` est nécessaire côté serveur Design Manager.

#### 2. Options de commande et scénarios de consommation

Les options de lancement choisissent ensuite comment les designs consomment les ressources disponibles :

- `-power` : demande le Power Licensing pour les simulations de design ;
- `-nosuite` : force l’usage de `DOEtoken` uniquement pour éviter le repli sur `ccmpsuite` ;
- `-preallocpower` : active la pré-allocation Power côté Design Manager (voir ci-dessous);
- `-dmnoshare` : active le mode General Job Submission (voir ci-dessous);
- `-passtodesign` : transmet aux simulations générées les options qui concernent leur propre exécution.

## Les 3 modes côté Design Manager

La consommation solver d’un design reste composée d’une partie `Session`, d’une partie `Core` et de composantes `Parallel` selon le nombre de processeurs utilisés. Ces composantes peuvent être satisfaites différemment selon le schéma Design Manager et les options de commande.

### 1. Mode par défaut

En mode par défaut, le serveur Design Manager prend une licence de `Session` et la partage avec les designs qu’il lance. Cette session peut être fournie par une licence `ccmpsuite`, `ccmppower` ou Power on Demand selon votre configuration.

Le détail exact des composantes `Core` et `Parallel` dépend ensuite de votre portefeuille de licences et des priorités de consommation configurées sur votre environnement. Dans de nombreux cas, les consommations de calcul associées aux designs s’appuient en priorité sur des `DOEtoken`, avec des possibilités de repli selon les autres options disponibles.

> Le flag `-nosuite` permet de forcer l’utilisation de `DOEtoken` pour ces consommations, ce qui peut être utile si vous souhaitez éviter d’immobiliser des `ccmpsuite`.

Cas typiques :

- vous avez une licence de session disponible pour Design Manager et des `DOEtoken` pour exécuter les designs ;
- vous voulez limiter le nombre de sessions STAR-CCM+ mobilisées pendant l’étude ;
- vous utilisez une configuration proche du comportement standard documenté par Siemens.

Exemple d'utilisation avec 3 `ccmpsuite` et 48 `DOEtoken` depuis la <a href="https://docs.sw.siemens.com/documentation/external/PL20250327063586548/en-US/userManual/starccmp_userguide_html/STARCCMP/GUID-7873A15A-2776-4096-8AE3-142F2B7A3BA5.html" target="_blank">documentation officielle</a>:
![alt text](default_licensing.png)

### 2. General Job Submission avec `-dmnoshare`

> Le mode **General Job Submission**, aussi appelé **Unlicensed Design Manager Server** s’active avec `-dmnoshare`.

Dans ce mode, Design Manager ne partage pas de licence de session avec les designs. Chaque design démarre donc comme une simulation STAR-CCM+ plus classique, avec son propre schéma de licensing côté solveur.

Cas typiques :

- vous disposez surtout de licences `ccmppower` et vous voulez que les designs les utilisent directement ;
- vous utilisez du `PoD` et chaque design doit partir avec les options associées ;
- vos designs ont des durées d’exécution très différentes et vous préférez que les ressources soient libérées design par design, au fil des fins de calcul.

Exemple d'utilisation de 3 `ccmppower` sans `ccmpsuite` depuis la <a href="https://docs.sw.siemens.com/documentation/external/PL20250327063586548/en-US/userManual/starccmp_userguide_html/STARCCMP/GUID-7873A15A-2776-4096-8AE3-142F2B7A3BA5.html" target="_blank">documentation officielle</a>:
![alt text](unlicensed_licensing.png)

> Vous souhaitez l’utiliser sur Qarnot ? Contactez-nous pour un accompagnement personnalisé à cette adresse : <a href="mailto:support-compute@qarnot-computing.com" target="_blank">support-compute@qarnot-computing.com</a>.

### 3. Pre-Allocation avec `-preallocpower`

> Dans les scripts de cet article, nous utilisons `-preallocpower`.

Ce mode signifie que Design Manager réserve à l’avance les ressources de licensing nécessaires avant de lancer les designs, depuis un seul pool de licences.

> Un pool de licences désigne ici un ensemble de ressources de licensing. Il est possible d’avoir plusieurs pools sur un même serveur, ou bien plusieurs serveurs redondants pour un même pool.

Ce mode est intéressant si vous voulez éviter les surprises en cours d’étude. Au lieu de laisser les designs démarrer puis découvrir plus tard qu’une ressource manque, Design Manager valide la disponibilité des licences en amont.

Cette prévisibilité a aussi une contrepartie : si une salve contient des designs très rapides et d’autres beaucoup plus longs, certaines ressources peuvent rester réservées pendant que Design Manager attend la fin de la salve. C’est particulièrement visible dans les études d’exploration ou d’optimisation, où Design Manager lance un groupe de designs, attend leurs résultats, puis utilise un algorithme pour choisir les prochains designs à explorer.

Cas typiques :

- vous lancez une étude longue ou coûteuse et vous préférez échouer immédiatement si les licences ne sont pas disponibles ;
- vous exécutez plusieurs designs en parallèle et vous voulez une consommation de licences plus prévisible ;
- vos designs ont des temps de calcul assez proches, donc la pré-allocation ne risque pas de laisser trop de ressources réservées inutilement ;
- vous lancez sur Qarnot et vous voulez un mode simple à automatiser en batch.

Autrement dit, on préfère vérifier en amont que l’étude pourra partir  plutôt que de démarrer des designs puis d’échouer plus tard faute de ressources disponibles.

Dans cet exemple, nous utiliserons le mode Pre-Allocation, qui est le plus simple à mettre en œuvre sur Qarnot.

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
