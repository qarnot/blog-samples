STAR-CCM+ Design Manager permet d’orchestrer automatiquement des campagnes d’exploration de design, de DOE ou d’optimisation à partir d’un projet unique. Concrètement, on décrit l’étude dans un fichier `.dmprj`, puis Design Manager lance et pilote les simulations nécessaires en s’appuyant sur une simulation de référence.

Dans notre cas, le projet est `industrialExhaust_optimization.dmprj` et il s’appuie sur la simulation de référence `industrialExhaust_referenceSimulation.sim`, tous deux rangés dans le dossier `exhaust_opti/`. Le lancement en batch signifie que tout se fait sans interface graphique : le projet est soumis, exécuté et suivi automatiquement depuis un script Python.

Dans cet article, nous allons :
- expliquer comment Design Manager consomme les licences,
- détailler la commande de lancement batch,
- présenter un script simple pour un lancement sur un seul Xeon,
- puis un script plus avancé pour aller plus loin sur des topologies plus puissantes.

## Licence

Pour lancer une simulation STAR-CCM+ sur Qarnot, vous devez nous autoriser à accéder à votre licence. Pour plus de détails, veuillez contacter notre équipe à l’adresse <a href="mailto:support-compute@qarnot-computing.com" target="_blank">support-compute@qarnot-computing.com</a>.

Nous supposerons ici que votre configuration de licence est déjà prête.

### Comment Design Manager consomme les licences

Le comportement de Design Manager côté licences détermine combien de features sont mobilisées pendant l’étude. Ici, le mot “coût” désigne donc une consommation de licences, pas un prix.

Les points suivants sont alignés avec la documentation Siemens <a href="https://docs.sw.siemens.com/documentation/external/PL20250327063586548/en-US/userManual/starccmp_userguide_html/STARCCMP/GUID-7873A15A-2776-4096-8AE3-142F2B7A3BA5.html" target="_blank">Design Manager Licensing</a> :
- pour lire ou mettre à jour la simulation de référence, Design Manager requiert soit `1 ccmpsuite`, soit `1 ccmppower`, soit `10 powerpre`
- la phase de configuration des études ne consomme pas de licence
- certains types d’étude, notamment `Optimization`, `DOE`, `Robustness and Reliability`, demandent `1 innovatesuite`
- si la simulation de référence embarque des fonctionnalités In-cylinder, une licence In-cylinder supplémentaire est nécessaire côté serveur Design Manager

### Mode par défaut

En mode par défaut, le serveur Design Manager prend une licence de session et la partage avec les simulations de design. Les designs consomment ensuite leurs propres licences de calcul :
- `1` licence cœur par design concurrent
- les licences parallèles correspondant au nombre de processeurs utilisés

Par défaut, les licences de calcul sont prises en priorité sur des `DOEtoken`, avec des possibilités de repli selon les options de licence disponibles.

### Pre-Allocation

Dans les scripts de cet article, nous utilisons `-preallocpower`. Ce mode signifie que Design Manager réserve à l’avance les licences nécessaires avant de lancer les designs, depuis un seul pool de licences.

Ce mode est utile quand vous voulez un comportement prévisible côté licences et que tout le checkout reste centralisé au niveau du serveur Design Manager.

### General Job Submission

L’autre variante importante est `General Job Submission`, activée avec `-dmnoshare`. Dans ce mode, Design Manager ne partage pas de licence avec les designs : chaque design démarre comme une simulation STAR-CCM+ standard.

Cette approche est notamment pertinente si vous souhaitez piloter vos runs avec des `ccmppower` ou du Power on Demand, tout en gardant Design Manager comme orchestrateur de l’étude.

## Comprendre la commande Design Manager

Le lancement batch passe par `starlaunch jobmanager`, qui pilote l’étude Design Manager et délègue aux simulations STAR-CCM+ la résolution proprement dite.

Pour le script simple sur un seul Xeon, la commande utile est de la forme :

```bash
starlaunch jobmanager --command "starccm+ -batch industrialExhaust_optimization.dmprj -preallocpower -passtodesign -power -licpath $CDLMD_LICENSE_FILE -mpi openmpi -np 26" --slots 0 --resourcefile /job/mpihosts
```

Dans le script avancé, vous pouvez ensuite passer :
- à `-np 94` sur une machine `96c`,
- ou à `-np 52` sur `2x28c`, avec `-machinefile /job/mpihosts` et `-mpiflags '--mca btl ^openib,tcp --mca pml ucx --mca osc ucx'` qui ne sont nécessaires qu’en multi-nœud.

Voici le rôle des principaux éléments :

- `starlaunch jobmanager` : lance le gestionnaire Design Manager qui orchestre l’étude et distribue les designs.
- `--command` : fournit la commande STAR-CCM+ que le job manager va exécuter pour les designs.
- `starccm+ -batch industrialExhaust_optimization.dmprj` : ouvre le projet Design Manager sans interface graphique.
- `-preallocpower` : active le mode Pre-Allocation côté licences.
- `-passtodesign` : transmet les options d’exécution et de licence aux simulations générées par Design Manager.
- `-power` : demande l’utilisation du mode Power licensing dans les runs solver.
- `-licpath $CDLMD_LICENSE_FILE` : indique où trouver le serveur de licences.
- `-mpi openmpi` : sélectionne l’implémentation MPI utilisée pour le calcul parallèle.
- `-np ...` : fixe le nombre total de processus MPI.
- `-machinefile /job/mpihosts` : indique la liste des nœuds alloués. Cette option n’est nécessaire qu’en multi-nœud.
- `-mpiflags ...` : passe des options OpenMPI adaptées au fonctionnement multi-nœud. Cette option n’est elle aussi nécessaire qu’en multi-nœud.
- `--slots 0` : laisse le job manager s’appuyer sur le fichier de ressources fourni.
- `--resourcefile /job/mpihosts` : donne au job manager la liste des ressources allouées au job.

## Versions et prérequis

Dans les exemples ci-dessous, les scripts utilisent STAR-CCM+ `20.04.008`. Si vous souhaitez changer de version, adaptez simplement `DOCKER_TAG` dans le script en fonction des versions disponibles dans le <a href="https://qarnot.com/logiciels/starccm-qarnot" target="_blank">catalogue logiciel Qarnot</a>.

Avant de lancer un calcul avec le SDK Python, quelques étapes sont nécessaires :
- <a href="https://app.qarnot.com/register" target="_blank">Créer un compte</a>
- Récupérer votre <a href="https://app.qarnot.com/settings/access-token" target="_blank">jeton d’authentification API</a>
- <a href="https://doc.tasq.qarnot.com/documentation/sdk-python/installation.html" target="_blank">Installer le SDK Python de Qarnot</a>
- Connaître votre profil Qarnot, par exemple `starccm-qarnot`

## Cas exemple

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

## Script simple sur un Xeon

Le premier script est volontairement allégé. Il vise un lancement simple sur un seul Xeon en `OnDemandScheduling`, avec `26` cœurs utilisés sur `28` pour laisser un peu de marge au système et aux communications.

<div class="wf-code-card"
     data-url="https://cdn.jsdelivr.net/gh/qarnot/blog-samples@main/starccm_DM/run_starccm_dm_batch.py"
     data-filename="run_starccm_dm_batch.py"
     data-language="python"
     data-linenumbers="true"
     data-maxheight="65vh"
     data-fontsize="13px"
     data-download="true"
     data-copy="true"></div>

## Script batch avancé

Le second script reprend la même logique avec davantage d’options et de commentaires. Il permet de documenter plus finement les topologies `96c` en mono-nœud et `2x28c` en multi-nœud.

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

Vous devriez maintenant avoir un dossier `industrial-exhaust-opti-out` dans votre répertoire de travail sur votre ordinateur si vous utilisez le script simple, ou `industrial-exhaust-opti-advanced-out` si vous utilisez le script avancé. Le même bucket de sortie est également disponible sur l’app <a href="https://app.qarnot.com/my-simulations" target="_blank">HPC</a> avec tous les fichiers générés par l’étude.

Vous pouvez visualiser directement sur l’app <a href="https://app.qarnot.com/my-simulations" target="_blank">HPC</a> certaines images et certains fichiers de logs générés par la simulation qui se trouvent dans votre bucket de sortie.

Vos résultats seront stockés dans le bucket de sortie défini dans le script et peuvent être récupérés de trois manières :
- Via la plateforme web : téléchargement direct depuis la section Bucket.
- Comme dans le script Python : à l’aide de la fonction <a href="https://doc.tasq.qarnot.com/documentation/sdk-python/api/compute/task.html#qarnot.task.Task.download_results" target="_blank">download_results</a>.
- Ou via l'une des <a href="https://qarnot.com/documentation/manage-data-dedicated-ui" target="_blank">applications opensource de gestion de bucket S3</a>.

Pour une grande quantité de fichiers ou plus de 5gb de données, il est conseillé d’utiliser rclone (linux) ou cyberduck (windows). Ce sont deux <a href="https://qarnot.com/documentation/manage-data-dedicated-ui" target="_blank">applications opensource de gestion de bucket S3</a>.
