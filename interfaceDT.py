import tkinter as tk
import shutil
import os
import sys
import subprocess
import threading

from tkinter import filedialog

from trouveSteam import steamOui

dossier_selectionne = ""

def testOui():

    dossier_exe = "ressources/"
    dossier_steam_name = "Hylics"
    gameID = "0"
    
    global dossier_selectionne
    
    if(dossier_selectionne == ""):
        dossier_selectionne = steamOui(dossier_steam_name, gameID)

    # Fonction appelée lors du clic sur le bouton
    def installer_patch():
        global dossier_selectionne
        
        bouton_parcourir.config(state="disabled")
        bouton.config(state="disabled")
        
        try:
            if(dossier_selectionne != "Inconnu."):
                labelAffiche.config(text="\n\nInstallation en cours...")
                labelAffiche.update_idletasks()
                
                shutil.copytree(os.path.join(dossier_exe, dossier_steam_name), dossier_selectionne, dirs_exist_ok=True)
                
                labelAffiche.config(text="\n\nPatch installé.")
            else:
                labelAffiche.config(text="\n\nLe jeu n'a pas été trouvé.")
        except Exception as e:
            print(f"Erreur lors de la copie dans le dossier '{dossier_selectionne}': {e}")
        
        bouton_parcourir.config(state="normal")
        bouton.config(state="normal")
    
    def bouton():
        thread = threading.Thread(target=installer_patch)
        thread.start()
    
    def centrer_et_redimensionner(fenetre):
        # Obtenez les dimensions de l'écran
        largeur_ecran = fenetre.winfo_screenwidth()
        hauteur_ecran = fenetre.winfo_screenheight()

        nouvelle_largeur = 600
        nouvelle_hauteur = 250
        
        # Calculez les coordonnées x et y pour centrer la fenêtre
        x = (largeur_ecran - nouvelle_largeur) // 2
        y = (hauteur_ecran - nouvelle_hauteur) // 2
        
        if x < 0:
            x = 0
        if y < 0:
            y = 0

        # Définissez les nouvelles dimensions et coordonnées de la fenêtre
        fenetre.geometry("{}x{}+{}+{}".format(nouvelle_largeur, nouvelle_hauteur, x, y))
    
    def parcourir_dossier():
        global dossier_selectionne
        dossier_selectionne = filedialog.askdirectory()
        if(dossier_selectionne == ""):
            dossier_selectionne = steamOui(dossier_steam_name, gameID)
        # print(dossier_selectionne)
        labelAffiche.config(text=f"\nDossier du jeu :\n{dossier_selectionne}")

    # Création de la fenêtre principale
    fenetre = tk.Tk()
    fenetre.title("Hylics - Traduction FR")

    # Création d'un widget Label (étiquette) pour afficher du texte
    label = tk.Label(fenetre, text="Crédits :\n\nTraducteur : Kesnos")
    label.pack()  # Ajout du widget à la fenêtre
    
    labelAffiche = tk.Label(fenetre, text=f"\nDossier du jeu :\n{dossier_selectionne}")
    labelAffiche.pack()
    
    # Création du bouton pour parcourir les fichiers
    bouton_parcourir = tk.Button(fenetre, text="Parcourir", command=parcourir_dossier)
    bouton_parcourir.pack()

    # Création d'un widget Button (bouton)
    bouton = tk.Button(fenetre, text="Installer", command=bouton, )
    bouton.pack(side="bottom", padx= 50,pady=10)

    #centre la fenêtre
    centrer_et_redimensionner(fenetre)
    fenetre.resizable(False, False)
    
    # icone
    fenetre.iconbitmap(os.path.join(dossier_exe, "Jeu.ico"))

    # Lancement de la boucle principale
    fenetre.mainloop()