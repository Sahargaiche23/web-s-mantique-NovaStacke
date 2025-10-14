#!/bin/bash

# Script de démarrage rapide pour EcoTravel
# Usage: ./start.sh

echo "=========================================="
echo "🌍 EcoTravel - Démarrage de l'application"
echo "=========================================="
echo ""

# Vérifier Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 n'est pas installé"
    exit 1
fi

echo "✓ Python détecté: $(python3 --version)"

# Créer l'environnement virtuel si nécessaire
if [ ! -d "venv" ]; then
    echo "📦 Création de l'environnement virtuel..."
    python3 -m venv venv
fi

# Activer l'environnement virtuel
echo "🔧 Activation de l'environnement virtuel..."
source venv/bin/activate

# Installer les dépendances
echo "📥 Installation des dépendances..."
pip install -q -r requirements.txt

# Vérifier que l'ontologie existe
if [ ! -f "ontology/ecotourisme.owl" ]; then
    echo "❌ Fichier ontologie manquant: ontology/ecotourisme.owl"
    exit 1
fi

echo "✓ Ontologie trouvée"

# Lancer l'application
echo ""
echo "=========================================="
echo "🚀 Lancement du serveur Flask..."
echo "=========================================="
echo ""
echo "📍 URL: http://localhost:5000"
echo "📖 Documentation: README.md"
echo "📚 Guide: GUIDE_UTILISATION.md"
echo ""
echo "Appuyez sur Ctrl+C pour arrêter le serveur"
echo ""

cd backend
python app.py
