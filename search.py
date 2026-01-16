from rdflib import Graph, Namespace
import os

EX = Namespace("http://example.org/biblio#")

g = Graph()
g.parse("biblio.owl", format="xml")

def get_book_info(livre_id):
    """Get book title and file path from book ID"""
    file_path = f"pages/livre_{livre_id.lower()}.txt"
    
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()
            # Extract title from "Titre: <title>"
            if first_line.startswith("Titre: "):
                titre = first_line.replace("Titre: ", "")
                return f"{titre} → {file_path}"
    
    # Fallback if file doesn't exist
    return f"{livre_id} → (fichier introuvable)"

def livres_par_categorie(categorie):
    """Search books by category"""
    print(f"\n📚 Livres dans la catégorie : {categorie}")
    q = f"""
    PREFIX ex: <http://example.org/biblio#>
    SELECT ?livre WHERE {{
        ?livre a ex:Livre .
        ?livre ex:appartientA ex:{categorie} .
    }}
    """
    results = list(g.query(q))
    if results:
        for row in results:
            livre_id = row.livre.split("#")[-1]
            print("-", get_book_info(livre_id))
    else:
        print("Aucun livre trouvé pour cette catégorie.")

def livres_empruntes_par(lecteur):
    """Search books borrowed by a user"""
    print(f"\n👤 Livres empruntés par : {lecteur}")
    q = f"""
    PREFIX ex: <http://example.org/biblio#>
    SELECT ?livre WHERE {{
        ex:{lecteur} ex:emprunte ?livre .
    }}
    """
    results = list(g.query(q))
    if results:
        for row in results:
            livre_id = row.livre.split("#")[-1]
            print("-", get_book_info(livre_id))
    else:
        print("Aucun livre trouvé pour cet utilisateur.")

def afficher_menu():
    """Display the main menu"""
    print("\n" + "="*50)
    print("🔍 SYSTÈME DE RECHERCHE BIBLIOTHÈQUE")
    print("="*50)
    print("1) Rechercher des livres par catégorie")
    print("2) Rechercher des livres empruntés par un utilisateur")
    print("3) Quitter")
    print("="*50)

def main():
    """Main program loop"""
    while True:
        afficher_menu()
        choix = input("\nChoisissez une option (1-3): ").strip()
        
        if choix == "1":
            categorie = input("\nEntrez le nom de la catégorie (ex: Informatique): ").strip()
            if categorie:
                livres_par_categorie(categorie)
            else:
                print("⚠️ Veuillez entrer un nom de catégorie valide.")
        
        elif choix == "2":
            lecteur = input("\nEntrez le nom de l'utilisateur (ex: Karim): ").strip()
            if lecteur:
                livres_empruntes_par(lecteur)
            else:
                print("⚠️ Veuillez entrer un nom d'utilisateur valide.")
        
        elif choix == "3":
            print("\n👋 Au revoir!")
            break
        
        else:
            print("\n❌ Option invalide. Veuillez choisir 1, 2 ou 3.")

if __name__ == "__main__":
    main()
