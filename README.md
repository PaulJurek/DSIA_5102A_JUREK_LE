
# Projet application e-commerce full stack

![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens)
![Jinja](https://img.shields.io/badge/jinja-white.svg?style=for-the-badge&logo=jinja&logoColor=black)


## Description
Cette application est une ébauche d'une plateforme e-commerce. Elle est développée avec le framework FastAPI. En back-end, nous réalisons des requêtes vers une base de données postgresql afin d'obtenir pour chaque client de la plateforme de réaliser des commandes. Pour le producteur cela permet de visualiser ses ventes. L'application est sécurisée avec un système d'authentification avec récupération d’un JWT à l’aide d’un username / password.

## Pré-requis
Ce projet nécessite l'utilisation de Docker. S'il n'est pas déjà téléchargé :

* [Pour Windows](https://docs.docker.com/desktop/install/windows-install/)

* [Pour Linux](https://docs.docker.com/desktop/install/linux-install/)

* [Pour Mac](https://docs.docker.com/desktop/install/mac-install/)


## Guide d'installation
Dans un terminal de commandes, commencez par vous déplacer vers le dossier où sera enregistré le projet avec la commande :

``
cd chemin_vers_le_dossier_de_votre_choix
``

Cloner le projet avec la commande:

``
git clone https://github.com/PaulJurek/DSIA_5102A_JUREK_LE
``

Créer les containers et les images du projet avec la commande (à la racine du projet)

``
docker-compose build 
``

Lancer  l'exécution du projet avec la commande 

``
docker-compose up -d
``

Enfin il suffit de se rendre sur l'adresse IP https://127.0.0.1:5000.



## Contributeurs

Ce projet a été développé par Van-Minh Christophe LE (étudiant 5e année filière DSIA) et Paul JUREK (étudiant 5e année filière AIC) dans le cadre de l'unité "Application full stack data" dispensée à l'ESIEE PARIS.
