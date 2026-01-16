from rdflib import Graph, Literal, RDF, RDFS, URIRef, Namespace
import os

# Namespace
EX = Namespace("http://example.org/biblio#")

# Graph
g = Graph()
g.bind("ex", EX)

# Classes
classes = ["Personne", "Lecteur", "Bibliothecaire", "Livre", "Auteur", "Categorie"]
for c in classes:
    g.add((EX[c], RDF.type, RDFS.Class))

# Sous-classes de Personne
g.add((EX.Lecteur, RDFS.subClassOf, EX.Personne))
g.add((EX.Bibliothecaire, RDFS.subClassOf, EX.Personne))

# Catégorie générale "Informatique" (instance, pas sous-classe)
g.add((EX.Informatique, RDF.type, EX.Categorie))

# Sous-classes spécialisées de Categorie (hiérarchie de catégories)
categories_specialisees = [
    "IntelligenceArtificielle",
    "DataScience",
    "Cybersecurite",
    "Reseaux",
    "Programmation",
    "BasesDeDonnees",
    "Systemes"
]

for cat in categories_specialisees:
    g.add((EX[cat], RDF.type, RDFS.Class))
    g.add((EX[cat], RDFS.subClassOf, EX.Categorie))

# Propriétés
g.add((EX.emprunte, RDF.type, RDF.Property))
g.add((EX.ecritPar, RDF.type, RDF.Property))
g.add((EX.appartientA, RDF.type, RDF.Property))

# Individus - Lecteurs
g.add((EX.Karim, RDF.type, EX.Lecteur))

# Individus - Auteurs
auteurs = [
    "Dupont",
    "Martin",
    "Rousseau",
    "Bernard",
    "Petit",
    "Dubois",
    "Lambert",
    "Fontaine"
]

for auteur in auteurs:
    g.add((EX[auteur], RDF.type, EX.Auteur))

# Définition des livres avec leurs métadonnées
livres_data = [
    {
        "id": "LivreIA",
        "titre": "Introduction à l'Intelligence Artificielle",
        "auteur": "Dupont",
        "categorie": "IntelligenceArtificielle",
        "description": "Ce livre explore les fondements de l'IA, depuis les algorithmes de base jusqu'aux réseaux de neurones. Une introduction complète pour comprendre les enjeux et applications modernes de l'intelligence artificielle."
    },
    {
        "id": "LivreBD",
        "titre": "Bases de Données Relationnelles",
        "auteur": "Dupont",
        "categorie": "BasesDeDonnees",
        "description": "Guide complet sur les systèmes de gestion de bases de données relationnelles. Couvre SQL, la normalisation, et l'optimisation des requêtes pour des performances maximales."
    },
    {
        "id": "LivreML",
        "titre": "Machine Learning Pratique",
        "auteur": "Martin",
        "categorie": "IntelligenceArtificielle",
        "description": "Apprenez le machine learning avec des exemples concrets et des projets pratiques. Des algorithmes supervisés aux techniques de deep learning, en passant par l'évaluation des modèles."
    },
    {
        "id": "LivreDataScience",
        "titre": "Data Science avec Python",
        "auteur": "Rousseau",
        "categorie": "DataScience",
        "description": "Maîtrisez l'analyse de données avec Python, pandas, numpy et matplotlib. Des techniques de visualisation aux modèles prédictifs, tout pour devenir data scientist."
    },
    {
        "id": "LivreCyber",
        "titre": "Cybersécurité Avancée",
        "auteur": "Bernard",
        "categorie": "Cybersecurite",
        "description": "Protégez vos systèmes contre les cyberattaques modernes. Ce livre couvre le pentesting, la cryptographie, et les meilleures pratiques de sécurité informatique."
    },
    {
        "id": "LivreReseaux",
        "titre": "Architecture des Réseaux Informatiques",
        "auteur": "Petit",
        "categorie": "Reseaux",
        "description": "Comprenez les protocoles TCP/IP, le routage, et la conception de réseaux d'entreprise. Une référence essentielle pour les administrateurs réseau."
    },
    {
        "id": "LivrePython",
        "titre": "Python pour Débutants",
        "auteur": "Dubois",
        "categorie": "Programmation",
        "description": "Apprenez Python de zéro avec des exercices progressifs. De la syntaxe de base à la programmation orientée objet, tout pour bien débuter."
    },
    {
        "id": "LivreJava",
        "titre": "Java Enterprise Edition",
        "auteur": "Lambert",
        "categorie": "Programmation",
        "description": "Développez des applications d'entreprise robustes avec Java EE. Servlets, JSP, EJB et frameworks modernes pour créer des systèmes évolutifs."
    },
    {
        "id": "LivreLinux",
        "titre": "Administration Système Linux",
        "auteur": "Fontaine",
        "categorie": "Systemes",
        "description": "Maîtrisez l'administration de serveurs Linux. Configuration, sécurité, scripts bash, et gestion de services pour des infrastructures professionnelles."
    },
    {
        "id": "LivreCloud",
        "titre": "Cloud Computing et DevOps",
        "auteur": "Martin",
        "categorie": "Systemes",
        "description": "Découvrez AWS, Azure et les pratiques DevOps modernes. Automatisation, containers Docker, Kubernetes et CI/CD pour déploiements efficaces."
    }
]

# Créer les livres et leurs relations
for livre in livres_data:
    # Créer l'instance de livre
    g.add((EX[livre["id"]], RDF.type, EX.Livre))
    
    # Ajouter les relations
    g.add((EX[livre["id"]], EX.ecritPar, EX[livre["auteur"]]))
    g.add((EX[livre["id"]], EX.appartientA, EX[livre["categorie"]]))
    
    # Tous les livres appartiennent aussi à la catégorie générale "Informatique"
    g.add((EX[livre["id"]], EX.appartientA, EX.Informatique))

# Relations d'emprunt (exemples)
g.add((EX.Karim, EX.emprunte, EX.LivreIA))
g.add((EX.Karim, EX.emprunte, EX.LivrePython))

# Générer les fichiers de contenu dans /pages
pages_dir = "pages"
if not os.path.exists(pages_dir):
    os.makedirs(pages_dir)

for livre in livres_data:
    filename = f"{pages_dir}/livre_{livre['id'].lower()}.txt"
    content = f"""Titre: {livre['titre']}
Auteur: {livre['auteur']}
Catégorie: {livre['categorie']}

Description:
{livre['description']}
"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Fichier créé: {filename}")

# Sauvegarde de l'ontologie
g.serialize("biblio.owl", format="xml")

print("\n✅ Ontologie étendue créée : biblio.owl")
print(f"✅ {len(livres_data)} livres ajoutés")
print(f"✅ {len(auteurs)} auteurs créés")
print(f"✅ {len(categories_specialisees) + 1} catégories créées (dont Informatique générale)")
