"""
Script qui permet la construction automatique des lots pour import par batch dans Dspace
    - Renommage des items
    - Création du content
    - Création du métadata
Auteur:Juliette Janes
Date:01/12/2022
"""

from lxml import etree
import os
import click
import pandas as pd

def creation_metadata(dir):
    """
    Fonction qui ajoute le fichier métadata au dossier traité
    :param dir: chemin vers le dossier lot
    :type dir: str
    :return: fichier XML nommé metadata qui paramètre Dspace pour la construction des métadonnées
    """
    # on créé une balise XML racine nommé dublin_core avec pour attribut schema qui a une valeur inserm
    racine = etree.Element("dublin_core", schema="inserm")
    # on associe à cette balise une sous balise dc_value avec pour attribut language (valeur autocreation) et element
    # (valeur lexicon)
    langage1 = etree.SubElement(racine,"dcvalue", language="",qualifier="autocreation", element="lexicon")
    # on ajoute le texte true encadrée par la balise language précédemment créée
    langage1.text="true"
    # on associe à la balise racine une deuxième sous balise language similaire avec des valeurs d'attribut différentes
    langage2 = etree.SubElement(racine,"dcvalue", language="",qualifier="conversion", element="bitstream")
    # on ajoute le texte true dans la balise langage 2
    langage2.text = "true"
    # on transforme la balise racine en un arbre XML
    racine = etree.ElementTree(racine)
    # on imprime l'arbre XML racine dans un fichier metadata.xml dans le dossier lot traité
    racine.write(dir + "/metadata_inserm.xml", encoding="utf-8")


def renommage_files(csv):
    """
    Fonction qui renomme les items
    :param csv: nom du fichier contenant les métadonnées
    """
    df = pd.read_csv(csv, sep=",")
    for el in os.listdir("test_PDF"):
        ligne_MD = df[df['nom pdf']==el]
        annee = ligne_MD.iloc[0]['annee']
        mois = ligne_MD.iloc[0]['mois']
        mois = f'{mois:02d}'
        num_item = ligne_MD.iloc[0]['item']
        num_item = f'{num_item:04d}'
        ### problème dans la récupération des items
        nom = "/CR_"+str(annee)+"_"+str(mois)+"_"+str(num_item)+".pdf"
        os.rename("test_PDF/" + el, 'test_PDF'+ nom)

def dispatch_PDF(dir):
    """
    fonction qui dispatch les PDF dans le lot correspondant
    :param dir: chemin vers le dossier lot
    :return:
    """
    


def windows2unix(dir):
    """
    Fonction qui permet de transformer un fichier contents encodé sous windows en fichier linux
    :param dir: chemin vers le dossier lot
    :type dir: str
    :return: fichier content encodé en unix
    """
    # création des chaînes de remplacement
    WINDOWS_LINE_ENDING = b'\r\n'
    UNIX_LINE_ENDING = b'\n'
    # chemin du fichier traité
    file_path = dir + "\contents"
    # ouverture du fichier et lecture
    with open(file_path, 'rb') as open_file:
        content = open_file.read()
    # remplacement des lignes windows par ligne unix
    content = content.replace(WINDOWS_LINE_ENDING, UNIX_LINE_ENDING)
    # impression du nouveau contenu dans un fichier unix
    with open(file_path, 'wb') as open_file:
        open_file.write(content)


def creation_content(dir):
    """
    Fonction qui récupère les éléments présents dans le dossier et créé le fichier content à partir de ceux-ci
    :param dir: chemin vers le dossier lot
    :type dir: str
    :return: fichier content détaillant le contenu du lot
    """
    # pour chaque fichier du dossier
    for el in os.listdir(dir):
        # si le fichier traité est le pdf de l'article
        if "pdf" in el:
            # on ouvre le fichier content
            with open(dir+"/contents", "a") as f:
                # on ajoute le nom du fichier avec sa description
                f.write(el+"\t\tdescription:Lire l'article PDF\n")
        elif "jpg" in el or "jpeg" in el or "png" in el:
            with open(dir+"/contents","a") as f:
                f.write(el+"\n")
    # mobilisation de la fonction windows2unix qui permet d'encoder le fichier contents en unix
    windows2unix(dir)


@click.command()
@click.argument("dossier", type=str)
@click.argument("csv", type=str)
def automate_file(dossier, csv):
    """
    """
    # on lance le renommage des fichiers avec la fonction renommage_files
    renommage_files(csv)
    # pour chaque lot dans le dossier
    for item in os.listdir(dossier):
        # on stocke le chemin vers le lot traité
        dir = dossier + "/" + item+"/"
        # on indique à l'utilisateur le traitement du lot
        print("Traitement du lot " + item)
        # on dispatche les PDF dans les lots correspondants
        dispatch_PDF(dir)
        # création du  fichier métadata en mobilisant la fonction creation_metadata
        creation_metadata(dir)
        # création du fichier content en mobilisant la fonction creation_content
        creation_content(dir)



if __name__ == "__main__":
    automate_file()

