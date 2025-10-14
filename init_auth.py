#!/usr/bin/env python3
"""
Script d'initialisation de la base de données et du système d'authentification
"""
import os
import sys
from getpass import getpass

# Ajouter le répertoire backend au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from flask import Flask
from models import db, User, bcrypt
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Créer une application Flask temporaire pour l'initialisation
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')

# Initialiser les extensions
db.init_app(app)
bcrypt.init_app(app)

def init_database():
    """Initialise la base de données"""
    with app.app_context():
        print("🔧 Création des tables de la base de données...")
        db.create_all()
        print("✅ Tables créées avec succès!")
        
        # Vérifier si l'admin existe déjà
        admin = User.query.filter_by(username='admin').first()
        if admin:
            print("⚠️  Un compte administrateur existe déjà.")
            choice = input("Voulez-vous créer un nouvel admin ? (o/n): ").lower()
            if choice != 'o':
                return
        
        # Créer un compte administrateur
        print("\n👑 Création du compte administrateur")
        print("-" * 50)
        
        username = input("Nom d'utilisateur (défaut: admin): ").strip() or "admin"
        email = input("Email (défaut: admin@ecotravel.com): ").strip() or "admin@ecotravel.com"
        
        # Demander le mot de passe avec confirmation
        while True:
            password = getpass("Mot de passe: ")
            if len(password) < 6:
                print("❌ Le mot de passe doit contenir au moins 6 caractères.")
                continue
            
            password_confirm = getpass("Confirmer le mot de passe: ")
            if password != password_confirm:
                print("❌ Les mots de passe ne correspondent pas.")
                continue
            
            break
        
        # Créer l'administrateur
        admin = User(
            username=username,
            email=email,
            role='admin',
            is_active=True
        )
        admin.set_password(password)
        
        db.session.add(admin)
        db.session.commit()
        
        print("\n✅ Compte administrateur créé avec succès!")
        print(f"   👤 Username: {username}")
        print(f"   📧 Email: {email}")
        print(f"   👑 Rôle: admin")
        
        # Créer quelques utilisateurs de test (optionnel)
        create_test = input("\nVoulez-vous créer des utilisateurs de test ? (o/n): ").lower()
        if create_test == 'o':
            create_test_users()

def create_test_users():
    """Crée des utilisateurs de test"""
    test_users = [
        {
            'username': 'voyageur1',
            'email': 'voyageur1@test.com',
            'password': 'password123',
            'role': 'voyageur'
        },
        {
            'username': 'voyageur2',
            'email': 'voyageur2@test.com',
            'password': 'password123',
            'role': 'voyageur'
        }
    ]
    
    with app.app_context():
        created = 0
        for user_data in test_users:
            # Vérifier si l'utilisateur existe déjà
            existing = User.query.filter_by(username=user_data['username']).first()
            if existing:
                print(f"⚠️  L'utilisateur {user_data['username']} existe déjà, ignoré.")
                continue
            
            user = User(
                username=user_data['username'],
                email=user_data['email'],
                role=user_data['role'],
                is_active=True
            )
            user.set_password(user_data['password'])
            db.session.add(user)
            created += 1
        
        db.session.commit()
        print(f"✅ {created} utilisateur(s) de test créé(s)")
        print("\n📝 Identifiants de test:")
        for user_data in test_users:
            print(f"   - {user_data['username']} / {user_data['password']}")

def reset_database():
    """Réinitialise complètement la base de données"""
    print("⚠️  ATTENTION: Cette opération va supprimer TOUTES les données!")
    confirm = input("Êtes-vous sûr de vouloir continuer ? (tapez 'CONFIRMER'): ")
    
    if confirm != 'CONFIRMER':
        print("❌ Opération annulée.")
        return
    
    with app.app_context():
        print("🗑️  Suppression de toutes les tables...")
        db.drop_all()
        print("✅ Tables supprimées")
        
        print("🔧 Recréation des tables...")
        db.create_all()
        print("✅ Tables recréées")
        
        # Créer un admin par défaut
        admin = User(
            username='admin',
            email='admin@ecotravel.com',
            role='admin',
            is_active=True
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        
        print("✅ Base de données réinitialisée!")
        print("👤 Admin par défaut créé: admin / admin123")

def show_stats():
    """Affiche les statistiques de la base de données"""
    with app.app_context():
        total_users = User.query.count()
        admins = User.query.filter_by(role='admin').count()
        voyageurs = User.query.filter_by(role='voyageur').count()
        active = User.query.filter_by(is_active=True).count()
        
        print("\n📊 Statistiques de la base de données")
        print("-" * 50)
        print(f"👥 Total utilisateurs: {total_users}")
        print(f"👑 Administrateurs: {admins}")
        print(f"🧳 Voyageurs: {voyageurs}")
        print(f"✅ Actifs: {active}")
        print(f"❌ Inactifs: {total_users - active}")
        
        print("\n📋 Liste des utilisateurs:")
        users = User.query.all()
        for user in users:
            status = "✅" if user.is_active else "❌"
            role_icon = "👑" if user.role == 'admin' else "🧳"
            print(f"   {status} {role_icon} {user.username} ({user.email}) - {user.role}")

def main():
    """Fonction principale"""
    print("=" * 60)
    print("🌍 EcoTravel - Initialisation du système d'authentification")
    print("=" * 60)
    print()
    print("Options disponibles:")
    print("1. Initialiser la base de données (première installation)")
    print("2. Créer un nouvel administrateur")
    print("3. Réinitialiser la base de données (DANGER!)")
    print("4. Afficher les statistiques")
    print("5. Quitter")
    print()
    
    choice = input("Votre choix (1-5): ").strip()
    
    if choice == '1':
        init_database()
    elif choice == '2':
        with app.app_context():
            db.create_all()  # S'assurer que les tables existent
        init_database()
    elif choice == '3':
        reset_database()
    elif choice == '4':
        show_stats()
    elif choice == '5':
        print("👋 Au revoir!")
        return
    else:
        print("❌ Choix invalide")
        return
    
    print("\n✅ Opération terminée!")
    print("🚀 Vous pouvez maintenant démarrer l'application avec: python backend/app.py")

if __name__ == '__main__':
    main()
