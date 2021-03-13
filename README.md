# stockage-azure

Le but de ce brief était d'intégrer des fonctionnalités de stockage Azure Blob dans une application développée en Python et l'application des bonnes practique de programmation.

## Technologies utilisées

  Azure.store.blog
  configparser
  logging

## Installation

   Pour l'installation de modulès necessaires au lancement du script veuillez utiliser la commande:
   pip install -r requirements.txt
    
## Configuration

   A fin de configurer vos propres credentielles sur le fichier config.ini veuillez remplir les variables de la manière suivante :
   
   [general]
   restoredir=data
   [storage]
   account=nom_du_compte_de_stockage
   container=nom_du_conteneur
   key=cle_dacces

  Ces information peuvent être retrouver sur votre compte azure.
  
## Mode d'emploi
   python main.py
    option: -h : manuelle
            -cfg : fichier de configuration, par défaut config.ini
            -lvl : niveau de logging - debug, info, warning, error, critical. Par défaut info
   {
   upload : chargement d'un fichier passer en argument comme blob sur un conteneur,
   download : téléchargement d'un blob sur le dossier data,
   list: liste de tous les blobs dans conteneur
   }
   
   ex : 
    chargemnt : python main.py upload README.md
    téléchargement : python main.py download README.md
    liste  : python main.py list
    Spécifier fichier de configuration : python main.py -cfg config_user.ini upload README.md
    Spécifier niveau de logging : python main.py -lvl debug upload README.md
