Writing

# GET /api/users

## Opis

Endpoint służy do pobierania listy użytkowników systemu. Umożliwia stronicowanie wyników oraz filtrowanie użytkowników według przypisanej roli.

**Metoda HTTP:** `GET`\
**Ścieżka:** `/api/users`

## Parametry zapytania (Query Parameters)

| Parametr | Typ | Wymagany | Domyślna wartość | Opis |
| --- | --- | --- | --- | --- |
| `page` | integer | Nie | `1` | Numer strony wyników. |
| `limit` | integer | Nie | `10` | Liczba użytkowników zwracanych na jednej stronie. Maksymalna wartość: `100`. |
| `role` | string | Nie | Brak | Filtruje użytkowników według przypisanej roli. |

## Przykładowe żądanie

Pobranie drugiej strony wyników, zawierającej maksymalnie 20 użytkowników z rolą `admin`:

http

```http
GET /api/users?page=2&limit=20&role=admin HTTP/1.1
Host: api.example.com
Accept: application/json
```

## Przykładowa odpowiedź

**Status HTTP:** `200 OK`

json

```json
{
  "users": [
    {
      "id": 1,
      "name": "Jan Kowalski",
      "email": "jan.kowalski@example.com",
      "role": "admin"
    },
    {
      "id": 2,
      "name": "Anna Nowak",
      "email": "anna.nowak@example.com",
      "role": "admin"
    }
  ],
  "pagination": {
    "page": 2,
    "limit": 20,
    "total": 42,
    "totalPages": 3
  }
}
```

> **Uwaga:** Powyższa struktura odpowiedzi jest przykładowa i zakłada, że API zwraca listę użytkowników wraz z informacjami o paginacji.

## Kody odpowiedzi HTTP

| Kod | Opis |
| --- | --- |
| `200 OK` | Lista użytkowników została pobrana pomyślnie. |
| `400 Bad Request` | Nieprawidłowe parametry zapytania, np. ujemny numer strony lub limit większy niż 100. |
| `401 Unauthorized` | Brak uwierzytelnienia. |
| `403 Forbidden` | Użytkownik nie ma uprawnień do pobierania listy użytkowników. |
| `500 Internal Server Error` | Wystąpił nieoczekiwany błąd serwera. |

## Dodatkowe informacje

- Jeśli parametr `page` nie zostanie podany, przyjmowana jest wartość `1`.
- Jeśli parametr `limit` nie zostanie podany, zwracanych jest domyślnie 10 użytkowników.
- Maksymalna liczba użytkowników na stronie wynosi 100.
- Parametr `role` jest opcjonalny i pozwala ograniczyć wyniki do użytkowników o określonej roli.
- W przypadku braku użytkowników spełniających kryteria filtrowania endpoint powinien zwrócić pustą listę.