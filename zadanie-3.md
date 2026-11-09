## I prompt:
Here's a basic Dockerfile for a Node.js application:

dockerfile

```dockerfile
# Use Node.js LTS image
FROM node:22-alpine

# Set working directory
WORKDIR /app

# Copy dependency files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy application source
COPY . .

# Expose application port
EXPOSE 3000

# Start application
CMD ["npm", "start"]
```

### Recommended `.dockerignore`

dockerignore

```dockerignore
node_modules
npm-debug.log
.git
.env
Dockerfile
.dockerignore
```

### Build and run

bash

```bash
# Build image
docker build -t my-node-app .

# Run container
docker run -d -p 3000:3000 --name node-app my-node-app
```

### For development

If you use `npm run dev`, replace the last line with:

dockerfile

```dockerfile
CMD ["npm", "run", "dev"]
```

Note: Make sure your `package.json` contains a `start` script, for example:

json

```json
{
  "scripts": {
    "start": "node index.js"
  }
}
```

I can also provide a production-ready Node.js Dockerfile with multi-stage builds and a non-root user.

## II prompt
Oto prosty `Dockerfile` dla aplikacji Node.js zgodny z podanymi wymaganiami:

dockerfile

```dockerfile
# Obraz bazowy Node.js 18
FROM node:18

# Katalog roboczy
WORKDIR /app

# Kopiowanie plików package.json i package-lock.json
COPY package*.json ./

# Instalacja zależności
RUN npm install

# Kopiowanie pozostałych plików aplikacji
COPY . .

# Wystawienie portu 3000
EXPOSE 3000

# Uruchomienie aplikacji
CMD ["npm", "start"]
```

Aby zbudować obraz i uruchomić kontener:

bash

```bash
docker build -t node-app .
docker run -p 3000:3000 node-app
```


## Podsumowanie 

Obie odpowiedzi zawierają poprawny, podstawowy Dockerfile dla aplikacji Node.js, ale różnią się szczegółowością i konfiguracją.
Odpowiedź na pierwszy prompt była też w języku angielskim, a druga w polskim (tak jak wskazuje mój prompt)