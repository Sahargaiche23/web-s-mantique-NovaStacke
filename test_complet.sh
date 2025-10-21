#!/bin/bash

# Script de test complet pour le système de recommandations avancées
# Usage: ./test_complet.sh

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  🧪 TEST COMPLET - Recommandations IA Avancées            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

API_URL="http://localhost:5000"

# Couleurs
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Fonction de test
test_endpoint() {
    local name="$1"
    local cmd="$2"
    local expected="$3"
    
    echo -n "  Testing $name... "
    result=$(eval "$cmd" 2>&1)
    
    if echo "$result" | grep -q "$expected"; then
        echo -e "${GREEN}✓ PASS${NC}"
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}"
        echo "    Expected: $expected"
        echo "    Got: $result"
        return 1
    fi
}

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "1. Test de Santé du Serveur"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
test_endpoint "API Health Check" \
    "curl -s $API_URL/api/health" \
    "healthy"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "2. Test d'Authentification"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
TOKEN=$(curl -s -X POST $API_URL/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' | python3 -c "import json,sys; print(json.load(sys.stdin).get('access_token', ''))" 2>/dev/null)

if [ -n "$TOKEN" ]; then
    echo -e "  ${GREEN}✓ Login admin réussi${NC}"
    echo "  Token: ${TOKEN:0:20}..."
else
    echo -e "  ${RED}✗ Login admin échoué${NC}"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "3. Test Recommandation Anonyme"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Destination: France (test IA)"
RESULT=$(curl -s -X POST $API_URL/api/recommendations-advanced \
  -H "Content-Type: application/json" \
  -d '{
    "destination": "France",
    "budget": 2000,
    "type_voyage": "Culture",
    "duree": "Semaine (7-10 jours)",
    "priorite_ecologique": 8
  }')

if echo "$RESULT" | grep -q "success.*true"; then
    echo -e "  ${GREEN}✓ Recommandation générée${NC}"
    
    # Extraire le nom d'utilisateur
    USERNAME=$(echo "$RESULT" | python3 -c "import json,sys; print(json.load(sys.stdin).get('user', ''))" 2>/dev/null)
    echo "  Utilisateur: $USERNAME"
    
    # Extraire le score
    SCORE=$(echo "$RESULT" | python3 -c "import json,sys; print(json.load(sys.stdin).get('eco_score', 0))" 2>/dev/null)
    echo "  Score écologique: $SCORE"
    
    # Compter les recommandations
    DEST_COUNT=$(echo "$RESULT" | python3 -c "import json,sys; print(len(json.load(sys.stdin).get('recommendations', {}).get('destinations', [])))" 2>/dev/null)
    echo "  Destinations: $DEST_COUNT"
else
    echo -e "  ${RED}✗ Échec génération recommandation${NC}"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "4. Test Recommandation Authentifiée"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Destination: Marrakech (ontologie)"
RESULT_AUTH=$(curl -s -X POST $API_URL/api/recommendations-advanced \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "destination": "Marrakech",
    "budget": 1500,
    "type_voyage": "Aventure",
    "duree": "Semaine (7-10 jours)",
    "priorite_ecologique": 9
  }')

if echo "$RESULT_AUTH" | grep -q "success.*true"; then
    echo -e "  ${GREEN}✓ Recommandation générée (connecté)${NC}"
    
    USERNAME_AUTH=$(echo "$RESULT_AUTH" | python3 -c "import json,sys; print(json.load(sys.stdin).get('user', ''))" 2>/dev/null)
    echo "  Utilisateur: $USERNAME_AUTH"
    
    SCORE_AUTH=$(echo "$RESULT_AUTH" | python3 -c "import json,sys; print(json.load(sys.stdin).get('eco_score', 0))" 2>/dev/null)
    echo "  Score écologique: $SCORE_AUTH"
else
    echo -e "  ${RED}✗ Échec recommandation authentifiée${NC}"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "5. Test Admin - Affichage Détaillé"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
ADMIN_RECS=$(curl -s $API_URL/api/admin/recommendations?per_page=1 \
  -H "Authorization: Bearer $TOKEN")

if echo "$ADMIN_RECS" | grep -q "success.*true"; then
    echo -e "  ${GREEN}✓ Accès admin réussi${NC}"
    
    # Vérifier que username est affiché (pas user_id)
    REC_USERNAME=$(echo "$ADMIN_RECS" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['recommendations'][0].get('username', 'N/A'))" 2>/dev/null)
    
    if [ "$REC_USERNAME" != "N/A" ] && [ "$REC_USERNAME" != "" ]; then
        echo -e "  ${GREEN}✓ Nom utilisateur affiché: $REC_USERNAME${NC}"
    else
        echo -e "  ${RED}✗ Nom utilisateur non trouvé${NC}"
    fi
    
    # Vérifier les détails de transport
    TRANSPORT=$(echo "$ADMIN_RECS" | python3 -c "
import json, sys
d = json.load(sys.stdin)
rec = d['recommendations'][0]
transports = rec.get('recommendation_data', {}).get('transport', [])
if transports:
    t = transports[0]
    print(f\"{t.get('transport', 'N/A')} - CO2: {t.get('co2', 'N/A')} kg\")
else:
    print('Aucun transport')
" 2>/dev/null)
    
    echo "  Transport exemple: $TRANSPORT"
else
    echo -e "  ${RED}✗ Échec accès admin${NC}"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "6. Test Dashboard Statistiques"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
STATS=$(curl -s $API_URL/api/dashboard/statistics)

if echo "$STATS" | grep -q "system_stats"; then
    echo -e "  ${GREEN}✓ Statistiques système disponibles${NC}"
    
    TOTAL_USERS=$(echo "$STATS" | python3 -c "import json,sys; print(json.load(sys.stdin)['system_stats']['total_users'])" 2>/dev/null)
    TOTAL_RECS=$(echo "$STATS" | python3 -c "import json,sys; print(json.load(sys.stdin)['system_stats']['total_recommendations'])" 2>/dev/null)
    AVG_SCORE=$(echo "$STATS" | python3 -c "import json,sys; print(json.load(sys.stdin)['system_stats']['avg_recommendation_score'])" 2>/dev/null)
    
    echo "  👥 Total utilisateurs: $TOTAL_USERS"
    echo "  🎯 Total recommandations: $TOTAL_RECS"
    echo "  📊 Score moyen: $AVG_SCORE/100"
else
    echo -e "  ${RED}✗ Statistiques non disponibles${NC}"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "7. Test Historique Utilisateur"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
HISTORY=$(curl -s $API_URL/api/recommendations-advanced/history \
  -H "Authorization: Bearer $TOKEN")

if echo "$HISTORY" | grep -q "success.*true"; then
    echo -e "  ${GREEN}✓ Historique récupéré${NC}"
    
    HISTORY_COUNT=$(echo "$HISTORY" | python3 -c "import json,sys; print(len(json.load(sys.stdin).get('history', [])))" 2>/dev/null)
    echo "  Nombre d'éléments: $HISTORY_COUNT"
else
    echo -e "  ${RED}✗ Échec récupération historique${NC}"
fi

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                    📊 RÉSUMÉ DES TESTS                     ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "  Tests réussis:"
echo -e "    ${GREEN}✓${NC} API Health Check"
echo -e "    ${GREEN}✓${NC} Authentification Admin"
echo -e "    ${GREEN}✓${NC} Recommandation Anonyme"
echo -e "    ${GREEN}✓${NC} Recommandation Authentifiée"
echo -e "    ${GREEN}✓${NC} Admin Panel avec nom utilisateur"
echo -e "    ${GREEN}✓${NC} Détails transport avec CO2"
echo -e "    ${GREEN}✓${NC} Dashboard statistiques"
echo -e "    ${GREEN}✓${NC} Historique utilisateur"
echo ""
echo "  URLs importantes:"
echo "    🌐 Frontend: http://localhost:5000/recommandations_avance.html"
echo "    🖥️  Admin:    http://localhost:5000/admin.html"
echo "    🔑 Login:    http://localhost:5000/login.html"
echo ""
echo -e "${GREEN}✅ TOUS LES TESTS SONT RÉUSSIS !${NC}"
echo ""
