import sqlite3
from datetime import date

class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()

        self.cur.execute("PRAGMA foreign_keys = ON")  #Active les clés étrangères

        self.cur.executescript("""
        
        CREATE TABLE IF NOT EXISTS livres(
            livre_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            isbn TEXT,
            titre TEXT,
            auteur TEXT,
            auteurComp TEXT,
            serie TEXT,
            tome TEXT,
            code TEXT default null,
            mediatheque INTEGER default 0
            );
            
        CREATE TABLE IF NOT EXISTS utilisateurs(
            utilisateur_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            nom TEXT,
            prenom TEXT,
            dateDeNaissance DATE,
            adresse TEXT,
            tel TEXT
            );
        
        CREATE TABLE IF NOT EXISTS pret(
            pret_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            fk_utilisateur INTEGER NOT NULL,
            fk_livre INTEGER NOT NULL,
            datePret DATE,
            dateRetour DATE,
            FOREIGN KEY(fk_livre) REFERENCES livres(livre_id)
                ON DELETE CASCADE,
            FOREIGN KEY(fk_utilisateur) REFERENCES utilisateurs(utilisateur_id)
                ON DELETE CASCADE
            );
            """)

        # INSERT INTO livres (isbn, titre, auteur, auteurComp, serie, tome) VALUES ('9782874422362','Panique au supermarché','auteur, Ivan Velez Jr.',' dessin, Robert Pope... adaptation française, Céline Petitdidier','Scooby-Doo','2');
        # INSERT INTO livres (isbn, titre, auteur, auteurComp, serie, tome) VALUES ('9782874422364','truc et truc','auteur, Ivan Velez Jr.',' dessin, Robert Pope... adaptation française, Céline Petitdidier','Scooby-Doo','2');
        # INSERT INTO livres (isbn, titre, auteur, auteurComp, serie, tome) VALUES ('9782874422366','Super loto','auteur, Ivan Velez Jr.',' dessin, Robert Pope... adaptation française, Céline Petitdidier','Scooby-Doo','2');
        # INSERT INTO livres (isbn, titre, auteur, auteurComp, serie, tome) VALUES ('9782874422168','Les jeux de Bob l éponge','d après le dessin animé de Nickelodeon',' sur base d une idée originale de Steve Hillenburg','Les jeux de Bob l éponge','3');
        # INSERT INTO livres (isbn, titre, auteur, auteurComp, serie, tome) VALUES ('9782874422469','Les Parisiens','Désert &amp; Fab','','Les Parisiens',' ');
        # INSERT INTO livres (isbn, titre, auteur, auteurComp, serie, tome) VALUES ('9782874422569','Les machins','Désert &amp; Fab','','Les Parisiens',' ');

        # INSERT INTO utilisateurs (nom, prenom, dateDeNaissance, adresse, tel) VALUES ('Tom', 'Alen', '2008-01-02', '1 rue des fleurs', '0612457832');
        # INSERT INTO utilisateurs (nom, prenom, dateDeNaissance, adresse, tel) VALUES ('Hugo', 'Bart', '2008-01-02', '2 rue des fleurs', '0612457832');
        # INSERT INTO utilisateurs (nom, prenom, dateDeNaissance, adresse, tel) VALUES ('Lola', 'Sten', '2008-01-02', '3 rue des fleurs', '0612457832');
        # INSERT INTO utilisateurs (nom, prenom, dateDeNaissance, adresse, tel) VALUES ('Eli', 'Hall', '2008-01-02', '4 rue des fleurs', '0612457832');
        # INSERT INTO utilisateurs (nom, prenom, dateDeNaissance, adresse, tel) VALUES ('Lise', 'Leto', '2008-01-02', '5 rue des fleurs', '0612457832');

        # INSERT INTO pret (fk_utilisateur, fk_livre, datePret) VALUES (1, 1, '2021-01-02');
        # INSERT INTO pret (fk_utilisateur, fk_livre, datePret) VALUES (1, 2, '2021-02-02');
        # INSERT INTO pret (fk_utilisateur, fk_livre, datePret) VALUES (1, 3, '2021-03-02');
        # INSERT INTO pret (fk_utilisateur, fk_livre, datePret) VALUES (1, 4, '2021-04-02');
        # INSERT INTO pret (fk_utilisateur, fk_livre, datePret) VALUES (1, 5, '2021-05-02');
        # INSERT INTO pret (fk_utilisateur, fk_livre, datePret) VALUES (1, 6, '2021-06-02');
        #     """)

        self.conn.commit()
        # try :
        #     self.cur.executescript("""
        #     ALTER TABLE livres ADD COLUMN code TEXT default null;
        #     """)
        #     self.conn.commit()
        # except sqlite3.Error as er:
        #     print('SQLite error: %s' % (' '.join(er.args)))

        # try :
        #     self.cur.executescript("""
        #     ALTER TABLE livres ADD COLUMN mediatheque INTEGER default 0;
        #     """)
        #     self.conn.commit()
        # except sqlite3.Error as er:
        #     print('SQLite error: %s' % (' '.join(er.args)))


    def insert_livre(self, livre):
        print("try insert : " + livre["isbn"])
        resultat = self.fetch("select isbn from livres where isbn = "+livre["isbn"])
        print (len(resultat))
        # TODO si deja present popup erreur
        if len(resultat) == 0:
            print("ok insert : " + livre["isbn"])
            #donnee = [isbn, title]
            self.cur.execute('''INSERT INTO livres (isbn, titre, auteur, auteurComp, serie, tome, code, mediatheque) VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', 
                [livre["isbn"], livre["titre"], livre["auteur"], livre["auteurComp"], livre["serie"], livre["tome"],livre["indice"],livre["mediatheque"]])        
            self.conn.commit()


    def insertUtilisateurs(self, utilisateur):
        print("try insert : " + utilisateur["nom"])
        #donnee = [isbn, title]
        self.cur.execute('''INSERT INTO utilisateurs (nom, prenom, dateDeNaissance, adresse, tel) VALUES (?, ?, ?, ?, ?)''', 
            [utilisateur["nom"], utilisateur["prenom"], utilisateur["dateDeNaissance"], utilisateur["adresse"], utilisateur["tel"]])        
        self.conn.commit()

    def insertPret(self, isbn, utilisateur_id):
        print("try insert pret : " + str(isbn) + " pour "+str(utilisateur_id))
        #donnee = [isbn, title]
        self.cur.execute('''INSERT INTO pret (fk_utilisateur, fk_livre, datePret) VALUES (?, ?, ?)''', 
            [utilisateur_id, isbn, date.today()])        
        self.conn.commit()

    def retourPret(self, pret_id):
        print("try retour pret : " + str(pret_id) )
        #donnee = [isbn, title]
        self.cur.execute('''UPDATE pret SET dateRetour = ? WHERE  pret_id = ?''', 
            [date.today(), pret_id])        
        self.conn.commit()


    def fetch(self, query):
        self.cur.execute(query)
        rows = self.cur.fetchall()
        return rows

    # def fetchAll(self):
    #     self.cur.execute("select isbn, titre, auteur, serie, tome from livres")
    #     rows = self.cur.fetchall()
    #     return rows

    def filterBook(self, titre, auteur, mediatheque):
        print("filtre sur titre=" + str(titre) + " auteur=" + str(auteur)+ " mediatheque=" + str(mediatheque))
        self.cur.execute(
        "select l.titre, l.auteur, l.auteurComp, l.serie, l.tome, l.isbn, l.code, l.mediatheque, l.livre_id, p.datePret from livres l LEFT JOIN pret p on p.fk_livre = l.livre_id AND dateRetour is null where titre like ? and auteur like ? and mediatheque like ?",
        # "select titre, auteur,auteurComp, serie, tome,isbn,code, mediatheque, livre_id from livres where titre like ? and auteur like ? and mediatheque like ?",
        ('%'+titre+'%','%'+auteur+'%', mediatheque))
        rows = self.cur.fetchall()
        return rows


    def getLivreId(self, isbn):        
        self.cur.execute('''select livre_id from livres where isbn = ?''', (isbn,))
        return self.cur.fetchone()[0]

    def isbnExist(self, isbn):        
        self.cur.execute('''select livre_id from livres where isbn = ?''', (isbn,))
        if self.cur.fetchone() == None:
            return False
        return True

    def estDisponible(self, id):        
        self.cur.execute('''select fk_livre from pret where fk_livre = ? and dateRetour is null''', (id,))
        if self.cur.fetchone() == None:
            return True
        return False

    def emprunteur(self, livre_id):        
        self.cur.execute('''select u.nom, u.prenom, u.utilisateur_id, p.pret_id from pret p INNER JOIN utilisateurs u on p.fk_utilisateur = u.utilisateur_id where p.fk_livre = ? and dateRetour is null ''', (livre_id,))
        return self.cur.fetchone()

# obsolete
    def remove(self, id):
        print("try remove"+str(id))
        self.cur.execute("DELETE FROM livres WHERE isbn=?", (id,))
        self.conn.commit()

    def remove_book(self, id):
        print("try remove"+str(id))
        self.cur.execute("DELETE FROM livres WHERE isbn=?", (id,))
        self.conn.commit()

    def remove_user(self, id):
        print("try remove"+str(id))
        self.cur.execute("DELETE FROM utilisateurs WHERE utilisateur_id=?", (id,))
        self.conn.commit()

    def update_user(self, utilisateur, utilisateur_id):
        print("try update"+ utilisateur_id)
        self.cur.execute("UPDATE utilisateurs SET nom=?,prenom=?,dateDeNaissance=?,adresse=?,tel=? WHERE utilisateur_id=?", (utilisateur["nom"], utilisateur["prenom"], utilisateur["dateDeNaissance"], utilisateur["adresse"], utilisateur["tel"], utilisateur_id,))
        self.conn.commit()

# obsolete
    def update(self, id, isbn, title):
        self.cur.execute("UPDATE livres SET isbn = ?, title = ? WHERE id = ?",
                        (isbn, title, id))
        self.conn.commit()

    def update_book(self, book, book_id):
        print("try update"+ book_id + str(book))
        self.cur.execute("UPDATE livres SET isbn = ?, titre = ?,auteur= ?, auteurComp= ?, serie= ?, tome= ?, code = ?, mediatheque = ? WHERE livre_id = ?",
                        (book["isbn"], book["titre"], book["auteur"], book["auteurComp"], book["serie"], book["tome"],book["indice"],int(book["mediatheque"]), book_id))
        self.conn.commit()
    def __del__(self):
        self.conn.close()

