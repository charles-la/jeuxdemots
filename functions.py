import sys
import re
import requests
import os
import numpy as np
from dictionnary import *

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

def find_key_by_value(dict, value_to_find):
    for key, value in dict.items():
        if value == value_to_find:
            return key
    return None

def extraire_elements(text,debut,fin):
    pattern = f"{debut}(.*?){fin}"
    match = re.findall(pattern, text, re.DOTALL)
    if match:
        return ''.join(match)
    else:
        return "marker fin pas trouve"

# chaine = dumb.txt
# relation = r_isa, ... , 
# id = nodeId
# deduction = (transitivity, induction, deduction)
# sens = e (entrant), s (sortant), es (entrant et sortant)
def trouver_voisins(chaine,relation,id,deduction,sens):
    
    # Séparer la chaîne en lignes
    lignes = chaine.split('\n')

    voisin = []

    # Parcourir chaque ligne, extraire le noeud different du id et l'ajouter à la liste
    for ligne in lignes:
        if ligne.startswith("r;"):
            elements = ligne.strip().split(';')

            if((int(elements[4]) == relation)): #and len(elements)==8        
                relation_name = find_key_by_value(tableau_correspondance_relation, int(elements[4]))
                if(int(elements[3]) == id and (sens == 'e' or sens == 'es')): # Relation Entrante
                    voisin.append((int(elements[2]), int(elements[5]),deduction,relation_name))
                if(int(elements[2]) == id and (sens == 's' or sens == 'es')): # Relation Sortante
                    voisin.append((int(elements[3]), int(elements[5]),deduction,relation_name))

            if(relation == "All" and int(elements[4]) != 6):
                relation_name = find_key_by_value(tableau_correspondance_relation, int(elements[4]))
                if(int(elements[3]) == id and (sens == 'e' or sens == 'es')): # Relation Entrante
                    voisin.append((int(elements[2]), int(elements[5]),deduction,relation_name))
                if(int(elements[2]) == id and (sens == 's' or sens == 'es')): # Relation Sortante
                    voisin.append((int(elements[3]), int(elements[5]),deduction,relation_name))

    return voisin

def trouver_nom(chaine, eid):

    # Séparer la chaîne en lignes
    lignes = chaine.split('\n')

    name = ''

    # Regex pattern to match numbers [0-9] and symbols (non-alphanumeric characters)
    pattern = '[0-9\W_]+'

    for ligne in lignes:
        if ligne.startswith("e;"):
            elements = ligne.strip().split(';')
            if int(elements[1]) == eid:
               name = elements[2]

    # Replace the matched patterns with an empty string (remove them)
    clean_name = re.sub(pattern, '', name)

    return clean_name


def trouver_voisins_communs(liste1, liste2):
    # Initialiser une liste pour stocker les nombres communs
    tuples_associes = []

    # Parcourir les tuples de la première liste
    for tuple1 in liste1:
        # Vérifier si le nombre est présent dans les tuples de la deuxième liste
        for tuple2 in liste2:
            if tuple1[0] == tuple2[0]:
                poids = np.sqrt((tuple1[1] if tuple1[1] is not None else 0)**2 + 
                                (tuple2[1] if tuple2[1] is not None else 0)**2)
                tuples_associes.append((tuple1[0],poids,tuple1[2],tuple1[3],tuple2[3]))

    return tuples_associes


def trouver_voisin_important(c_voisins):
    # Trier les triplets en fonction du deuxième élément
    c_voisins_tries = sorted(filter(lambda x: x[1] != 0, c_voisins), key=lambda x: x[1])
    
    return c_voisins_tries

def trouver_une_relation_direct(chaine,eid1,eid2,relation):
     # Séparer la chaîne en lignes
    lignes = chaine.split('\n')

    relation_direct = False

    for ligne in lignes:
        if ligne.startswith("r;"):
            elements = ligne.strip().split(';')
            if int(elements[2]) == eid1 and int(elements[3]) == eid2 and int(elements[4]) == relation:
               relation_direct = True

    return relation_direct