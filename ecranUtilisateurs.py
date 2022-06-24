from tkinter import * 
from tkinter import ttk
#from tkinter.messagebox import *
from tkinter.messagebox import *
from tkinter import messagebox
import logging
from ttkbootstrap import Style

class ecranUtilisateurs:
    def __init__(self, parent):
        self.parent = parent
        self.selectionFiltred = []
        self.utilisateur_id = 0

        self.style = Style("flatly")

    def clearPanel(self, panel):
        # destroy all widgets from frame
        for widget in panel.winfo_children():
            widget.destroy()
        panel.pack_forget()


    def updateList(self, data):
        self.lb_utilisateur.delete(0,'end')

        for item in data:
            self.lb_utilisateur.insert(END,item[0]+" "+item[1])

    def build_tv_utilisateur(self, frame):
        # get current size of main window
        curMainWindowHeight = self.parent.fenetre.winfo_height()
        curMainWindowWidth = self.parent.fenetre.winfo_width()
        print("The width of Tkinter window:", curMainWindowWidth)

        maxWidth = round((curMainWindowWidth-95) / 5)

        # init grid utilisateurs
        columns = [ 'nom', 'prenom', 'dateDeNaissance','adresse', 'tel']
        self.tv_utilisateur = ttk.Treeview(frame, columns=columns, show="headings",style='info.Treeview')
        for col in columns:
            self.tv_utilisateur.column(col, width=maxWidth)
            self.tv_utilisateur.heading(col, text=col)
        self.tv_utilisateur.bind('<<TreeviewSelect>>', lambda event : self.select_tv_utilisateur(event))
        self.populate_liste_utilisateur(self.tv_utilisateur)
        self.tv_utilisateur.grid(row = 1, column = 0, columnspan = 5)

        return self.tv_utilisateur

    def populate_liste_utilisateur(self, tv_utilisateur):
        rows = self.parent.db.fetch("Select nom,prenom,dateDeNaissance,adresse,tel,utilisateur_id from utilisateurs")

        tv_utilisateur.tag_configure('oddrow', background='#FFFFFF')
        tv_utilisateur.tag_configure('even', background='#AFAFDF')

        for i in tv_utilisateur.get_children():
            tv_utilisateur.delete(i)
        n = 0
        for row in rows:
            n = n+1
            print (row)
            if (n % 2) == 0:
                tv_utilisateur.insert('', 'end', values=row,tags = ('oddrow',))
            else:
                tv_utilisateur.insert('', 'end', values=row,tags = ('even',))



        self.bt_maj_utilisateur['state'] = DISABLED
        self.bt_supprimer_utilisateur['state'] = DISABLED

    def select_tv_utilisateur(self, event):
        try:
            self.bt_maj_utilisateur['state'] = NORMAL
            self.bt_supprimer_utilisateur['state'] = NORMAL
            index = self.tv_utilisateur.selection()[0]
            self.sv_nom.set(self.tv_utilisateur.item(index)['values'][0])
            self.sv_prenom.set(self.tv_utilisateur.item(index)['values'][1])
            self.sv_dateDeNaissance.set(self.tv_utilisateur.item(index)['values'][2])
            self.sv_adresse.set(self.tv_utilisateur.item(index)['values'][3])
            self.sv_tel.set(self.tv_utilisateur.item(index)['values'][4])
        except Exception as e:
            self.parent.logger.exception('--select_tv_utilisateur--' + str(e))   
        
    def supprimer_utilisateur(self,tv_utilisateur):
        index = tv_utilisateur.selection()[0]
        if askyesno('Titre 1', 'Êtes-vous sûr de vouloir supprimer ' +str(tv_utilisateur.item(index)['values'][1]) + ' '+str(tv_utilisateur.item(index)['values'][2]) + ' ?' + ' ID='+str(tv_utilisateur.item(index)['values'][5]) ):       
            # showwarning('Titre 2', 'Tant pis...')
            try:
                global selected_item
                selected_item = tv_utilisateur.item(index)['values']
                self.parent.db.remove_user(str(selected_item[5]))
                self.populate_liste_utilisateur(tv_utilisateur)
            except Exception as e:
                self.parent.logger.exception('--supprimer_utilisateur--' + str(e))   

    def modifier_utilisateur(self,tv_utilisateur):
        index = tv_utilisateur.selection()[0]
        if askyesno('Titre 1', 'Êtes-vous sûr de vouloir modifier ' +str(tv_utilisateur.item(index)['values'][1]) + ' '+str(tv_utilisateur.item(index)['values'][2]) + ' ?' + ' ID='+str(tv_utilisateur.item(index)['values'][5]) ):       
            # showwarning('Titre 2', 'Tant pis...')
            try:
                resultats = {"nom":"","prenom":"","dateDeNaissance":"","adresse":" ","tel":" "}
                resultats["nom"] = self.sv_nom.get()
                resultats["prenom"] = self.sv_prenom.get()
                resultats["dateDeNaissance"] = self.sv_dateDeNaissance.get()
                resultats["adresse"] = self.sv_adresse.get()
                resultats["tel"] = self.sv_tel.get()                
                self.parent.db.update_user(resultats,str(tv_utilisateur.item(index)['values'][5]))
                self.populate_liste_utilisateur(tv_utilisateur)
            except Exception as e:
                self.parent.logger.exception('--modifier_utilisateur--' + str(e))  

    def ajouter_utilisateur(self,tv_utilisateur):
        try:
            resultats = {"nom":"","prenom":"","dateDeNaissance":"","adresse":" ","tel":" "}
            resultats["nom"] = self.sv_nom.get()
            resultats["prenom"] = self.sv_prenom.get()
            resultats["dateDeNaissance"] = self.sv_dateDeNaissance.get()
            resultats["adresse"] = self.sv_adresse.get()
            resultats["tel"] = self.sv_tel.get()                
            self.parent.db.insertUtilisateurs(resultats)
            self.populate_liste_utilisateur(tv_utilisateur)
        except Exception as e:
            self.parent.logger.exception('--ajouter_utilisateur--' + str(e)) 


    def afficherEcran(self, pr, fenetre, db):
        self.parent.logger.info('--afficherEcran--')
        try:
            self.clearPanel(pr)
            self.pr = PanedWindow(pr, orient=VERTICAL)
            self.pr.pack(side=TOP, expand=Y, fill=BOTH, pady=2, padx=2)

            self.pr_top = PanedWindow(fenetre, orient=VERTICAL)
            self.pr.add(self.pr_top)
            self.pr_bottom = PanedWindow(fenetre, orient=VERTICAL)
            self.pr.add(self.pr_bottom)

            self.sv_nom = StringVar()
            self.sv_prenom = StringVar()
            self.sv_dateDeNaissance = StringVar()
            self.sv_adresse = StringVar()
            self.sv_tel = StringVar()


            frame = Frame(self.pr_bottom,
                    # border=1,
                    relief=GROOVE
                    # background="blue"
                )

            frame.grid(row=0, column=0, rowspan=6)


            self.bt_ajouter_utilisateur = Button(frame, text="Ajouter", command=lambda: self.ajouter_utilisateur(self.tv_utilisateur))
            self.bt_maj_utilisateur = Button(frame, text="Modifier", state = DISABLED, command=lambda: self.modifier_utilisateur(self.tv_utilisateur))
            self.bt_supprimer_utilisateur = Button(frame, text="Supprimer", state = DISABLED, command=lambda: self.supprimer_utilisateur(self.tv_utilisateur))


            # self.tv_utilisateur = self.build_tv_utilisateur(self.pr_top)
            self.tv_utilisateur = self.build_tv_utilisateur(frame)

            label = ttk.Label(self.pr_top, text="Utilisateurs",bootstyle='inverse-info',background="blue").grid(row = 0, column = 0,padx=20,pady=20)
            
            

            self.bt_ajouter_utilisateur.grid(row = 2, column = 0,padx=20,pady=20)
            self.bt_maj_utilisateur.grid(row = 2, column = 2,padx=20,pady=20)
            self.bt_supprimer_utilisateur.grid(row = 2, column = 4,padx=20,pady=20)



            lb_nom = Label(frame, text = "Nom :").grid(row = 4, column = 0)
            e_nom = Entry(frame,textvariable=self.sv_nom).grid(row = 4, column = 1,columnspan = 4)

            lb_prenom = Label(frame, text = "Prénom :").grid(row = 5, column = 0)
            e_prenom = Entry(frame,textvariable=self.sv_prenom).grid(row = 5, column = 1,columnspan = 4)

            lb_dateDeNaissance = Label(frame, text = "Date de naissance :").grid(row = 6, column = 0)
            e_dateDeNaissance = Entry(frame,textvariable=self.sv_dateDeNaissance).grid(row = 6, column = 1,columnspan = 4)

            lb_adresse = Label(frame, text = "Prénom :").grid(row = 7, column = 0)
            e_adresse = Entry(frame,textvariable=self.sv_adresse).grid(row = 7, column = 1,columnspan = 4)

            lb_tel = Label(frame, text = "Tel :").grid(row = 8, column = 0)
            e_tel = Entry(frame,textvariable=self.sv_tel).grid(row = 8, column = 1,columnspan = 4)

        # bt_search=Button(pr_top, text="Rechercher", command=lambda: self.Rechercher(tv_catalogue)).grid(row = 1, column = 2)


        except Exception as e:
            self.parent.logger.exception('--afficherEcran--' + str(e)) 




