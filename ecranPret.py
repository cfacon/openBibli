from tkinter import * 
from tkinter import ttk
#from tkinter.messagebox import *
from tkinter import messagebox

class ecranPret:
    def __init__(self, parent):
        self.parent = parent
        self.selectionFiltred = []
        self.utilisateur_id = 0

    def popup(self, message):
        fInfos = Toplevel()		  # Popup -> Toplevel()
        fInfos.title('Infos')
        Button(fInfos, text='Quitter', command=fInfos.destroy).grid(row = 0, column = 0)
        label = Label(fInfos, text=message, bg="yellow").grid(row = 1, column = 0)
        fInfos.transient(jeu) 	  # Réduction popup impossible 
        fInfos.grab_set()		  # Interaction avec fenetre jeu impossible
        jeu.wait_window(fInfos)   # Arrêt script principal


    def clearPanel(self, panel):
        # destroy all widgets from frame
        for widget in panel.winfo_children():
            widget.destroy()
        panel.pack_forget()

    def select_tv_pret(self, event,tv_pret):
        index = self.tv_pret.selection()[0]
        self.parent.logger.info('--select_tv_pret--' + str(self.tv_pret.item(index)['values'][0]))
        self.sv_isbn_retour.set(self.tv_pret.item(index)['values'][0])


    def populate_liste_pret(self, tv, withHistory):
        print("populate_liste_pret"+str(self.utilisateur_id))

        query = """Select l.isbn, l.titre, p.datePret, p.dateRetour, l.mediatheque from pret p, utilisateurs u, livres l 
        where p.fk_utilisateur = u.utilisateur_id
        and u.utilisateur_id = """+str(self.utilisateur_id)+"""
        and p.fk_livre = l.livre_id
        and dateRetour is null
        """
        if withHistory:
            query = """Select l.isbn, l.titre, p.datePret, p.dateRetour, l.mediatheque from pret p, utilisateurs u, livres l 
        where p.fk_utilisateur = u.utilisateur_id
        and u.utilisateur_id = """+str(self.utilisateur_id)+"""
        and p.fk_livre = l.livre_id
        and dateRetour is not null
        """

        rows = self.parent.db.fetch(query)

        # self.tv_pret.tag_configure('oddrow', background='orange')
        # self.tv_pret.tag_configure('evenrow', background='purple')
        tv.tag_configure('oddrow', background='#E8E8E8')
        tv.tag_configure('even', background='#DFDFDF')

        for i in tv.get_children():
            tv.delete(i)
        n = 0
        for row in rows:
            n = n+1
            print (row)
            row = list(row)
            if (row[4] == 1) :
                row[4] = 'oui'
            else : 
                row[4] = 'non'
                            
            if (n % 2) == 0:
                tv.insert('', 'end', values=row,tags = ('oddrow',))
            else:
                tv.insert('', 'end', values=row,tags = ('even',))
        #tv.pack()



    def updateList(self, data):
        self.lb_utilisateur.delete(0,'end')

        for item in data:
            self.lb_utilisateur.insert(END,item[0]+" "+item[1]+" "+item[2])

    def CurSelet(self, event):
        self.sv_nom_selectionne.set("------")
        selectionName = self.lb_utilisateur.get(self.lb_utilisateur.curselection())

        index = int(self.lb_utilisateur.curselection()[0])
        #print(self.selectionFiltred[index][5])
        self.utilisateur_id = self.selectionFiltred[index][5]
        self.populate_liste_pret(self.tv_pret,False)
        self.populate_liste_pret(self.tv_pret_historique,True)


        # self.e_nom.insert(0,selectionName)
        self.sv_nom_selectionne.set(selectionName)

        self.bt_emprunter.config(state=NORMAL)
        
#        self.bt_emprunter.config(text="Emprunter pour "+selectionName)
        self.sv_bt_emprunter.set("Emprunter pour "+selectionName)
        self.sv_listeEmprunt.set("3 - Liste des emprunts de "+selectionName)

# autocomplete pour recherche user
    def check(self, e):    
        print("check")
        typed = self.sv_nom_selectionne.get()
        if typed == '':
            data = self.utilisateurs
        else:
            data = []
            for item in self.utilisateurs:
                if typed.lower() in item[0].lower()+" "+item[1].lower()+" "+item[2].lower():
                    data.append(item)


        self.selectionFiltred = data
        self.updateList(data)



    # tree view qui affiche la liste des prêts d'un user
    def build_tv_pret(self, frame):
        # init grid pret
        columns = [ 'isbn', 'titre', 'dateDePret', 'dateRetour','mediatheque']

        self.tv_pret = ttk.Treeview(frame, columns=columns, show="headings",style='info.Treeview')
        for col in columns:
            self.tv_pret.column(col, width=180)
            self.tv_pret.heading(col, text=col)
        self.tv_pret.bind('<<TreeviewSelect>>', lambda event : self.select_tv_pret(event, self.tv_pret))
        self.tv_pret.grid(row = 5, column = 0, columnspan = 3)
        return self.tv_pret

    # tree view qui affiche l'historique des prêts d'un user
    def build_tv_pret_historique(self, frame):
        # init grid pret
        columns = [ 'isbn', 'titre', 'dateDePret', 'dateRetour','mediatheque']

        self.tv_pret_historique = ttk.Treeview(frame, columns=columns, show="headings",style='info.Treeview')
        for col in columns:
            self.tv_pret_historique.column(col, width=180)
            self.tv_pret_historique.heading(col, text=col)
        self.tv_pret_historique.bind('<<TreeviewSelect>>', lambda event : self.select_tv_pret(event, self.tv_pret_historique))
        self.tv_pret_historique.grid(row = 7, column = 0, columnspan = 3)
        return self.tv_pret_historique

    def retour(self):
        # verifier qu'un user est bien selectionné et est connu
        livre_id = self.parent.db.getLivreId(self.sv_isbn_retour.get())
        print("retour de " + str(livre_id))
        if self.parent.db.estDisponible(livre_id):
            print("estDisponible donc pas de retour")
            messagebox.showwarning(title="Attention", message="ce livre n'est pas emprunté actuellement")
        else:
            emprunteur = self.parent.db.emprunteur(livre_id)
            self.parent.db.retourPret(emprunteur[3])
            print("bien retourné")
            self.populate_liste_pret(self.tv_pret,False)
            self.populate_liste_pret(self.tv_pret_historique,True)
            self.sv_isbn.set("")


    def emprunter(self):
        # verifier qu'un user est bien selectionné et est connu
        print("emprunter")

        # vérifier que l'isbn est ok aussi
        if self.parent.db.isbnExist(self.sv_isbn.get()):
            livre_id = self.parent.db.getLivreId(self.sv_isbn.get())
            if self.parent.db.estDisponible(livre_id):
                self.parent.db.insertPret(livre_id, self.utilisateur_id)
            else:
                emprunteur = self.parent.db.emprunteur(livre_id)
                # si l'id de l'emprunteur est le même que le user c'est un retour !
                if emprunteur[2] == self.utilisateur_id:
                    print("retour !")
                    print(emprunteur)
                    # print("emprunteur "+ emprunteur[0]+"-"+emprunteur[1]+"-"+emprunteur[2]+"-"+emprunteur[3])
                    self.parent.db.retourPret(emprunteur[3])
                else:
                    print(emprunteur)
                    messagebox.showwarning(title="Attention", message="ce livre est déjà emprunté par " + emprunteur[0]+" "+emprunteur[1])
        else:
            messagebox.showwarning(title="Attention", message="ISBN inconnue dans le catalogue !")
            #self.popup("attention ISBN inconnue dans le catalogue !")
        self.populate_liste_pret(self.tv_pret,False)
        self.populate_liste_pret(self.tv_pret_historique,True)
        self.sv_isbn.set("")


    def checkedHistory(self):
#        print("The checkbutton original value is {}".format(self.var1.get()))
        if self.var1.get():
            self.tv_pret_historique.grid(row = 7, column = 0, columnspan = 3)
        else:
            self.tv_pret_historique.grid_forget()

    def afficherEcran(self, pr, fenetre, db):
        self.sv_isbn = StringVar()
        self.sv_isbn_retour = StringVar()
        self.clearPanel(pr)
        self.pr = PanedWindow(pr, orient=VERTICAL)
        self.pr.pack(side=TOP, expand=Y, fill=BOTH, pady=2, padx=2)

        self.pr_top = PanedWindow(fenetre, orient=VERTICAL)
        self.pr.add(self.pr_top)
        self.pr_bottom = PanedWindow(fenetre, orient=VERTICAL)
        self.pr.add(self.pr_bottom)


        frame = Frame(self.pr_bottom,
                # border=1,
                relief=GROOVE
                # background="blue"
            )

        frame.grid(row=0, column=0, rowspan=6)



        # label = Label(frame, text="Ecran Prêt", bg="yellow").grid(row = 0, column = 0)
        lb_nom = Label(frame, text = "1 - Selectionnez un emprunteur: ").grid(row = 1, column = 0, padx = 0, pady = 0)


        # champe de filtre
        self.sv_nom_selectionne = StringVar()
        self.e_nom = Entry(frame,textvariable=self.sv_nom_selectionne, width=60)
        self.e_nom.bind('<KeyRelease>', self.check)
        self.e_nom.grid(row = 1, column = 1, padx = 0, pady = 0,sticky=W,columnspan = 3)

        # liste des utilisateurs
        self.utilisateurs = self.parent.db.fetch("Select nom,prenom,code, dateDeNaissance,adresse,tel,utilisateur_id from utilisateurs")
        self.selectionFiltred = self.utilisateurs


        self.lb_utilisateur=Listbox(frame,width=40,height=10,font=('times',13))
        self.lb_utilisateur.bind('<<ListboxSelect>>',self.CurSelet)
        self.lb_utilisateur.grid(row=2,column=1, padx = 0, pady = 0,sticky=W,columnspan = 3)

        # peuple la liste des users
        for user in self.utilisateurs:
            self.lb_utilisateur.insert(END,user[0]+" "+user[1]+" "+user[2])



        lb_isbn = Label(frame, text = "2 - Scan ISBN à emprunter: ").grid(sticky="W", row = 3, column = 0)
        # self.sv_isbn.set("9782874422362")
        self.e_isbn = Entry(frame,textvariable=self.sv_isbn).grid(sticky="W", row = 3, column = 1)



        self.sv_bt_emprunter = StringVar()
        self.sv_bt_emprunter.set("Sélectionner un emprunteur en 1")
        self.bt_emprunter=Button(frame, textvariable=self.sv_bt_emprunter,state=DISABLED, command=lambda: self.emprunter())
        self.bt_emprunter.grid(sticky="W", row = 3, column = 2)

        self.sv_listeEmprunt = StringVar()
        self.sv_listeEmprunt.set("3 - Liste des emprunts")
        self.lb_listeEmprunt = Label(frame, textvariable=self.sv_listeEmprunt)
        self.lb_listeEmprunt.grid(sticky="W", row = 4, column = 0,columnspan = 4)        
        self.tv_pret = self.build_tv_pret(frame)



        self.var1 = BooleanVar()
        self.var1.set(True)
        self.c1 = ttk.Checkbutton(frame, text="Afficher l'historique",variable=self.var1, onvalue=1, offvalue=0, command=lambda: self.checkedHistory())
        self.c1.grid(sticky="W", row = 6, column = 0,columnspan = 4)

        self.tv_pret_historique = self.build_tv_pret_historique(frame)

        #### RETOUR ####

        self.sv_titre_retour = StringVar()
        self.sv_titre_retour.set(" Retours")
        self.lb_listeEmprunt = Label(frame, textvariable=self.sv_titre_retour)
        self.lb_listeEmprunt.grid(sticky="W", row = 8, column = 0,columnspan = 4)        

        lb_isbn_retour = Label(frame, text = "1 - Scan ISBN pour retour: ").grid(sticky="W", row = 9, column = 0)
        self.sv_isbn_retour.set("")
        self.e_isbn_retour = Entry(frame,textvariable=self.sv_isbn_retour).grid(sticky="W", row = 9, column = 1)

        self.bt_retour=Button(frame, text="Valider retour", command=lambda: self.retour())
        self.bt_retour.grid(sticky="W", row = 9, column = 2, padx=5)
