## Logi
May 19 10:15:32 server dockerd[1234]: time="2025-05-19T10:15:32.123456789Z" level=info msg="Container 78a2b3c4 health status changed from starting to healthy"
May 19 10:16:45 server dockerd[1234]: time="2025-05-19T10:16:45.987654321Z" level=info msg="Container 78a2b3c4 failed to connect to 172.17.0.3:5432: connection refused"
May 19 10:16:47 server dockerd[1234]: time="2025-05-19T10:16:47.246813579Z" level=warning msg="Container 78a2b3c4 health status changed from healthy to unhealthy"

## Analiza

Logi przedstawiają problem z komunikacją między kontenerem Docker a usługą bazodanową (najprawdopodobniej PostgreSQL), działającą na adresie `172.17.0.3` i porcie `5432`.

Najważniejszy problem: kontener początkowo działał poprawnie, ale później utracił możliwość połączenia z bazą danych, co spowodowało zmianę jego statusu zdrowia na `unhealthy`.

## 1. Analiza poszczególnych wpisów

### Wpis 1 – 10:15:32

text

```text
level=info msg="Container 78a2b3c4 health status changed from starting to healthy"
```

Healthy- Kontener `78a2b3c4` zakończył fazę uruchamiania.
- Mechanizm Docker Health Check uznał go za działający poprawnie.
- Kontener był w stanie `healthy`.

Nie widać tutaj żadnego problemu.

### Wpis 2 – 10:16:45

text

```text
level=info msg="Container 78a2b3c4 failed to connect to 172.17.0.3:5432: connection refused"
```

Problem z połączeniemTo najważniejszy wpis w przedstawionych logach.

Oznacza, że:

- Kontener próbował połączyć się z adresem `172.17.0.3`.
- Próbował uzyskać dostęp do portu `5432`.
- Połączenie zostało odrzucone (`connection refused`).

Port `5432` jest domyślnym portem PostgreSQL.

Możliwe przyczyny:

1. PostgreSQL nie działa lub uległ awarii.
2. PostgreSQL nie nasłuchuje na porcie `5432`.
3. Usługa bazodanowa została zrestartowana.
4. Konfiguracja sieci Docker jest nieprawidłowa.
5. Baza danych nasłuchuje tylko na `localhost`, zamiast na interfejsie dostępnym dla innych kontenerów.

Warto zauważyć, że `connection refused` zwykle oznacza, że host jest osiągalny, ale na wskazanym porcie nie ma usługi akceptującej połączenia.

### Wpis 3 – 10:16:47

text

```text
level=warning msg="Container 78a2b3c4 health status changed from healthy to unhealthy"
```

Unhealthy- Docker wykrył problem z działaniem kontenera.
- Health Check nie przeszedł pomyślnie.
- Status kontenera zmienił się z `healthy` na `unhealthy`.

Prawdopodobnie problem z połączeniem z bazą danych spowodował niepowodzenie testu zdrowia kontenera.

## 2. Chronologia zdarzeń

| Czas | Zdarzenie | Status |
| --- | --- | --- |
| 10:15:32 | Kontener uruchomiony poprawnie | Healthy |
| 10:16:45 | Odrzucone połączenie z PostgreSQL | Problem |
| 10:16:47 | Nieudany Health Check | Unhealthy |

Schemat problemu

Kontener HEALTHY

10:15:32

Connection refused

10:16:45 – brak możliwości połączenia z PostgreSQL

Kontener UNHEALTHY

10:16:47

## 3. Jak zdiagnozować problem?

Proponuję wykonać następujące polecenia.

1. Sprawdzenie statusu kontenerów:

bash

```bash
docker ps -a
```

Sprawdź, czy kontener PostgreSQL nadal działa.

2. Sprawdzenie logów bazy danych:

bash

```bash
docker logs <postgres_container>
```

Szukaj błędów związanych z uruchamianiem PostgreSQL, awariami i restartami.

3. Sprawdzenie konfiguracji Health Check:

bash

```bash
docker inspect 78a2b3c4
```

Zwróć uwagę na sekcję `Health`, szczególnie `Log` i `FailingStreak`.

4. Sprawdzenie dostępności portu z kontenera aplikacji:

bash

```bash
docker exec -it 78a2b3c4 sh
```

Następnie:

bash

```bash
nc -zv 172.17.0.3 5432
```

5. Sprawdzenie nasłuchiwania PostgreSQL:

W kontenerze bazy danych:

bash

```bash
ss -lntp
```

## 4. Zidentyfikowane problemy – podsumowanie

| Problem | Możliwa przyczyna | Priorytet |
| --- | --- | --- |
| Odrzucone połączenie TCP | PostgreSQL nie nasłuchuje | Wysoki |
| Zmiana statusu na unhealthy | Nieudany Health Check | Wysoki |
| Możliwa niedostępność bazy | Awaria lub restart PostgreSQL | Wysoki |
| Potencjalny problem sieciowy | Błędna konfiguracja Docker | Średni |

## 5. Moja rekomendacja

W pierwszej kolejności sprawdziłbym kontener PostgreSQL, ponieważ komunikat `connection refused` wskazuje przede wszystkim na problem z usługą docelową lub jej konfiguracją nasłuchiwania.

Warto również sprawdzić, czy aplikacja nie korzysta ze statycznego adresu IP `172.17.0.3`. W środowisku Docker Compose lepiej używać nazwy usługi, np. `postgres:5432`, ponieważ adresy IP kontenerów mogą się zmieniać.

Ważne: same logi nie dowodzą, że PostgreSQL uległ awarii. Potwierdzają jedynie, że połączenie zostało odrzucone, a następnie kontener stracił status `healthy`.

Mogę również pomóc przeanalizować konfigurację `docker-compose.yml` i wskazać, co może powodować ten problem.