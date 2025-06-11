# Utilise l'image officielle Python 3.9 allégée basée sur Debian Buster comme base
FROM python:3.9-slim-buster

# Définit le répertoire de travail à l'intérieur du conteneur
WORKDIR /annuaire_student

# Met à jour les paquets système et installe les outils nécessaires comme gcc et wget
RUN apt-get update && apt-get install -y gcc wget

# Télécharge et extrait le connecteur MariaDB C version 3.3.3 pour Debian Bullseye
RUN wget https://dlm.mariadb.com/2678574/Connectors/c/connector-c-3.3.3/mariadb-connector-c-3.3.3-debian-bullseye-amd64.tar.gz -O - | tar -xz

# Met à jour les paquets système et installe les bibliothèques client et de développement MariaDB
RUN apt-get update && apt-get install -y libmariadb3 libmariadb-dev

# Met à jour pip, le gestionnaire de paquets Python
RUN pip install --upgrade pip

# Installe la version spécifique 1.0.11 du connecteur Python pour MariaDB
RUN pip install mariadb==1.0.11 

# Installe les bibliothèques de développement nécessaires pour compiler certains paquets Python
RUN apt-get install pkg-config python3-dev default-libmysqlclient-dev build-essential -y

# Copie le fichier requirements.txt dans l'image Docker
COPY requirements.txt requirements.txt

# Installe les dépendances Python listées dans requirements.txt
RUN pip install -r requirements.txt

# Copie tous les fichiers du projet local dans le conteneur
COPY . .

# Déclare que le conteneur écoute sur le port 5000
EXPOSE 5000

# Définit la variable d’environnement FLASK_APP pour indiquer à Flask quel fichier exécuter
ENV FLASK_APP=run.py

# Définit la commande par défaut pour démarrer l'application Flask sans le mode debugger
CMD ["flask", "run", "--host", "0.0.0.0", "--no-debugger"]
