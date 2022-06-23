
# DÃ©mineur 

from tkinter import *
import random, sys

# Dessine la grille de jeu
def grille(nb_col, nb_lignes, dim, origine):
    x1= origine
    y1= origine
    # DÃ©termine la largeur de la grille
    y2 = y1 + (dim*nb_lignes)
    # DÃ©termine la hauteur de la grille
    x2 = x1 + (dim*nb_col)
    colonne = 0
    while colonne <= nb_col:
        colonne=colonne+1
        # CrÃ©ation de la ligne verticale
        can.create_line(x1,y1,x1,y2,width=2, fill="black") 
        # DÃ©calage de la ligne vers la droite
        x1 = x1 + dim 
    x1 = origine
    ligne = 0
    while ligne <= nb_lignes:
        ligne=ligne+1
        # CrÃ©ation de la ligne horizontale
        can.create_line(x1,y1,x2,y1,width=2, fill="black") 
        # DÃ©calage de la ligne vers le bas
        y1 = y1 + dim 

# Initialise le niveau de jeu
def init_niveau():
    global nb_col, nb_lig, nb_mines 
    niveau = choix.get()
    # niveau dÃ©butant
    if niveau == 1:
        nb_col, nb_lig, nb_mines = 10, 10, 12
    # niveau avancÃ©   
    elif niveau == 2:
        nb_col, nb_lig, nb_mines = 15, 15, 30
    # niveau expert
    else:
        nb_col, nb_lig, nb_mines = 20, 20, 50
    # taille du canevas pour chaque niveau
    can.configure(width=(nb_col*dim)+gap , height=(nb_lig*dim)+gap)
    init_jeu()

# Initialistion des paramÃ¨tres du jeu
def init_jeu():
    global nb_mines_cachees, nb_cases_vues, on_joue
    on_joue = True
    nb_cases_vues = 0
    can.delete(ALL)
    nb_mines_cachees = nb_mines
    affiche_compteurs()  
    # Initialisation des 2 tableaux avec des chaines vides
    y = 0
    while y < nb_lig:
        x = 1
        y += 1
        while x <= nb_col:
            tab_m[x,y]= 0 # Initialisation dans le tableau des mines
            tab_j[x,y]= "" # Initialisation dans le tableau de jeu
            can.create_rectangle((x-1)*dim+gap,(y-1)*dim+gap,
                                 x*dim+gap,y*dim+gap,width=0, fill="grey")
            x += 1
    grille(nb_col, nb_lig, dim, gap) # Dessine la grille
    # place les mines alÃ©atoirement dans la grille de jeu
    nb_mines_voisines = 0
    while nb_mines_voisines < nb_mines:
        col = random.randint(1, nb_col)
        lig = random.randint(1, nb_lig)
        if tab_m[col, lig] != 9: # VÃ©rifie si la cellule contient dÃ©jÃ  une mine
            tab_m[col, lig] = 9 
            nb_mines_voisines = nb_mines_voisines + 1

# calcule le nombre de mines qu'il reste Ã  trouver
def affiche_compteurs():
    decompte_mines.configure(text=str(nb_mines_cachees))
    # DÃ©compte des case Ã  traiter pour la fonction gagnÃ©
    decompte_cases.configure(text=str((nb_col*nb_lig)-nb_cases_vues))
    
# affiche le nombre de mines restantes
def affiche_nb_mines (nb_mines_voisines, col, lig):
    global nb_mines_cachees,nb_cases_vues
    # si la case est vide
    if tab_j[col, lig] == "":
        nb_cases_vues = nb_cases_vues + 1
        # S'il y a un drapeau : modification du compteur de mines
        if (tab_j[col, lig] == "d"):
            # Ajout d'une mine
            nb_mines_cachees = nb_mines_cachees + 1
            # le drapeau est considÃ©rÃ© comme une case vue
            nb_cases_vues = nb_cases_vues - 1
            affiche_compteurs()
        tab_j[col, lig] = nb_mines_voisines
        # Dessine un carrÃ© "ivoire"
        can.create_rectangle((col-1)*dim+gap+3,(lig-1)*dim+gap+3,
                             col*dim+gap-3,lig*dim+gap-3,width=0, fill="ivory")
        # Affichage du nombre de mines avec les couleurs corespondantes
        coul = ['blue','orange','red','green','cyan','skyblue','pink']
        can.create_text(col*dim-dim//2+gap, lig*dim-dim//2+gap,
                        text=str(nb_mines_voisines),
                        fill=coul[nb_mines_voisines-1],font='Arial 22')


# calcule le nombre de mines qui touchent la case
def nb_mines_adj(col, ligne):
    if col > 1:
        min_col = col - 1
    else:
        min_col = 1
    if col < nb_col:
        max_col = col + 1
    else:
        max_col = col       
    if ligne > 1:
        min_lig = ligne - 1
    else:
        min_lig = 1
    if ligne < nb_lig:
        max_lig = ligne + 1
    else:
        max_lig = nb_lig
    txtinfo = ""
    nb_mines = 0
    indice_lig = min_lig
    while indice_lig <= max_lig:
        indice_col = min_col
        while indice_col <= max_col:
            if tab_m [indice_col,indice_lig] == 9:
                nb_mines += 1       
            indice_col = indice_col + 1      
        indice_lig = indice_lig +1
    return nb_mines


# Affiche toutes les cases zÃ©ro adjacentes et leur bordure
def vide_plage_zero(col, ligne):
    global nb_mines_cachees, nb_cases_vues
    # si on a dÃ©jÃ  la cellule n'est pas vide
    if tab_j[col, ligne] != 0:
        # S'l y a un drapeau on modifie le compteur de mines et de cases traitÃ©es
        if (tab_j[col, ligne] == "d"):
            nb_mines_cachees = nb_mines_cachees + 1
            nb_cases_vues = nb_cases_vues - 1
        # Affichage du fond
        can.create_rectangle((col-1)*dim+gap+3, (ligne-1)*dim+gap+3,
                             col*dim+gap-3, ligne*dim+gap-3,
                             width=0, fill="seashell2")
        # Stockage des 0 dans le tableau de jeu
        tab_j[col, ligne] = 0
        nb_cases_vues = nb_cases_vues + 1
        # VÃ©rifie les cases voisines en croix
        if col > 1:
            nb_mines_voisines = nb_mines_adj(col-1, ligne)
            if nb_mines_voisines == 0:
                vide_plage_zero(col-1, ligne)
            else:
                affiche_nb_mines(nb_mines_voisines, col-1, ligne)
        if col < nb_col:
            nb_mines_voisines = nb_mines_adj (col+1, ligne)
            if nb_mines_voisines == 0:
                vide_plage_zero(col+1, ligne)
            else:
                affiche_nb_mines(nb_mines_voisines, col+1, ligne)
        if ligne > 1:
            nb_mines_voisines = nb_mines_adj (col, ligne-1)
            if nb_mines_voisines == 0:
                vide_plage_zero(col, ligne-1)
            else:
                affiche_nb_mines(nb_mines_voisines, col, ligne-1)
        if ligne < nb_lig:
            nb_mines_voisines = nb_mines_adj (col, ligne+1)
            if nb_mines_voisines == 0:
                vide_plage_zero(col, ligne+1)
            else:
                affiche_nb_mines (nb_mines_voisines, col, ligne+1)
        # VÃ©rification des diagonales pour afficher les bords de la plage zÃ©ro
        if col > 1 and ligne > 1:
            nb_mines_voisines = nb_mines_adj(col-1, ligne-1)
            if nb_mines_voisines == 0:
                vide_plage_zero(col-1, ligne-1)
            else:
                affiche_nb_mines(nb_mines_voisines, col-1, ligne-1)
        if col > 1 and ligne < nb_lig:
            nb_mines_voisines = nb_mines_adj(col-1, ligne+1)
            if nb_mines_voisines == 0:
                vide_plage_zero(col-1, ligne+1)           
            else:
                affiche_nb_mines(nb_mines_voisines, col-1, ligne+1)
        if col < nb_col and ligne > 1:
            nb_mines_voisines = nb_mines_adj(col+1, ligne-1)
            if nb_mines_voisines == 0:
                vide_plage_zero(col+1, ligne-1)
            else:
                affiche_nb_mines (nb_mines_voisines, col+1, ligne-1)
        if col < nb_col and ligne < nb_lig:
            nb_mines_voisines = nb_mines_adj(col+1, ligne+1)
            if nb_mines_voisines == 0:
                vide_plage_zero(col+1, ligne+1)
            else:
                affiche_nb_mines(nb_mines_voisines, col+1, ligne+1)
        affiche_compteurs()


def perdu():
    global on_joue
    on_joue  = False
    # Parcours du tableau pour afficher toutes les mines
    nLig = 0
    while nLig < nb_lig:
        nCol = 1
        nLig = nLig +1
        while nCol <= nb_col:
            # affichage de grille exacte
            if tab_m[nCol, nLig] == 9:
                if tab_j[nCol, nLig] == "?":
                    can.create_image(nCol*dim-dim//2+gap,
                                     nLig*dim-dim//2+gap, image = im_mine)
                elif tab_j[nCol, nLig] == "":
                    can.create_image(nCol*dim-dim//2+gap,
                                     nLig*dim-dim//2+gap, image = im_mine)
            else :
                if tab_j[nCol, nLig] == "d":
                    can.create_image(nCol*dim-dim//2+gap,
                                     nLig*dim-dim//2+gap, image = im_erreur)
            nCol = nCol+1
    can.create_text((nb_col/2)*dim-15+gap, (nb_lig/2)*dim-5+gap,
                    text='Perdu !', fill='black', font='Arial 50')
    fen.update_idletasks() # rafraichit la fenÃªtre avant le bruitage
    winsound.PlaySound('explosion.wav', winsound.SND_FILENAME)


def gagne():
    can.create_text((nb_col/2)*dim-15+gap, (nb_lig/2)*dim-5+gap,
                    text='Bravo !', fill='black', font='Arial 50')
    fen.update_idletasks() 
    winsound.PlaySound('gagne.wav', winsound.SND_FILENAME)


# gÃ¨re le clic gauche de la souris
def pointeurG(event):
    global nb_cases_vues
    # si la partie n'est pas en cours (quand on a perdu), blocage du jeu
    if on_joue :
        nCol = (event.x - gap) // dim +1
        nLig = (event.y - gap) // dim +1 
        # si la cellule est vide
        if tab_j[nCol, nLig] == "":
            # VÃ©rifie si on est bien dans le tableau
            if nCol>=1 and nCol<=nb_col and nLig>=1 and nLig<=nb_lig:
                # VÃ©rifie si la cellule contient une mine
                if (tab_m[nCol, nLig] == 9):
                    perdu()
                else:
                    nb_mines_voisines = nb_mines_adj(nCol, nLig )
                    if nb_mines_voisines >= 1:
                        affiche_nb_mines(nb_mines_voisines, nCol, nLig ) 
                        affiche_compteurs()
                    else: # Traitement des cases vides
                        vide_plage_zero(nCol, nLig)
            # VÃ©rification des compteurs
            if ((nb_col*nb_lig) == nb_cases_vues and nb_mines_cachees == 0):
                gagne()


# gÃ¨re le clic droit de la souris
def pointeurD(event):
    global nb_mines_cachees, nb_cases_vues
    # si la partie n'est pas en cours (quand on a perdu), blocage du jeu
    if on_joue :
        nCol = (event.x - gap)// dim+1
        nLig = (event.y - gap) // dim+1
        # si la cellule est vide
        if tab_j[nCol, nLig]=="":
            # Affiche le drapeau
            can.create_image(nCol*dim-dim//2+gap, nLig*dim-dim//2+gap,
                             image = im_flag)
            tab_j[nCol, nLig]="d"
            nb_cases_vues = nb_cases_vues + 1
            nb_mines_cachees = nb_mines_cachees - 1
        # si la cellule contient  un drapeau    
        elif tab_j[nCol, nLig] == "d":
            # Remise Ã  blanc
            can.create_rectangle((nCol-1)*dim+gap+3,(nLig-1)*dim+gap+3,
                                 nCol*dim+gap-3,nLig*dim+gap-3,width=0, fill="grey")
            # Affiche le ?
            can.create_text(nCol*dim-dim//2+gap, nLig*dim-dim//2+gap,
                            text="?", fill='black',font='Arial 20')
            tab_j[nCol, nLig] = "?"
            # le ? n'est pas considÃ©rÃ© comme une case traitÃ©e
            nb_cases_vues = nb_cases_vues - 1
            # Ajoute une mine car le ? ne dÃ©signe pas une mine
            nb_mines_cachees = nb_mines_cachees + 1
        # si la cellule contient un ?
        elif tab_j[nCol, nLig] == "?":
            # Remise Ã  blanc
            can.create_rectangle((nCol-1)*dim+gap+3,(nLig-1)*dim+gap+3,
                                 nCol*dim+gap-3,nLig*dim+gap-3,
                                 width=0, fill="grey")
            # Stocke du vide dans le tableau de jeu  
            tab_j[nCol, nLig] = ""
        affiche_compteurs()
        # VÃ©rification des compteurs
        if ((nb_col*nb_lig) == nb_cases_vues and nb_mines_cachees == 0):
            gagne()


# ----------------------------------------------------------------------------------------
# DÃ©but du programme
# ----------------------------------------------------------------------------------------
   
fen=Tk()
fen.title("DÃ©mineur")
fen.resizable(width=False, height=False)

# DÃ©clarations des variables lorsqu'on ouvre la fenÃªtre principale
# (niveau dÃ©butant par dÃ©faut)
nb_col, nb_lig, nb_mines = 0,0,0
dim, gap, nb_cases_vues = 30, 3, 0
on_joue = True
# Chargement des images 
im_mine = PhotoImage(file = "minej.gif")
im_erreur = PhotoImage(file = "croixj.gif")
im_flag = PhotoImage(file = "drapeauj.gif")
tab_m = {} # tableau des mines
tab_j = {} # tableau des cases modifiÃ©es par le joueur

can=Canvas(fen, width=(nb_col*dim)+gap, height=(nb_lig*dim)+gap, bg="grey")
can.bind("<Button-1>",pointeurG)
can.bind("<Button-3>",pointeurD)
can.pack(side=RIGHT)

# Frame Ã  gauche de la grille de jeu pour disposer les boutons radios
f2 = Frame(fen)
# CrÃ©ation de cases Ã  cocher pour le niveau
choix=IntVar()
choix.set(1)
case1=Radiobutton(f2)
case1.configure(text='DÃ©butant', command=init_niveau, variable=choix,value=1)
case1.pack(anchor= NW ,padx=30)
case2=Radiobutton(f2)
case2.configure(text='AvancÃ©', padx=3, command=init_niveau, variable=choix,value=2)
case2.pack(anchor= NW, padx=30)
case3=Radiobutton(f2)
case3.configure(text='Expert', padx=3, command=init_niveau, variable=choix,value=3)
case3.pack(anchor= NW ,padx=30)
f2.pack()

# Frame Ã  gauche de la grille de jeu pour les compteurs
f3 = Frame(fen)
# Champ pour l'affichage du dÃ©compte des mines
texte_mines = Label (f3, text = "Mines restantes :")
decompte_mines = Label (f3, text = "100")
texte_mines.grid(row=4,column=1,sticky='NW')
decompte_mines.grid(row=4,column=2,sticky='NE')
# Champ pour l'affichage du dÃ©compte des cases
texte_cases = Label (f3, text = "Cases Ã  traiter :")
decompte_cases = Label (f3, text = "10")
texte_cases.grid(row=5,column=1,sticky='NW')
decompte_cases.grid(row=5,column=2,sticky='NE')
f3.pack()

# Frame Ã  gauche de la grille de jeu pour disposer les boutons
f1 = Frame(fen)
bou1 = Button(f1, width=14, text="Nouvelle partie", font="Arial 10", command=init_jeu)
bou1.pack(side=BOTTOM, padx=5, pady=5)
f1.pack(side=BOTTOM)

# Frame Ã  gauche de la grille de jeu pour afficher l'image
f4 = Frame(fen)
photo=PhotoImage(file="mine1.gif")
labl = Label(f4, image=photo)
labl.pack(side=BOTTOM)
f4.pack(side=BOTTOM)

init_niveau()
init_jeu()
fen.mainloop() 
