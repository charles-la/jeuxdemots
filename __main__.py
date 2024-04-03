import sys
import re
import requests
import time
import os

from dictionnary import *
from functions import * 

separation_label = "----------------------------------------------------------------------------------------------------------"
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

        print('Verifier si la relation direct existe dans jeudemots')
        
        relation_direct = trouver_une_relation_direct(a_code_txt,a_id,b_id,num_relation)

        if relation_direct == True:
            return print(f"La relation {arg[1]} {arg[2]} {arg[3]} existe dans jeudemots")

        print(f"La relation {arg[1]} {arg[2]} {arg[3]} n'existe pas dans jeudemots")    
        


        print(separation_label)

        ## TRANSITIVITE
        print('Transitivity')
        # si la relation est r-agent-1, on ne regarde pas la transitivite
        if(num_relation != 24):

            a_voisins = trouver_voisins(a_code_txt,num_relation,a_id,'Transitivity','es')
            b_voisins = trouver_voisins(b_code_txt,num_relation,b_id,'Transitivity','es')   
            c_voisins = trouver_voisins_communs(a_voisins,b_voisins)
            c_voisins_important = trouver_voisin_important(c_voisins)

            print(c_voisins)
            print(c_voisins_important)
        
        print(separation_label)

        ## INDUCTION
        print('Induction')
        # si la relation est r-agent-1, on ne regarde pas la transitivite
        if(num_relation == 24):
            # changer la relation ici
            a_voisins = trouver_voisins(a_code_txt,8,a_id,'Induction','s')
            b_voisins = trouver_voisins(b_code_txt,num_relation,b_id,'Induction','e')   
            c_voisins = trouver_voisins_communs(a_voisins,b_voisins)
            c_voisins_important = trouver_voisin_important(c_voisins)

            print(c_voisins)
            print(c_voisins_important)
        
        print(separation_label)

        ## DEDUCTION
        print('Deduction')
        if(num_relation == 24):
            # le numero de la relation r_isa = 6
            a_voisins = trouver_voisins(a_code_txt,6,a_id,'Deduction','s')
            b_voisins = trouver_voisins(b_code_txt,num_relation,b_id,'Deduction','e')   
            c_voisins = trouver_voisins_communs(a_voisins,b_voisins)
            c_voisins_important = trouver_voisin_important(c_voisins)

            print(c_voisins)
            print(c_voisins_important)
        
        print(separation_label)
        
        # Affichage des resultats
        print('Resultat')
        ## afficher les 10 premieres inference
        if(c_voisins_important != None):
            c_name = trouver_nom(a_code_txt,c_voisins_important[0])
            if(c_voisins_important[2]=='Transitivity'):
                print('On a ici une relation de transitivite')
                print(f'\'{arg[1]}\' {arg[2]} \'{arg[3]}\' --> oui, car \'{arg[1]}\' {arg[2]} {c_name} et \'{arg[3]}\' {arg[2]} {c_name}')
            if(c_voisins_important[2]=='Deduction'):
                print('On a ici une relation de deduction')
                print(f'\'{arg[1]}\' {arg[2]} \'{arg[3]}\' --> oui, car \'{arg[1]}\' r_isa {c_name} et \'{arg[3]}\' r_agent_1 {c_name}')        
            if(c_voisins_important[2]=='Induction'):
                print('On a ici une relation d\'induction')
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
