### Stwórz prosty diagram ASCII Art przedstawiający połączenie klienta, serwera aplikacji i bazy danych

text

```text
     +------------------+
     |      KLIENT      |
     | (przeglądarka /  |
     |   aplikacja)     |
     +------------------+
              |
              | Żądanie HTTP
              v
     +------------------+
     | SERWER APLIKACJI |
     |                  |
     |  Logika biznesowa|
     |  Przetwarzanie   |
     |     danych       |
     +------------------+
              |
              | Zapytanie SQL
              v
     +------------------+
     |   BAZA DANYCH    |
     |                  |
     |  Przechowywanie  |
     |      danych      |
     +------------------+
              |
              | Wynik zapytania
              v
     +------------------+
     | SERWER APLIKACJI |
     +------------------+
              |
              | Odpowiedź HTTP
              v
     +------------------+
     |      KLIENT      |
     +------------------+
```

Przepływ komunikacji:

1. Klient wysyła żądanie do serwera aplikacji.
2. Serwer przetwarza żądanie i komunikuje się z bazą danych.
3. Baza danych zwraca wyniki do serwera.
4. Serwer odsyła odpowiedź do klienta.


### Dodaj do diagramu opisy elementów i kierunki przepływu danych.

Poniżej diagram ASCII Art z opisami poszczególnych elementów oraz zaznaczonymi kierunkami przepływu danych.

## Diagram architektury systemu

text

```text
+----------------------------------+
|              KLIENT              |
|----------------------------------|
| - Interfejs użytkownika (UI)     |
| - Przeglądarka / aplikacja       |
| - Wysyłanie żądań                |
| - Odbieranie odpowiedzi          |
+----------------------------------+
                 |
                 | 1. ŻĄDANIE HTTP
                 |    (GET / POST / PUT / DELETE)
                 v
+----------------------------------+
|         SERWER APLIKACJI         |
|----------------------------------|
| - Obsługa żądań klienta          |
| - Logika biznesowa               |
| - Walidacja danych               |
| - Przetwarzanie danych           |
| - Komunikacja z bazą danych      |
+----------------------------------+
                 |
                 | 2. ZAPYTANIE SQL
                 |    (SELECT / INSERT / UPDATE)
                 v
+----------------------------------+
|            BAZA DANYCH           |
|----------------------------------|
| - Przechowywanie danych          |
| - Organizacja tabel              |
| - Odczyt i zapis informacji     |
| - Zarządzanie danymi             |
+----------------------------------+
                 |
                 | 3. WYNIK ZAPYTANIA
                 |    (rekordy / status operacji)
                 v
+----------------------------------+
|         SERWER APLIKACJI         |
|----------------------------------|
| - Odbiór wyników                 |
| - Przetwarzanie odpowiedzi       |
| - Przygotowanie danych JSON      |
+----------------------------------+
                 |
                 | 4. ODPOWIEDŹ HTTP
                 |    (JSON / HTML / status)
                 v
+----------------------------------+
|              KLIENT              |
|----------------------------------|
| - Odbiór odpowiedzi              |
| - Aktualizacja interfejsu       |
| - Wyświetlenie danych            |
+----------------------------------+
```

## Kierunki przepływu danych

| Etap | Kierunek | Opis |
| --- | --- | --- |
| 1 | Klient → Serwer | Wysłanie żądania HTTP |
| 2 | Serwer → Baza | Wykonanie zapytania SQL |
| 3 | Baza → Serwer | Przekazanie wyników |
| 4 | Serwer → Klient | Odesłanie odpowiedzi HTTP |

Najważniejsza zasada architektury:

- Klient komunikuje się z serwerem aplikacji.
- Serwer aplikacji komunikuje się z bazą danych.
- Klient nie komunikuje się bezpośrednio z bazą danych.

Taki model nazywamy architekturą trójwarstwową (Three-Tier Architecture).