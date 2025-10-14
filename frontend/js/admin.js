/**
 * Admin Dashboard JavaScript
 */

const API_URL = 'http://localhost:5000';
let currentUser = null;
let allUsers = [];

// Check authentication on load
window.onload = function() {
    checkAuthentication();
    loadDashboardData();
};

function checkAuthentication() {
    const token = localStorage.getItem('access_token');
    const userStr = localStorage.getItem('user');
    
    if (!token || !userStr) {
        window.location.href = 'login.html';
        return;
    }
    
    try {
        currentUser = JSON.parse(userStr);
        
        // Check if user is admin
        if (currentUser.role !== 'admin') {
            alert('Accès refusé. Cette page est réservée aux administrateurs.');
            window.location.href = 'index.html';
            return;
        }
        
        document.getElementById('admin-name').textContent = `👤 ${currentUser.username}`;
    } catch (e) {
        console.error('Error parsing user data:', e);
        window.location.href = 'login.html';
    }
}

function getAuthHeaders() {
    const token = localStorage.getItem('access_token');
    return {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
    };
}

function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
    window.location.href = 'login.html';
}

// Tab Management
function showTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.add('hidden');
    });
    
    // Remove active class from all buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('border-b-2', 'border-indigo-600', 'text-indigo-600');
        btn.classList.add('text-gray-600');
    });
    
    // Show selected tab
    document.getElementById(`tab-${tabName}`).classList.remove('hidden');
    
    // Add active class to clicked button
    event.target.classList.remove('text-gray-600');
    event.target.classList.add('border-b-2', 'border-indigo-600', 'text-indigo-600');
    
    // Load data for the tab
    switch(tabName) {
        case 'dashboard':
            loadDashboardData();
            break;
        case 'users':
            loadUsers();
            break;
        case 'activities':
            loadActivities();
            break;
        case 'recommendations':
            loadRecommendations();
            break;
    }
}

// ==================== DASHBOARD ====================

async function loadDashboardData() {
    try {
        const response = await fetch(`${API_URL}/api/admin/dashboard/stats`, {
            headers: getAuthHeaders()
        });
        
        if (!response.ok) throw new Error('Failed to load dashboard data');
        
        const data = await response.json();
        
        if (data.success) {
            // Update statistics
            document.getElementById('stat-total-users').textContent = data.users.total;
            document.getElementById('stat-new-users').textContent = `+${data.users.new_last_30d} ce mois`;
            document.getElementById('stat-sparql-queries').textContent = data.activities.sparql_queries;
            document.getElementById('stat-recommendations').textContent = data.recommendations.total;
            document.getElementById('stat-avg-eco-score').textContent = data.recommendations.avg_eco_score;
            document.getElementById('stat-total-activities').textContent = data.activities.total;
            document.getElementById('stat-logins').textContent = `${data.activities.logins} connexions`;
            
            // Update user role chart
            createUserRoleChart(data.users);
            
            // Update daily activity chart
            createDailyActivityChart(data.daily_activity);
            
            // Update top destinations
            displayTopDestinations(data.top_destinations);
        }
    } catch (error) {
        console.error('Error loading dashboard:', error);
        showNotification('Erreur lors du chargement du dashboard', 'error');
    }
}

function createUserRoleChart(userData) {
    const ctx = document.getElementById('chart-user-roles');
    if (!ctx) return;
    
    // Destroy existing chart if any
    if (window.userRoleChart) {
        window.userRoleChart.destroy();
    }
    
    window.userRoleChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Voyageurs', 'Admins'],
            datasets: [{
                data: [userData.voyageurs, userData.admins],
                backgroundColor: ['#10b981', '#6366f1'],
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

function createDailyActivityChart(activityData) {
    const ctx = document.getElementById('chart-daily-activity');
    if (!ctx) return;
    
    // Destroy existing chart if any
    if (window.dailyActivityChart) {
        window.dailyActivityChart.destroy();
    }
    
    const dates = activityData.map(a => a.date);
    const counts = activityData.map(a => a.count);
    
    window.dailyActivityChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: dates,
            datasets: [{
                label: 'Activités',
                data: counts,
                borderColor: '#6366f1',
                backgroundColor: 'rgba(99, 102, 241, 0.1)',
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        precision: 0
                    }
                }
            }
        }
    });
}

function displayTopDestinations(destinations) {
    const container = document.getElementById('top-destinations');
    if (!container) return;
    
    if (destinations.length === 0) {
        container.innerHTML = '<p class="text-gray-500 col-span-3">Aucune destination consultée</p>';
        return;
    }
    
    container.innerHTML = destinations.map((dest, index) => `
        <div class="bg-gradient-to-br from-blue-50 to-indigo-50 p-4 rounded-lg border border-blue-200">
            <div class="flex justify-between items-start mb-2">
                <span class="text-2xl font-bold text-indigo-600">#${index + 1}</span>
                <span class="bg-indigo-600 text-white px-2 py-1 rounded text-xs font-semibold">${dest.views} vues</span>
            </div>
            <p class="font-semibold text-gray-800">${dest.name}</p>
        </div>
    `).join('');
}

// ==================== USERS MANAGEMENT ====================

async function loadUsers() {
    try {
        const search = document.getElementById('filter-user-search')?.value || '';
        const role = document.getElementById('filter-user-role')?.value || '';
        const activeOnly = document.getElementById('filter-user-status')?.value === 'active';
        
        const params = new URLSearchParams();
        if (search) params.append('search', search);
        if (role) params.append('role', role);
        if (activeOnly) params.append('active_only', 'true');
        
        const response = await fetch(`${API_URL}/api/admin/users?${params}`, {
            headers: getAuthHeaders()
        });
        
        if (!response.ok) throw new Error('Failed to load users');
        
        const data = await response.json();
        
        if (data.success) {
            allUsers = data.users;
            displayUsers(data.users);
        }
    } catch (error) {
        console.error('Error loading users:', error);
        showNotification('Erreur lors du chargement des utilisateurs', 'error');
    }
}

function displayUsers(users) {
    const tbody = document.getElementById('users-table-body');
    if (!tbody) return;
    
    if (users.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="px-6 py-4 text-center text-gray-500">Aucun utilisateur trouvé</td></tr>';
        return;
    }
    
    tbody.innerHTML = users.map(user => {
        const roleColor = user.role === 'admin' ? 'bg-purple-100 text-purple-800' : 'bg-blue-100 text-blue-800';
        const statusColor = user.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800';
        const date = user.created_at ? new Date(user.created_at).toLocaleDateString('fr-FR') : 'N/A';
        
        return `
            <tr class="hover:bg-gray-50">
                <td class="px-6 py-4 text-sm">${user.id}</td>
                <td class="px-6 py-4">
                    <div class="font-semibold text-gray-900">${user.username}</div>
                </td>
                <td class="px-6 py-4 text-sm text-gray-600">${user.email}</td>
                <td class="px-6 py-4">
                    <span class="px-2 py-1 rounded text-xs font-semibold ${roleColor}">
                        ${user.role}
                    </span>
                </td>
                <td class="px-6 py-4">
                    <span class="px-2 py-1 rounded text-xs font-semibold ${statusColor}">
                        ${user.is_active ? 'Actif' : 'Inactif'}
                    </span>
                </td>
                <td class="px-6 py-4 text-sm text-gray-600">${date}</td>
                <td class="px-6 py-4">
                    <div class="flex space-x-2">
                        <button onclick="editUser(${user.id})" class="text-blue-600 hover:text-blue-800 text-sm font-semibold">
                            ✏️ Modifier
                        </button>
                        <button onclick="viewUserDetails(${user.id})" class="text-green-600 hover:text-green-800 text-sm font-semibold">
                            👁️ Détails
                        </button>
                        ${user.id !== currentUser.id ? `
                            <button onclick="deleteUser(${user.id}, '${user.username}')" class="text-red-600 hover:text-red-800 text-sm font-semibold">
                                🗑️ Supprimer
                            </button>
                        ` : ''}
                    </div>
                </td>
            </tr>
        `;
    }).join('');
}

function filterUsers() {
    loadUsers();
}

function showCreateUserModal() {
    document.getElementById('modal-title').textContent = 'Créer un nouvel utilisateur';
    document.getElementById('user-form').reset();
    document.getElementById('user-id').value = '';
    document.getElementById('user-active').checked = true;
    document.getElementById('user-modal').classList.remove('hidden');
}

function editUser(userId) {
    const user = allUsers.find(u => u.id === userId);
    if (!user) return;
    
    document.getElementById('modal-title').textContent = 'Modifier l\'utilisateur';
    document.getElementById('user-id').value = user.id;
    document.getElementById('user-username').value = user.username;
    document.getElementById('user-email').value = user.email;
    document.getElementById('user-role').value = user.role;
    document.getElementById('user-active').checked = user.is_active;
    document.getElementById('user-password').value = '';
    document.getElementById('user-modal').classList.remove('hidden');
}

function closeUserModal() {
    document.getElementById('user-modal').classList.add('hidden');
}

async function handleUserSubmit(event) {
    event.preventDefault();
    
    const userId = document.getElementById('user-id').value;
    const userData = {
        username: document.getElementById('user-username').value,
        email: document.getElementById('user-email').value,
        role: document.getElementById('user-role').value,
        is_active: document.getElementById('user-active').checked
    };
    
    const password = document.getElementById('user-password').value;
    if (password) {
        userData.password = password;
    }
    
    try {
        let response;
        if (userId) {
            // Update existing user
            response = await fetch(`${API_URL}/api/admin/users/${userId}`, {
                method: 'PUT',
                headers: getAuthHeaders(),
                body: JSON.stringify(userData)
            });
        } else {
            // Create new user
            if (!password) {
                showNotification('Le mot de passe est requis pour créer un utilisateur', 'error');
                return;
            }
            response = await fetch(`${API_URL}/api/admin/users`, {
                method: 'POST',
                headers: getAuthHeaders(),
                body: JSON.stringify(userData)
            });
        }
        
        const data = await response.json();
        
        if (data.success) {
            showNotification(data.message, 'success');
            closeUserModal();
            loadUsers();
        } else {
            showNotification(data.error || 'Erreur lors de l\'enregistrement', 'error');
        }
    } catch (error) {
        console.error('Error saving user:', error);
        showNotification('Erreur lors de l\'enregistrement', 'error');
    }
}

async function deleteUser(userId, username) {
    if (!confirm(`Êtes-vous sûr de vouloir supprimer l'utilisateur "${username}" ?`)) {
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/api/admin/users/${userId}`, {
            method: 'DELETE',
            headers: getAuthHeaders()
        });
        
        const data = await response.json();
        
        if (data.success) {
            showNotification('Utilisateur supprimé avec succès', 'success');
            loadUsers();
        } else {
            showNotification(data.error || 'Erreur lors de la suppression', 'error');
        }
    } catch (error) {
        console.error('Error deleting user:', error);
        showNotification('Erreur lors de la suppression', 'error');
    }
}

async function viewUserDetails(userId) {
    try {
        const response = await fetch(`${API_URL}/api/admin/users/${userId}`, {
            headers: getAuthHeaders()
        });
        
        const data = await response.json();
        
        if (data.success) {
            const user = data.user;
            const stats = data.statistics;
            
            alert(`
📊 Détails de l'utilisateur: ${user.username}

📧 Email: ${user.email}
👤 Rôle: ${user.role}
✅ Statut: ${user.is_active ? 'Actif' : 'Inactif'}
📅 Inscription: ${new Date(user.created_at).toLocaleDateString('fr-FR')}
🕐 Dernière connexion: ${user.last_login ? new Date(user.last_login).toLocaleDateString('fr-FR') : 'Jamais'}

📈 Statistiques:
- Total activités: ${stats.total_activities}
- Connexions: ${stats.total_logins}
- Requêtes SPARQL: ${stats.total_queries}
- Recommandations: ${stats.total_recommendations}
            `);
        }
    } catch (error) {
        console.error('Error loading user details:', error);
        showNotification('Erreur lors du chargement des détails', 'error');
    }
}

// ==================== ACTIVITIES ====================

async function loadActivities() {
    try {
        const type = document.getElementById('filter-activity-type')?.value || '';
        
        const params = new URLSearchParams();
        if (type) params.append('type', type);
        params.append('per_page', '50');
        
        // For now, we'll get all activities (we can add user-specific later)
        const response = await fetch(`${API_URL}/api/admin/dashboard/activity-timeline?days=30`, {
            headers: getAuthHeaders()
        });
        
        if (!response.ok) throw new Error('Failed to load activities');
        
        const data = await response.json();
        
        if (data.success) {
            displayActivities(data.timeline);
        }
    } catch (error) {
        console.error('Error loading activities:', error);
        showNotification('Erreur lors du chargement des activités', 'error');
    }
}

function displayActivities(activities) {
    const container = document.getElementById('activities-list');
    if (!container) return;
    
    if (activities.length === 0) {
        container.innerHTML = '<p class="text-gray-500 text-center py-8">Aucune activité trouvée</p>';
        return;
    }
    
    // Group by date
    const grouped = {};
    activities.forEach(activity => {
        if (!grouped[activity.date]) {
            grouped[activity.date] = [];
        }
        grouped[activity.date].push(activity);
    });
    
    container.innerHTML = Object.entries(grouped).map(([date, acts]) => `
        <div class="bg-white border rounded-lg p-4">
            <h4 class="font-bold text-gray-800 mb-3">📅 ${new Date(date).toLocaleDateString('fr-FR', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}</h4>
            <div class="space-y-2">
                ${acts.map(act => {
                    const icon = getActivityIcon(act.activity_type);
                    return `
                        <div class="flex items-center justify-between bg-gray-50 p-3 rounded">
                            <div class="flex items-center gap-3">
                                <span class="text-2xl">${icon}</span>
                                <div>
                                    <p class="font-semibold text-gray-800">${getActivityLabel(act.activity_type)}</p>
                                    <p class="text-sm text-gray-600">${act.count} fois</p>
                                </div>
                            </div>
                        </div>
                    `;
                }).join('')}
            </div>
        </div>
    `).join('');
}

function getActivityIcon(type) {
    const icons = {
        'login': '🔐',
        'sparql_query': '💻',
        'search': '🔍',
        'recommendation': '🎯',
        'registration': '📝'
    };
    return icons[type] || '📊';
}

function getActivityLabel(type) {
    const labels = {
        'login': 'Connexion',
        'sparql_query': 'Requête SPARQL',
        'search': 'Recherche',
        'recommendation': 'Recommandation',
        'registration': 'Inscription'
    };
    return labels[type] || type;
}

// ==================== RECOMMENDATIONS ====================

async function loadRecommendations() {
    try {
        const response = await fetch(`${API_URL}/api/admin/recommendations?per_page=20`, {
            headers: getAuthHeaders()
        });
        
        if (!response.ok) throw new Error('Failed to load recommendations');
        
        const data = await response.json();
        
        if (data.success) {
            displayRecommendations(data.recommendations);
            updateRecommendationStats(data.recommendations);
        }
    } catch (error) {
        console.error('Error loading recommendations:', error);
        showNotification('Erreur lors du chargement des recommandations', 'error');
    }
}

function displayRecommendations(recommendations) {
    const container = document.getElementById('recommendations-list');
    if (!container) return;
    
    if (recommendations.length === 0) {
        container.innerHTML = '<p class="text-gray-500 text-center py-8">Aucune recommandation générée</p>';
        return;
    }
    
    container.innerHTML = recommendations.map(rec => {
        const date = rec.created_at ? new Date(rec.created_at).toLocaleDateString('fr-FR') : 'N/A';
        const ecoScore = rec.eco_score ? rec.eco_score.toFixed(1) : 'N/A';
        const scoreColor = rec.eco_score >= 80 ? 'text-green-600' : rec.eco_score >= 60 ? 'text-yellow-600' : 'text-red-600';
        
        return `
            <div class="bg-white border rounded-lg p-4 hover:shadow-md transition">
                <div class="flex justify-between items-start mb-3">
                    <div>
                        <span class="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm font-semibold">
                            ${rec.recommendation_type}
                        </span>
                        <p class="text-sm text-gray-600 mt-2">User ID: ${rec.user_id || 'Anonymous'}</p>
                    </div>
                    <div class="text-right">
                        <p class="text-sm text-gray-600">Score écologique</p>
                        <p class="text-2xl font-bold ${scoreColor}">${ecoScore}</p>
                    </div>
                </div>
                <p class="text-xs text-gray-500">📅 ${date}</p>
            </div>
        `;
    }).join('');
}

function updateRecommendationStats(recommendations) {
    const stats = {
        destination: 0,
        accommodation: 0,
        activity: 0,
        transport: 0
    };
    
    recommendations.forEach(rec => {
        if (stats.hasOwnProperty(rec.recommendation_type)) {
            stats[rec.recommendation_type]++;
        }
    });
    
    document.getElementById('rec-destinations').textContent = stats.destination;
    document.getElementById('rec-accommodations').textContent = stats.accommodation;
    document.getElementById('rec-activities').textContent = stats.activity;
    document.getElementById('rec-transports').textContent = stats.transport;
}

// ==================== NOTIFICATIONS ====================

function showNotification(message, type = 'info') {
    const colors = {
        success: 'bg-green-500',
        error: 'bg-red-500',
        info: 'bg-blue-500'
    };
    
    const notification = document.createElement('div');
    notification.className = `fixed top-4 right-4 ${colors[type]} text-white px-6 py-3 rounded-lg shadow-lg z-50 animate-fade-in`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 3000);
}
