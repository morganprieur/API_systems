
# API Acquisition    

API permettant de consulter les données enregistrées pour les systèmes installés et configurés. Les techniciens peuvent enregistrer les systèmes avant de les mettre en service. 
Gestion différenciée des utilisateurs. 

Disclaimer : Adaptation d'un projet réel. Toutes les informations sensibls ont été retirées ou anonymisées. Il peut en résulter des erreurs. Ne pas utiliser tel quel, et envoyez un feedback en cas de problème. 

La BDD et l'API sont dans des containers Docker gérés par un fichier compose.yaml. 
    BDD -> container "db" 
    API -> container "api" 

**Technologies** 
Django 
PostgreSQL 
Django Signals
JWT 
Django permissions 
Docker 


## Installation 

### 1. Créer un superutilisateur après le lancement des containers

*  Depuis le dossier contant docker-compose : lancer le container 'web' avec `exec` et lancer une invite de commande pour accéder à une console dans le container :     
`docker exec -it <nom_du_container> bash` 

*  Lancer la commande de création du superutilisateur
`python manage.py createsuperuser`

*  Répondre aux questions : 
Username
Email
Password
Password again

On peut bypasser la solidité du pass du superutilisateur, mais pas ceux des utilisateurs lambda (à configurer si besoin).

*  Pour se connecter en tant que superutilisateur, ouvrir le navigateur à l'adresse : 
`localhost:<port>/admin`    


### 2. Créer 2 groupes 

Dans l'interface admin `http://localhost:8000/admin/` ajouter 2 groupes : 
1. owner_group pour les clients, 
2. sys_group pour les Systèmes 
<!-- 2. bei_group pour les Systèmes  -->


## Pour tester les routes ou pour mettre l'api en ligne, ajouter des données  

Le fichier de fixtures :     
`dashboard/fixtures/fixture_data.json`    

**Pour le lancer depuis la console :**     
`python manage.py loaddata dashboard/fixtures/fixture_data.json` 


## Modèles 

### Colonnes/Champs "date" dans les modèles 

*  Eviter d'utiliser le mot "date" ou "Date", c'est un terme réservé (la plupart du temps ça n'a pas l'air de poser de problème) 


### Pour date + heure auto 

**A la création :** 
*  Uniquement dans le moldèle : 
`    created_at = models.DateTimeField(auto_now_add = True)`

**A l'update :**
`    updated_at = models.DateTimeField(auto_now = True)`


### Faire les migrations quand on modifie un/des modèle/s

*  Dans le container, via la console (l'invite de commande commence par '#') : 
`python manage.py makemigrations`
`python manage.py migrate`
Chaque commande indique le résultat. 


## Tests 

*  Emplacement du fichier de test :    
`api/bei/tests.py`    

*  Lancer les tests :     
`python manage.py test bei.tests -v 3` 
Régler la quantité de détails avec `-v` : `3` = le maximum    


## Autres 

### Créer un utilisateur via la console 

*  Une fois dans le container, ouvrir une console python :    
`python manage.py shell`    

*  Taper le code pour créer l'utilisateur : 
`from django.contrib.auth.models import User`    
`from django.contrib.auth.hashers import make_password`    
`user = User.objects.create_user('<username>','<mail>')`    
`user.password = make_password('<password>')`    
`user.save()`    

*  Vérifier dans l'itf web qu'il est bien créé.    

