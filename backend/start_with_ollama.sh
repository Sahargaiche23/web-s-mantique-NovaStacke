#!/bin/bash
# Script de démarrage EcoTravel avec Ollama

echo "🌍 Démarrage d'EcoTravel avec Ollama..."
echo "========================================"

# Charger les variables d'environnement
if [ -f .env ]; then
    echo "✓ Chargement des variables d'environnement..."
    export $(cat .env | grep -v '^#' | xargs)
fi

# Vérifier qu'Ollama est en cours d'exécution
if curl -s http://localhost:11434/api/version > /dev/null; then
    echo "✓ Ollama est en cours d'exécution"
else
    echo "❌ Ollama n'est pas en cours d'exécution"
    echo "   Démarrez Ollama avec: ollama serve"
    exit 1
fi

# Vérifier que le modèle est disponible
if ollama list | grep -q "qwen2.5:3b-instruct"; then
    echo "✓ Modèle qwen2.5:3b-instruct disponible"
else
    echo "❌ Modèle qwen2.5:3b-instruct non trouvé"
    echo "   Installez-le avec: ollama pull qwen2.5:3b-instruct"
    exit 1
fi

# Démarrer le serveur Flask
echo "🚀 Démarrage du serveur Flask..."
./venv/bin/python app.py
