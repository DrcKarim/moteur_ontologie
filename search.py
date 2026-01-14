from rdflib import Graph, Namespace

EX = Namespace("http://example.org/biblio#")

g = Graph()
g.parse("biblio.owl", format="xml")

def livres_par_categorie(categorie):
    print(f"\n📚 Livres dans la catégorie : {categorie}")
    q = f"""
    PREFIX ex: <http://example.org/biblio#>
    SELECT ?livre WHERE {{
        ?livre a ex:Livre .
        ?livre ex:appartientA ex:{categorie} .
    }}
    """
    for row in g.query(q):
        print("-", row.livre.split("#")[-1])

def livres_empruntes_par(lecteur):
    print(f"\n👤 Livres empruntés par : {lecteur}")
    q = f"""
    PREFIX ex: <http://example.org/biblio#>
    SELECT ?livre WHERE {{
        ex:{lecteur} ex:emprunte ?livre .
    }}
    """
    for row in g.query(q):
        print("-", row.livre.split("#")[-1])

# Tests demandés dans le devoir
livres_par_categorie("Informatique")
livres_empruntes_par("Karim")
