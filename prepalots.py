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
import sys
import shutil

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


def renommage_files(csv,coll):
    """
    Fonction qui renomme les pdf dans une version normée NomCollection_annee_mois_numérod'item.pdf
    :param csv: nom du fichier contenant les métadonnées
    :type param: str
    :param coll: nom abrégé de la collection traitée, correspond au NomCollection dans le nom des pdf
    :type coll: str
    :return: pdf renommés et csv avec une nouvelle colonne correspondant à ce nouveau nom
    """
    # lecture du csv métadonnées
    df = pd.read_csv(csv, sep=",")
    # pour chaque fichier pdf du dossier pdf
    for el in os.listdir("PDF"):
        # on récupère la ligne correspondant au fichier dans le csv
        ligne_MD = df[df['nom_pdf']==el]
        # si la ligne est vide on la passe
        if ligne_MD.empty:
            print(" > Les PDF sont déjà renommés")
        else:
            # sinon on récupère l'année, le mois et le numéro d'item du fichier
            annee = int(ligne_MD.iloc[0]['annee'])
            mois = int(ligne_MD.iloc[0]['mois'])
            mois = f'{mois:02d}'
            num_item = int(ligne_MD.iloc[0]['item'])
            num_item_propre = f'{num_item:04d}'
            ### on créé le nouveau nom du document
            nom = f'/{coll}_{annee}_{mois}_{num_item_propre}.pdf'
            # on renomme le document
            os.rename("PDF/" + el, 'PDF' + nom)
            # on ajoute le nouveau nom dans le csv
            df.at[num_item - 1, 'nv_nom_pdf'] = nom
    #on imprime la nouvelle colonne dans le fichier csv
    df.to_csv(csv)

def create_lots(df_line, thematique):
    """Fonction qui créé des lots pour import dans iPubli par la suite"""
    num_item = f'{df_line["item"]:04d}'
    if thematique:
        path = f'Lots/{df_line["categorie"]}/item{num_item}'
    else:
        path = f'Lots/item_{num_item}'
    isExist = os.path.exists(path)
    if not isExist:
        os.makedirs(path)
    # renvoi du chemin obtenu
    return path


def dispatch_PDF(csv, thematique):
    """
    fonction qui dispatch les PDF dans le lot correspondant
    :param csv: csv contenant les métadonnées des documents traités
    :type csv: str
    """
    df = pd.read_csv(csv, sep=",")
    for n in range(len(df)):
        df_line = df.iloc[n]
        path = create_lots(df_line, thematique)
        nom_pdf = df_line["nv_nom_pdf"]
        try:
            os.rename(f'PDF{nom_pdf}', f'{path}{nom_pdf}')
        except FileNotFoundError as e:
            print(e)
            print(f"Le fichier PDF{nom_pdf} n'existe pas ou a déjà été déplacé dans le fichier item correspondant.")


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


def creation_content(dir, license):
    """
    Fonction qui récupère les éléments présents dans le dossier et créé le fichier content à partir de ceux-ci
    :param dir: chemin vers le dossier lot
    :type dir: str
    :param license: bool qui indique si la licence des comités d'histoire sera présente dans les lots
    :type license: bool
    :return: fichier content détaillant le contenu du lot
    """
    # pour chaque fichier du dossier
    for el in os.listdir(dir):
        # si le fichier traité est le pdf de l'article
        if "pdf" in el:
            # on ouvre le fichier content
            with open(dir+"/contents", "a") as f:
                # on ajoute le nom du fichier avec sa description
                f.write(el+"\t\tbundle:ORIGINAL\t\tdescription:Lire l'article PDF\n")
        elif "jpg" in el or "jpeg" in el or "png" in el:
            with open(dir+"/contents","a") as f:
                f.write(el+"\n")
        if license:
            with open(dir+"/contents", "a") as f:
                f.write("license.txt\t\tbundle: LICENSE\t\tdc.title: license.txt\n")
    # mobilisation de la fonction windows2unix qui permet d'encoder le fichier contents en unix
    windows2unix(dir)

def copy_license():
    """
    Fonction qui ajoute la license à chaque item
    """
    for el in os.listdir("Lots"):
        shutil.copy("license.txt", "Lots/"+el+"/license.txt")


@click.command()
@click.option("csv", type=str)
@click.option("coll", type=str)
@click.option("-l","--lic","license", is_flag=True, default=False, help="Ajout de la license du Comité Histoire")
@click.option("-t", "--them", "thematique", is_flag=True, default=False, help="si création avec dossier thématique")
@click.option("-p", "--pdf", "dispatchtexte", is_flag=True, default=False, help="si on veut dispatcher des pdf")
@click.option("-r", "--rename", "renamefiles", is_flag=True, default=False, help="si on veut renommer les fichiers")
@click.option("-i", "--img","dispatchimages", is_flag=True, default=False, help="si on veut dispatcher des images")
@click.option("-c", "--content", "contentcreation", is_flag=True, default=False, help="si on veut que le content soit créé")
def automate_file(csv,coll,license, thematique, dispatchtexte, renamefiles, dispatchimages, contentcreation):
    """
    Script qui permet la construction d'un lot de document pour import dans Dspace
    :param csv: tableur contenant les métadonnées nécessaires à la construction des lots (pour chaque document: nom du pdf,
    numéro d'item, mois et année de parution)
    :type csv: str
    :param coll: nom de la collection des documents traités
    :type coll: str
    Ces deux éléments sont nécessaires si l'on renommer les fichiers et dispatcher les pdf dans les lots.
    :param license: indication click si l'on souhaite l'ajout de la licence aux items
    :param thematique: indication click si l'on souhaite la structuration des dossiers items en dossiers thématiques
    :param dispatchtexte: indication click si l'on souhaite dispatcher dans chaque lot le pdf correspondant
    :param renamefiles: indication click si l'on souhaite renommer les fichiers et items
    :param dispatchimages: indication click si l'on souhaite dispatcher dans chaque lot une image
    :param contentcreation: indication click si l'on souhaite créer le content dans chaque lot
    """
    if renamefiles:
        if csv and coll:
        # on lance le renommage des fichiers avec la fonction renommage_files
            print(" > Renommage des PDF")
            renommage_files(csv,coll)
        elif csv:
            print("Il manque l'indication de collection pour renommer correctement les fichiers. Relancer la commande en "
                  "y ajoutant la collection traitée.")
        elif coll:
            print("Il manque le csv de métadonnées permettant de renommer les fichiers. Consulter la procédure, préparer le tableur et relancer la commande.")
        else:
            print("Il manque l'indication de collection et le csv de métadonnées pour renommer correctement les fichiers. Consulter la procédure, préparer le programme et relancer la commande")


    if dispatchtexte:
        if csv and coll:
            # on lance le renommage des fichiers avec la fonction renommage_files
            print(" > Ajout des PDF dans leur dossier item")
            dispatch_PDF(csv, thematique)
        elif csv:
            print("Il manque l'indication de collection pour renommer correctement les fichiers. Relancer la commande en "
                  "y ajoutant la collection traitée.")
        elif coll:
            print("Il manque le csv de métadonnées permettant de renommer les fichiers. Consulter la procédure, préparer le tableur et relancer la commande.")
        else:
            print("Il manque l'indication de collection et le csv de métadonnées pour renommer correctement les fichiers. Consulter la procédure, préparer le programme et relancer la commande")


    # pour chaque lot dans le dossier
    for dir in os.listdir("Lots"):
        dir = f'Lots/{dir}'
        # création du  fichier métadata en mobilisant la fonction creation_metadata
        creation_metadata(dir)

        # création du fichier content en mobilisant la fonction creation_content
        creation_content(dir, license)
    print(" > Ajout des fichiers metadata et content")
    print(""" > Les items sont récupérables dans le dossier Lots. \n
                            - Renommage des PDF
                            - Création des dossiers items si non existants
                            - Ajout des PDF dans le dossier item correspondant
                            - Ajout des fichiers metadata et contents 
                    """)
    # Si une license est demandée, on l'ajoute dans chaque item
    if license:
        print(" > Ajout des licences")
        copy_license()


if __name__ == "__main__":
    automate_file()

