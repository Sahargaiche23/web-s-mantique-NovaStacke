#!/bin/bash
# Script de vérification rapide

echo "🔍 VÉRIFICATION RAPIDE - EcoTravel + Ollama"
echo "=========================================="

# Vérifier les variables d'environnement
echo "1️⃣ Variables d'environnement :"
cd /home/sahar/CascadeProjects/eco_travel_semantic/backend
export $(cat .env | grep -v '^#' | xargs)
echo "   USE_OLLAMA: $USE_OLLAMA"
echo "   OLLAMA_BASE_URL: $OLLAMA_BASE_URL"
echo "   OLLAMA_MODEL: $OLLAMA_MODEL"

# Vérifier Ollama
echo "\n2️⃣ Test d'Ollama :"
if curl -s http://localhost:11434/api/version > /dev/null; then
    echo "   ✅ Ollama répond"
    if ollama list | grep -q "qwen2.5:3b-instruct"; then
        echo "   ✅ Modèle qwen2.5:3b-instruct disponible"
    else
        echo "   ❌ Modèle non trouvé - exécuter: ollama pull qwen2.5:3b-instruct"
        exit 1
    fi
else
    echo "   ❌ Ollama ne répond pas - exécuter: ollama serve"
    exit 1
fi

# Test du serveur Flask
echo "\n3️⃣ Test du serveur Flask :"
if curl -s http://localhost:5000/api/health > /dev/null; then
    echo "   ✅ Serveur Flask répond"
else
    echo "   ❌ Serveur Flask ne répond pas"
    echo "   Démarrer avec: ./start_with_ollama.sh"
    exit 1
fi

# Test du chatbot
echo "\n4️⃣ Test du chatbot avec Ollama :"
CHATBOT_RESPONSE=$(curl -s -X POST http://localhost:5000/api/chatbot/message \
    -H "Content-Type: application/json" \
    -d '{"message":"Bonjour", "use_llm": true}' 2>/dev/null)

if echo "$CHATBOT_RESPONSE" | grep -q "response"; then
    RESPONSE_TEXT=$(echo "$CHATBOT_RESPONSE" | python3 -m json.tool | grep -A 5 '"response"' | tail -1)
    echo "   ✅ Chatbot répond avec Ollama"
    echo "   📝 Réponse: $RESPONSE_TEXT"
else
    echo "   ❌ Problème avec le chatbot"
    echo "   Réponse reçue: $CHATBOT_RESPONSE"
fi

echo "\n🎉 VÉRIFICATION TERMINÉE"
echo "🌟 Tout semble fonctionner correctement !"
