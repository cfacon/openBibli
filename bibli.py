from ttkbootstrap import Style
from tkinter import * 
from tkinter import ttk
from tkinter.messagebox import *

import database
import APIBooks
import ecranPret
import ecranUtilisateurs
import ecranCatalogue
import logging
import sys
import configparser

config = configparser.ConfigParser()
config.sections()
config.read('bibli.ini')
config.sections()

#prepare les logs
def setup_custom_logger(name):
    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    handler = logging.FileHandler(config['LOG']['FileName'], mode='a')
    handler.setFormatter(formatter)
    screen_handler = logging.StreamHandler(stream=sys.stdout)
    screen_handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    logger.addHandler(screen_handler)
    return logger

class ResizingCanvas(Canvas):
    def __init__(self,parent,**kwargs):
        Canvas.__init__(self,parent,**kwargs)
        self.bind("<Configure>", self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

    def on_resize(self,event):
        # determine the ratio of old width/height to new width/height
        wscale = float(event.width)/self.width
        hscale = float(event.height)/self.height
        self.width = event.width
        self.height = event.height
        print("The width of Tkinter window:", event.width)
        print("The height of Tkinter window:", event.height)

class Bibli:

    def __init__(self):
        self.logger = setup_custom_logger('mylogger')
        self.logger.info('------------------------------------------')
        self.logger.info('-------------Lancement init---------------')

        #initialisation des classes
        self.db = database.Database("dbBibli.db")
        self.bks = APIBooks.APIBooks()

        self.ep = ecranPret.ecranPret(self)
        self.usr = ecranUtilisateurs.ecranUtilisateurs(self)
        self.ctlg = ecranCatalogue.ecranCatalogue(self)
        self.style = Style("flatly")
        self.fenetre = self.style.master
        self.fenetre.geometry(config['DEFAULT']['Width'] + "x" +config['DEFAULT']['Height'])
        self.fenetre.title('Marliens Bibli')
        self.fenetre['bg']='white'

        # initialisation des champs en global
        self.sv_isbn = StringVar()
        self.sv_isbn_retour = StringVar()
        self.e_isbn = Entry(self.fenetre,textvariable=self.sv_isbn)

        self.e_titre = ""
        self.sv_titre = StringVar()
        self.sv_auteur = StringVar()
        self.sv_auteurComp = StringVar()
        self.sv_serie = StringVar()
        self.sv_tome = StringVar()


            # organisation des panneaux
        self.p = PanedWindow(self.fenetre, orient=HORIZONTAL)
        self.p.pack(side=TOP, expand=Y, fill=BOTH, pady=2, padx=2)
        self.p_left = PanedWindow(self.fenetre, orient=VERTICAL)
        self.p.add(self.p_left)
        self.p_right = PanedWindow(self.fenetre, orient=VERTICAL)
        self.p.add(self.p_right)

        # boutons menu gauche

        #  affiche la version        
        self.lb_vide = Label(self.fenetre, text = "")
        self.lb_version = Label(self.fenetre, text = "Version 1.02")
        self.lb_version.pack()

        self.bt_pret=Button(self.fenetre, text="Prêt", command=lambda: self.ep.afficherEcran(self.p_right, self.fenetre, self.db))
        self.bt_pret.pack()
        self.bt_user=Button(self.fenetre, text="Utilisateurs", command=lambda: self.usr.afficherEcran(self.p_right, self.fenetre, self.db))
        self.bt_user.pack()
        self.bt_catalogue=Button(self.fenetre, text="Catalogue", command=lambda: self.ctlg.afficherEcran(self.p_right, self.fenetre, self.db))
        self.bt_catalogue.pack()
        self.bt_close=Button(self.fenetre, text="Fermer", command=self.fenetre.quit)
        self.bt_close.pack()
        self.p_left.add(self.bt_pret)
        self.p_left.add(self.bt_user)
        self.p_left.add(self.bt_catalogue)
        self.p_left.add(self.bt_close)
        self.p_left.add(self.lb_version)
        self.p_left.add(self.lb_vide)
        self.lb_utilisateur = None
        self.p.pack()

    def clearPanelRight(self):
        # destroy all widgets from frame
        for widget in self.p_right.winfo_children():
            widget.destroy()        
        self.p_right.pack_forget()

    def main(self):
        self.logger.info('--main--')

        mycanvas = ResizingCanvas(self.p_right,width=1, height=1, bg="red", highlightthickness=0)
        mycanvas.pack(fill=BOTH, expand=YES)
        # tag all of the drawn widgets
        mycanvas.addtag_all("all")


        try:
            self.fenetre.mainloop()
        except Exception:
            logger.exception("Fatal error in main loop")
        self.ep.afficherEcran(self.p_right, self.fenetre, self.db)

if __name__ == '__main__':
    bibli = Bibli()
    bibli.main()