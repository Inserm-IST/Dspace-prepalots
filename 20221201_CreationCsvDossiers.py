import os
import pandas as pd
import click



@click.command()
@click.argument("dossier", type=str)
@click.option("-t","--them","thematique",is_flag=True, default=False, help="Si sous dossiers")
def get_pdf(dossier,thematique):
    """
    Fonction qui récupère les noms des différents PDF et les ajoute dans un csv
    :param dossier: nom du chemin vers les PDF
    :type dossier: str
    :return:
    """
    liste_dir = []
    liste_pdf = []
    num_item = 0
    num_liste = []
    if thematique:
        for dir in os.listdir(dossier):
            pdf = os.listdir(f'{dossier}/{dir}')
            for el in pdf:
                if 'pdf' in el:
                    liste_dir.append(dir)
                    liste_pdf.append(el)
                    num_item += 1
                    num_liste.append(num_item)
    else:
        pdf = os.listdir(f'{dossier}')
        for el in pdf:
            if 'pdf' in el:
                liste_dir.append(dossier)
                liste_pdf.append(el)
                num_item += 1
                num_liste.append(num_item)

    df = pd.DataFrame({'item': num_liste, 'nom_pdf': liste_pdf, 'categorie': liste_dir})

    df.to_csv('pdf.csv')
    print("le fichier pdf.csv est créé.")

if __name__ == "__main__":
    get_pdf()
