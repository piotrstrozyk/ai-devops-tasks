Ignorowanie odpowiednich plików w `.gitignore` jest ważne przede wszystkim ze względu na bezpieczeństwo, porządek w repozytorium i prawidłową współpracę zespołową.

W projekcie Node.js + Docker + MongoDB ma to szczególne znaczenie.

## 1. Bezpieczeństwo danych i haseł

Pliki takie jak `.env` mogą zawierać poufne informacje:

env

```env
MONGO_URI=mongodb://admin:secret123@localhost:27017/mydb
JWT_SECRET=my-super-secret-key
PORT=3000
```

Jeśli dodasz taki plik do Git:

- Hasła mogą zostać ujawnione innym osobom.
- Dane dostępowe mogą trafić do publicznego repozytorium GitHub.
- Ktoś może uzyskać dostęp do Twojej bazy danych lub innych usług.

Dlatego ignorujemy `.env`, ale pozostawiamy `.env.example`, który zawiera nazwy zmiennych bez prawdziwych sekretów.

## 2. Ochrona danych MongoDB

MongoDB przechowuje dane w plikach binarnych, np. w katalogu `mongo-data/`.

MongoDB disk space increases abruptly - WiredTigerLAS.wt - Ops and Admin - MongoDB Community Hub

[mongodb.com](<https://www.mongodb.com/community/forums/t/mongodb-disk-space-increases-abruptly-wiredtigerlas-wt/3620?utm_source=chatgpt.com>)

Dlaczego nie należy ich commitować?

- Mogą zajmować dużo miejsca.
- Zmieniają się przy każdej operacji na bazie.
- Mogą zawierać dane użytkowników, hasła lub inne informacje poufne.
- Mogą powodować konflikty między różnymi wersjami bazy.

Zamiast tego każdy programista powinien mieć własną lokalną bazę danych.

Jeżeli potrzebujesz współdzielić dane testowe, lepiej przygotować skrypt seedujący lub kontrolowany eksport danych.

## 3. Nieprzechowywanie node\_modules

Katalog `node_modules/` może zawierać tysiące plików i zajmować setki megabajtów.

Nie ma potrzeby umieszczania go w Git, ponieważ zależności można odtworzyć za pomocą:

bash

```bash
npm install
```

W przypadku projektu z `package-lock.json` lepiej używać:

bash

```bash
npm ci
```

Zapewnia to instalację wersji zależności zgodnych z plikiem blokady.

## 4. Ograniczenie zbędnych plików Dockera

Niektóre pliki lokalne, np. `docker-compose.override.yml`, mogą zawierać indywidualną konfigurację środowiska programisty.

Ignorowanie ich zapobiega przypadkowemu nadpisaniu konfiguracji innych osób.

Warto jednak pamiętać:

- `Dockerfile` – powinien być w Git.
- `docker-compose.yml` – powinien być w Git.
- `docker-compose.override.yml` – można ignorować, jeśli zawiera lokalne ustawienia.

## 5. Czy wszystkie pliki należy ignorować?

Nie. Istotne jest rozróżnienie między plikami projektu a lokalnymi danymi.

| Plik / katalog | W Git? | Dlaczego? |
| --- | --- | --- |
| `package.json` | Tak | Lista zależności |
| `package-lock.json` | Tak | Powtarzalne instalacje |
| `Dockerfile` | Tak | Konfiguracja obrazu |
| `docker-compose.yml` | Tak | Konfiguracja usług |
| `.env` | Nie | Sekrety i konfiguracja lokalna |
| `.env.example` | Tak | Szablon konfiguracji |
| `node_modules/` | Nie | Odtwarzalne zależności |
| `mongo-data/` | Nie | Lokalne dane bazy |
| `logs/` | Nie | Pliki generowane podczas pracy |

## 6. Ważne: .gitignore nie usuwa wcześniej dodanych plików

Jeśli przypadkowo dodałeś już `.env` lub `mongo-data/` do repozytorium, samo wpisanie ich do `.gitignore` nie wystarczy.

Musisz usunąć je z indeksu Git:

bash

```bash
git rm --cached .env
git rm -r --cached mongo-data/
git commit -m "Remove local files from repository"
```

Pliki pozostaną na Twoim komputerze.

Uwaga: jeśli sekrety zostały już opublikowane w zdalnym repozytorium, należy je zmienić. Samo usunięcie pliku nie usuwa ich z historii Git.

Najważniejsza zasada: w Git przechowuj kod źródłowy, konfigurację potrzebną do uruchomienia projektu i definicje zależności. Nie przechowuj lokalnych danych, sekretów ani plików, które można automatycznie odtworzyć.