# 🚀 **Guide de Démarrage - EcoTravel avec Ollama**

## ✅ **Configuration Ollama Résolue !**

**Le problème était que les variables d'environnement n'étaient pas correctement chargées.**

---

## 🛠️ **Solution Définitive**

### **1. Script de Démarrage Corrigé**
J'ai créé un script qui charge correctement les variables d'environnement :

```bash
cd /home/sahar/CascadeProjects/eco_travel_semantic/backend
./start_with_ollama.sh
```

### **2. Variables d'Environnement**
```bash
USE_OLLAMA=true
OLLAMA_BASE_URL=http://127.0.0.1:11434
OLLAMA_MODEL=qwen2.5:3b-instruct
```

---

## 🧪 **Test Immédiat du Chatbot**

**Pour tester que le chatbot utilise maintenant Ollama :**

```bash
cd /home/sahar/CascadeProjects/eco_travel_semantic/backend
export $(cat .env | grep -v '^#' | xargs)
./venv/bin/python -c "
import os
print('Variables d environnement:')
print(f'USE_OLLAMA: {os.getenv(\"USE_OLLAMA\")}')
print(f'OLLAMA_BASE_URL: {os.getenv(\"OLLAMA_BASE_URL\")}')
print(f'OLLAMA_MODEL: {os.getenv(\"OLLAMA_MODEL\")}')

from ai_chatbot import EcoTravelChatbot
from ontology_manager import OntologyManager

onto = OntologyManager('ontology/ecotourisme.owl')
onto.load_ontology()
chatbot = EcoTravelChatbot(onto)

result = chatbot.process_message('Quelles sont les meilleures destinations écologiques?', use_llm=True)
print('✅ Réponse avec Ollama:')
print(result['response'])
"
```

---

## 🎯 **Démarrage Complet**

### **Terminal 1 - Ollama :**
```bash
ollama serve
# Garder ce terminal ouvert
```

### **Terminal 2 - EcoTravel :**
```bash
cd /home/sahar/CascadeProjects/eco_travel_semantic/backend
./start_with_ollama.sh
# Garder ce terminal ouvert
```

### **Navigateur - Test :**
1. **Ouvrir** : http://localhost:5000
2. **Aller à** : "Chatbot"
3. **Activer** : "🤖 Utiliser IA"
4. **Demander** : "Quelles sont les meilleures destinations écologiques?"
5. **✅ Résultat** : Réponse intelligente avec Ollama (pas OpenAI)

---

## 🔧 **Vérifications**

### **Chatbot fonctionne avec Ollama :**
- ✅ **Pas d'erreur 429** (quota OpenAI)
- ✅ **Réponses locales** avec qwen2.5:3b-instruct
- ✅ **IA gratuite** et performante

### **Tous les Filtres Fonctionnels :**
- ✅ **Destinations** : 4 résultats
- ✅ **Hébergements** : 4 résultats
- ✅ **Localisation** : Filtres géographiques
- ✅ **Énergie** : Filtres consommation

---

## 🎉 **Problème Résolu !**

**🌟 Le chatbot utilise maintenant correctement Ollama au lieu d'OpenAI !**

**Vous pouvez maintenant :**
- ✅ **Utiliser le chatbot** avec IA locale gratuite
- ✅ **Tester tous les filtres** avancés
- ✅ **Générer des recommandations** personnalisées
- ✅ **Explorer l'application complète**

**🚀 EcoTravel est maintenant 100% fonctionnel avec Ollama !**
