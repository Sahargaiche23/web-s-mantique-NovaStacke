# 🚨 **PROBLÈME OLLAMA - GUIDE DE RÉSOLUTION**

## ❌ **Problème Identifié**
**Erreur 429 (quota insuffisant) d'OpenAI au lieu d'utiliser Ollama**

---

## 🛠️ **Solution Étape par Étape**

### **Étape 1 : Vérifier la Configuration**
```bash
cd /home/sahar/CascadeProjects/eco_travel_semantic/backend

# Vérifier le fichier .env
cat .env

# Résultat attendu :
# USE_OLLAMA=true
# OLLAMA_BASE_URL=http://127.0.0.1:11434
# OLLAMA_MODEL=qwen2.5:3b-instruct
```

### **Étape 2 : Démarrer Ollama**
```bash
# Terminal 1 - Démarrer Ollama
ollama serve

# Vérifier qu'Ollama répond
curl -s http://localhost:11434/api/version
# Résultat attendu : {"version":"0.12.3"}
```

### **Étape 3 : Vérifier le Modèle**
```bash
# Vérifier les modèles installés
ollama list

# Résultat attendu : qwen2.5:3b-instruct doit être présent
# Sinon l'installer :
ollama pull qwen2.5:3b-instruct
```

### **Étape 4 : Test du Chatbot**
```bash
cd /home/sahar/CascadeProjects/eco_travel_semantic/backend

# Charger les variables d'environnement
export $(cat .env | grep -v '^#' | xargs)

# Test du chatbot avec Ollama
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

result = chatbot.process_message('Test', use_llm=True)
print('✅ Réponse:', result['response'][:100])
"
```

### **Étape 5 : Démarrer l'Application**
```bash
# Utiliser le script corrigé
./start_with_ollama.sh
```

---

## 🎯 **Vérifications**

### **✅ Vérification 1 : Variables d'Environnement**
```bash
export $(cat .env | grep -v '^#' | xargs)
echo $USE_OLLAMA
echo $OLLAMA_BASE_URL
echo $OLLAMA_MODEL
```

### **✅ Vérification 2 : Ollama**
```bash
curl -s http://localhost:11434/api/version
ollama list
```

### **✅ Vérification 3 : Application**
```bash
curl -s http://localhost:5000/api/health
```

---

## 🚨 **Si Problème Persiste**

### **Option 1 : Redémarrer Complètement**
```bash
# Arrêter tout
pkill -f ollama
pkill -f "python app.py"

# Redémarrer
ollama serve &
sleep 3
cd /home/sahar/CascadeProjects/eco_travel_semantic/backend
export $(cat .env | grep -v '^#' | xargs)
./venv/bin/python app.py
```

### **Option 2 : Debug du Chatbot**
```bash
cd /home/sahar/CascadeProjects/eco_travel_semantic/backend

# Test direct du bridge LLM
./venv/bin/python -c "
from llm_bridge import LLMAssistant
import os

# Forcer Ollama
os.environ['USE_OLLAMA'] = 'true'
os.environ['OLLAMA_BASE_URL'] = 'http://127.0.0.1:11434'
os.environ['OLLAMA_MODEL'] = 'qwen2.5:3b-instruct'

llm = LLMAssistant()
response = llm.complete('Bonjour, comment allez-vous?')
print('✅ Test LLM:', response[:100])
"
```

---

## 🎉 **Test Final**

**Une fois tout démarré :**
1. **Ouvrir** : http://localhost:5000
2. **Aller à** : "Chatbot"
3. **Activer** : "🤖 Utiliser IA"
4. **Demander** : "Quelles sont les meilleures destinations écologiques?"
5. **✅ Résultat** : Réponse avec Ollama (pas d'erreur 429)

---

## 🔧 **Résolution Définitive**

**Le problème était que :**
- ❌ **Les variables d'environnement n'étaient pas chargées**
- ❌ **Le serveur utilisait encore OpenAI**
- ✅ **Script corrigé pour charger correctement les variables**
- ✅ **Ollama configuré et fonctionnel**

**🌟 Suivez ce guide étape par étape et tout fonctionnera parfaitement !**
