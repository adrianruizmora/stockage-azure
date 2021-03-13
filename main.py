import sys
import argparse
import configparser
import logging
import os.path
from azure.storage.blob import BlobServiceClient, ContainerClient, BlobClient
"""
Biblithèque natives du python:
    1. sys - permet l'accès au variables ou fonctions de l'interpreteur.
    2. argparse - définie les argumetns nécessaires pour lancer un programme par le CLI.
    3. configparser - permet l'implémentation d'une configuration basique.
    4. logging - permet d'implémenter un système de logging.
    5. os.path - permet d'implémenter des fonctions pour les nom de chemins.
Biblithèque client de Azure Storage blob:
    1. BlobServiceClient - Un client pour intéragir avec le Blob Service à un niveau du compte.
    2. ContainerClient - Un client pour intéragir avec un contenuer spécifique.
    3. BlobClient - Permet de manipuler les Azure Storage blobs
"""


def listb(args, containerclient):
    """
    Fonction qui necesite un seul paramètres:
        1. containerclient - conteneur dans le compte de stockage du client.
        2. args - pas necessaire pour cette fonction.
    Liste les blobs du contenuer indiqué.
    Ne renvoie rien.
    """
    blob_list=containerclient.list_blobs()
    for blob in blob_list:
        print(blob.name)


def upload(cible, blobclient):
    """
    Fonction qui prend deux paramètres : 
        1. cible - ficier que l'on va manipuler (upload)
        2.blobclient - client qui interagit avec le blob services   
    Charge le blob dans le contenur du client.
    Ne renvoie rien
    """
    with open(cible, "rb") as f:

        blobclient.upload_blob(f)


def download(filename, dl_folder, blobclient):
    """
    Fonction qui prend trois paramètres :
        1. filename - fichier à télécharger.
        2. dl_folder - dossier où l'on va télécharger le fichier.
        3. blobclient - client qui interagit avec le blob services.
    Téléchager le blob et le place dans le dossier créé à cette fin.
    Ne renvoie rien.
    """
    with open(os.path.join(dl_folder,filename), "wb") as my_blob:
        blob_data=blobclient.download_blob()
        blob_data.readinto(my_blob)


def main(args,config):
    """
    Fonction qui s'excute au lancement du programe.
    Prend deux paramètres:
        1. args - arguments passer en ligne de commande :
            a. cfg - fichier de configuration, par defaut config.ini
            b. download/upload/list
            c. lvl - niveau du débugg
        2. config - configuration
    Permet la connexion au client  pour retrouver et configurer les propriétés du compte.
    Ne renvoie rien
    """
    blobclient=BlobServiceClient(
        f"https://{config['storage']['account']}.blob.core.windows.net",
        config["storage"]["key"],
        logging_enable=False)
    containerclient=blobclient.get_container_client(config["storage"]["container"])
    if args.action=="list":
        return listb(args, containerclient)
    else:
        if args.action=="upload":
            blobclient=containerclient.get_blob_client(os.path.basename(args.cible))
            return upload(args.cible, blobclient)
        elif args.action=="download":
            blobclient=containerclient.get_blob_client(os.path.basename(args.remote))
            return download(args.remote, config["general"]["restoredir"], blobclient)
    

if __name__=="__main__":
    """
    Condition execute le script comme programme principale et execution de fonction main.
    Definition d'argparse pour récuperer les arguments par ligne de commande.
    Definition de niveau des logs.
    """
    parser=argparse.ArgumentParser("Logiciel d'archivage de documents")
    parser.add_argument("-cfg",default="config.cfg",help="chemin du fichier de configuration")
    parser.add_argument("-lvl",default="info",help="niveau de log")
    subparsers=parser.add_subparsers(dest="action",help="type d'operation")
    subparsers.required=True
    
    parser_s=subparsers.add_parser("upload")
    parser_s.add_argument("cible",help="fichier à envoyer")

    parser_r=subparsers.add_parser("download")
    parser_r.add_argument("remote",help="nom du fichier à télécharger")
    parser_r=subparsers.add_parser("list")

    args=parser.parse_args()

    #erreur dans logging.warning : on a la fonction au lieu de l'entier
    loglevels={"debug":logging.DEBUG, "info":logging.INFO, "warning":logging.WARNING, "error":logging.ERROR, "critical":logging.CRITICAL}
    print(loglevels[args.lvl.lower()])
    logging.basicConfig(level=loglevels[args.lvl.lower()])

    config=configparser.ConfigParser()
    config.read(args.cfg)

    sys.exit(main(args,config))