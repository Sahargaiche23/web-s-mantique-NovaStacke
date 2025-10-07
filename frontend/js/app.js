// Configuration API
const API_BASE = 'http://localhost:5000/api';

// Navigation
function showPage(pageName) {
    document.querySelectorAll('.page-content').forEach(page => {
        page.classList.add('hidden');
    });
    document.getElementById(`page-${pageName}`).classList.remove('hidden');
    
    // Charger les données spécifiques à la page
    if (pageName === 'home') loadHomeData();
    if (pageName === 'sparql') loadSPARQLQueries();
    if (pageName === 'visualizations') loadVisualizations();
    if (pageName === 'ontology') loadOntologyData();
    if (pageName === 'chat') initChat();
}

// ==================== RECOMMANDATIONS ====================
document.getElementById('user-budget')?.addEventListener('input', (e) => {
    document.getElementById('budget-display').textContent = e.target.value + '€';
});

async function generateRecommendations() {
    const budgetEl = document.getElementById('user-budget');
    const profileEl = document.getElementById('user-eco-profile');
    const prefsEl = document.getElementById('user-preferences');
    const container = document.getElementById('recommendations-container');
    if (!container) return;
    const budget = budgetEl ? parseFloat(budgetEl.value || '0') : 0;
    const profile = profileEl ? profileEl.value : 'Modéré';
    const prefs = prefsEl ? prefsEl.value : '';
    container.innerHTML = '<p class="text-gray-500">Génération en cours...</p>';

    const payload = {
        max_budget: budget,
        eco_profile: profile,
        preferences: prefs
    };
    try {
        const res = await fetch(`${API_BASE}/recommendations/travel-plan`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.error || 'Erreur API');
        
        // Afficher score et empreinte
        if (data.total_eco_score !== undefined) {
            document.getElementById('estimated-eco-score').classList.remove('hidden');
            document.getElementById('eco-score-value').textContent = Math.round(data.total_eco_score);
        }
        if (data.estimated_carbon_footprint !== undefined || data.total_eco_score !== undefined) {
            const summary = document.getElementById('recommendations-summary');
            summary.classList.remove('hidden');
            document.getElementById('carbon-footprint').textContent = Math.round(data.estimated_carbon_footprint || 0);
            document.getElementById('total-eco-score').textContent = Math.round(data.total_eco_score || 0);
        }
        
        renderRecommendations(data);
    } catch (e) {
        container.innerHTML = `<p class="text-red-600">${e.message}</p>`;
    }
}

async function generateRecommendation() { return generateRecommendations(); }

function renderRecommendations(plan) {
    const container = document.getElementById('recommendations-container');
    if (!container) return;
    let html = '';
    
    const recs = plan.recommendations || {};
    
    if (recs.destinations && recs.destinations.length > 0) {
        html += '<div class="mb-6"><h4 class="font-bold text-lg mb-3 text-green-700 border-b-2 border-green-200 pb-2">🏞️ Destinations</h4><div class="space-y-2">';
        recs.destinations.forEach(d => { 
            const txt = d.destination ? `${d.destination} (${d.localisation}) - Score: ${Math.round(d.final_score)}` : d;
            html += `<div class="p-3 bg-green-50 border-l-4 border-green-500 rounded">${txt}</div>`; 
        });
        html += '</div></div>';
    }
    if (recs.accommodations && recs.accommodations.length > 0) {
        html += '<div class="mb-6"><h4 class="font-bold text-lg mb-3 text-blue-700 border-b-2 border-blue-200 pb-2">🏨 Hébergements</h4><div class="space-y-2">';
        recs.accommodations.forEach(a => { 
            const txt = a.hebergement ? `${a.hebergement} - ${a.energie} kWh - ${a.niveau} - Score: ${Math.round(a.final_score)}` : a;
            html += `<div class="p-3 bg-blue-50 border-l-4 border-blue-500 rounded">${txt}</div>`; 
        });
        html += '</div></div>';
    }
    if (recs.activities && recs.activities.length > 0) {
        html += '<div class="mb-6"><h4 class="font-bold text-lg mb-3 text-purple-700 border-b-2 border-purple-200 pb-2">🎯 Activités</h4><div class="space-y-2">';
        recs.activities.forEach(a => { 
            const txt = a.activite ? `${a.activite} - ${a.impact} - Score: ${Math.round(a.final_score)}` : a;
            html += `<div class="p-3 bg-purple-50 border-l-4 border-purple-500 rounded">${txt}</div>`; 
        });
        html += '</div></div>';
    }
    if (recs.transport && recs.transport.length > 0) {
        html += '<div class="mb-6"><h4 class="font-bold text-lg mb-3 text-yellow-700 border-b-2 border-yellow-200 pb-2">🚆 Transports</h4><div class="space-y-2">';
        recs.transport.forEach(t => { 
            const txt = t.transport ? `${t.transport} - ${t.co2} kg CO2 - Score: ${Math.round(t.final_score)}` : t;
            html += `<div class="p-3 bg-yellow-50 border-l-4 border-yellow-500 rounded">${txt}</div>`; 
        });
        html += '</div></div>';
    }
    if (plan.message) html += `<div class="p-4 bg-gray-100 rounded-lg border border-gray-300">${plan.message}</div>`;
    if (!html) html = '<p class="text-gray-500 text-center py-8">Aucune recommandation disponible</p>';
    container.innerHTML = html;
}

// ==================== HOME ====================
async function loadHomeData() {
    try {
        // Essayer d'abord le résumé détaillé
        let summary = await fetch(`${API_BASE}/ontology/summary`).then(r => r.json());
        if (summary && (summary.nbDestinations || summary.nbHebergements || summary.nbActivites)) {
            document.getElementById('stat-destinations').textContent = summary.nbDestinations || 0;
            document.getElementById('stat-accommodations').textContent = summary.nbHebergements || 0;
            document.getElementById('stat-activities').textContent = summary.nbActivites || 0;
        } else {
            // Fallback vers anciennes statistiques
            const stats = await fetch(`${API_BASE}/ontology/statistics`).then(r => r.json());
            document.getElementById('stat-destinations').textContent = stats.individuals || 0;
            document.getElementById('stat-accommodations').textContent = stats.classes || 0;
            document.getElementById('stat-activities').textContent = stats.object_properties || 0;
        }
    } catch (error) {
        console.error('Erreur chargement stats:', error);
    }
}

// ==================== RECHERCHE ====================
function clearSearchFilters() {
    document.getElementById('filter-text').value = '';
    document.getElementById('filter-energy').value = '';
    document.getElementById('filter-location').value = '';
    document.getElementById('filter-type').value = '';
    document.getElementById('search-results').innerHTML = '';
    document.getElementById('search-results-count').innerHTML = '';
}

async function performSearch() {
    const text = document.getElementById('filter-text').value;
    const energy = document.getElementById('filter-energy').value;
    const location = document.getElementById('filter-location').value;
    const type = document.getElementById('filter-type').value;
    
    const resultsDiv = document.getElementById('search-results');
    const countDiv = document.getElementById('search-results-count');
    resultsDiv.innerHTML = '<p class="text-gray-500">Recherche en cours...</p>';
    
    try {
        // Utiliser l'endpoint de filtrage avancé pour plus de dynamisme
        const payload = {};
        if (energy) payload.max_energy = parseFloat(energy);
        if (location) payload.location = location;
        if (text) payload.text = text;
        if (type) payload.entity_type = type;  // Ajouter le filtre de type

        const response = await fetch(`${API_BASE}/advanced/filter`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(payload)
        });

        const data = await response.json();
        let mapped = (data.results || []).map(r => ({
            'Entité': r.entity || '-',
            'Type': r.type || '-',
            'Localisation': r.localisation || '-',
            'Énergie': r.energie || '-',
            'Certification': r.niveau || '-'
        }));
        
        // Fallback: si aucun résultat mais du texte fourni, utiliser la recherche textuelle simple
        if ((!mapped || mapped.length === 0) && text) {
            const res2 = await fetch(`${API_BASE}/ontology/search`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ text })
            });
            const data2 = await res2.json();
            mapped = (data2.results || []).map(r => ({
                'Entité': r.subject || r.entity || '-',
                'Type': r.predicate || r.type || '-',
                'Localisation': r.object || r.value || r.relatedEntity || '-',
                'Énergie': '-',
                'Certification': '-'
            }));
        }
        
        // Mettre à jour le compteur APRÈS avoir récupéré tous les résultats
        countDiv.innerHTML = `<span class="font-semibold">${mapped.length}</span> résultat(s) trouvé(s)`;
        
        // Rendu
        if (!mapped || mapped.length === 0) {
            resultsDiv.innerHTML = '<p class="text-gray-500 text-center py-8">Aucun résultat trouvé</p>';
            return;
        }
        const keys = Object.keys(mapped[0]);
        let html = '<table class="min-w-full divide-y divide-gray-200">';
        html += '<thead class="bg-gray-50"><tr>';
        keys.forEach(k => { html += `<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">${k}</th>`; });
        html += '</tr></thead>';
        html += '<tbody class="bg-white divide-y divide-gray-200">';
        mapped.forEach(row => {
            html += '<tr>';
            keys.forEach(k => { html += `<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${row[k] || '-'}</td>`; });
            html += '</tr>';
        });
        html += '</tbody></table>';
        resultsDiv.innerHTML = html;
    } catch (error) {
        resultsDiv.innerHTML = `<p class="text-red-500">Erreur: ${error.message}</p>`;
    }
}
 
// ==================== SPARQL ====================
async function loadSPARQLQueries() {
    try {
        const response = await fetch(`${API_BASE}/sparql/queries`);
        const data = await response.json();
        const listDiv = document.getElementById('sparql-queries-list');
        let html = '<div class="space-y-2">';
        (data.queries || []).forEach(query => {
            const label = query.replaceAll('_', ' ');
            html += `
                <button id="sparql-btn-${query}" class="w-full text-left px-3 py-2 rounded hover:bg-green-50" onclick="loadPredefinedQuery('${query}')">
                    ${label}
                </button>
            `;
        });
        html += '</div>';
        listDiv.innerHTML = html;
        // Auto-charger la première requête pour pré-remplir l'éditeur
        if (data.queries && data.queries.length > 0) {
            loadPredefinedQuery(data.queries[0]);
        } else {
            const editor = document.getElementById('sparql-editor');
            if (editor) editor.value = '# Entrez une requête SPARQL ici';
            const resultsDiv = document.getElementById('sparql-results');
            if (resultsDiv) resultsDiv.innerHTML = '<p class="text-gray-500">Aucune requête prédéfinie disponible</p>';
        }
    } catch (error) {
        console.error('Erreur chargement requêtes:', error);
    }
}

function displaySPARQLResults(results) {
    const resultsDiv = document.getElementById('sparql-results');
    if (!results || results.length === 0) {
        resultsDiv.innerHTML = '<p class="text-gray-500">Aucun résultat</p>';
        return;
    }
    // Construire l'union des colonnes sur toutes les lignes
    const keySet = new Set();
    results.forEach(row => {
        Object.keys(row || {}).forEach(k => keySet.add(k));
    });
    const keys = Array.from(keySet);
    if (keys.length === 0) {
        resultsDiv.innerHTML = '<p class="text-gray-500">Aucun résultat</p>';
        return;
    }
    let html = `<div class=\"mb-2 text-xs text-gray-500\">${results.length} résultat(s)</div>`;
    html += '<table class="min-w-full divide-y divide-gray-200">';
    html += '<thead class="bg-gray-50"><tr>';
    keys.forEach(key => { html += `<th class=\"px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase\">${key}</th>`; });
    html += '</tr></thead>';
    html += '<tbody class="bg-white divide-y divide-gray-200">';
    results.forEach(row => {
        html += '<tr>';
        keys.forEach(key => { html += `<td class=\"px-6 py-4 whitespace-nowrap text-sm text-gray-900\">${(row && row[key]) || '-'}</td>`; });
        html += '</tr>';
    });
    html += '</tbody></table>';
    resultsDiv.innerHTML = html;
    resultsDiv.scrollIntoView({behavior:'smooth', block:'start'});
}
async function loadPredefinedQuery(queryName) {
    try {
        const response = await fetch(`${API_BASE}/sparql/predefined/${queryName}`);
        const data = await response.json();
        // Remplir l'éditeur avec la requête pour que l'utilisateur puisse la voir/éditer
        const editor = document.getElementById('sparql-editor');
        if (editor && data.query) editor.value = data.query;
        // Marquer actif le bouton sélectionné
        document.querySelectorAll('#sparql-queries-list button').forEach(b=>b.classList.remove('bg-green-100'));
        const activeBtn = document.getElementById(`sparql-btn-${queryName}`);
        if (activeBtn) activeBtn.classList.add('bg-green-100');
        // Afficher résultats et compteur
        displaySPARQLResults(data.results);
        const resultsDiv = document.getElementById('sparql-results');
        if (resultsDiv) resultsDiv.scrollIntoView({behavior:'smooth', block:'start'});
    } catch (error) {
        document.getElementById('sparql-results').innerHTML = 
            `<p class="text-red-500">Erreur: ${error.message}</p>`;
    }
}

async function executeSPARQL() {
    const query = document.getElementById('sparql-editor').value;
    
    if (!query.trim()) {
        alert('Veuillez entrer une requête SPARQL');
        return;
    }
    
    try {
        const resultsDiv = document.getElementById('sparql-results');
        if (resultsDiv) resultsDiv.innerHTML = '<p class="text-gray-500">Exécution en cours...</p>';
        const response = await fetch(`${API_BASE}/sparql/execute`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({query: query})
        });
        
        const data = await response.json();
        if (!response.ok) {
            if (resultsDiv) resultsDiv.innerHTML = `<p class="text-red-500">Erreur API: ${data.error || 'Erreur inconnue'}</p>`;
            return;
        }
        displaySPARQLResults(data.results || []);
    } catch (error) {
        document.getElementById('sparql-results').innerHTML = 
            `<p class="text-red-500">Erreur: ${error.message}</p>`;
    }
}

// ==================== VISUALISATIONS ====================
async function loadVisualizations() {
    await loadCarbonChart();
    await loadEnergyChart();
    await loadEcoScoresChart();
    await loadCertificationsChart();
}

async function loadCarbonChart() {
    try {
        const response = await fetch(`${API_BASE}/visualizations/carbon-comparison`);
        const data = await response.json();
        
        const ctx = document.getElementById('chart-carbon').getContext('2d');
        new Chart(ctx, {
            type: data.type || 'bar',
            data: {
                labels: data.labels || [],
                datasets: data.datasets || []
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: data.title || 'Comparaison Carbone'
                    }
                }
            }
        });
    } catch (error) {
        console.error('Erreur graphique carbone:', error);
    }
}

async function loadEnergyChart() {
    try {
        const response = await fetch(`${API_BASE}/visualizations/energy-consumption`);
        const data = await response.json();
        
        const ctx = document.getElementById('chart-energy').getContext('2d');
        new Chart(ctx, {
            type: data.type || 'line',
            data: {
                labels: data.labels || [],
                datasets: data.datasets || []
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: data.title || 'Consommation Énergétique'
                    }
                }
            }
        });
    } catch (error) {
        console.error('Erreur graphique énergie:', error);
    }
}

async function loadEcoScoresChart() {
    try {
        const response = await fetch(`${API_BASE}/visualizations/eco-scores`);
        const data = await response.json();
        
        const ctx = document.getElementById('chart-eco-scores').getContext('2d');
        new Chart(ctx, {
            type: data.type || 'radar',
            data: {
                labels: data.labels || [],
                datasets: data.datasets || []
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: data.title || 'Scores Écologiques'
                    }
                }
            }
        });
    } catch (error) {
        console.error('Erreur graphique scores:', error);
    }
}

async function loadCertificationsChart() {
    const ctx = document.getElementById('chart-certifications').getContext('2d');
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Gold', 'Silver', 'Bronze'],
            datasets: [{
                data: [5, 3, 2],
                backgroundColor: [
                    'rgba(255, 206, 86, 0.8)',
                    'rgba(192, 192, 192, 0.8)',
                    'rgba(205, 127, 50, 0.8)'
                ]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Distribution Certifications'
                }
            }
        }
    });
}

// ==================== ONTOLOGIE ====================
async function loadOntologyData() {
    await loadClasses();
    await loadProperties();
    await loadIndividuals();
}

async function loadClasses() {
    try {
        const response = await fetch(`${API_BASE}/ontology/classes`);
        const data = await response.json();
        
        const div = document.getElementById('ontology-classes');
        let html = '<div class="space-y-2">';
        
        data.classes.forEach(cls => {
            html += `
                <div class="p-2 bg-blue-50 rounded border-l-4 border-blue-500">
                    <p class="font-semibold text-sm">${cls.class || 'Class'}</p>
                </div>
            `;
        });
        
        html += '</div>';
        div.innerHTML = html;
    } catch (error) {
        console.error('Erreur chargement classes:', error);
    }
}

async function loadProperties() {
    try {
        const response = await fetch(`${API_BASE}/ontology/properties`);
        const data = await response.json();
        
        const div = document.getElementById('ontology-properties');
        let html = '<div class="space-y-2">';
        
        data.properties.forEach(prop => {
            html += `
                <div class="p-2 bg-green-50 rounded border-l-4 border-green-500">
                    <p class="font-semibold text-sm">${prop.property || 'Property'}</p>
                    <p class="text-xs text-gray-600">${prop.type || ''}</p>
                </div>
            `;
        });
        
        html += '</div>';
        div.innerHTML = html;
    } catch (error) {
        console.error('Erreur chargement propriétés:', error);
    }
}

async function loadIndividuals() {
    try {
        const response = await fetch(`${API_BASE}/ontology/individuals`);
        const data = await response.json();
        
        const div = document.getElementById('ontology-individuals');
        let html = '<div class="space-y-2">';
        
        data.individuals.forEach(ind => {
            html += `
                <div class="p-2 bg-purple-50 rounded border-l-4 border-purple-500">
                    <p class="font-semibold text-sm">${ind.individual || 'Individual'}</p>
                    <p class="text-xs text-gray-600">${ind.type || ''}</p>
                </div>
            `;
        });
        
        html += '</div>';
        div.innerHTML = html;
    } catch (error) {
        console.error('Erreur chargement individus:', error);
    }
}

// Initialisation
document.addEventListener('DOMContentLoaded', () => {
    loadHomeData();
});

// ==================== CHATBOT ====================
function appendChatMessage(role, text) {
    const win = document.getElementById('chat-window');
    if (!win) return;
    const wrapper = document.createElement('div');
    wrapper.className = role === 'user' ? 'text-right' : 'text-left';
    const bubble = document.createElement('div');
    bubble.className = `inline-block px-3 py-2 rounded ${role === 'user' ? 'bg-green-600 text-white' : 'bg-gray-100 text-gray-800'}`;
    bubble.textContent = text;
    wrapper.appendChild(bubble);
    win.appendChild(wrapper);
    win.scrollTop = win.scrollHeight;
}

async function sendChatMessage() {
    const input = document.getElementById('chat-input');
    const llmToggle = document.getElementById('chat-llm-toggle');
    if (!input || !input.value.trim()) return;
    const message = input.value.trim();
    appendChatMessage('user', message);
    input.value = '';

    try {
        const res = await fetch(`${API_BASE}/chatbot/message`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ message, use_llm: llmToggle && llmToggle.checked })
        });
        const data = await res.json();
        if (data.error) throw new Error(data.error);
        if (data.response) appendChatMessage('assistant', data.response);
        renderChatSuggestions(data.suggestions || []);
    } catch (e) {
        appendChatMessage('assistant', `Erreur: ${e.message}`);
    }
}

async function clearChat() {
    try {
        await fetch(`${API_BASE}/chatbot/clear`, { method: 'POST' });
        const win = document.getElementById('chat-window');
        if (win) win.innerHTML = '';
        renderChatSuggestions([]);
    } catch (e) {
        console.error(e);
    }
}

async function initChat() {
    const win = document.getElementById('chat-window');
    if (win) win.innerHTML = '';
    try {
        const res = await fetch(`${API_BASE}/chatbot/history`);
        const data = await res.json();
        (data.history || []).forEach(m => appendChatMessage(m.role, m.message));
        renderChatSuggestions([
            'Quelles sont les meilleures destinations écologiques?',
            'Quels hébergements certifiés à Tunis?',
            "Comparer train et avion en CO2",
            'Activités à faible impact à Djerba'
        ]);
    } catch (e) {
        console.error(e);
    }
}

function renderChatSuggestions(suggestions) {
    const c = document.getElementById('chat-suggestions');
    if (!c) return;
    if (!suggestions.length) { c.innerHTML = '<p class="text-gray-500">Aucune suggestion</p>'; return; }
    c.innerHTML = '';
    suggestions.forEach(s => {
        const btn = document.createElement('button');
        btn.className = 'w-full text-left p-2 bg-gray-100 hover:bg-gray-200 rounded';
        btn.textContent = s;
        btn.onclick = () => { document.getElementById('chat-input').value = s; sendChatMessage(); };
        c.appendChild(btn);
    });
}
