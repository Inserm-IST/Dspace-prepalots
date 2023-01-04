# Dspace-prepalots

Programme python permettant de construire automatiquement les lots de documents conformes au standard de Dspace pour leur import en masse. <br/>
Il a été développé pour une préparation facilitée des documents à importer des documents d'[iPubli](https://www.ipubli.inserm.fr/), l'archive ouverte institutionnelle de l'Inserm, gérée par le service de l'Information Scientifique et Technique.<br/>
Le script reste générique et est donc réemployable sur tout autre projet d'import de documents via Batch Import sur un site en Dspace. Il s'emploie à la suite du programme python qui génère les fichiers XML Dublin core contenant les métadonnées des documents, récupérable [ici](https://www.github.com/Inserm-IST/Dspace-csv2XMLDB).

## Guide d'utilisation
Une procédure est disponible dans le dossier Documentation pour la création du csv à traiter puis le lancement du programme. <br/>
Le tableur <i>métadonnées</i> décrit les différentes métadonnées disponibles et traitables par le programme.<br/>
Un exemple de dossier de travail est disponible dans le dossier Exemple. Il contient un fichier PDF, où se trouvent les fichiers PDF des documents à dispatcher dans les lots et un exemple de tableur de métadonnées. Le dossier Lots correspond au résultat obtenu par le programme à partir de ces données.

## Crédits
Ce projet a été réalisé par le DISC-IST.
- Michel Pohl: Directeur adjoint du service de l'Information Scientifique et Technique de l'Inserm
- Juliette Janes: Responsable informatique du projet
- Charlotte Iizuka: Responsable éditoriale d'iPubli

## Conditions d'utilisation
![68747470733a2f2f692e6372656174697665636f6d6d6f6e732e6f72672f6c2f62792f322e302f38387833312e706e67](https://user-images.githubusercontent.com/56683417/115525743-a78d2400-a28f-11eb-8e45-4b6e3265a527.png)

## Contacts
Pour toute question, contactez l'adresse générique du projet iPubli: ipubli@inserm.fr
