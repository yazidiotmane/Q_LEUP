import sys, os
from colorama import *
from outils import *

def afficher_titre(titre):
    string = '\n\t\t' + Back.CYAN + 'Décision foncière v0.1'
    if titre:
        string = string + Style.RESET_ALL + ' / ' + titre
    string = string + '\n\n'
    print(string)


def menu_principal():
    afficher_titre('')
    print('\t[A] - Acquisition des données depuis l\'HCP.')
    print('\t[T] - Translation d\'une installation.')
    print('\t[B] - Balayage avec une installation existante.')
    print('\t[E] - Export d\'un scénario.\n')
    print('\t[Q] - Sortie de l\'application\n')
    choix = input('>> ')
    dispatcher(choix)

def menu_acquistion():
    afficher_titre('Acquisition')
    db.remplir_communes()
    input()
    dispatcher('menu_principal')

def menu_insertion():
    afficher_titre('Insertion')
    print('WKT de l\'installation ?')
    wkt = input('>> ')
    db.inserer_installation(wkt,'nom')
    input()
    dispatcher('menu_principal')

def menu_balayage():
    afficher_titre('Balayage - WKT Source')
    multi_poly = False
    print('Choix du WKT source : \n')
    for key in db.installations:
        print('\t[{0}] - {1}'.format(key,db.installations[key][0]))
    print('\nSélectionnez une installation :')
    choix = int(input('>> '))
    wkt_source = db.installations[choix][1]
    invocation = db.installations[choix][2]()
    if len(invocation) > 3:
        multi_poly = True

    os.system('cls')
    afficher_titre('Balayage - Paramètres [{0}]'.format(db.installations[choix][0]))
    print('\nSaisissez le pas en X et Y (m) :')
    pas = int(input('>> '))
    print('\nSaisissez l\'angle (rad) :')
    rotation_angle = float(input('>> '))
    print('\nSaisissez le nombre de rotations :')
    rotation_nombre = int(input('>> '))
    print('\nL\'installation touche la voirie ? [O/N] :')
    o_n = input('>> ')
    touche_voirie = True if o_n == 'O' else False
    tag = db.installations[choix][0]

    if multi_poly:
        for el in invocation:
            wkt_cible = el[0]
            db.balayage_installation(pas, rotation_angle, rotation_nombre, wkt_source, wkt_cible, tag, touche_voirie)
    else:
        wkt_cible = invocation[2]
        db.balayage_installation(pas, rotation_angle, rotation_nombre, wkt_source, wkt_cible, tag, touche_voirie)

    input()
    dispatcher('menu_principal')

def menu_export():
    for key in db.installations:
        os.system('cls')
        afficher_titre('Analyse [{0}]'.format(db.installations[key][0]))
        print('\nSaisissez le pourcentage maximal d\'intersection ? :')
        perc_max = float(input('>> '))
        resultats = db.get_resultat_equite(perc_max,db.installations[key][0])
        os.system('cls')
        afficher_titre('Analyse [{0}]'.format(db.installations[key][0]))
        if len(resultats) == 0:
            print(Back.RED + 'Aucun résultat!')
            input()
            dispatcher('menu_principal')
            return
        for (id,self_inters,max_inters) in resultats:
            print('[{0}] - inter_commune:{1} % | inter_parcelle:{2}'.format(id,self_inters,max_inters))
        print('\nSaisissez l\'ID de l\'installation à exporter :')
        id = int(input('>> '))
        db.export_geojson(id)
        input()
        
        


def menu_quitter():
    afficher_titre('A propos')
    print('\tProgrammé par : MEFTAH Basma ; FAHMI Iliass')
    print('\tEncadré par   : Pr. EL YAZIDI EL ALAOUI Otmane')
    input()
    exit()

menu_actions = {
    'menu_principal': menu_principal,
    'a': menu_acquistion,
    'c': menu_insertion,
    'b': menu_balayage,
    'q': menu_quitter,
    'e': menu_export
}

def dispatcher(choix):
    os.system('cls')
    if choix == '':
        menu_actions['menu_principal']()
    else:
        #try:
        menu_actions[choix.lower()]()
        # except KeyError:
        #     print (Back.RED + 'Erreur :' + Style.RESET_ALL +" Choix invalide\n")
        #     menu_actions['menu_principal']()
    return



if __name__ == "__main__":
    init(autoreset=True)
    print('Chargement..')
    db = Connexiondb('config.ini')
    dispatcher('menu_principal')