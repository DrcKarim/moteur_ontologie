from flask import Flask, render_template, request
from rdflib import Graph, Namespace
import os

app = Flask(__name__)

# Load the ontology
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
                return {
                    'titre': titre,
                    'fichier': file_path
                }
    
    # Fallback if file doesn't exist
    return {
        'titre': livre_id,
        'fichier': '(fichier introuvable)'
    }

@app.route('/')
def home():
    """Home page with search options"""
    return render_template('index.html')

@app.route('/search-category')
def search_category_form():
    """Show the category search form"""
    return render_template('search_category.html')

@app.route('/search-user')
def search_user_form():
    """Show the user search form"""
    return render_template('search_user.html')

@app.route('/results-category', methods=['POST'])
def results_category():
    """Execute SPARQL query for books by category"""
    categorie = request.form.get('categorie', '').strip()
    
    if not categorie:
        return render_template('results.html', 
                             query_type="Catégorie", 
                             search_term="(vide)", 
                             results=[],
                             error="Veuillez entrer un nom de catégorie.")
    
    q = f"""
    PREFIX ex: <http://example.org/biblio#>
    SELECT ?livre WHERE {{
        ?livre a ex:Livre .
        ?livre ex:appartientA ex:{categorie} .
    }}
    """
    
    results = []
    for row in g.query(q):
        livre_id = row.livre.split("#")[-1]
        results.append(get_book_info(livre_id))
    
    return render_template('results.html', 
                         query_type="Catégorie", 
                         search_term=categorie, 
                         results=results)

@app.route('/results-user', methods=['POST'])
def results_user():
    """Execute SPARQL query for books borrowed by user"""
    lecteur = request.form.get('lecteur', '').strip()
    
    if not lecteur:
        return render_template('results.html', 
                             query_type="Utilisateur", 
                             search_term="(vide)", 
                             results=[],
                             error="Veuillez entrer un nom d'utilisateur.")
    
    q = f"""
    PREFIX ex: <http://example.org/biblio#>
    SELECT ?livre WHERE {{
        ex:{lecteur} ex:emprunte ?livre .
    }}
    """
    
    results = []
    for row in g.query(q):
        livre_id = row.livre.split("#")[-1]
        results.append(get_book_info(livre_id))
    
    return render_template('results.html', 
                         query_type="Utilisateur", 
                         search_term=lecteur, 
                         results=results)

if __name__ == '__main__':
    app.run(debug=True)
