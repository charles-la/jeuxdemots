import sys
import re
import requests
import time
import os

from dictionnary import *
from functions import * 

separation_label = "---------------------------------------------------------------------------------------------------------------"
erreur_label = "-----> ERREUR ----->"

def main(arg):

    print(separation_label)
    print(f'Voici vos arguments : {arg}')
    print(separation_label)
    
    if len(sys.argv) >= 4:
        
        # remove_all_files_in_folder('output/') #### Supprimer cache
        
        chemin_arg1 = f"output/{arg[1]}.txt"
        chemin_arg3 = f"output/{arg[3]}.txt"

        if os.path.exists(chemin_arg1):
            print(f"Le fichier {arg[1]}.txt existe.")
            with open(chemin_arg1, 'r') as file:
                a_code_txt = file.read()
        else:
            print("Le fichier n'existe pas.")
            a_dumb_txt = recup_fichier_jdm(arg[1])

            # Extraction du premier mot
            a_code_txt = extraire_elements(a_dumb_txt,"<CODE>","</CODE>")
            write_to_file(a_code_txt,f'{arg[1]}.txt')


        if os.path.exists(chemin_arg3):
            print(f"Le fichier {arg[3]}.txt existe.")
            with open(chemin_arg3, 'r') as file:
                b_code_txt = file.read()
        else:
            print(f"Le fichier {arg[3]}.txt n'existe pas.")
            b_dumb_txt = recup_fichier_jdm(arg[3])
                
            # Extraction du deuxieme mot
            b_code_txt = extraire_elements(b_dumb_txt,"<CODE>","</CODE>")
            write_to_file(b_code_txt,f'{arg[3]}.txt')


        # Enregistrer le temps de début
        start_time = time.time()
        
        print(separation_label)

        a_id = int(extraire_elements(a_code_txt,"\(eid=","\)"))
        b_id = int(extraire_elements(b_code_txt,"\(eid=","\)"))
        print(f'{arg[1]} eid is : {a_id}')
        print(f'{arg[3]} eid is : {b_id}')

        # Convertir le nom de la relation en nombre pour utiliser les relations de jeu de mots
        if arg[2] in tableau_correspondance_relation:
            num_relation = tableau_correspondance_relation[arg[2]]
            print(f'{arg[2]} est la relation : {num_relation}')
        else:
            print(erreur_label +" La relation entrée n'existe pas")
            exit()


        ## Direct relation
        print(separation_label) 
        print('Direct Relation')
        
        relation_direct = trouver_une_relation_direct(a_code_txt,a_id,b_id,num_relation)

        if relation_direct == True:
            print(f"La relation {arg[1]} {arg[2]} {arg[3]} existe dans jeudemots")

        # print(f"La relation {arg[1]} {arg[2]} {arg[3]} n'existe pas dans jeudemots")    
        

        print(separation_label)
        
        c_voisins = []

        ## TRANSITIVITE
        print('Transitivity')
        # si la relation est r-agent-1, on regarde la transitivite
        a_voisins = trouver_voisins(a_code_txt,num_relation,a_id,'Transitivity','es')
        b_voisins = trouver_voisins(b_code_txt,num_relation,b_id,'Transitivity','es')   
        c_voisin_temp = trouver_voisins_communs(a_voisins,b_voisins)
        print(f'{c_voisin_temp[0:2]} ..... {len(c_voisin_temp)} inferences')
        c_voisins += c_voisin_temp
        
        print(separation_label)

        ## INDUCTION
        print('Induction')
        a_voisins = trouver_voisins(a_code_txt,'All',a_id,'Induction','s')
        b_voisins = trouver_voisins(b_code_txt,num_relation,b_id,'Induction','e')   
        c_voisin_temp = trouver_voisins_communs(a_voisins,b_voisins)
        print(f'{c_voisin_temp[0:2]} ..... {len(c_voisin_temp)} inferences')
        c_voisins += c_voisin_temp
        
        print(separation_label)

        ## DEDUCTION
        print('Deduction')
        # le numero de la relation r_isa = 6
        a_voisins = trouver_voisins(a_code_txt,6,a_id,'Deduction','s')
        b_voisins = trouver_voisins(b_code_txt,num_relation,b_id,'Deduction','e')   
        c_voisin_temp = trouver_voisins_communs(a_voisins,b_voisins)
        print(f'{c_voisin_temp[0:2]} ..... {len(c_voisin_temp)} inferences')
        c_voisins += c_voisin_temp

        ## afficher les 10 premieres inference
        c_voisins_important_ordre = trouver_voisin_important(c_voisins)
        c_voisins_important = []
        
        # Affichage des resultats
        print(separation_label)
        print('Resultat - 10 principales inferences')
        if(c_voisins_important_ordre != None and len(c_voisins_important_ordre) > 0):
            
            num_inference = len(c_voisins_important_ordre)
            if(num_inference >= 10):
                num_inference = 10

            for i in range(num_inference):
                ## Apres afficher linference principal
                c_voisins_important = c_voisins_important_ordre[i]            
                c_name = trouver_nom(a_code_txt,c_voisins_important[0])

                if(c_voisins_important[2]=='Transitivity'):
                    print(f'{i+1} : \'{arg[1]}\' {arg[2]} \'{arg[3]}\' --> oui, car par transitivite \'{arg[1]}\' {arg[2]} \'{c_name}\' et \'{c_name}\' {arg[2]} \'{arg[3]}\'')
                if(c_voisins_important[2]=='Deduction'):
                    print(f'{i+1} : \'{arg[1]}\' {arg[2]} \'{arg[3]}\' --> oui, car par deduction \'{arg[1]}\' r_isa \'{c_name}\' et \'{c_name}\' {arg[2]} \'{arg[3]}\'')      
                if(c_voisins_important[2]=='Induction'):
                    print(f'{i+1} : \'{arg[1]}\' {arg[2]} \'{arg[3]}\' --> oui, car par induction \'{arg[1]}\' {c_voisins_important[3]} \'{c_name}\' et \'{c_name}\' {arg[2]} \'{arg[3]}\'')


            # Add the inference in the code
            # r;rid;node1;node2;type;w;w_normed;rank
            
            # relation a vers b (sortante)
            inferrence_to_add_1 = '\n' + f'r;null;{a_id};{b_id};{num_relation};{int(round(c_voisins_important[1]))}' 
            
            # relation a vers b (entrante)
            inferrence_to_add_2 = '\n' + f'r;null;{b_id};{a_id};{num_relation};{int(round(c_voisins_important[1]))}'
            
            with open(chemin_arg1, 'a') as file:
                file.write(inferrence_to_add_1)

            with open(chemin_arg3, 'a') as file:
                file.write(inferrence_to_add_2)

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
