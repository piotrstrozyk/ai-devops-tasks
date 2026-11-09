Writing

# Simple Task API

REST API do zarządzania zadaniami, stworzone przy użyciu **Node.js**, **Express.js** oraz **MongoDB**.

## Opis

Simple Task API to prosta aplikacja backendowa umożliwiająca zarządzanie zadaniami (CRUD).

Główne funkcjonalności:

- Tworzenie nowych zadań.
- Pobieranie listy zadań oraz szczegółów wybranego zadania.
- Aktualizowanie istniejących zadań.
- Usuwanie zadań.
- Filtrowanie zadań według statusu i priorytetu.
- Podstawowa autoryzacja użytkowników.

## Instalacja

### Wymagania

- Node.js (18 lub nowszy)
- MongoDB
- npm

### Kroki instalacji

1. Sklonuj repozytorium:

bash

```bash
git clone https://github.com/username/simple-task-api.git
```

2. Przejdź do katalogu projektu:

bash

```bash
cd simple-task-api
```

3. Zainstaluj zależności:

bash

```bash
npm install
```

4. Utwórz plik `.env` w głównym katalogu projektu:

env

```env
PORT=3000
MONGODB_URI=mongodb://localhost:27017/simple-task-api
JWT_SECRET=your_secret_key
```

5. Uruchom serwer:

bash

```bash
npm start
```

Serwer będzie dostępny pod adresem:

text

```text
http://localhost:3000
```

## Użycie

API umożliwia wykonywanie operacji na zadaniach za pomocą żądań HTTP.

Przykładowe żądanie tworzące zadanie:

http

```http
POST /api/tasks
Content-Type: application/json
Authorization: Bearer YOUR_TOKEN
```

Przykładowe dane JSON:

json

```json
{
  "title": "Przygotować dokumentację",
  "description": "Napisać README.md dla projektu",
  "status": "pending",
  "priority": "high"
}
```

Przykładowe uruchomienie trybu deweloperskiego:

bash

```bash
npm run dev
```

## Endpointy API

### Zadania (`/api/tasks`)

| Metoda | Endpoint | Opis |
| --- | --- | --- |
| GET | `/api/tasks` | Pobieranie wszystkich zadań |
| GET | `/api/tasks/:id` | Pobieranie zadania po ID |
| POST | `/api/tasks` | Tworzenie nowego zadania |
| PUT | `/api/tasks/:id` | Aktualizacja zadania |
| DELETE | `/api/tasks/:id` | Usuwanie zadania |

### Filtrowanie zadań

Możliwe jest filtrowanie zadań za pomocą parametrów zapytania:

http

```http
GET /api/tasks?status=pending
GET /api/tasks?priority=high
GET /api/tasks?status=completed&priority=low
```

### Autoryzacja (`/api/auth`)

| Metoda | Endpoint | Opis |
| --- | --- | --- |
| POST | `/api/auth/register` | Rejestracja użytkownika |
| POST | `/api/auth/login` | Logowanie użytkownika |

Po zalogowaniu użytkownik otrzymuje token JWT, który należy przekazywać w nagłówku:

http

```http
Authorization: Bearer YOUR_TOKEN
```

---

## Technologie

- **Node.js** – środowisko uruchomieniowe JavaScript.
- **Express.js** – framework do tworzenia REST API.
- **MongoDB** – baza danych NoSQL.
- **Mongoose** – obsługa modeli i komunikacji z MongoDB.
- **JWT** – uwierzytelnianie użytkowników.

## Licencja

Projekt edukacyjny. Licencja do ustalenia.
