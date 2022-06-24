import urllib
import urllib.request
import json
import textwrap

ns = {"srw":"http://www.loc.gov/zing/srw/", 
      "m":"http://catalogue.bnf.fr/namespaces/InterXMarc",
      "mn":"http://catalogue.bnf.fr/namespaces/motsnotices",
       "mxc":"info:lc/xmlns/marcxchange-v2",
       "dc":"http://purl.org/dc/elements/1.1/",
       "oai_dc":"http://www.openarchives.org/OAI/2.0/oai_dc/"}
ns_bnf = {"srw":"http://www.loc.gov/zing/srw/", 
          "m":"http://catalogue.bnf.fr/namespaces/InterXMarc",
          "mn":"http://catalogue.bnf.fr/namespaces/motsnotices",
          "mxc":"info:lc/xmlns/marcxchange-v2",
          "dc":"http://purl.org/dc/elements/1.1/",
          "oai_dc":"http://www.openarchives.org/OAI/2.0/oai_dc/"}

ns_abes = {
    "bibo" : "http://purl.org/ontology/bibo/",
    "bio" : "http://purl.org/vocab/bio/0.1/",
    "bnf-onto" : "http://data.bnf.fr/ontology/bnf-onto/",
    "dbpedia-owl" : "http://dbpedia.org/ontology/",
    "dbpprop" : "http://dbpedia.org/property/",
    "dc" : "http://purl.org/dc/elements/1.1/",
    "dcterms" : "http://purl.org/dc/terms/",
    "dctype" : "http://purl.org/dc/dcmitype/",
    "fb" : "http://rdf.freebase.com/ns/",
    "foaf" : "http://xmlns.com/foaf/0.1/",
    "frbr" : "http://purl.org/vocab/frbr/core#",
    "gr" : "http://purl.org/goodrelations/v1#",
    "isbd" : "http://iflastandards.info/ns/isbd/elements/",
    "isni" : "http://isni.org/ontology#",
    "marcrel" : "http://id.loc.gov/vocabulary/relators/",
    "owl" : "http://www.w3.org/2002/07/owl#",
    "rdac" : "http://rdaregistry.info/Elements/c/",
    "rdae" : "http://rdaregistry.info/Elements/e/",
    "rdaelements" : "http://rdvocab.info/Elements/",
    "rdafrbr1" : "http://rdvocab.info/RDARelationshipsWEMI/",
    "rdafrbr2" : "http://RDVocab.info/uri/schema/FRBRentitiesRDA/",
    "rdai" : "http://rdaregistry.info/Elements/i/",
    "rdam" : "http://rdaregistry.info/Elements/m/",
    "rdau" : "http://rdaregistry.info/Elements/u/",
    "rdaw" : "http://rdaregistry.info/Elements/w/",
    "rdf" : "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "rdfs" : "http://www.w3.org/2000/01/rdf-schema#",
    "skos" : "http://www.w3.org/2004/02/skos/core#"
    }

#myisbn = ' all "9782874422362"'
myisbn = ' all "9782733884201"'
myisbn = urllib.parse.quote(myisbn)
myurl = 'https://catalogue.bnf.fr/api/SRU?version=1.2&operation=searchRetrieve&query=bib.fuzzyISBN'+myisbn+'&recordSchema=unimarcxchange&maximumRecords=20&startRecord=1'

#dublincore
myurl = 'https://catalogue.bnf.fr/api/SRU?version=1.2&operation=searchRetrieve&query=bib.fuzzyISBN'+myisbn+'&recordSchema=dublincore&maximumRecords=20&startRecord=1'



from lxml import etree
import urllib.parse
from urllib import request
import urllib.error as error
from pathlib import Path

class APIBooks:
    def lookupGoogleApi(self, id):
        base_api_link = "https://www.googleapis.com/books/v1/volumes?q=isbn:"
        
        title = "non trouvé"
        authors = ""
        subtitle = ""
        with urllib.request.urlopen(base_api_link + id) as f:
            text = f.read()

        decoded_text = text.decode("utf-8")
        
        print(decoded_text)
        
        try:
            obj = json.loads(decoded_text) # deserializes decoded_text to a Python object
            volume_info = obj["items"][0] 
            title = volume_info["volumeInfo"]["title"]
            subtitle = volume_info["volumeInfo"]["subtitle"]
            authors = volume_info["volumeInfo"]["authors"]
            # imageLinks = volume_info["volumeInfo"]["imageLinks"]
        except KeyError:
            print("champ(s) absent google api..")
        except JSONDecodeError:
            pass        
        except :
            print("champ(s) absent google api..")
        # displays title, summary, author, domain, page count and language

        resultats = {"titre":"","auteur":"","auteurComp":"","serie":" ","tome":" "}
        resultats["titre"] = str(title)
        resultats["auteur"] = str(authors)
        resultats["auteurComp"] = str(subtitle)
        

        return resultats

    def lookupBNF(self, id, recordSchema):
        myisbn = ' all "'+id+'"'
        myisbn = urllib.parse.quote(myisbn)
        myurl = 'https://catalogue.bnf.fr/api/SRU?version=1.2&operation=searchRetrieve&query=bib.fuzzyISBN'+myisbn+'&'+recordSchema+'=dublincore&maximumRecords=20&startRecord=1'

        print ("------------------>"+myurl)

        resultats = {"titre":"","auteur":"","auteurComp":"","serie":" ","tome":" "}
        title =""
        authorSub=""
        try:
            resultat = etree.parse(request.urlopen(myurl))
        except etree.XMLSyntaxError as err:
            print_error

        # unimarc
        if (resultat.find("//srw:recordData/mxc:record", namespaces=ns) is not None):
            print("unimarc")
            record = resultat.xpath("//srw:recordData/mxc:record",namespaces=ns)[0]
            path = "mxc:datafield[@tag='200']"
            for field in record.xpath(path,namespaces=ns):
                for subfield in field.xpath("mxc:subfield",namespaces=ns):
                    if (subfield.get("code") == "a" and subfield.text != ""):
                        #print("title:"+str(subfield.text))
                        resultats["titre"] = str(subfield.text)
                    if (subfield.get("code") == "f" and subfield.text != ""):
                        resultats["auteur"] = str(subfield.text)
                    if (subfield.get("code") == "g" and subfield.text != ""):
                        resultats["auteurComp"] = resultats["auteurComp"] + " " + str(subfield.text)
            path = "mxc:datafield[@tag='461']"
            for field in record.xpath(path,namespaces=ns):
                for subfield in field.xpath("mxc:subfield",namespaces=ns):
                    if (subfield.get("code") == "t" and subfield.text != ""):
                        resultats["serie"] = str(subfield.text)
                    if (subfield.get("code") == "v" and subfield.text != ""):
                        resultats["tome"] = str(subfield.text)

        print (resultats)

        # DublinCore
        if (resultat.find("//srw:recordData/oai_dc:dc", namespaces=ns) is not None):
            print("DublinCore")

            namespaces = {'dc':'http://purl.org/dc/elements/1.1/',
                        'rdf':'http://www.w3.org/1999/02/22-rdf-syntax-ns#'}

            title_elements = resultat.findall('.//dc:title', namespaces) 
            # Each title element has a text method
            for title_element in title_elements:
                print(title_element.text)
                title = title_element.text
        
        return resultats