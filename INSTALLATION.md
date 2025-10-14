# 🔧 Guide d'Installation - EcoTravel

## Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)
- Navigateur web moderne (Chrome, Firefox, Safari, Edge)
- 500 MB d'espace disque

## Installation Complète

### Méthode 1: Script Automatique (Recommandé)

```bash
cd /home/sahar/CascadeProjects/eco_travel_semantic
chmod +x start.sh
./start.sh
```

Le script effectue automatiquement:
1. Création de l'environnement virtuel
2. Installation des dépendances
3. Vérification de l'ontologie
4. Lancement du serveur

### Méthode 2: Installation Manuelle

```bash
# 1. Aller dans le répertoire
cd /home/sahar/CascadeProjects/eco_travel_semantic

# 2. Créer l'environnement virtuel
python3 -m venv venv

# 3. Activer l'environnement
source venv/bin/activate

# 4. Installer les dépendances
pip install -r requirements.txt

# 5. Lancer l'application
cd backend
python app.py
```

## Vérification de l'Installation

### Test 1: Vérifier l'API
```bash
curl http://localhost:5000/api/health
```

Résultat attendu:
```json
{
  "status": "healthy",
  "ontology_loaded": true
}
```

### Test 2: Accéder à l'interface
Ouvrir: http://localhost:5000

Vous devriez voir la page d'accueil avec les statistiques.

## Dépendances Installées

- flask==3.0.0
- flask-cors==4.0.0
- rdflib==7.0.0
- scikit-learn==1.3.2
- numpy==1.26.2
- pandas==2.1.4
- matplotlib==3.8.2
- seaborn==0.13.0
- plotly==5.18.0
- Et autres...

## Dépannage

### Problème: Python non trouvé
```bash
# Installer Python 3
sudo apt-get install python3 python3-pip  # Ubuntu/Debian
brew install python3  # macOS
```

### Problème: Permission refusée
```bash
chmod +x start.sh
chmod 644 ontology/*.owl
```

### Problème: Port 5000 occupé
Modifier le port dans `backend/app.py`:
```python
app.run(port=5001)  # Changer 5000 en 5001
```

## Prochaines Étapes

1. ✅ Installation terminée
2. 📖 Lire QUICK_START.md
3. 🎯 Tester les fonctionnalités
4. 📚 Consulter GUIDE_UTILISATION.md

Bon voyage écologique! 🌍🌱
