#!/bin/bash

echo "============================================================"
echo "🌍 EcoTravel - Démarrage avec Authentification"
echo "============================================================"
echo ""

# Vérifier si Python est installé
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 n'est pas installé. Veuillez l'installer d'abord."
    exit 1
fi

# Vérifier si pip est installé
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 n'est pas installé. Veuillez l'installer d'abord."
    exit 1
fi

# Vérifier si la base de données existe
if [ ! -f "database.db" ]; then
    echo "⚠️  Base de données non trouvée."
    echo ""
    echo "Options:"
    echo "1. Initialiser la base de données maintenant"
    echo "2. Quitter et initialiser manuellement avec 'python init_auth.py'"
    echo ""
    read -p "Votre choix (1 ou 2): " choice
    
    if [ "$choice" == "1" ]; then
        echo ""
        echo "🔧 Initialisation de la base de données..."
        python3 init_auth.py
        
        if [ $? -ne 0 ]; then
            echo "❌ Erreur lors de l'initialisation de la base de données."
            exit 1
        fi
    else
        echo "👋 Au revoir! N'oubliez pas d'exécuter: python3 init_auth.py"
        exit 0
    fi
fi

# Vérifier si les dépendances sont installées
echo "📦 Vérification des dépendances..."
if ! python3 -c "import flask" &> /dev/null; then
    echo "⚠️  Certaines dépendances semblent manquantes."
    read -p "Voulez-vous installer les dépendances maintenant? (o/n): " install_deps
    
    if [ "$install_deps" == "o" ] || [ "$install_deps" == "O" ]; then
        echo "📥 Installation des dépendances..."
        pip3 install -r requirements.txt
        
        if [ $? -ne 0 ]; then
            echo "❌ Erreur lors de l'installation des dépendances."
            exit 1
        fi
    else
        echo "⚠️  Certaines fonctionnalités pourraient ne pas fonctionner."
    fi
fi

# Vérifier si le fichier .env existe
if [ ! -f ".env" ]; then
    echo "⚠️  Fichier .env non trouvé."
    if [ -f ".env.example" ]; then
        read -p "Voulez-vous créer un fichier .env depuis .env.example? (o/n): " create_env
        
        if [ "$create_env" == "o" ] || [ "$create_env" == "O" ]; then
            cp .env.example .env
            echo "✅ Fichier .env créé. Veuillez le configurer si nécessaire."
        fi
    fi
fi

echo ""
echo "============================================================"
echo "🚀 Démarrage du serveur..."
echo "============================================================"
echo ""
echo "📌 Informations importantes:"
echo "   - Interface principale: http://localhost:5000"
echo "   - Connexion: http://localhost:5000/login.html"
echo "   - Admin Dashboard: http://localhost:5000/admin.html"
echo ""
echo "👤 Compte admin par défaut:"
echo "   - Username: admin"
echo "   - Password: admin123"
echo ""
echo "⚠️  Appuyez sur Ctrl+C pour arrêter le serveur"
echo "============================================================"
echo ""

# Démarrer l'application
cd backend
python3 app.py
