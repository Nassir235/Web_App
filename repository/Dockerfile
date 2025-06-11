# Utilisation de l'image officielle MariaDB (dernière version disponible sur Docker Hub)
FROM mariadb:latest

# Définition du mot de passe pour l'utilisateur root de MariaDB 
ENV MYSQL_ROOT_PASSWORD=266139

# Exposition du port 3306 (port par défaut utilisé par MariaDB) 
EXPOSE 3306

# Copie du fichier SQL d'initialisation dans le dossier surveillé par l'entrée Docker de MariaDB
# Tous les fichiers placés ici seront exécutés automatiquement lors du premier démarrage du conteneur
COPY init.sql /docker-entrypoint-initdb.d/

# Déclaration d’un volume pour stocker les données de la base de manière persistante
# Cela permet de conserver les données même si le conteneur est supprimé
VOLUME /var/lib/mysql
