# Made with <3 by Kellian Bredeau and Thomas Gaveau
# Date: 15/11/2021
# Version: 1.0
# Description: Jeu du Uno
# Dépendance : Python 3.10.0 (default, Oct  4 2021, 00:00:00) [GCC 11.2.1 20210728 (Red Hat 11.2.1-1)] on linux
# Utilisation des fstrings, ne fonctionnera pas sur une version antérieure à 3.7, le fonctionnement n'est pas garanti sur les versions antérieures à 3.10.0

import random
import time

# Définition des classes

# Classe Jeu
class Jeu:
    def __init__(self):
        self.joueurs = []
        self.inverse = False
        self.tour = 0
        self.pile = None
        self.cartes = []
        couleurs_base = ['Rouge', 'Vert', 'Bleu', 'Jaune']
        valeurs_base = ['0', '1', '2', '3', '4', '5',
                        '6', '7', '8', '9', '+2', 'Reverse', 'Block']
        for i in range(4):
            for j in range(13):
                self.cartes.append(Carte(couleurs_base[i], valeurs_base[j]))
        self.cartes.append(Carte('Noir', '+4'))
        self.cartes.append(Carte('Noir', 'Select'))

    couleurs_base = ['Rouge', 'Vert', 'Bleu', 'Jaune']

    # Fonction de démarrage du jeu
    def demarrage(self):
        self.pile = Pile(random.choice(self.cartes)) # On tire au hasard une carte
        while self.pile.defausse.couleur == 'Noir':  # On évite la carte noir en début de partie
            self.pile = Pile(random.choice(self.cartes))
        print(f"Pile : {self.pile.aff_pile()}") # On affiche la pile

#Classe Carte
class Carte (Jeu):

    def __init__(self, couleur, valeur):
        self.couleur = couleur
        self.valeur = valeur

    def valeur(self):
        return self.valeur

    def couleur(self):
        return self.couleur

    # Fonction de formattage de carte
    def split(self, text):
        carte = text.split()
        if len(carte) == 1:
            return (0, carte)
        nvl_carte = Carte(carte[1], carte[0])
        return nvl_carte

    # Fonction vérifiant si la carte est noire
    def est_noir(self):
        if str(self.couleur) == 'Noir':
            return True
        else:
            return False

    def __repr__(self):
        return str(self.valeur) + ' ' + str(self.couleur)

# Classe Main du joueur
class Main (Carte):

    def __init__(self, cartes):
        self.cartes = cartes

    def __repr__(self):
        return str(Carte.valeur(self.cartes)) + ' ' + str(Carte.couleur(self.cartes))

# Classe Pile (defausse)
class Pile (Carte):

    def __init__(self, defausse):
        self.defausse = defausse

    def aff_pile(self):
        return self.defausse

    def __repr__(self):
        return str(Carte.valeur(self.defausse)) + ' ' + str(Carte.couleur(self.defausse))

# Classe Joueur
class Joueur (Jeu):

    # Fonction de création d'un joueur
    # On crée un joueur avec un nom et une main
    def __init__(self, nom=0, game=0):
        self.nom = nom
        self.main = []
        for i in range(7):
            self.main += [Main(random.choice(game.cartes))]
        self.bloque = False

    def __repr__(self):
        return self.nom + ' ' + str(self.main)

    # Fonction de formattage de carte
    def split(self, text):
        carte = text.split()
        if len(carte) == 1:
            carte.append('Noir')
        nvl_carte = Carte(carte[1], carte[0])
        return nvl_carte

    # Fonction permettant de calculer le bonus d'une carte
    def bonus_carte(self, carte, game):
        carte = self.split(str(carte))
        print(carte.valeur)
        if carte.valeur == 'Reverse':  # La carte est-elle un reverse ?
            game.joueurs = game.joueurs.reverse()  # Change le sens
        if carte.valeur == 'Block':  # La carte est-elle un block ?
            game.joueurs[(idn + 1) % len(game.joueurs)].bloque = True
        if carte.valeur == '+2':
            for j in range(2):
                game.joueurs[(idn + 1) % len(game.joueurs)
                             ].main.append(random.choice(game.cartes))

    
    def creerJoueur(self):
        nom = input('Entrez votre nom : ')
        self.nom = nom

    # Tour du bot
    def tourBot(self, jeu):
        print(f'Tour de : {self.nom}')
        print(f"Dernière carte posée : {jeu.pile.aff_pile()}")
        if self.bloque:
            print("T'es bloqué, pas de chance")
            self.bloque = False
            return

        for carte in self.main:
            if carte.couleur == 'Noir' or str(self.split(str(carte)).couleur) == 'Noir':
                couleur_choisie = random.choice(jeu.couleurs_base)
                jeu.pile = Pile(Carte(couleur_choisie, 0))
                print(f"La nouvelle couleur choisie est {couleur_choisie} ")
                if carte.valeur == '+4':
                    for j in range(4):
                        jeu.joueurs[(idn + 1) % len(jeu.joueurs)
                                    ].main.append(random.choice(game.cartes))
                return

        for carte in self.main:
            if str(self.split(str(jeu.pile.defausse)).couleur) in str(self.split(str(carte)).couleur):
                jeu.pile = Pile(carte)
                self.bonus_carte(carte, jeu)
                self.main.remove(carte)
                print(f'{self.nom} a posé : {carte}')
                return

        for carte in self.main:
            if str(self.split(str(jeu.pile.defausse)).valeur) in str(self.split(str(carte)).valeur):
                jeu.pile = Pile(carte)
                self.bonus_carte(carte, jeu)
                self.main.remove(carte)
                print(f'{self.nom} a posé : {carte}')
                return
        # Si aucune carte n'a été posée, on tire une carte
        print('Vous ne pouvez pas poser de carte')
        self.main.append(random.choice(jeu.cartes))
        return

    def new_method(self, jeu):
        print(jeu.pile.defausse)

    # Tour du joueur
    def tourHumain(self, game):
        print(f"A votre tour : {self.nom}")
        print(f"Dernière carte posée : {game.pile.aff_pile()}")
        print(self.main)
        if self.bloque:
            print("T'es bloqué, pas de chance")
            return
        demande = input('Quelle carte voulez-vous poser ?')
        if demande != 'Rien':
            demande = self.split(str(demande))
            for carte in self.main:
                cartef = carte.split(str(carte))
                if str(demande) == str(carte):
                    game.pile = Pile(self.split(str(game.pile.aff_pile())))
                    if cartef.couleur == game.pile.defausse.couleur or cartef.valeur == game.pile.defausse.valeur:
                        game.pile = Pile(carte)
                        self.bonus_carte(carte, game)
                        self.main.remove(carte)
                        print(f'Vous avez posé : {carte}')
                        return
                    if cartef.est_noir():
                        couleur_choisie = input(
                            "Quelle couleur souhaitez-vous ?")
                        game.pile = Pile(Carte(couleur_choisie, ''))
                        if carte.valeur == '+4':  # La carte est-elle un +4 ?
                            for j in range(4):
                                joueur[(idn + 1) % len(game.joueurs)
                                       ].main.append(random.choice(game.cartes))
                        return
            print("T'as voulu tricher je t'ai vu ! +1 carte")
            self.main.append(random.choice(game.cartes))
        else:
            print("Tu as pioché 1 carte")
            self.main.append(random.choice(game.cartes))


#--------------------------------------------------------------------------------------------#
game = Jeu()
game.demarrage()

# Tour
game.joueurs = [Joueur('Joueur 1', game), Joueur(
    'Joueur 2', game), Joueur('Joueur 3', game)]
player = Joueur(1, game)
player.creerJoueur()
game.joueurs.append(player)

running = True
while running:
    for idn, joueur in enumerate(game.joueurs):
        print("\n")
        if joueur.nom != player.nom:
            joueur.tourBot(game)
            time.sleep(1)
            if len(joueur.main) == 0:
                print(f'{joueur.nom} a gagné !')
                running = False
                break
        else:
            joueur.tourHumain(game)
            if len(joueur.main) == 0:
                print(f'{joueur.nom} a gagné !')
                running = False
                break
