Oto 5 kluczowych praktyk bezpieczeństwa dla aplikacji Dockerowych w środowisku produkcyjnym, które pomagają ograniczyć ryzyko włamania, eskalacji uprawnień, wycieku danych i przejęcia kontenerów.

## 1. Minimalizacja obrazu Docker i regularne skanowanie podatności

Podstawa bezpieczeństwa- Używaj lekkich obrazów bazowych, np. Alpine lub Distroless.
- Instaluj wyłącznie niezbędne pakiety i zależności.
- Regularnie aktualizuj obrazy bazowe oraz biblioteki.
- Skanuj obrazy pod kątem CVE (Common Vulnerabilities and Exposures).
- Korzystaj z narzędzi takich jak:
  - Trivy
  - Docker Scout
  - Grype

Przykład:

bash

```bash
trivy image --severity HIGH,CRITICAL myapp:latest
```

## 2. Uruchamianie kontenerów jako non-root

Nigdy nie uruchamiaj aplikacji jako root, jeśli nie jest to absolutnie konieczne.

- Twórz dedykowanego użytkownika w Dockerfile.
- Ustaw `USER` na użytkownika nieuprzywilejowanego.
- Ogranicz możliwości eskalacji uprawnień.
- Używaj `no-new-privileges`.

Przykład Dockerfile:

dockerfile

```dockerfile
FROM node:22-alpine

WORKDIR /app

COPY --chown=node:node . .

USER node

CMD ["node", "server.js"]
```

Dodatkowo w Docker Compose:

yaml

```yaml
services:
  app:
    image: myapp:latest
    security_opt:
      - no-new-privileges:true
```

## 3. Ograniczenie uprawnień i izolacja kontenerów

Stosuj zasadę Least Privilege (najmniejszych uprawnień).

Najważniejsze praktyki:

- Nie używaj `privileged: true`.
- Ogranicz capabilities za pomocą `cap_drop`.
- Nie montuj bez potrzeby katalogów hosta.
- Nie udostępniaj socketu `/var/run/docker.sock`.
- Korzystaj z read-only filesystem.
- Ustaw limity CPU i RAM.

Przykład:

yaml

```yaml
services:
  app:
    image: myapp:latest
    read_only: true

    cap_drop:
      - ALL

    security_opt:
      - no-new-privileges:true

    tmpfs:
      - /tmp

    mem_limit: 512m
    cpus: 1.0
```

Dzięki temu ewentualne przejęcie aplikacji nie daje atakującemu automatycznie pełnej kontroli nad hostem.

## 4. Bezpieczne zarządzanie sekretami i konfiguracją

Wysoki priorytetNigdy nie zapisuj haseł, tokenów API ani kluczy prywatnych bezpośrednio w:

- Dockerfile.
- Obrazach Docker.
- Repozytorium Git.
- Plikach `docker-compose.yml`.

Zamiast tego wykorzystuj:

- Docker Secrets.
- HashiCorp Vault.
- AWS Secrets Manager.
- Azure Key Vault.
- Kubernetes Secrets (z odpowiednim szyfrowaniem i kontrolą dostępu).

Przykład Docker Compose:

yaml

```yaml
services:
  app:
    image: myapp:latest
    secrets:
      - db_password

secrets:
  db_password:
    file: ./secrets/db_password.txt
```

Dodatkowo:

- Regularnie rotuj sekrety.
- Ogranicz dostęp do nich.
- Nie zapisuj sekretów w logach.
- Nie przekazuj ich jako argumentów CLI.

## 5. Monitoring, logowanie i bezpieczeństwo sieci

Bezpieczeństwo produkcji wymaga ciągłego monitorowania.

Sieć:

- Izoluj kontenery za pomocą dedykowanych sieci Docker.
- Udostępniaj tylko niezbędne porty.
- Nie wystawiaj bezpośrednio baz danych do Internetu.
- Stosuj TLS dla komunikacji zewnętrznej.

Monitoring i logi:

- Monitoruj nietypowe procesy i połączenia sieciowe.
- Centralizuj logi.
- Ustaw alerty na podejrzane zdarzenia.
- Monitoruj zmiany w konfiguracji kontenerów.

Przydatne narzędzia:

- Falco – wykrywanie podejrzanych zachowań runtime.
- Prometheus – monitoring.
- Grafana – wizualizacja metryk.
- Wazuh – monitoring bezpieczeństwa.

## Podsumowanie – 5 praktyk

| # | Praktyka | Główny cel |
| --- | --- | --- |
| 1 | Minimalne obrazy i skanowanie CVE | Redukcja podatności |
| 2 | Non-root | Ograniczenie eskalacji uprawnień |
| 3 | Izolacja i Least Privilege | Ograniczenie skutków włamania |
| 4 | Bezpieczne zarządzanie sekretami | Ochrona danych uwierzytelniających |
| 5 | Monitoring i segmentacja sieci | Wykrywanie i ograniczanie zagrożeń |

## Dodatkowa rekomendacja

W środowisku produkcyjnym warto wdrożyć również kontrolę bezpieczeństwa w CI/CD:

1. Skanowanie obrazów przed publikacją.
2. Weryfikację podpisów obrazów (np. Cosign).
3. Skanowanie zależności aplikacji.
4. Blokowanie wdrożeń z krytycznymi podatnościami.
5. Przypinanie obrazów do konkretnych wersji lub digestów zamiast używania `latest`.

Moja rekomendacja: zacznij od uruchamiania kontenerów jako non-root, ograniczenia capabilities, skanowania obrazów Trivy oraz bezpiecznego zarządzania sekretami. To cztery działania, które dają bardzo dobry punkt wyjścia do zabezpieczenia produkcyjnego środowiska Docker.


### Prompt uzupełniający

Pierwszą praktykę, czyli minimalizację obrazów Docker i regularne skanowanie podatności, możesz wdrożyć na dwóch poziomach:

1. W `Dockerfile` – budowanie małego obrazu zawierającego tylko niezbędne zależności.
2. W `docker-compose.yml` – korzystanie z konkretnej wersji obrazu i kontrolowanie jego budowania.

Pokażę Ci przykład dla aplikacji Node.js. Podobne podejście można zastosować do Pythona, Javy czy PHP.

## 1. Dockerfile – wykorzystanie multi-stage build

Zastosuj wieloetapowe budowanie obrazu (multi-stage build). Dzięki temu narzędzia potrzebne do kompilacji nie trafią do obrazu produkcyjnego.

RekomendowaneDockerfile:

dockerfile

```dockerfile
# Etap 1: instalacja zależności
FROM node:22-alpine AS builder

WORKDIR /app

COPY package*.json ./

RUN npm ci

COPY . .

# Budowanie aplikacji
RUN npm run build


# Etap 2: obraz produkcyjny
FROM node:22-alpine AS production

ENV NODE_ENV=production

WORKDIR /app

# Kopiujemy tylko niezbędne pliki
COPY package*.json ./

RUN npm ci --omit=dev \
    && npm cache clean --force

COPY --from=builder /app/dist ./dist

# Dedykowany użytkownik
USER node

EXPOSE 3000

CMD ["node", "dist/server.js"]
```

Co tutaj zyskujesz?

- Oddzielenie środowiska budowania od produkcyjnego.
- Brak narzędzi developerskich w obrazie końcowym.
- Instalację tylko zależności produkcyjnych.
- Mniejszą powierzchnię potencjalnego ataku.

Uwaga: dostosuj ścieżkę `dist` i polecenie startowe do struktury swojej aplikacji.

## 2. .dockerignore – nie kopiuj niepotrzebnych plików

Utwórz plik `.dockerignore` w katalogu projektu.

dockerignore

```dockerignore
node_modules
.git
.gitignore
.env
.env.*
!.env.example

Dockerfile*
docker-compose*
README.md

npm-debug.log
coverage
tests
```

Dzięki temu do kontekstu budowania nie trafią m.in. lokalne zależności, historia Git ani pliki konfiguracyjne z sekretami.

## 3. docker-compose.yml – konfiguracja produkcyjna

Przykładowa konfiguracja:

yaml

```yaml
services:
  app:
    build:
      context: .
      dockerfile: Dockerfile

    image: myapp:1.0.0

    container_name: myapp

    restart: unless-stopped

    environment:
      NODE_ENV: production

    ports:
      - "3000:3000"
```

Warto pamiętać o dwóch rzeczach:

- Używaj konkretnych wersji obrazów zamiast `latest`.
- W przypadku obrazów bazowych rozważ przypięcie digestu SHA256, aby zagwarantować niezmienność pobieranej wersji.

## 4. Skanowanie obrazu za pomocą Trivy

Top 10 Open-Source Kubernetes Security Tools Every DevOps Engineer Needs in 2025 | by Baivab Mukhopadhyay | devdotcom | Medium

Trivy

Skaner podatności obrazów kontenerowych

[Oficjalna dokumentacja](<https://trivy.dev/?utm_source=chatgpt.com>)

Zainstaluj Trivy zgodnie z dokumentacją, a następnie zbuduj obraz:

bash

```bash
docker compose build
```

Przeprowadź skanowanie:

bash

```bash
trivy image \
  --severity HIGH,CRITICAL \
  --exit-code 1 \
  myapp:1.0.0
```

Parametry:

- `HIGH,CRITICAL` – sprawdzanie poważnych i krytycznych podatności.
- `--exit-code 1` – zwrócenie kodu błędu, jeśli zostaną znalezione podatności.
- `myapp:1.0.0` – nazwa skanowanego obrazu.

Możesz też sprawdzić podatności bezpośrednio podczas budowania:

bash

```bash
trivy config .
```

To dodatkowo analizuje konfigurację Dockerfile i Compose.

## 5. Automatyzacja w CI/CD

Warto uruchamiać skanowanie przy każdym wdrożeniu lub publikacji obrazu.

Przykładowy fragment GitHub Actions:

yaml

```yaml
name: Docker Security Scan

on:
  push:
    branches: [main]

jobs:
  security:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Build Docker image
        run: docker build -t myapp:1.0.0 .

      - name: Scan image with Trivy
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: myapp:1.0.0
          severity: HIGH,CRITICAL
          exit-code: 1
```

W produkcji przypnij akcje GitHub do zweryfikowanych wersji lub commit SHA zamiast używać ruchomej referencji `master`.

## 6. Checklista wdrożeniowa

Postęp zabezpieczania obrazu

# 0/8

[ ]Używam lekkiego obrazu bazowego (Alpine lub Distroless).

[ ]Stosuję multi-stage build.

[ ]Instaluję tylko zależności produkcyjne.

[ ]Posiadam plik .dockerignore.

[ ]Nie kopiuję sekretów do obrazu.

[ ]Używam konkretnych wersji obrazów.

[ ]Skanuję obrazy za pomocą Trivy.

[ ]Blokuję wdrożenia z krytycznymi podatnościami.

## Mogę przygotować konfigurację dla Twojego projektu

Żeby przygotować Ci produkcyjny `Dockerfile` i `docker-compose.yml`, potrzebuję jednej informacji:

W jakiej technologii napisana jest Twoja aplikacja?

- Node.js / Express / NestJS
- Python / Django / FastAPI
- Java / Spring Boot
- PHP / Laravel
- .NET
- Inna

Na tej podstawie przygotuję konkretne pliki z optymalizacją obrazu, skanowaniem Trivy i konfiguracją bezpieczeństwa gotową do dalszego wdrożenia.