#ISBN de test 9782924442883

from tkinter import * 
from tkinter import ttk
from tkinter.messagebox import *
from tkinter import messagebox
import logging

class ecranCatalogue:
    def __init__(self, parent):
        self.parent = parent
        self.selectionFiltred = []
        self.catalogue_id = 0

    def clearPanel(self, panel):
        # destroy all widgets from frame
        for widget in panel.winfo_children():
            widget.destroy()
        panel.pack_forget()


    def updateList(self, data):
        self.lb_catalogue.delete(0,'end')

        for item in data:
            self.lb_catalogue.insert(END,item[0]+" "+item[1])

    def build_tv_catalogue(self, frame):
        # get current size of main window
        curMainWindowHeight = self.parent.fenetre.winfo_height()
        curMainWindowWidth = self.parent.fenetre.winfo_width()
        print("The width of Tkinter window:", curMainWindowWidth)
        maxWidth = round((curMainWindowWidth-95) / 18) * 3
        minWidth = round((curMainWindowWidth-95) / 18)

        # init grid catalogue
        columns = [ 'Titre', 'Auteur', 'Complément', 'Serie', 'Tome','ISBN', 'Indice', 'Médiathèque','Numéro', 'Prêt']
        tv_catalogue = ttk.Treeview(frame, columns=columns, show="headings",style='info.Treeview')


        verscrlbar = ttk.Scrollbar(frame, orient ="vertical", command = tv_catalogue.yview)
        verscrlbar.grid(row = 2, column = 6, columnspan = 5, sticky="nse")

        tv_catalogue.configure(yscroll=verscrlbar.set)

        # for col in columns:
        tv_catalogue.column(columns[0], width=maxWidth)
        tv_catalogue.heading(columns[0], text=columns[0])
        tv_catalogue.column(columns[1], width=maxWidth)
        tv_catalogue.heading(columns[1], text=columns[1])
        tv_catalogue.column(columns[2], width=maxWidth)
        tv_catalogue.heading(columns[2], text=columns[2])
        tv_catalogue.column(columns[3], width=minWidth)
        tv_catalogue.heading(columns[3], text=columns[3])
        tv_catalogue.column(columns[4], width=minWidth)
        tv_catalogue.heading(columns[4], text=columns[4])
        tv_catalogue.column(columns[5], width=minWidth)
        tv_catalogue.heading(columns[5], text=columns[5])
        tv_catalogue.column(columns[6], width=minWidth)
        tv_catalogue.heading(columns[6], text=columns[6])
        tv_catalogue.column(columns[7], width=minWidth)
        tv_catalogue.heading(columns[7], text=columns[7])
        tv_catalogue.column(columns[8], width=minWidth)
        tv_catalogue.heading(columns[8], text=columns[8])
        tv_catalogue.column(columns[9], width=maxWidth)
        tv_catalogue.heading(columns[9], text=columns[9])



        tv_catalogue.bind('<<TreeviewSelect>>', lambda event : self.select_tv_catalogue(event))
        tv_catalogue.grid(row = 2, column = 0, columnspan = 7)
        self.populate_liste_catalogue(tv_catalogue)
        return tv_catalogue


    def populate_liste_catalogue(self, tv_catalogue):
        rows = self.parent.db.fetch("select l.titre, l.auteur, l.auteurComp, l.serie, l.tome, l.isbn, l.code, l.mediatheque, l.livre_id, p.datePret from livres l LEFT JOIN pret p on p.fk_livre = l.livre_id AND dateRetour is null ")
        self.fill_treeview(tv_catalogue, rows)

    # se repositionne sur le dernier element de la liste
    def jump_to_last(event, tree):
        first = tree.get_children()[0]
        # if tree.focus() == first:
        # print("if ok")
        last = tree.get_children()[-1]
        tree.selection_set(last) # move selection
        tree.focus(last) # move focus
        tree.see(last) # scroll to show it
        return "break" # don't send event to TreeView

    def fill_treeview(self, tv_catalogue, rows):
        tv_catalogue.tag_configure('oddrow', background='#FFFFFF')
        tv_catalogue.tag_configure('even', background='#AFAFDF')

        for i in tv_catalogue.get_children():
            tv_catalogue.delete(i)
        n = 0
        for row in rows:
            row = list(row)
            if (row[7] == 1) :
                row[7] = 'oui'
            else : 
                row[7] = 'non'


            n = n+1
            if (n % 2) == 0:
                tv_catalogue.insert('', 'end', values=row,tags = ('oddrow',))
            else:
                tv_catalogue.insert('', 'end', values=row,tags = ('even',))


        self.bt_maj_catalogue['state'] = DISABLED
        self.bt_supprimer_catalogue['state'] = DISABLED
        if (len(rows) > 0):
            self.jump_to_last(tv_catalogue)


    def filtre_liste_catalogue(self, tv_catalogue):
        mediaFiltre = "%"
        if(self.sv_mediatheque_filtre.get() == '1') :
            mediaFiltre = "1"


        rows = self.parent.db.filterBook(self.sv_titre_filtre.get(),self.sv_auteur_filtre.get(),self.sv_isbn_filtre.get(),mediaFiltre)
        self.fill_treeview(tv_catalogue, rows)

    def select_tv_catalogue(self, event):
        self.sv_log.set("")
        try:
            self.bt_maj_catalogue['state'] = NORMAL
            self.bt_supprimer_catalogue['state'] = NORMAL
            index = self.tv_catalogue.selection()[0]
            self.sv_titre.set(self.tv_catalogue.item(index)['values'][0])
            self.sv_auteur.set(self.tv_catalogue.item(index)['values'][1])
            self.sv_auteurComp.set(self.tv_catalogue.item(index)['values'][2])
            self.sv_serie.set(self.tv_catalogue.item(index)['values'][3])
            self.sv_tome.set(self.tv_catalogue.item(index)['values'][4])
            self.sv_isbn.set(self.tv_catalogue.item(index)['values'][5])
            self.sv_indice.set(self.tv_catalogue.item(index)['values'][6])
            self.sv_mediatheque.set(self.tv_catalogue.item(index)['values'][7])
        except Exception as e:
            self.parent.logger.exception('--select_tv_catalogue--' + str(e))                
        
    def supprimer_catalogue(self,tv_catalogue):
        index = tv_catalogue.selection()[0]

        self.parent.logger.info('--modifier_catalogue--' +str(tv_catalogue.item(index)['values'][1]) + ' '+str(tv_catalogue.item(index)['values'][2]) + ' ?' + ' ID='+str(tv_catalogue.item(index)['values'][6]) + ' ID='+str(tv_catalogue.item(index)['values'][5]))

        if askyesno('Titre 1', 'Êtes-vous sûr de vouloir supprimer ' +str(tv_catalogue.item(index)['values'][1]) + ' '+str(tv_catalogue.item(index)['values'][2]) + ' ?' + ' ID='+str(tv_catalogue.item(index)['values'][6]) + ' ID='+str(tv_catalogue.item(index)['values'][5])):       
            # showwarning('Titre 2', 'Tant pis...')
            try:
                global selected_item
                selected_item = tv_catalogue.item(index)['values']
                self.parent.db.remove_book(str(selected_item[5]))
                self.populate_liste_catalogue(tv_catalogue)
            except Exception as e:
                self.parent.logger.exception('--supprimer_catalogue--' + str(e))                
            except IndexError:
                pass

    def modifier_catalogue(self,tv_catalogue):
        self.sv_log.set("")
        index = tv_catalogue.selection()[0]
        self.parent.logger.info('--modifier_catalogue--' + str(tv_catalogue.item(index)['values'][1]) + ' '+str(tv_catalogue.item(index)['values'][2]) + ' ?' + ' ID='+str(tv_catalogue.item(index)['values'][8]))                

        if askyesno('Titre 1', 'Êtes-vous sûr de vouloir modifier ' +str(tv_catalogue.item(index)['values'][1]) + ' '+str(tv_catalogue.item(index)['values'][2]) + ' ?' + ' ID='+str(tv_catalogue.item(index)['values'][8]) ):       
            try:
                resultats = {"isbn":"","titre":"","auteur":"","auteurComp":"","serie":" ","tome":" ","indice":" ","mediatheque":" " }
                resultats["isbn"] = self.sv_isbn.get()
                resultats["titre"] = self.sv_titre.get()
                resultats["auteur"] = self.sv_auteur.get()
                resultats["auteurComp"] = self.sv_auteurComp.get()
                resultats["serie"] = self.sv_serie.get()
                resultats["tome"] = self.sv_tome.get()                
                resultats["indice"] = self.sv_indice.get()             
                mediatheque = 1
                print(self.sv_mediatheque.get())
                if self.sv_mediatheque.get() == 'non':
                    mediatheque = 0
                resultats["mediatheque"] = mediatheque
                self.parent.db.update_book(resultats,str(tv_catalogue.item(index)['values'][8]))
                self.populate_liste_catalogue(tv_catalogue)
            except Exception as e:
                self.parent.logger.exception('--modifier_catalogue--' + str(e))                
            except IndexError:
                pass

    def ajouter_catalogue(self,tv_catalogue):
        # TODO verifier les valeurs des champs !! surtout la forme de l'isbn
        self.sv_log.set("")
        self.parent.logger.info('--ajouter_catalogue--' + str(self.sv_isbn.get()))

        if(self.parent.db.isbnExist(self.sv_isbn.get())):
            self.sv_log.set("il y a déjà un livre dans le catalogue avec cet ISBN")
        else:
            try:
                resultats = {"isbn":"","titre":"","auteur":"","auteurComp":"","serie":" ","tome":" ","indice":" ","mediatheque":" " }
                resultats["isbn"] = self.sv_isbn.get()
                resultats["titre"] = self.sv_titre.get()
                resultats["auteur"] = self.sv_auteur.get()
                resultats["auteurComp"] = self.sv_auteurComp.get()
                resultats["serie"] = self.sv_serie.get()
                resultats["tome"] = self.sv_tome.get()
                resultats["indice"] = self.sv_indice.get()
                resultats["mediatheque"] = self.sv_mediatheque.get()           
                self.parent.db.insert_livre(resultats)
                self.populate_liste_catalogue(tv_catalogue)

                #clean ISBN et formulaire
                self.sv_isbn = StringVar()
                self.sv_titre = StringVar()
                self.sv_auteur = StringVar()
                self.sv_auteurComp = StringVar()
                self.sv_serie = StringVar()
                self.sv_tome = StringVar()
                self.sv_log = StringVar()
                self.e_isbn.focus()
            except Exception as e:
                self.parent.logger.exception('--erreur dans ajouter_catalogue --> ' + str(e))                
            except IndexError:
                pass

    def Rechercher(self, tv_catalogue):
        self.sv_log.set("")
        self.bt_maj_catalogue['state'] = DISABLED
        self.bt_supprimer_catalogue['state'] = DISABLED

        self.sv_titre.set("")
        self.sv_auteur.set("")
        self.sv_auteurComp.set("")
        self.sv_serie.set("")
        self.sv_tome.set("")

        self.myisbn = self.sv_isbn.get()
        self.recordSchema = "unimarcxchange"
        self.recordSchema = "dublincore"

        resultats = self.parent.bks.lookupBNF(self.myisbn, self.recordSchema)
        print ("res1=" + resultats["titre"] + "--")
        if (resultats["titre"] == ""):
            # print ("2pas de résultat pour cet ISBN !")
            resultats = self.parent.bks.lookupGoogleApi(self.myisbn)
            print ("res2=" + resultats["titre"]+ "--")

        resultats["isbn"] = self.myisbn
        self.sv_titre.set(resultats["titre"])
        self.sv_auteur.set(resultats["auteur"])
        self.sv_auteurComp.set(resultats["auteurComp"])
        self.sv_serie.set(resultats["serie"])
        self.sv_tome.set(resultats["tome"])
        self.e_isbn.focus()
        self.sv_log.set("Résultat de la recherche")

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

            self.sv_isbn = StringVar()
            self.sv_titre = StringVar()
            self.sv_auteur = StringVar()
            self.sv_auteurComp = StringVar()
            self.sv_serie = StringVar()
            self.sv_tome = StringVar()
            self.sv_indice = StringVar()
            self.sv_mediatheque = StringVar()            
            self.sv_mediatheque = StringVar()
            self.sv_log = StringVar()

            self.sv_titre_filtre = StringVar()
            self.sv_auteur_filtre = StringVar()
            self.sv_isbn_filtre = StringVar()
            self.sv_mediatheque_filtre = StringVar()
            self.sv_mediatheque_filtre.set(0)

            # s = Style()
            # s.configure('My.TFrame', background='red')

            frame = Frame(self.pr_bottom,
                    # border=1,
                    relief=GROOVE
                    ,bg='red'
                )

            frame.grid(row=1, column=0, columnspan=8, rowspan=8)

            # Filtre
            lb_titre_filtre = Label(self.pr_bottom, text = "Filtre titre :").grid(row = 0, column = 0)
            e_titre_filtre = Entry(self.pr_bottom,textvariable=self.sv_titre_filtre,).grid(row = 0, column = 1)
            lb_auteur_filtre = Label(self.pr_bottom, text = "Auteur :").grid(row = 0, column = 2)
            e_auteur_filtre = Entry(self.pr_bottom,textvariable=self.sv_auteur_filtre,width=20).grid(row = 0, column = 3)
            lb_isbn_filtre = Label(self.pr_bottom, text = "ISBN :").grid(row = 0, column = 4)
            e_isbn_filtre = Entry(self.pr_bottom,textvariable=self.sv_isbn_filtre,width=20).grid(row = 0, column = 5)
            c1f = Checkbutton(self.pr_bottom, text='Médiathèque',variable=self.sv_mediatheque_filtre, onvalue=1, offvalue=0).grid(row = 0, column = 6)
            self.bt_filtre = Button(self.pr_bottom, text="Filtrer", command=lambda: self.filtre_liste_catalogue(self.tv_catalogue))
            self.bt_filtre.grid(row = 0, column = 7,padx=2)


            # Bouton d'action
            self.bt_ajouter_catalogue = Button(frame, text="Ajouter", command=lambda: self.ajouter_catalogue(self.tv_catalogue))
            self.bt_maj_catalogue = Button(frame, text="Modifier", state = DISABLED, command=lambda: self.modifier_catalogue(self.tv_catalogue))
            self.bt_supprimer_catalogue = Button(frame, text="Supprimer", state = DISABLED, command=lambda: self.supprimer_catalogue(self.tv_catalogue))


            # Grille
            self.tv_catalogue = self.build_tv_catalogue(frame)
            label = ttk.Label(self.pr_top, text="Catalogue",bootstyle='inverse-info',background="blue").grid(row = 0, column = 0,padx=20,pady=20)





            
            self.bt_ajouter_catalogue.grid(row = 3, column = 0,padx=20,pady=20)
            self.bt_maj_catalogue.grid(row = 3, column = 2,padx=20,pady=20)
            self.bt_supprimer_catalogue.grid(row = 3, column = 4,padx=20,pady=20)


            # Formulaire CRUD
            lb_titre = Label(frame, text = "Titre :").grid(row = 5, column = 0)
            e_titre = Entry(frame,textvariable=self.sv_titre,width=60).grid(row = 5, column = 1)

            lb_auteur = Label(frame, text = "Auteur :").grid(row = 6, column = 0)
            e_auteur = Entry(frame,textvariable=self.sv_auteur,width=60).grid(row = 6, column = 1)

            lb_auteurComp = Label(frame, text = "Complément :").grid(row = 7, column = 0)
            e_auteurComp = Entry(frame,textvariable=self.sv_auteurComp,width=60).grid(row = 7, column = 1)

            lb_serie = Label(frame, text = "Série :").grid(row = 8, column = 0)
            e_serie = Entry(frame,textvariable=self.sv_serie,width=60).grid(row = 8, column = 1)

            lb_tome = Label(frame, text = "Tome :").grid(row = 9, column = 0)
            e_tome = Entry(frame,textvariable=self.sv_tome,width=60).grid(row = 9, column = 1)

            # TODO liste a mettre en base
            indices = [
                "R",
                "RP",
                "D",
                "BD",
                "C",
                "P",
                "JA",
                "JD",
                "BDJ",
                "JC",
                "JR"
            ]
            
            # initial menu text
            self.sv_indice.set( "..." )
            
            # Create Dropdown menu
            lb_code = Label(frame, text = "Indice :").grid(row = 10, column = 0)
            self.drop = OptionMenu( frame , self.sv_indice , *indices).grid(row = 10, column = 1)

            #lb_mediatheque = Label(frame, text = "Indice :").grid(row = 10, column = 0)
            c1 = Checkbutton(frame, text='Médiathèque',variable=self.sv_mediatheque, onvalue=1, offvalue=0).grid(row = 10, column = 2)

            lb_isbn = Label(frame, text = "ISBN :").grid(row = 11, column = 0)
            self.e_isbn = Entry(frame,textvariable=self.sv_isbn,width=60)
            self.e_isbn.grid(row = 11, column = 1)
            bt_search=Button(frame, text="Rechercher", command=lambda: self.Rechercher(self.tv_catalogue)).grid(row = 11, column = 2)

            self.lb_log = Label(frame, textvariable=self.sv_log,width=60).grid(row = 12, column = 0)

        # bt_search=Button(pr_top, text="Rechercher", command=lambda: self.Rechercher(tv_catalogue)).grid(row = 1, column = 2)

        except Exception as e:
            self.parent.logger.exception('--afficherEcran--' + str(e))
            

