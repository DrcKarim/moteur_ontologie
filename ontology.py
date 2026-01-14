from rdflib import Graph, Literal, RDF, RDFS, URIRef, Namespace

# Namespace
EX = Namespace("http://example.org/biblio#")

# Graph
g = Graph()
g.bind("ex", EX)

# Classes
classes = ["Personne", "Lecteur", "Bibliothecaire", "Livre", "Auteur", "Categorie"]
for c in classes:
    g.add((EX[c], RDF.type, RDFS.Class))

# Sous-classes
g.add((EX.Lecteur, RDFS.subClassOf, EX.Personne))
g.add((EX.Bibliothecaire, RDFS.subClassOf, EX.Personne))

# Propriétés
g.add((EX.emprunte, RDF.type, RDF.Property))
g.add((EX.ecritPar, RDF.type, RDF.Property))
g.add((EX.appartientA, RDF.type, RDF.Property))

# Individus
g.add((EX.Karim, RDF.type, EX.Lecteur))
g.add((EX.Dupont, RDF.type, EX.Auteur))

g.add((EX.LivreIA, RDF.type, EX.Livre))
g.add((EX.LivreBD, RDF.type, EX.Livre))

g.add((EX.Informatique, RDF.type, EX.Categorie))

# Relations
g.add((EX.Karim, EX.emprunte, EX.LivreIA))
g.add((EX.LivreIA, EX.ecritPar, EX.Dupont))
g.add((EX.LivreIA, EX.appartientA, EX.Informatique))

g.add((EX.LivreBD, EX.ecritPar, EX.Dupont))
g.add((EX.LivreBD, EX.appartientA, EX.Informatique))

# Sauvegarde
g.serialize("biblio.owl", format="xml")

print("Ontologie créée : biblio.owl")
