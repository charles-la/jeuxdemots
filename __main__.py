import sys
import re
import requests

from dictionnary import *
from functions import * 

separation_label = "----------------------------------------------------------------------------------------------------------"

def main(arg):

    print(separation_label)
    print(f'Voici vos arguments : {arg}')
    print(separation_label)

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

        print(a_id)

        ## TRANSITIVITE
        # Convertir le nom de la relation en nombre pour utiliser les relations de jeu de mots
        num_relation = tableau_correspondance_relation[arg[2]]

        a_voisins_transitivite = trouver_voisins(a_code_txt,num_relation,a_id)
        b_voisins_transitivite = trouver_voisins(b_code_txt,num_relation,b_id)   
        
        print(a_voisins_transitivite)
        print(b_voisins_transitivite)

        print(trouver_nombres_communs(a_voisins_transitivite,b_voisins_transitivite))
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

if __name__ == "__main__":
    main(sys.argv)