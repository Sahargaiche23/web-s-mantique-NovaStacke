# 🚨 **INSTRUCTIONS URGENTES - Résoudre le Problème Ollama**

## ❌ **Problème Actuel**
**Ollama est en cours d'exécution mais avec des problèmes de permissions**

---

## 🛠️ **Résolution Immédiate**

### **Étape 1 : Arrêter Ollama (avec sudo)**
```bash
# Dans votre terminal, exécutez :
sudo kill 606976

# Ou plus généralement :
sudo pkill -f ollama
```

### **Étape 2 : Vérifier qu'Ollama est arrêté**
```bash
ps aux | grep ollama
# Ne doit rien retourner
```

### **Étape 3 : Redémarrer Ollama correctement**
```bash
# Démarrer Ollama en arrière-plan
ollama serve &
sleep 3

# Vérifier qu'il répond
curl -s http://localhost:11434/api/version
# Résultat attendu : {"version":"0.12.3"}
```

### **Étape 4 : Installer le modèle**
```bash
# Installer le modèle qwen2.5
ollama pull qwen2.5:3b-instruct

# Vérifier l'installation
ollama list
# Résultat attendu : qwen2.5:3b-instruct présent
```

### **Étape 5 : Configurer EcoTravel**
```bash
cd /home/sahar/CascadeProjects/eco_travel_semantic/backend

# Charger les variables d'environnement
export $(cat .env | grep -v '^#' | xargs)

# Vérifier la configuration
echo "USE_OLLAMA: $USE_OLLAMA"
echo "OLLAMA_BASE_URL: $OLLAMA_BASE_URL"
echo "OLLAMA_MODEL: $OLLAMA_MODEL"
```

### **Étape 6 : Tester le Chatbot**
```bash
cd /home/sahar/CascadeProjects/eco_travel_semantic/backend

# Test du chatbot avec Ollama
./venv/bin/python -c "
import os
print('Configuration:')
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

### **Étape 7 : Démarrer l'Application**
```bash
# Utiliser le script corrigé
./start_with_ollama.sh
```

---

## 🎯 **Vérification Finale**

### **Terminal 1 - Vérifier Ollama :**
```bash
curl -s http://localhost:11434/api/version
ollama list
```

### **Terminal 2 - Vérifier EcoTravel :**
```bash
curl -s http://localhost:5000/api/health
```

### **Navigateur - Test Final :**
1. **Ouvrir** : http://localhost:5000
2. **Aller à** : "Chatbot"
3. **Activer** : "🤖 Utiliser IA"
4. **Demander** : "Quelles destinations écologiques recommandez-vous?"
5. **✅ Résultat** : Réponse intelligente avec Ollama

---

## 🚨 **Commandes Importantes**

```bash
# Arrêter Ollama (avec sudo si nécessaire)
sudo pkill -f ollama

# Démarrer Ollama
ollama serve &

# Installer le modèle
ollama pull qwen2.5:3b-instruct

# Démarrer EcoTravel
cd /home/sahar/CascadeProjects/eco_travel_semantic/backend
./start_with_ollama.sh
```

---

## 🎉 **Vous Serez Bientôt Prêt !**

**Suivez ces étapes dans l'ordre et tout fonctionnera parfaitement !**
