import sys
import re
import requests
import time

from dictionnary import *
from functions import * 


separation_label = "----------------------------------------------------------------------------------------------------------"

def main(arg):

    print(separation_label)
    print(f'Voici vos arguments : {arg}')
    print(separation_label)

    # Enregistrer le temps de début
    start_time = time.time()
    
    if len(sys.argv) >= 4:
        print(separation_label)
        # remove_all_files_in_folder('output/')
        # a_dumb_txt = recup_fichier_jdm(arg[1])
        # b_dumb_txt = recup_fichier_jdm(arg[3])

        with open('output/piston.txt', 'r') as file:
            a_dumb_txt = file.read()
        with open('output/voiture.txt', 'r') as file:
            b_dumb_txt = file.read()

        # Extraction du premier mot
        a_code_txt = extraire_elements(a_dumb_txt,"<CODE>","</CODE>")
        # a_relation_sortante = extraire_elements(a_code_txt,"// les relations sortantes","// les relations entrantes")
        # a_relation_entrante = extraire_elements(a_code_txt,"// les relations entrantes","// END")

        write_to_file(a_dumb_txt,f'{arg[1]}.txt')
        write_to_file(a_code_txt,f'{arg[1]}_code.txt')

        print(separation_label)

        # Extraction du deuxieme mot
        b_code_txt = extraire_elements(b_dumb_txt,"<CODE>","</CODE>")
        # b_relation_sortante = extraire_elements(b_code_txt,"// les relations sortantes","// les relations entrantes")
        # b_relation_entrante = extraire_elements(b_code_txt,"// les relations entrantes","// END")

        write_to_file(b_dumb_txt,f'{arg[3]}.txt')
        write_to_file(b_code_txt,f'{arg[3]}_code.txt')
        
        print(separation_label)

        a_id = int(extraire_elements(a_code_txt,"\(eid=","\)"))
        b_id = int(extraire_elements(b_code_txt,"\(eid=","\)"))
        print(f'{arg[1]} eid is : {a_id}')
        print(f'{arg[3]} eid is : {b_id}')

        # Convertir le nom de la relation en nombre pour utiliser les relations de jeu de mots
        num_relation = tableau_correspondance_relation[arg[2]]
        print(f'{arg[2]} est la relation : {num_relation}')
        print(separation_label)

        ## TRANSITIVITE
        a_voisins_transitivite = trouver_voisins(a_code_txt,num_relation,a_id,'Transitivity')
        b_voisins_transitivite = trouver_voisins(b_code_txt,num_relation,b_id,'Transitivity')   
        c_voisins_transitivite = trouver_nombres_communs(a_voisins_transitivite,b_voisins_transitivite)

        #### DEBUG ####
        # Trier les triplets en fonction du deuxième élément
        c_voisins_transitivite_tries = sorted(filter(lambda x: x[1] != 0, c_voisins_transitivite), key=lambda x: x[1])

        # Sélectionner le deuxième triplet de la liste triée
        c_voisins_transitive_important = c_voisins_transitivite_tries[0]




        ## INDUCTION
        



        ## DEDUCTION




        print('Transitivity')
        print(c_voisins_transitivite)
        print(separation_label)
        print(c_voisins_transitive_important)


        # Affichage des resultats
        print('Resultat')
        c_id = c_voisins_transitive_important[0]
        if(c_id != None):
            c_name = trouver_nom(a_code_txt,c_id)
            # if(transitif)
            print(f'\'{arg[1]}\' {arg[2]} \'{arg[3]}\' --> oui, car \'{arg[1]}\' {arg[2]} {c_name} et \'{arg[3]}\' {arg[2]} {c_name}')
        else:
            print(f'\'{arg[1]}\' {arg[2]} \'{arg[3]}\' --> non')
        print(separation_label)

    # Enregistrer le temps de fin
    end_time = time.time()

    # Calculer la durée d'exécution
    execution_time = end_time - start_time
    print("Temps d'exécution:", execution_time, "secondes")


if __name__ == "__main__":
    main(sys.argv)








# print(trouver_nombres_communs(b_voisins_sortant_transitivite,a_voisins_entrent_transitivite))

# 113317 - paris

# print(separation_label)
# print(f'Trouver les voisins de "arg[1]"')
# voisin1 = trouver_premiers_voisins(codetxt_1)

# print(separation_label)
# print(f'Trouver les voisins de "arg[2]"')
# voisin2 = trouver_premiers_voisins(codetxt_2)

# print(separation_label)
# print(trouver_nombres_communs(voisin1,voisin2))


# with open('output/matou_code.txt', 'r') as file:
#     codetxt = file.read()

# test = search_word_in_string(codetxt,arg[2])
# print(test)
