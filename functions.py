import sys
import re
import requests
import os

def recup_fichier_jdm(terme):

    base_url = "https://www.jeuxdemots.org/rezo-dump.php"
    params = {
        "gotermsubmit": "Chercher",
        "gotermrel": terme,
        "rel": ""
    }
 
    response = requests.get(base_url, params=params)
    print(f'Search for "{terme}" in jeuxdemots database')

    if response.status_code == 200:
        return response.text
    else:
        print("Query Failed. Status code:", response.status_code)
        return None


# write file in the repo
def write_to_file(data, filename):
    filename = 'output/'+filename
    with open(filename, 'w') as file:
        print(f'Create file ---> {filename}')
        file.write(data)


def remove_all_files_in_folder(folder_path):
    # List all elements in the folder
    elements = os.listdir(folder_path)

    # Iterate over each element
    for element in elements:
        # Construct the full path of the element
        element_path = os.path.join(folder_path, element)
        
        # Check if the element is a file
        if os.path.isfile(element_path):
            # If it's a file, remove it
            print(f'Remove ---> {element_path}')
            os.remove(element_path)


def extraire_elements(text,debut,fin):
    pattern = f"{debut}(.*?){fin}"
    match = re.findall(pattern, text, re.DOTALL)
    if match:
        return ''.join(match)
    else:
        return "marker fin pas trouve"


def trouver_voisins(chaine,relation,id):
    
    # Séparer la chaîne en lignes
    lignes = chaine.split('\n')

    # Initialiser une liste pour stocker les quatrièmes éléments
    quatriemes_elements = []

    # Parcourir chaque ligne, extraire le noeud different du id et l'ajouter à la liste
    for ligne in lignes:
        if ligne.startswith("r;"):
            elements = ligne.strip().split(';')
            if((int(elements[4]) == relation) and len(elements)==8):
                if(int(elements[3]) == id):
                    quatriemes_elements.append((int(elements[2]), int(elements[7])))
                if(int(elements[2]) == id):
                    quatriemes_elements.append((int(elements[3]), int(elements[7])))
            if((int(elements[4]) == relation) and len(elements)!=8):
                if(int(elements[3]) == id):
                    quatriemes_elements.append((int(elements[2]), None))
                if(int(elements[2]) == id):
                    quatriemes_elements.append((int(elements[3]), None))

    return quatriemes_elements

def trouver_nombres_communs(liste1, liste2):
    # Initialiser une liste pour stocker les nombres communs
    tuples_associes = []

    # Parcourir les tuples de la première liste
    for tuple1 in liste1:
        # Extraire le premier élément du tuple
        nombre = tuple1[0]

        # Vérifier si le nombre est présent dans les tuples de la deuxième liste
        for tuple2 in liste2:
            if nombre == tuple2[0]:
                tuples_associes.append(tuple2)

    return tuples_associes


# def trouver_nombres_communs(liste1, liste2):
#     # Initialiser une liste pour stocker les nombres communs
#     nombres_communs = []

#     # Parcourir les éléments de la première liste
#     for nombre in liste1:
#         # Vérifier si le nombre est présent dans la deuxième liste et s'il n'a pas déjà été ajouté
#         if nombre in liste2 and nombre not in nombres_communs:
#             nombres_communs.append(nombre)

#     return nombres_communs


# def trouver_nombres_avant_pattern(chaine, pattern):

#     # Séparer la chaîne en lignes
#     lignes = chaine.split('\n')

#     # Initialiser la liste pour stocker les nombres trouvés
#     nombres = []

#     # Parcourir chaque ligne et rechercher le motif
#     for ligne in lignes:
#         if ligne.startswith("r"):
#             matches = re.findall(r'(\d+)' + re.escape(pattern), ligne)
#             nombres.extend([int(match) for match in matches])

#     return nombres