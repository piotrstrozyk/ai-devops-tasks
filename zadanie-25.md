Jenkinsfile to plik konfiguracyjny opisujący proces automatyzacji CI/CD (Continuous Integration / Continuous Delivery). W przedstawionym przykładzie Jenkins wykonuje kolejno operacje związane z pobraniem kodu aplikacji Node.js, instalacją zależności, testowaniem, budowaniem aplikacji oraz przygotowaniem i publikacją obrazu Docker.

Poniżej wyjaśnię działanie każdego etapu, poszczególne instrukcje oraz dobre praktyki, które warto stosować przy projektowaniu pipeline'ów Jenkins.

# 1. Struktura deklaratywnego Jenkinsfile

Podstawowa struktura pipeline'u wygląda następująco:

groovy

```groovy
pipeline {
    agent any

    environment {
        // Zmienne środowiskowe
    }

    stages {
        stage('Nazwa etapu') {
            steps {
                // Instrukcje do wykonania
            }
        }
    }

    post {
        // Akcje wykonywane po zakończeniu pipeline'u
    }
}
```

Najważniejsze elementy:

| Element | Znaczenie |
| --- | --- |
| `pipeline` | Definiuje cały pipeline. |
| `agent` | Określa, gdzie pipeline będzie wykonywany. |
| `environment` | Definiuje zmienne środowiskowe. |
| `stages` | Zawiera wszystkie etapy procesu CI/CD. |
| `stage` | Reprezentuje pojedynczy etap. |
| `steps` | Zawiera polecenia wykonywane w danym etapie. |
| `post` | Definiuje działania wykonywane po zakończeniu pipeline'u. |

## 2. Wyjaśnienie poszczególnych etapów

### Etap 1: Checkout – pobieranie kodu

groovy

```groovy
stage('Checkout') {
    steps {
        checkout scm
    }
}
```

Co się dzieje?

Jenkins pobiera kod źródłowy aplikacji z repozytorium Git, np. GitHub, GitLab lub Bitbucket.

Instrukcja:

groovy

```groovy
checkout scm
```

oznacza, że Jenkins wykorzystuje konfigurację repozytorium przypisaną do bieżącego zadania (job).

W praktyce pobierane są:

- pliki źródłowe aplikacji,
- `package.json`,
- `package-lock.json`,
- `Dockerfile`,
- testy automatyczne,
- pozostałe pliki projektu.

Dobra praktyka:

- Przechowuj Jenkinsfile razem z kodem aplikacji (Pipeline as Code).
- Korzystaj z webhooków, aby uruchamiać pipeline po zmianach w repozytorium.
- W przypadku ważnych wdrożeń zapisuj informację o konkretnym commicie, który został zbudowany.

### Etap 2: Install Dependencies – instalacja zależności

groovy

```groovy
stage('Install Dependencies') {
    steps {
        sh 'npm install'
    }
}
```

Co się dzieje?

Jenkins uruchamia polecenie:

bash

```bash
npm install
```

Narzędzie npm odczytuje plik `package.json` i instaluje wymagane biblioteki.

Przykładowo aplikacja może korzystać z:

- Express.js,
- Axios,
- Jest,
- Lodash.

Zależności zostaną zainstalowane w katalogu:

text

```text
node_modules/
```

Dlaczego jest to potrzebne?

Aplikacja Node.js potrzebuje zewnętrznych bibliotek do prawidłowego działania. Bez nich testy i budowanie aplikacji mogą zakończyć się błędem.

Dobra praktyka:

W pipeline'ach CI lepiej używać:

bash

```bash
npm ci
```

zamiast:

bash

```bash
npm install
```

Dlaczego?

| `npm install` | `npm ci` |
| --- | --- |
| Może aktualizować lockfile. | Nie modyfikuje lockfile. |
| Może zmieniać wersje zależności zgodnie z semver. | Instaluje wersje określone w lockfile. |
| Może być mniej przewidywalne. | Zapewnia bardziej powtarzalne instalacje. |
| Może zachować istniejący katalog `node_modules`. | Usuwa go przed instalacją. |

W środowisku CI zalecane jest `npm ci`, jeśli projekt posiada `package-lock.json`.

### Etap 3: Run Tests – uruchamianie testów

groovy

```groovy
stage('Run Tests') {
    steps {
        sh 'npm test'
    }
}
```

Co się dzieje?

Jenkins uruchamia testy zdefiniowane w projekcie Node.js.

Przykładowo w `package.json` może znajdować się:

json

```json
{
    "scripts": {
        "test": "jest"
    }
}
```

W takim przypadku polecenie:

bash

```bash
npm test
```

uruchomi framework Jest.

Testy mogą sprawdzać:

- poprawność działania funkcji,
- obsługę błędów,
- działanie endpointów API,
- integrację z bazą danych,
- poprawność walidacji danych.

Co się stanie, jeśli testy nie przejdą?

Jenkins otrzyma kod zakończenia różny od zera i oznaczy etap jako nieudany.

Domyślnie kolejne etapy pipeline'u nie zostaną wykonane.

Dobre praktyki:

- Uruchamiaj testy przed budowaniem obrazu Docker.
- Oddzielaj testy jednostkowe od integracyjnych.
- Generuj raporty testów, np. w formacie JUnit XML.
- Nie ignoruj błędów testów.
- Dbaj o powtarzalność testów i izolację środowiska.

### Etap 4: Build Application – budowanie aplikacji

groovy

```groovy
stage('Build Application') {
    steps {
        sh 'npm run build'
    }
}
```

Co się dzieje?

Jenkins uruchamia skrypt `build` zdefiniowany w `package.json`.

Przykład:

json

```json
{
    "scripts": {
        "build": "tsc"
    }
}
```

W tym przypadku aplikacja TypeScript zostanie skompilowana do JavaScript.

W zależności od technologii etap może wykonywać:

- kompilację TypeScript,
- bundlowanie aplikacji,
- optymalizację plików JavaScript,
- minifikację kodu,
- generowanie plików produkcyjnych.

Przykładowy rezultat:

text

```text
project/
├── src/
├── dist/
│   ├── index.js
│   └── app.js
├── package.json
└── Dockerfile
```

Dobra praktyka:

- Buduj aplikację w trybie produkcyjnym.
- Upewnij się, że wynik budowania jest poprawny.
- Nie umieszczaj sekretów ani danych uwierzytelniających w artefaktach.
- Warto przechowywać artefakty budowania, jeśli będą wykorzystywane w kolejnych etapach lub wdrożeniach.

### Etap 5: Build Docker Image – budowanie obrazu Docker

groovy

```groovy
stage('Build Docker Image') {
    steps {
        sh """
            docker build -t ${DOCKER_REGISTRY}/${DOCKER_IMAGE}:${DOCKER_TAG} .
        """
    }
}
```

Co się dzieje?

Jenkins uruchamia polecenie `docker build`, które tworzy obraz Docker na podstawie pliku `Dockerfile`.

Przykładowy Dockerfile:

dockerfile

```dockerfile
FROM node:22-alpine

WORKDIR /app

COPY package*.json ./

RUN npm ci --omit=dev

COPY dist ./dist

EXPOSE 3000

CMD ["node", "dist/index.js"]
```

Polecenie:

bash

```bash
docker build -t docker.io/my-node-app:123 .
```

oznacza:

- `docker build` – budowanie obrazu,
- `-t` – nadanie nazwy i tagu,
- `docker.io` – rejestr Docker Hub,
- `my-node-app` – nazwa obrazu,
- `123` – tag odpowiadający numerowi buildu,
- `.` – bieżący katalog jako kontekst budowania.

Rezultatem jest gotowy obraz Docker.

Fundamentos contenedores Docker - CFL 410 - Clase 3

[docker.idepba.com.ar](<https://docker.idepba.com.ar/clase3.html?utm_source=chatgpt.com>)

Dobre praktyki:

- Używaj oficjalnych i przypiętych wersji obrazów bazowych.
- Stosuj wieloetapowe budowanie (multi-stage builds), jeśli jest potrzebne.
- Wykorzystuj `.dockerignore`, aby wykluczyć niepotrzebne pliki.
- Nie kopiuj do obrazu katalogu `node_modules` z hosta, jeśli zależności instalujesz w obrazie.
- Nie umieszczaj haseł ani tokenów w Dockerfile.
- Minimalizuj rozmiar obrazu.

### Etap 6: Push Docker Image – publikowanie obrazu

groovy

```groovy
stage('Push Docker Image') {
    steps {
        withCredentials([
            usernamePassword(
                credentialsId: "${DOCKER_CREDENTIALS}",
                usernameVariable: 'DOCKER_USER',
                passwordVariable: 'DOCKER_PASS'
            )
        ]) {
            sh """
                echo "\$DOCKER_PASS" | docker login ${DOCKER_REGISTRY} \
                    -u "\$DOCKER_USER" --password-stdin

                docker push ${DOCKER_REGISTRY}/${DOCKER_IMAGE}:${DOCKER_TAG}

                docker logout ${DOCKER_REGISTRY}
            """
        }
    }
}
```

Co się dzieje?

Ten etap odpowiada za uwierzytelnienie w rejestrze Docker i przesłanie obrazu.

Proces składa się z trzech operacji.

1. Pobranie poświadczeń

groovy

```groovy
withCredentials([
    usernamePassword(
        credentialsId: "${DOCKER_CREDENTIALS}",
        usernameVariable: 'DOCKER_USER',
        passwordVariable: 'DOCKER_PASS'
    )
])
```

Jenkins pobiera dane logowania zapisane w swoim magazynie Credentials.

Nie trzeba przechowywać haseł bezpośrednio w Jenkinsfile.

2. Logowanie do Docker Hub

bash

```bash
echo "$DOCKER_PASS" | docker login docker.io \
    -u "$DOCKER_USER" --password-stdin
```

Jenkins uwierzytelnia się w rejestrze Docker.

Użycie `--password-stdin` jest bezpieczniejsze niż przekazywanie hasła bezpośrednio jako argumentu polecenia.

3. Publikowanie obrazu

bash

```bash
docker push docker.io/my-node-app:123
```

Obraz zostaje przesłany do repozytorium Docker Hub.

Po zakończeniu można go pobrać np. na serwerze produkcyjnym:

bash

```bash
docker pull docker.io/my-node-app:123
```

Dobre praktyki:

- Korzystaj z Jenkins Credentials.
- Preferuj tokeny dostępu zamiast haseł konta.
- Ogranicz uprawnienia tokenów do niezbędnego minimum.
- Nie publikuj obrazów, jeśli testy zakończyły się błędem.
- Stosuj unikalne tagi obrazów, np. numer buildu lub SHA commita.
- Nie polegaj wyłącznie na tagu `latest`.

### Etap 7: Post – działania po zakończeniu pipeline'u

groovy

```groovy
post {
    success {
        echo 'Pipeline zakończony sukcesem!'
    }

    failure {
        echo 'Pipeline zakończony błędem!'
    }

    always {
        echo 'Zakończono wykonywanie pipeline.'
    }
}
```

Blok `post` umożliwia wykonanie dodatkowych operacji po zakończeniu pipeline'u.

Jenkins udostępnia kilka warunków:

| Warunek | Kiedy jest wykonywany? |
| --- | --- |
| `success` | Pipeline zakończył się sukcesem. |
| `failure` | Pipeline zakończył się błędem. |
| `always` | Zawsze, niezależnie od wyniku. |
| `unstable` | Pipeline ma status niestabilny. |
| `aborted` | Pipeline został przerwany. |
| `changed` | Status pipeline'u zmienił się względem poprzedniego wykonania. |

Przykładowe zastosowania:

- wysłanie powiadomienia na Slack,
- publikowanie raportów testowych,
- archiwizacja logów,
- czyszczenie środowiska,
- informowanie zespołu o błędach.

# 3. Najlepsze praktyki przy tworzeniu pipeline'ów Jenkins

Poniżej najważniejsze zasady, które warto stosować w rzeczywistych projektach.

## 3.1. Pipeline as Code

Przechowuj Jenkinsfile w repozytorium Git razem z kodem aplikacji.

Przykładowa struktura:

text

```text
my-node-app/
├── src/
├── tests/
├── dist/
├── Dockerfile
├── .dockerignore
├── package.json
├── package-lock.json
└── Jenkinsfile
```

Zalety:

- historia zmian pipeline'u,
- możliwość code review,
- łatwe odtworzenie konfiguracji,
- wspólne zarządzanie kodem i procesem CI/CD.

## 3.2. Używaj zmiennych środowiskowych

Zamiast wielokrotnie wpisywać te same wartości, definiuj je w `environment`.

Przykład:

groovy

```groovy
environment {
    APP_NAME = 'my-node-app'
    DOCKER_REGISTRY = 'docker.io'
    DOCKER_TAG = "${BUILD_NUMBER}"
}
```

Dzięki temu zmiana nazwy aplikacji lub rejestru nie wymaga modyfikacji wielu etapów.

Ważne: sekretów nie należy definiować bezpośrednio w `environment`. Powinny pochodzić z Jenkins Credentials.

## 3.3. Wykorzystuj agenty Jenkins

W prostym przykładzie użyliśmy:

groovy

```groovy
agent any
```

Oznacza to, że Jenkins może wykonać pipeline na dowolnym dostępnym agencie spełniającym wymagania.

W większych projektach warto określić konkretne środowisko:

groovy

```groovy
agent {
    label 'nodejs-docker'
}
```

Wtedy pipeline zostanie uruchomiony na agencie oznaczonym etykietą `nodejs-docker`.

Możesz dzięki temu rozdzielić:

- agentów do testów Node.js,
- agentów do budowania obrazów Docker,
- agentów do wdrażania aplikacji.

## 3.4. Ograniczaj czas wykonywania pipeline'u

Używaj `timeout`, aby uniknąć sytuacji, w której pipeline działa bez końca.

groovy

```groovy
options {
    timeout(time: 30, unit: 'MINUTES')
}
```

Możesz również ograniczyć liczbę równoczesnych wykonań:

groovy

```groovy
options {
    disableConcurrentBuilds()
}
```

Jest to szczególnie przydatne, gdy kilka buildów mogłoby jednocześnie modyfikować wspólne środowisko.

## 3.5. Wykorzystuj cache zależności

Instalacja wszystkich zależności przy każdym uruchomieniu pipeline'u może być czasochłonna.

Warto wykorzystać cache npm, np.:

bash

```bash
npm config get cache
```

Następnie skonfigurować cache na poziomie agenta lub mechanizmu cache wykorzystywanego przez pipeline.

Pozwala to ograniczyć czas instalacji zależności.

## 3.6. Rozdzielaj etapy CI i CD

Warto rozumieć różnicę:

- CI (Continuous Integration) – pobieranie kodu, instalacja zależności, testy i budowanie aplikacji.
- CD (Continuous Delivery/Deployment) – przygotowanie i wdrażanie aplikacji na środowiska docelowe.

Przykładowy podział:

CIContinuous Integration

1. Checkout
2. Install Dependencies
3. Run Tests
4. Build Application
5. Build Docker Image

CDContinuous Delivery / Deployment

1. Push Docker Image
2. Deploy to Staging
3. Integration Tests
4. Deploy to Production

Dzięki temu można np. automatycznie budować aplikację po każdym commicie, ale wdrażanie na produkcję uzależnić od zatwierdzenia przez członka zespołu.

## 3.7. Zabezpieczaj pipeline

Bezpieczeństwo jest jednym z najważniejszych elementów CI/CD.

Zalecenia:

- Nie zapisuj haseł w Jenkinsfile.
- Używaj Jenkins Credentials.
- Ograniczaj uprawnienia użytkowników i agentów.
- Nie uruchamiaj niezaufanego kodu z pull requestów z dostępem do produkcyjnych sekretów.
- Regularnie aktualizuj pluginy Jenkins.
- Skanuj obrazy Docker pod kątem podatności.
- Korzystaj z podpisywania obrazów, np. Cosign.

## 3.8. Archiwizuj artefakty i raporty

W Jenkinsie możesz wykorzystać:

groovy

```groovy
post {
    always {
        archiveArtifacts artifacts: 'dist/**',
                         allowEmptyArchive: true
    }
}
```

Dzięki temu pliki z katalogu `dist` będą dostępne z poziomu historii wykonania pipeline'u.

Można również publikować raporty testowe przy użyciu pluginu JUnit:

groovy

```groovy
post {
    always {
        junit 'reports/**/*.xml'
    }
}
```

# 4. Przykładowy ulepszony Jenkinsfile

Poniżej przykład uwzględniający część opisanych praktyk: `npm ci`, timeout, ograniczenie równoczesnych buildów, archiwizację artefaktów oraz bezpieczne pobieranie poświadczeń.

groovy

```groovy

pipeline {
    agent {
        label 'nodejs-docker'
    }

    options {
        timeout(time: 30, unit: 'MINUTES')
        disableConcurrentBuilds()
        timestamps()
    }

    environment {
        DOCKER_IMAGE = 'my-node-app'
        DOCKER_TAG = "${BUILD_NUMBER}"
        DOCKER_REGISTRY = 'docker.io'
        DOCKER_CREDENTIALS = 'dockerhub-credentials'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'npm ci'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'npm test'
            }
        }

        stage('Build Application') {
            steps {
                sh 'npm run build'
            }
        }

        stage('Archive Artifacts') {
            steps {
                archiveArtifacts artifacts: 'dist/**',
                                 allowEmptyArchive: false
            }
        }

        stage('Build Docker Image') {
            steps {
                sh """
                    docker build \
                        -t ${DOCKER_REGISTRY}/${DOCKER_IMAGE}:${DOCKER_TAG} .
                """
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: "${DOCKER_CREDENTIALS}",
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )
                ]) {
                    sh """
                        set +x
                        echo "\$DOCKER_PASS" | docker login \
                            ${DOCKER_REGISTRY} \
                            -u "\$DOCKER_USER" \
                            --password-stdin

                        docker push \
                            ${DOCKER_REGISTRY}/${DOCKER_IMAGE}:${DOCKER_TAG}

                        docker logout ${DOCKER_REGISTRY}
                    """
                }
            }
        }
    }

    post {
        success {
            echo 'Build zakończony sukcesem!'
        }

        failure {
            echo 'Build zakończony błędem!'
        }

        always {
            echo 'Pipeline zakończony.'
        }
    }
}
```

Uwaga: agent `nodejs-docker` musi mieć zainstalowane Node.js i Docker oraz odpowiednie uprawnienia do uruchamiania Dockera. Przykład zakłada również, że aplikacja generuje katalog `dist`.

# 5\. Podsumowanie – najważniejsze zasady

| Obszar | Zalecana praktyka |
| --- | --- |
| Kod pipeline'u | Jenkinsfile w Git |
| Instalacja npm | `npm ci` |
| Testy | Testowanie przed budowaniem obrazu |
| Docker | Małe obrazy i `.dockerignore` |
| Tagowanie | Numer buildu lub SHA commita |
| Sekrety | Jenkins Credentials |
| Agenty | Dedykowane etykiety |
| Wydajność | Cache zależności |
| Stabilność | `timeout`, `disableConcurrentBuilds` |
| Raportowanie | `junit`, `archiveArtifacts` |
| Bezpieczeństwo | Skanowanie i podpisywanie obrazów |
| Wdrożenia | Oddzielenie CI od CD |

Moja najważniejsza rekomendacja: traktuj Jenkinsfile jak zwykły kod produkcyjny. Powinien być wersjonowany, testowany, czytelny i bezpieczny. Dobrze zaprojektowany pipeline powinien zapewniać powtarzalność procesu – ten sam commit powinien prowadzić do tego samego artefaktu, niezależnie od tego, ile razy uruchomisz budowanie.