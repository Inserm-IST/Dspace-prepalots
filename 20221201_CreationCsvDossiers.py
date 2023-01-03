import os
import pandas as pd
import click



@click.command()
@click.argument("dir", type=str)
def get_pdf(dossier):
    """
    Fonction qui récupère les noms des différents PDF et les ajoute dans un csv
    :param dir: nom du chemin vers les PDF
    :type dir: str
    :return:
    """
    liste_dir = []
    liste_pdf = []
    num_item = 0
    num_liste = []
    for dir in os.listdir(dossier):
        pdf = os.listdir(dossier + dir)
        for el in pdf:
            print(el)
            if 'pdf' in el:
                liste_dir.append(dir)
                liste_pdf.append(el)
                num_item += 1
                num_liste.append(num_item)

    df = pd.DataFrame({'item': num_liste, 'nom_pdf': liste_pdf, 'categorie': liste_dir})

    df.to_csv('pdf.csv')
    print("le fichier pdf.csv est créé.")

if __name__ == "__main__":
    automate_file()
