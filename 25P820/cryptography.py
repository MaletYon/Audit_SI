"""
============================================================
  Application de Chiffrement : César & Vigenère
  Interface graphique Tkinter
  Auteur : NGONO ZANG Jacques Cédric [25P820]
============================================================
"""

import tkinter as tk
from tkinter import messagebox


# ============================================================
#  ALPHABET GLOBAL (utilisé par toutes les fonctions)
# ============================================================

alphabet = list('abcdefghijklmnopqrstuvwxyz')


# ============================================================
#  FONCTIONS DE CHIFFREMENT / DÉCHIFFREMENT
# ============================================================

def chiffrer_cesar(message, decalage):
    """Chiffre un message avec le chiffre de César."""
    resultat = ""
    for caractere in message.lower():
        if caractere in alphabet:
            index = alphabet.index(caractere)          # position dans l'alphabet (0-25)
            nouvel_index = (index + decalage) % 26     # décalage avec bouclage
            resultat += alphabet[nouvel_index]
        else:
            resultat += caractere                      # espaces, chiffres, ponctuation inchangés
    return resultat


def dechiffrer_cesar(message, decalage):
    """Déchiffre un message César en inversant le décalage."""
    return chiffrer_cesar(message, 26 - decalage)      # décaler dans l'autre sens


def chiffrer_vigenere(message, cle):
    """
    Chiffre un message avec le chiffre de Vigenère.
    Utilise le carré de Vigenère (tableau 26x26).
    """
    cle = cle.lower()   # normalisation en minuscules

    # Construction du carré de Vigenère : chaque ligne est l'alphabet décalé de i positions
    carre = [alphabet[i:] + alphabet[:i] for i in range(26)]

    resultat = ""
    index_cle = 0   # curseur qui avance sur la clé (cycliquement)

    for caractere in message.lower():
        if caractere in alphabet:
            col = alphabet.index(caractere)                  # colonne = lettre du message
            lig = alphabet.index(cle[index_cle % len(cle)]) # ligne   = lettre de la clé
            resultat += carre[lig][col]                      # lecture dans le carré
            index_cle += 1                                   # on avance dans la clé
        else:
            resultat += caractere   # espaces, chiffres, ponctuation inchangés

    return resultat


def dechiffrer_vigenere(message_chiffre, cle):
    """
    Déchiffre un message Vigenère.
    On parcourt la ligne correspondant à la lettre de la clé
    et on retrouve la colonne (= lettre originale).
    """
    cle = cle.lower()   # normalisation en minuscules

    # Construction du carré de Vigenère
    carre = [alphabet[i:] + alphabet[:i] for i in range(26)]

    resultat = ""
    index_cle = 0

    for caractere in message_chiffre.lower():
        if caractere in alphabet:
            lig = alphabet.index(cle[index_cle % len(cle)])  # ligne = lettre de la clé
            col = carre[lig].index(caractere)                 # on cherche la lettre chiffrée dans la ligne
            resultat += alphabet[col]                         # la colonne donne la lettre originale
            index_cle += 1
        else:
            resultat += caractere

    return resultat


# ============================================================
#  APPLICATION PRINCIPALE (Tkinter)
# ============================================================

class App(tk.Tk):
    """Fenêtre principale — joue le rôle de contrôleur entre les pages."""

    # --- Palette de couleurs ---
    COULEUR_FOND    = "#1a1a2e"   # Bleu nuit profond
    COULEUR_CADRE   = "#16213e"   # Bleu foncé (cadres)
    COULEUR_ACCENT  = "#e94560"   # Rouge vif (titres, accents)
    COULEUR_TEXTE   = "#eaeaea"   # Blanc cassé
    COULEUR_BOUTON  = "#0f3460"   # Bleu moyen (boutons principaux)
    COULEUR_ENTREE  = "#0d0d1a"   # Fond des champs de saisie
    COULEUR_VERT    = "#00b894"   # Vert pour afficher les résultats

    # --- Polices ---
    POLICE_TITRE    = ("Courier New", 18, "bold")
    POLICE_LABEL    = ("Courier New", 11)
    POLICE_BOUTON   = ("Courier New", 10, "bold")
    POLICE_RESULTAT = ("Courier New", 12, "bold")

    def __init__(self):
        super().__init__()
        self.title("Chiffrement César & Vigenère")
        self.geometry("640x520")
        self.resizable(False, False)
        self.configure(bg=self.COULEUR_FOND)

        # Conteneur principal — toutes les pages sont empilées ici
        conteneur = tk.Frame(self, bg=self.COULEUR_FOND)
        conteneur.pack(fill="both", expand=True)
        conteneur.grid_rowconfigure(0, weight=1)
        conteneur.grid_columnconfigure(0, weight=1)

        # Création et stockage de toutes les pages
        self.pages = {}
        for PageClasse in (PageMenu, PageCesar, PageVigenere):
            page = PageClasse(parent=conteneur, controleur=self)
            self.pages[PageClasse.__name__] = page
            page.grid(row=0, column=0, sticky="nsew")

        # Afficher le menu au démarrage
        self.afficher_page("PageMenu")

    def afficher_page(self, nom_page):
        """Amène la page demandée au premier plan."""
        self.pages[nom_page].lift()

    def arreter(self):
        """Demande confirmation puis ferme l'application."""
        if messagebox.askyesno("Quitter", "Voulez-vous vraiment quitter l'application ?"):
            self.destroy()


# ============================================================
#  PAGE 1 : MENU PRINCIPAL
# ============================================================

class PageMenu(tk.Frame):
    """Page d'accueil avec choix de l'algorithme."""

    def __init__(self, parent, controleur):
        super().__init__(parent, bg=controleur.COULEUR_FOND)
        self.controleur = controleur

        # --- Titre ---
        tk.Label(
            self,
            text="╔══════════════════════════╗\n"
                 "║   CHIFFREMENT CLASSIQUE  ║\n"
                 "╚══════════════════════════╝",
            font=controleur.POLICE_TITRE,
            bg=controleur.COULEUR_FOND,
            fg=controleur.COULEUR_ACCENT
        ).pack(pady=(40, 20))

        tk.Label(
            self,
            text="Choisissez un algorithme de chiffrement :",
            font=controleur.POLICE_LABEL,
            bg=controleur.COULEUR_FOND,
            fg=controleur.COULEUR_TEXTE
        ).pack(pady=(10, 5))

        # Variable liée aux boutons radio (1 = César, 2 = Vigenère)
        self.choix = tk.IntVar(value=1)

        # Cadre contenant les boutons radio
        cadre_choix = tk.Frame(self, bg=controleur.COULEUR_CADRE, bd=2, relief="ridge")
        cadre_choix.pack(padx=60, pady=10, fill="x")

        tk.Radiobutton(
            cadre_choix,
            text="  1. Chiffrement de César",
            variable=self.choix, value=1,
            font=controleur.POLICE_LABEL,
            bg=controleur.COULEUR_CADRE,
            fg=controleur.COULEUR_TEXTE,
            selectcolor=controleur.COULEUR_BOUTON,
            activebackground=controleur.COULEUR_CADRE,
            activeforeground=controleur.COULEUR_ACCENT
        ).pack(anchor="w", padx=20, pady=8)

        tk.Radiobutton(
            cadre_choix,
            text="  2. Chiffrement de Vigenère",
            variable=self.choix, value=2,
            font=controleur.POLICE_LABEL,
            bg=controleur.COULEUR_CADRE,
            fg=controleur.COULEUR_TEXTE,
            selectcolor=controleur.COULEUR_BOUTON,
            activebackground=controleur.COULEUR_CADRE,
            activeforeground=controleur.COULEUR_ACCENT
        ).pack(anchor="w", padx=20, pady=8)

        # Séparateur visuel
        tk.Frame(self, height=2, bg=controleur.COULEUR_ACCENT).pack(fill="x", padx=60, pady=15)

        # Boutons Continuer / Arrêter
        cadre_boutons = tk.Frame(self, bg=controleur.COULEUR_FOND)
        cadre_boutons.pack()

        tk.Button(
            cadre_boutons, text="  Continuer",
            font=controleur.POLICE_BOUTON,
            bg=controleur.COULEUR_BOUTON,
            fg=controleur.COULEUR_TEXTE,
            activebackground=controleur.COULEUR_ACCENT,
            relief="flat", cursor="hand2", padx=18, pady=8,
            command=self.continuer
        ).grid(row=0, column=0, padx=15)

        tk.Button(
            cadre_boutons, text="  Arrêter",
            font=controleur.POLICE_BOUTON,
            bg="#c0392b", fg=controleur.COULEUR_TEXTE,
            activebackground="#e74c3c",
            relief="flat", cursor="hand2", padx=18, pady=8,
            command=controleur.arreter
        ).grid(row=0, column=1, padx=15)

    def continuer(self):
        """Redirige vers la page César ou Vigenère selon le choix."""
        if self.choix.get() == 1:
            self.controleur.afficher_page("PageCesar")
        else:
            self.controleur.afficher_page("PageVigenere")


# ============================================================
#  PAGE 2 : CHIFFREMENT CÉSAR
# ============================================================

class PageCesar(tk.Frame):
    """Page de chiffrement / déchiffrement César."""

    def __init__(self, parent, controleur):
        super().__init__(parent, bg=controleur.COULEUR_FOND)
        self.controleur = controleur

        # --- Titre ---
        tk.Label(
            self, text="[ CHIFFRE DE CÉSAR ]",
            font=controleur.POLICE_TITRE,
            bg=controleur.COULEUR_FOND,
            fg=controleur.COULEUR_ACCENT
        ).pack(pady=(30, 15))

        # --- Champ Message ---
        tk.Label(self, text="Message :",
                 font=controleur.POLICE_LABEL,
                 bg=controleur.COULEUR_FOND,
                 fg=controleur.COULEUR_TEXTE).pack(anchor="w", padx=60)

        self.champ_message = tk.Entry(
            self, font=("Courier New", 12),
            bg=controleur.COULEUR_ENTREE,
            fg=controleur.COULEUR_TEXTE,
            insertbackground=controleur.COULEUR_ACCENT,
            relief="flat", bd=4, width=48
        )
        self.champ_message.pack(padx=60, pady=(3, 12))

        # --- Champ Décalage ---
        tk.Label(self, text="Décalage (entier > 0, non multiple de 26) :",
                 font=controleur.POLICE_LABEL,
                 bg=controleur.COULEUR_FOND,
                 fg=controleur.COULEUR_TEXTE).pack(anchor="w", padx=60)

        self.champ_decalage = tk.Entry(
            self, font=("Courier New", 12),
            bg=controleur.COULEUR_ENTREE,
            fg=controleur.COULEUR_TEXTE,
            insertbackground=controleur.COULEUR_ACCENT,
            relief="flat", bd=4, width=10
        )
        self.champ_decalage.pack(anchor="w", padx=60, pady=(3, 15))

        # --- Boutons ---
        cadre_boutons = tk.Frame(self, bg=controleur.COULEUR_FOND)
        cadre_boutons.pack()

        tk.Button(
            cadre_boutons, text=" Chiffrer",
            font=controleur.POLICE_BOUTON,
            bg=controleur.COULEUR_BOUTON,
            fg=controleur.COULEUR_TEXTE,
            activebackground=controleur.COULEUR_ACCENT,
            relief="flat", cursor="hand2", padx=12, pady=6,
            command=lambda: self.traiter(chiffrer=True)
        ).grid(row=0, column=0, padx=8)

        tk.Button(
            cadre_boutons, text=" Déchiffrer",
            font=controleur.POLICE_BOUTON,
            bg="#2c3e50", fg=controleur.COULEUR_TEXTE,
            activebackground="#3d5a73",
            relief="flat", cursor="hand2", padx=12, pady=6,
            command=lambda: self.traiter(chiffrer=False)
        ).grid(row=0, column=1, padx=8)

        tk.Button(
            cadre_boutons, text=" Retour",
            font=controleur.POLICE_BOUTON,
            bg="#6c757d", fg=controleur.COULEUR_TEXTE,
            activebackground="#868e96",
            relief="flat", cursor="hand2", padx=12, pady=6,
            command=self.retour_menu
        ).grid(row=0, column=2, padx=8)

        tk.Button(
            cadre_boutons, text=" Arrêter",
            font=controleur.POLICE_BOUTON,
            bg="#c0392b", fg=controleur.COULEUR_TEXTE,
            activebackground="#e74c3c",
            relief="flat", cursor="hand2", padx=12, pady=6,
            command=controleur.arreter
        ).grid(row=0, column=3, padx=8)

        # --- Zone Résultat ---
        tk.Frame(self, height=2, bg=controleur.COULEUR_ACCENT).pack(fill="x", padx=60, pady=12)

        tk.Label(self, text="Résultat :",
                 font=controleur.POLICE_LABEL,
                 bg=controleur.COULEUR_FOND,
                 fg=controleur.COULEUR_TEXTE).pack(anchor="w", padx=60)

        self.label_resultat = tk.Label(
            self, text="",
            font=controleur.POLICE_RESULTAT,
            bg=controleur.COULEUR_CADRE,
            fg=controleur.COULEUR_VERT,
            wraplength=480, justify="left",
            relief="flat", padx=10, pady=8, width=48
        )
        self.label_resultat.pack(padx=60, pady=5, fill="x")

    def traiter(self, chiffrer: bool):
        """Valide les entrées puis chiffre ou déchiffre le message."""

        message      = self.champ_message.get().strip()
        decalage_str = self.champ_decalage.get().strip()

        # Vérification : message non vide
        if not message:
            messagebox.showwarning("Champ vide", "Veuillez entrer un message.")
            return

        # Vérification : décalage est un entier
        if not decalage_str.lstrip("-").isdigit():
            messagebox.showerror("Décalage invalide",
                                 "Le décalage doit être un nombre entier.")
            return

        decalage = int(decalage_str)

        # Vérification : décalage strictement positif
        if decalage <= 0:
            messagebox.showerror("Décalage invalide",
                                 "Le décalage doit être strictement positif (> 0).")
            return

        # Vérification : décalage non multiple de 26 (ne chiffrerait rien)
        if decalage % 26 == 0:
            messagebox.showwarning("Décalage inutile",
                                   "Un décalage multiple de 26 ne chiffre rien !\n"
                                   "Choisissez un autre décalage.")
            return

        # Chiffrement ou déchiffrement
        if chiffrer:
            resultat = chiffrer_cesar(message, decalage)
            prefixe  = " Chiffré   : "
        else:
            resultat = dechiffrer_cesar(message, decalage)
            prefixe  = " Déchiffré : "

        self.label_resultat.config(text=prefixe + resultat)

    def retour_menu(self):
        """Vide les champs et retourne au menu principal."""
        self.champ_message.delete(0, tk.END)
        self.champ_decalage.delete(0, tk.END)
        self.label_resultat.config(text="")
        self.controleur.afficher_page("PageMenu")


# ============================================================
#  PAGE 3 : CHIFFREMENT VIGENÈRE
# ============================================================

class PageVigenere(tk.Frame):
    """Page de chiffrement / déchiffrement Vigenère."""

    def __init__(self, parent, controleur):
        super().__init__(parent, bg=controleur.COULEUR_FOND)
        self.controleur = controleur

        # --- Titre ---
        tk.Label(
            self, text="[ CHIFFRE DE VIGENÈRE ]",
            font=controleur.POLICE_TITRE,
            bg=controleur.COULEUR_FOND,
            fg=controleur.COULEUR_ACCENT
        ).pack(pady=(30, 15))

        # --- Champ Message ---
        tk.Label(self, text="Message :",
                 font=controleur.POLICE_LABEL,
                 bg=controleur.COULEUR_FOND,
                 fg=controleur.COULEUR_TEXTE).pack(anchor="w", padx=60)

        self.champ_message = tk.Entry(
            self, font=("Courier New", 12),
            bg=controleur.COULEUR_ENTREE,
            fg=controleur.COULEUR_TEXTE,
            insertbackground=controleur.COULEUR_ACCENT,
            relief="flat", bd=4, width=48
        )
        self.champ_message.pack(padx=60, pady=(3, 12))

        # --- Champ Clé avec validation en temps réel ---
        tk.Label(self, text="Clé de chiffrement (exactement 4 lettres) :",
                 font=controleur.POLICE_LABEL,
                 bg=controleur.COULEUR_FOND,
                 fg=controleur.COULEUR_TEXTE).pack(anchor="w", padx=60)

        # Validation : max 4 caractères alphabétiques autorisés à la saisie
        vcmd = (self.register(self._valider_cle), "%P")
        self.champ_cle = tk.Entry(
            self, font=("Courier New", 12),
            bg=controleur.COULEUR_ENTREE,
            fg=controleur.COULEUR_TEXTE,
            insertbackground=controleur.COULEUR_ACCENT,
            relief="flat", bd=4, width=10,
            validate="key", validatecommand=vcmd
        )
        self.champ_cle.pack(anchor="w", padx=60, pady=(3, 15))

        # --- Boutons ---
        cadre_boutons = tk.Frame(self, bg=controleur.COULEUR_FOND)
        cadre_boutons.pack()

        tk.Button(
            cadre_boutons, text=" Chiffrer",
            font=controleur.POLICE_BOUTON,
            bg=controleur.COULEUR_BOUTON,
            fg=controleur.COULEUR_TEXTE,
            activebackground=controleur.COULEUR_ACCENT,
            relief="flat", cursor="hand2", padx=12, pady=6,
            command=lambda: self.traiter(chiffrer=True)
        ).grid(row=0, column=0, padx=8)

        tk.Button(
            cadre_boutons, text=" Déchiffrer",
            font=controleur.POLICE_BOUTON,
            bg="#2c3e50", fg=controleur.COULEUR_TEXTE,
            activebackground="#3d5a73",
            relief="flat", cursor="hand2", padx=12, pady=6,
            command=lambda: self.traiter(chiffrer=False)
        ).grid(row=0, column=1, padx=8)

        tk.Button(
            cadre_boutons, text=" Retour",
            font=controleur.POLICE_BOUTON,
            bg="#6c757d", fg=controleur.COULEUR_TEXTE,
            activebackground="#868e96",
            relief="flat", cursor="hand2", padx=12, pady=6,
            command=self.retour_menu
        ).grid(row=0, column=2, padx=8)

        tk.Button(
            cadre_boutons, text=" Arrêter",
            font=controleur.POLICE_BOUTON,
            bg="#c0392b", fg=controleur.COULEUR_TEXTE,
            activebackground="#e74c3c",
            relief="flat", cursor="hand2", padx=12, pady=6,
            command=controleur.arreter
        ).grid(row=0, column=3, padx=8)

        # --- Zone Résultat ---
        tk.Frame(self, height=2, bg=controleur.COULEUR_ACCENT).pack(fill="x", padx=60, pady=12)

        tk.Label(self, text="Résultat :",
                 font=controleur.POLICE_LABEL,
                 bg=controleur.COULEUR_FOND,
                 fg=controleur.COULEUR_TEXTE).pack(anchor="w", padx=60)

        self.label_resultat = tk.Label(
            self, text="",
            font=controleur.POLICE_RESULTAT,
            bg=controleur.COULEUR_CADRE,
            fg=controleur.COULEUR_VERT,
            wraplength=480, justify="left",
            relief="flat", padx=10, pady=8, width=48
        )
        self.label_resultat.pack(padx=60, pady=5, fill="x")

    @staticmethod
    def _valider_cle(valeur):
        """
        Validation en temps réel du champ clé.
        N'autorise que des lettres (max 4 caractères).
        Retourne True pour accepter la frappe, False pour la bloquer.
        """
        return valeur == "" or (len(valeur) <= 4 and valeur.isalpha())

    def traiter(self, chiffrer: bool):
        """Valide les entrées puis chiffre ou déchiffre le message."""

        message = self.champ_message.get().strip()
        cle     = self.champ_cle.get().strip()

        # Vérification : message non vide
        if not message:
            messagebox.showwarning("Champ vide", "Veuillez entrer un message.")
            return

        # Vérification : clé exactement 4 caractères
        if len(cle) != 4:
            messagebox.showerror("Clé invalide",
                                 "La clé doit contenir exactement 4 lettres.")
            return

        # Chiffrement ou déchiffrement (cle.lower() est géré dans les fonctions)
        if chiffrer:
            resultat = chiffrer_vigenere(message, cle)
            prefixe  = " Chiffré   : "
        else:
            resultat = dechiffrer_vigenere(message, cle)
            prefixe  = " Déchiffré : "

        self.label_resultat.config(text=prefixe + resultat)

    def retour_menu(self):
        """Vide les champs et retourne au menu principal."""
        self.champ_message.delete(0, tk.END)
        self.champ_cle.delete(0, tk.END)
        self.label_resultat.config(text="")
        self.controleur.afficher_page("PageMenu")


# ============================================================
#  POINT D'ENTRÉE
# ============================================================

if __name__ == "__main__":
    app = App()       # Crée et configure la fenêtre principale
    app.mainloop()    # Lance la boucle événementielle Tkinter