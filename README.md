# BigDataProject - AWS

A chaque fois, les services d'AWS sont configurés pour être dans le même VPC avec le même Sécurity Group

## RDS

Pour cette architecture sous AWS, il faut créer une base de données MySQL hébergée sous RDS.

Les seules modifications dans la configuration de base sont le choix de MySQL, et les informations de connexion (nom de la base de données, nom de l'utilisateur et mot de passe).

Puis, directement sur RDS ou à l'aide d'une fonction lambda, il faut créer les tables suivantes : 
* `CREATE TABLE user (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, login VARCHAR(255) NOT NULL, password VARCHAR(255) NOT NULL, UNIQUE(login))`
* `CREATE TABLE statistics (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, user_id INT NOT NULL, quizz_id INT NOT NULL, date VARCHAR(255) NOT NULL, score INT NOT NULL)`

--- 

## Lambda 

Chaque lambda est dans le dossier associée. 

Au début de chaque fichier, il y a un objet JSON qui est un exemple de d'objet à passer à la fonction lambda.

### Dépendances 

Pour les dépendances des fonctions Lambda, il faut installer les dépendances en local dans un dossier `./pyhton` : `pip install -t ./pyhton <package_name>`.

Ensuite il faut compressé ce dossier `./pyhton` dans un .zip. 

Sous S3, il faut créer un bucket et y déposer tous les fichiers zip des dépendances (les renommer avec le nom de package pour mieux s'y retrouver).

Sous Lambda, créer une nouvelle couche (layers) en y ajoutant le chemin du fichier compressé présent dans le bucket. 

Dans la fonction il suffit d'ajouter une couche (layers) avec les bonnes dépendances.

--- 

## S3

Il va falloir plusieurs bucket S3 pour cette architecture : 
* Un bucket avec les dépendances (présenté dans la partie lambda)
* Un bucket avec les fichiers audio temporaire (avec accès public et modification des autorisation CORS avec `./S3/Autorisation-CORS`)
* Un bucket avec l'application Web Angular hébergeant un site Web statique (avec accès public)
* Un bucket avec le model de machine learning contenant le fichier `./S3/conv2d_divider6_dropout0.5_epoch50.h5`

---

## EC2

Créer une intsance EC2 (dans notre cas on a utilisé une t2.medium sous ubuntu 22).

Copier tous les fichiers du dossier `EC2-machine-learning` dans l'instance.

Lancer la commande pour installer toutes les dépendances : `pip install -r requirements.txt`.

Lancer le serveur avec `python3 main.py`.
