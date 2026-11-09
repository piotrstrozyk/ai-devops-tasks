# Jak uruchomić Jenkins z konfiguracją JCasC?

Najwygodniejszym sposobem uruchomienia Jenkinsa z przygotowanym szablonem jest wykorzystanie Dockera i Docker Compose.

Dzięki temu:

- Jenkins uruchamia się automatycznie w kontenerze.
- Wtyczki są instalowane podczas budowania obrazu.
- Konfiguracja Jenkinsa jest pobierana z pliku `jenkins.yaml`.
- Zadania Pipeline są tworzone automatycznie.
- Dane Jenkinsa są zachowywane po restarcie kontenera.

Poniżej znajduje się instrukcja krok po kroku.

## 1. Wymagania wstępne

Przed rozpoczęciem upewnij się, że masz zainstalowane:

| Oprogramowanie | Zastosowanie |
| --- | --- |
| Docker | Uruchamianie kontenerów |
| Docker Compose | Zarządzanie kontenerem Jenkins |
| Git | Pobieranie i wersjonowanie konfiguracji |
| Edytor tekstu | Edycja plików YAML i Dockerfile |

Sprawdź instalację:

bash

```bash
docker --version
docker compose version
git --version
```

## 2. Przygotowanie katalogu projektu

Utwórz katalog przechowujący konfigurację Jenkinsa:

bash

```bash
mkdir jenkins-configuration
cd jenkins-configuration
```

Utwórz następującą strukturę:

text

```text
jenkins-configuration/
│
├── Dockerfile
├── docker-compose.yml
├── plugins.txt
├── jenkins.yaml
└── .env
```

Każdy plik ma określone zadanie:

- `Dockerfile` – buduje obraz Jenkinsa z wymaganymi wtyczkami.
- `docker-compose.yml` – definiuje sposób uruchomienia kontenera.
- `plugins.txt` – zawiera listę wtyczek.
- `jenkins.yaml` – zawiera konfigurację JCasC.
- `.env` – przechowuje zmienne środowiskowe, np. hasło administratora.

## 3. Przygotowanie plików konfiguracyjnych

### 3.1. Dockerfile

Utwórz plik `Dockerfile`:

dockerfile

```dockerfile

FROM jenkins/jenkins:lts

USER root

COPY plugins.txt /usr/share/jenkins/ref/plugins.txt

RUN jenkins-plugin-cli \
    --plugin-file /usr/share/jenkins/ref/plugins.txt

USER jenkins
```

Co robi ten plik?

1. Pobiera oficjalny obraz Jenkins LTS.
2. Kopiuje listę wymaganych wtyczek.
3. Instaluje wtyczki.
4. Przywraca użytkownika `jenkins`.

### 3.2. Lista wtyczek

W pliku `plugins.txt` umieść:

text

```text

configuration-as-code
workflow-aggregator
git
git-client
credentials
credentials-binding
ssh-credentials
pipeline-stage-view
pipeline-utility-steps
job-dsl
maven-plugin
nodejs
docker-workflow
timestamper
ws-cleanup
```

Wtyczka `configuration-as-code` jest szczególnie ważna – odpowiada za odczytywanie konfiguracji YAML.

### 3.3. Plik jenkins.yaml

Umieść przygotowany wcześniej plik `jenkins.yaml` w katalogu projektu.

Ważne: w konfiguracji JCasC nie ma uniwersalnego parametru `timeout` dla całego serwera. Limit czasu wykonania zadania najlepiej ustawić w Pipeline:

groovy

```groovy
options {
    timeout(time: 30, unit: 'MINUTES')
}
```

Warto również pamiętać, że konfiguracja narzędzi musi odpowiadać dokładnym wersjom zainstalowanych wtyczek.

### 3.4. Plik `.env`

Utwórz plik `.env`:

dotenv

```dotenv
JENKINS_ADMIN_PASSWORD=ZmienToNaSilneHaslo123!
```

Nie umieszczaj tego pliku w repozytorium Git. Dodaj go do `.gitignore`.

### 3.5. Plik docker-compose.yml

Utwórz plik:

yaml

```yaml

services:
  jenkins:
    build: .
    container_name: jenkins
    restart: unless-stopped

    ports:
      - "8080:8080"
      - "50000:50000"

    environment:
      CASC_JENKINS_CONFIG: /var/jenkins_home/casc_configs/jenkins.yaml
      JENKINS_ADMIN_USER: admin
      JENKINS_ADMIN_PASSWORD: "${JENKINS_ADMIN_PASSWORD}"

    volumes:
      - jenkins_home:/var/jenkins_home
      - ./jenkins.yaml:/var/jenkins_home/casc_configs/jenkins.yaml:ro

volumes:
  jenkins_home:
```

Najważniejszy parametr to:

yaml

```yaml
CASC_JENKINS_CONFIG: /var/jenkins_home/casc_configs/jenkins.yaml
```

Informuje on plugin JCasC, gdzie znajduje się plik konfiguracyjny. Plugin odczytuje go podczas inicjalizacji Jenkinsa.

Jenkins plugin

+1

## 4. Budowanie obrazu Jenkins

Otwórz terminal w katalogu `jenkins-configuration`.

Wykonaj:

bash

```bash
docker compose build
```

Docker wykona następujące operacje:

1. Pobierze bazowy obraz Jenkins LTS.
2. Zainstaluje wymagane wtyczki.
3. Przygotuje obraz zawierający środowisko Jenkins.

Po zakończeniu możesz sprawdzić dostępne obrazy:

bash

```bash
docker images
```

## 5. Uruchomienie Jenkinsa

Uruchom kontener:

bash

```bash
docker compose up -d
```

Parametr `-d` uruchamia kontener w tle.

Sprawdź jego status:

bash

```bash
docker compose ps
```

Powinieneś zobaczyć kontener Jenkins ze statusem `Up`.

Następnie sprawdź logi:

bash

```bash
docker compose logs -f jenkins
```

W logach szukaj komunikatów dotyczących:

- uruchomienia Jenkins;
- instalacji i ładowania wtyczek;
- odczytania konfiguracji JCasC;
- utworzenia zadania Pipeline.

Jeżeli pojawi się błąd `ConfiguratorException`, sprawdź poprawność YAML oraz zgodność konfiguracji z zainstalowanymi wtyczkami.

## 6. Dostęp do interfejsu Jenkins

How to schedule a job in Jenkins

Jenkins Web UI

# [http://localhost:8080](<http://localhost:8080?utm_source=chatgpt.com>)

Domyślny port HTTP

Otwórz przeglądarkę i przejdź pod wskazany adres.

Jeżeli konfiguracja JCasC poprawnie ustawiła `securityRealm` i użytkownika administratora, zaloguj się danymi z pliku `.env`.

Jeśli konfiguracja zabezpieczeń nie została zastosowana, sprawdź logi. W przypadku standardowego kreatora pierwszego uruchomienia hasło można odczytać poleceniem:

bash

```bash
docker exec jenkins \
  cat /var/jenkins_home/secrets/initialAdminPassword
```

Nie należy jednak tworzyć drugiego konta administratora w kreatorze bez sprawdzenia, czy konto z JCasC zostało już utworzone.

## 7. Weryfikacja konfiguracji JCasC

Po zalogowaniu przejdź do:

Manage Jenkins → Configuration as Code

Powinna być dostępna strona zarządzania konfiguracją.

Wybierz opcję View Configuration, aby zobaczyć konfigurację załadowaną przez Jenkins.

Sprawdź następujące elementy:

| Element | Oczekiwany rezultat |
| --- | --- |
| System Message | Jenkins skonfigurowany automatycznie |
| Number of executors | 3 |
| Maven | Maven-3.9 |
| Node.js | NodeJS-20 |
| Pipeline | example-pipeline |
| Security | Logowanie wymagane |

Jeśli zmienisz plik `jenkins.yaml`, możesz ponownie załadować konfigurację przez Manage Jenkins → Configuration as Code → Reload existing configuration. Nie trzeba wówczas restartować serwera.

Jenkins

## 8. Uruchomienie przykładowego Pipeline

Przejdź do głównego dashboardu Jenkins.

Powinno być dostępne zadanie:

example-pipeline

Oczekiwane zadanie

Kliknij zadanie, a następnie:

1. Wybierz Build Now.
2. Przejdź do Build History.
3. Otwórz wykonane zadanie.
4. Wybierz Console Output.

Pipeline powinien wykonać kolejno:

## Przebieg Pipeline

1. Checkout
   Pobranie kodu źródłowego z repozytorium.
2. Build
   Budowanie aplikacji za pomocą Maven.
3. Test
   Uruchomienie testów jednostkowych.
4. Node Build
   Instalacja zależności i budowanie aplikacji frontendowej.
5. Docker Build
   Budowanie obrazu Docker.

Uwaga: przykładowy Pipeline zakłada dostęp do repozytorium Git, plików `pom.xml`, `package.json` i `Dockerfile`. Ponadto agent musi mieć zainstalowane lub dostępne odpowiednie narzędzia. Sama instalacja wtyczki Docker nie zapewnia dostępu do Docker Engine.

Jenkins plugin

+1

## 9. Zarządzanie Jenkins po uruchomieniu

Najważniejsze polecenia administracyjne:

| Operacja | Polecenie |
| --- | --- |
| Uruchomienie | `docker compose up -d` |
| Zatrzymanie | `docker compose stop` |
| Restart | `docker compose restart` |
| Wyświetlenie logów | `docker compose logs -f jenkins` |
| Status | `docker compose ps` |
| Przebudowanie obrazu | `docker compose build` |
| Usunięcie kontenera | `docker compose down` |

Ważne: `docker compose down` nie usuwa domyślnie wolumenu `jenkins_home`. Dzięki temu konfiguracja, zadania i historia buildów pozostają zachowane.

Nie używaj `docker compose down -v`, jeśli chcesz zachować dane Jenkinsa.

## 10. Schemat działania całego rozwiązania

Repozytorium konfiguracji

Dockerfile · jenkins.yaml · plugins.txt

Docker Compose

Budowanie i uruchamianie kontenera

Jenkins + JCasC

Automatyczne zastosowanie konfiguracji YAML

Narzędzia

Maven, Node.js, Docker

Wtyczki

Git, Pipeline, JCasC

Automatycznie utworzony Pipeline

Build → Test → Node Build → Docker Build

## 11. Dokumentacja

Przydatne oficjalne materiały:

- [Jenkins – Configuration as Code](<https://www.jenkins.io/doc/book/managing/casc/?utm_source=chatgpt.com>)
- [JCasC Plugin – dokumentacja wtyczki](<https://plugins.jenkins.io/configuration-as-code/?utm_source=chatgpt.com>)
- [Jenkins – instalacja przez Docker](<https://www.jenkins.io/doc/book/installing/docker/?utm_source=chatgpt.com>)
- [Jenkins Configuration as Code – projekt](<https://www.jenkins.io/projects/jcasc/?utm_source=chatgpt.com>)

