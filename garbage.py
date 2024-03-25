
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



