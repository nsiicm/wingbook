FROM node:lts-alpine

# installe un simple serveur http pour servir un contenu statique
RUN npm install -g serve

# définit le dossier 'app' comme dossier de travail
WORKDIR /app

# Accept build arg for VITE_API_BASE_URL
ARG VITE_API_BASE_URL
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL
RUN echo "VITE_API_BASE_URL=$VITE_API_BASE_URL" > .env

# copie 'package.json' et 'package-lock.json' (si disponible)
COPY package*.json ./

# installe les dépendances du projet
RUN npm install

# copie les fichiers et dossiers du projet dans le dossier de travail (par exemple : le dossier 'app')
COPY . .

# construit l'app pour la production en la minifiant
RUN npm run build

EXPOSE 3000
CMD [ "serve", "-s", "dist" ]
