# BigDataProject - Front Web

Cette application Front Web a été généré avec Angular 15.0.2.

## Modification des credentials AWS dans le code

Il faut pensez à modifier les credentials d'AWS dans le fichier `./src/app/global-variables.ts` pour que l'application Angular puisse accéder aus services AWS.

--- 

## Déploiement en local

Pour lancer le Front Web en local, lancez la commande `ng serve`. Il pourra être accessible depuis `http://localhost:4200/`.

--- 

## Déploiement sur AWS

Créer un bucket S3 hébergeant un site Web statique (point d'entrée : `index.html`) et en configurant l'accès public.

Dans la racine du projet, lancer le build : `ng build --aot`.

Puis ajoutez le build au précédent bucket S3 : `aws s3 cp ./dist/big-data s3://bucket-big-data-angular --recursive`.
(Ne pas oubliez de mettre les credentials pour AWS CLI : par exemple sous Windows `C:\Users\PC\.aws\credentials`)
Il est aussi possible de déposer tous les fichiers présents sous `./dist/big-data/` directement dans le bucket.
