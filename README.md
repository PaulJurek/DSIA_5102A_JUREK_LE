
# Projet application e-commerce full stack

![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens)
![Jinja](https://img.shields.io/badge/jinja-white.svg?style=for-the-badge&logo=jinja&logoColor=black)


## Description
Cette application est une ébauche d'une plateforme e-commerce. Ce site permet à un agriculteur de vendre directement ses produits en circuit court à ses clients en ligne. Elle est développée avec le framework FastAPI. En back-end, nous réalisons des requêtes vers une base de données postgresql afin d'obtenir pour chaque client de la plateforme de réaliser des commandes. Pour le producteur cela permet de visualiser ses ventes. L'application est sécurisée avec un système d'authentification avec récupération d’un JWT à l’aide d’un username / password.

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
docker-compose up -build
``

Enfin il suffit de se rendre sur l'adresse IP https://127.0.0.1:5000.

## Remplir les db la première fois

Ce projet utilise 3 db postgre "UTILISATEURS", "PRODUITS" et "PANIERS". Comme nous ne savons pas comment transmettre des db déja remplies via GITHUB, voilà une liste de commandes SQL pour pouvoir commencer à utiliser l'application. 

Pour alimenter le catalogue de produits :

``
INSERT INTO "PRODUITS" (id, nom, description, prix, imageurl, date_creation, date_modification) VALUES
('3f12fa8c-d3be-4a3b-8835-b01c02d3b9d7', 'Carotte', 'Légume racine riche en vitamine A', 1.25, 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Carrots_on_Display.jpg/800px-Carrots_on_Display.jpg', NOW(), NOW()),
('2f99e81c-8cd1-45f6-95f3-2454e3a50432', 'Tomate', 'Fruit juteux, idéal pour les salades', 2.50, 'https://www.lesfruitsetlegumesfrais.com/app/uploads/cache/2021/03/tomate/2511319199.png', NOW(), NOW()),
('f5e0c75e-bf72-46f9-bf5e-88a63bfe5b8f', 'Pomme de terre', 'Légume polyvalent pour divers plats', 0.80, 'https://www.marechal-fraicheur.fr/media/cache/synolia_cms_image_mobile_max_size/media/file/a5/e6/e9458c7ba03d4d96717bb924be24.jpg', NOW(), NOW()),
('1be25b96-d14e-485f-9b0f-e6b59e94f91b', 'Oignon', 'Ingrédient de base pour de nombreuses recettes', 1.00, 'https://media.venturatravel.org/unsafe/800x600/smart/gal/animal/galapagos-fur-seal-1.jpg', NOW(), NOW()),
('ee768b0f-cbf2-45b7-a2ba-29ad47064d38', 'Courgette', 'Légume léger et savoureux', 2.00, 'https://media.venturatravel.org/unsafe/800x600/smart/gal/animal/galapagos-fur-seal-1.jpg', NOW(), NOW()),
('1e68bda9-98ca-42b9-8e36-c02d1e3e5053', 'Aubergine', 'Légume tendre pour les gratins', 2.20, 'https://media.venturatravel.org/unsafe/800x600/smart/gal/animal/galapagos-fur-seal-1.jpg', NOW(), NOW()),
('0aeeeb59-f9ad-44bc-a4a4-229faec87b98', 'Brocoli', 'Source importante de vitamine C', 2.40, 'https://media.venturatravel.org/unsafe/800x600/smart/gal/animal/galapagos-fur-seal-1.jpg', NOW(), NOW()),
('e2c9d4a7-2be0-4878-944f-28b4b95f48c6', 'Poivron rouge', 'Légume coloré, riche en antioxydants', 2.50, 'https://media.venturatravel.org/unsafe/800x600/smart/gal/animal/galapagos-fur-seal-1.jpg', NOW(), NOW()),
('17b26a6b-77cd-4239-b4b7-fd8debb7fc0d', 'Salade verte', 'Légume frais, parfait pour accompagner vos plats', 1.30, 'https://media.venturatravel.org/unsafe/800x600/smart/gal/animal/galapagos-fur-seal-1.jpg', NOW(), NOW()),
('7a214b6c-073b-428f-b5ec-437c0c68d531', 'Céleri', 'Légume croquant et rafraîchissant', 1.80, 'https://media.venturatravel.org/unsafe/800x600/smart/gal/animal/galapagos-fur-seal-1.jpg', NOW(), NOW()),
('c988f62b-1336-41a7-9c45-f8a22b7b4c1a', 'Radis', 'Petit légume piquant, idéal en salade', 1.00, 'https://media.venturatravel.org/unsafe/800x600/smart/gal/animal/galapagos-fur-seal-1.jpg', NOW(), NOW()),
('83b378e6-35ad-41ca-8d42-605ecb4c0197', 'Concombre', 'Légume frais et hydratant', 1.50, 'https://media.venturatravel.org/unsafe/800x600/smart/gal/animal/galapagos-fur-seal-1.jpg', NOW(), NOW());
``

Ensuite, vous pouvez lancer l'application grace au docker-compose. En visitant votre http://localhost:5000/produits, vous vous retrouverez face à une page de connexion, inscrivez vous d'abord puis connectez vous et commencez à utiliser l'application : vous pouvez consulter le catalogue de produits, constituer un panier et commander.

Cependant, certaines options vous sont bloquées, ce sont les actions côté commerçant. Vous pouvez accéder à ces parties en vous connectant avec un utilisateur admin.

Une commande SQL pour ajouter un utilisateur admin : 

``
INSERT INTO "UTILISATEURS" (nom_utilisateur, mot_de_passe, admin, date_creation, date_modification) VALUES
('Charlie', '$2b$12$Lr4sJF7crhWXML0EnfHa5u1qb3fmrDxCoKmemCRDsy7gcnSyOHlpW', 1, NOW(), NOW());
``

``
nom d'utilisateur : Charlie
mot de passe : motdepasseadmin
``

Vous avez maintenant accès aux fonctions commerçant comme ajouter, modifier ou supprimer des produits du catalogue ou bien supprimer les commandes une fois qu'elles ont été réalisées.

## Problèmes rencontrés

Le temps accordé pour développer le projet était assez cours, ce qui nous a demandé beaucoup d'efforts pour assimiler rapidement toutes les notions vues en cours (notamment pour l'authentification jwt) 

A ce propos, un des membres du groupe n'avait encore jamais travaillé sur docker auparavent, il a donc fallu prendre le temps de lui faire revoir tous les concepts et les opérations utiles pour par la suite réussir à se répartir le travail indépendamment des contraintes logicielles. Les premiers TP bien que très utiles et instructifs ne lui suffisaient pas à bien assimiler les concepts.

De plus, même si le côté front-end n'était pas un critère d'évaluation, nous avons estimé que réaliser une application full-stack sans front aurait été dommage. Nous nous sommes donc investis afin de comprendre comemnt fonctionne le moteur de template Jinja et mobiliser des connaissances pas toujours complètement acquises en HTML et CSS.

Enfin, dans l'architecture du projet, nous avons des modèles permettant de spécifier sous quel format les données sont sauvegardées sous forme d'attributs dans la base de données. Les interactions entre les attributs avec la notion de clés primaire et étrangères venait juste d'être découverte dans le cadre du développement d'API. Cela aussi nous a demandé du temps pour réaliser les opérations correctement.

## Point d'amélioration

Avec plus de temps, nous aurions aimé écrire des tests unitaires, s'ils avaient pu être abordés dans le cours.

## Contributeurs

Ce projet a été développé par Van-Minh Christophe LE (étudiant 5e année filière DSIA) et Paul JUREK (étudiant 5e année filière AIC) dans le cadre de l'unité "Application full stack data" dispensée à l'ESIEE PARIS.