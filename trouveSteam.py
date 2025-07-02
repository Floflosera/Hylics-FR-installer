import winreg
import os
import shutil

import utils

def steamOui(dossier_steam_name, gameID):
    def trouver_dossier_steam():
        """recupère le chemin du dossier steam via les registres

        Returns:
            str: chemin du dossier steam
        """
        KEY_PATH_STEAM = r"SOFTWARE\\Valve\\Steam"
        KEY_NAME = "SteamPath"
        try:
            key_steam = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER, KEY_PATH_STEAM, 0, winreg.KEY_READ
            )
            chemin_steam = winreg.QueryValueEx(key_steam, KEY_NAME)[0]
            return chemin_steam
        except Exception:
            utils.logging.error("dossier steam non trouvé")
    
    def extraire_path_dans_ligne(ligne):
        """récupère le path de la steamlibrary de la
        ligne du fichier libraryfolders.vdf
                    "path"		"F:\\SteamLibrary"
        la ligne se présente comme ceci, on récupère le string
        situé entre les 3ème et 4ème guillemets

        Args:
            ligne (str): ligne de libraryfolders.vdf où est le situé le chemin de la steamlibrary

        Returns:
            int, int: début et fin de la sous-chaine de la ligne présentant le chemin de la steamlibrary
        """
        compteur_apostrophes = 0
        index_debut = 0
        index_fin = 0
        for index, caractere in enumerate(ligne):
            if caractere == '"':
                compteur_apostrophes += 1
                if compteur_apostrophes == 3:
                    index_debut = index + 1
                if compteur_apostrophes == 4:
                    index_fin = index
        return index_debut, index_fin
    
    def trouver_dossiers_jeux(chemin_steam):
        """ouvre le fichier libraryfolders.vdf présent dans le dossier steam
        pour trouver les path des steamlibrary

        Args:
            chemin_steam (str): chemin absolu du répertoire steam

        Returns:
            list(str): liste des chemin des steamlibrary
        """
        dossiers_jeux = []
        fichier_libraryfolders = chemin_steam + "\\steamapps\\libraryfolders.vdf"
        if os.path.exists(fichier_libraryfolders):
            with open(fichier_libraryfolders, "r") as fichier:
                for ligne in fichier:
                    if ligne.find("path") != -1:  # si on trouve "path" dans la ligne
                        index_debut, index_fin = extraire_path_dans_ligne(ligne)
                        path = utils.convertir_double_slash_en_simple(
                            ligne[index_debut:index_fin]
                        )
                        dossiers_jeux.append(path)
        else:
            utils.logging.error("fichier libraryfolders.vdf non trouvé")
        return dossiers_jeux

    def trouver_jeu():
        """récupère le chemin absolu du ze1_data.bin du dossier steam du jeu

        Returns:
            str: chemin du jeu
        """
        try:
            dossier_steam = trouver_dossier_steam()
            if os.path.exists(dossier_steam) and gameID != "0" and os.path.exists(dossier_steam + "\\appcache\\librarycache\\" + gameID):
                dossier_exe = "ressources/"
                shutil.copy(os.path.join(dossier_exe, "Images_Steam/" + "header.jpg"),dossier_steam + "\\appcache\\librarycache\\" + gameID + "/header.jpg")
                shutil.copy(os.path.join(dossier_exe, "Images_Steam/" + "library_600x900.jpg"),dossier_steam + "\\appcache\\librarycache\\" + gameID + "/library_600x900.jpg")
                shutil.copy(os.path.join(dossier_exe, "Images_Steam/" + "logo.png"),dossier_steam + "\\appcache\\librarycache\\" + gameID + "/logo.png")
            dossiers_jeux = trouver_dossiers_jeux(dossier_steam)
            for chemin in dossiers_jeux:
                chemin_complet = chemin + "\\steamapps\\common\\" + dossier_steam_name
                if os.path.exists(chemin_complet) and os.path.isdir(chemin_complet):
                    return chemin_complet
            utils.logging.error("Dossier du jeu non trouvé")
            return -1
        except Exception as e:
            print(f"Erreur lors de la recherche de Steam : {e}")
            return -1
    
    cheminJeu_steam = trouver_jeu()
    
    if cheminJeu_steam != -1:
        return cheminJeu_steam
    else:
        return "Inconnu."
