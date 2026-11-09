## Dane wyjściowe

Metryki serwera API (ostatnie 24h):
- Średni czas odpowiedzi: 230ms
- 95 percentyl czasu odpowiedzi: 450ms
- 99 percentyl czasu odpowiedzi: 1200ms
- Liczba zapytań: 15,000
- Liczba błędów 5xx: 120
- Użycie CPU: średnio 45%, max 80%
- Użycie pamięci: średnio 2.1GB, max 3.5GB (z 4GB dostępnych)

# Analiza:

Na podstawie tych metryk widzę kilka potencjalnych problemów. Najbardziej niepokojące są wysoki 99. percentyl czasu odpowiedzi, poziom wykorzystania pamięci oraz liczba błędów 5xx.

Ogólnie serwer nie wygląda na przeciążony przez cały czas, ale prawdopodobnie występują okresowe problemy z wydajnością, które dotykają części użytkowników.

## 1. Analiza poszczególnych metryk

Średni czas odpowiedzi

Dobry

# 230 ms

średnia

Czas odpowiedzi jest akceptowalny dla większości typowych API. Nie wskazuje na ogólny problem z wydajnością.95. percentyl

Do obserwacji

# 450 ms

5% zapytań trwa dłużej niż 450 ms. Może to wskazywać na wolniejsze endpointy, zapytania SQL lub okresowe oczekiwanie na zależności zewnętrzne.99. percentyl

Problem

# 1200 ms

1% zapytań trwa ponad 1,2 sekundy. To istotna różnica względem średniej.Błędy 5xx

Do zbadania

# 0,8%

120 błędów na 15 000 zapytań. To około 1 błąd na 125 żądań.CPU

Zdrowy poziom

# 45%

Średnie wykorzystanie CPU jest umiarkowane. Maksimum 80% sugeruje jednak okresowe skoki obciążenia.Pamięć RAM

Wysokie wykorzystanie

# 3,5 / 4 GB

Maksymalnie wykorzystano 87,5% dostępnej pamięci. Pozostaje tylko 512 MB zapasu.

## 2. Najważniejsze potencjalne problemy

### Problem 1: Nierównomierny czas odpowiedzi (Latency)

Zestawienie czasów:

| Metryka | Czas |
| --- | --- |
| Średnia | 230 ms |
| P95 | 450 ms |
| P99 | 1200 ms |

P99 jest ponad 5 razy większy od średniej.

Może to oznaczać:

- Niektóre endpointy wykonują bardzo kosztowne operacje.
- Występują wolne zapytania do bazy danych.
- Pojawiają się blokady lub kolejki połączeń.
- API czeka na zewnętrzne usługi.
- Garbage Collection powoduje chwilowe zatrzymania aplikacji (jeśli środowisko korzysta z GC).

Moja rekomendacja: zidentyfikować 10 najwolniejszych endpointów i sprawdzić ich P95 oraz P99 osobno.

### Problem 2: Wysokie wykorzystanie pamięci

Maksymalne wykorzystanie RAM

# 87,5%

3,5 GB z 4 GB

Zajęte: 3,5 GB

Wolne: 0,5 GB

To potencjalnie najbardziej ryzykowna metryka.

Możliwe przyczyny:

- Memory leak.
- Zbyt duże obiekty przechowywane w pamięci.
- Nadmierny cache.
- Zbyt duża liczba równoległych żądań.
- Nieprawidłowa konfiguracja puli połączeń.

Przy dalszym wzroście pamięci może dojść do:

- OOM Killer i restartowania procesu.
- Długich pauz Garbage Collection.
- Spadku wydajności.
- Błędów 5xx.

Rekomendacje:

1. Zbadać trend pamięci w czasie, nie tylko maksimum.
2. Sprawdzić, czy pamięć zwalnia po spadku ruchu.
3. Wykonać profilowanie pamięci (heap profiling).
4. Przejrzeć konfigurację cache i jego limity.
5. Sprawdzić liczbę równoległych requestów.

Nie zwiększałbym od razu RAM bez sprawdzenia, czy nie występuje wyciek pamięci.

### Problem 3: Błędy 5xx

120 błędów na 15 000 zapytań oznacza:

$$
\frac{120}{15000}\times100 = 0,8\%
$$

To nie jest katastrofalny wynik, ale zdecydowanie warto go poprawić.

Najpierw sprawdziłbym rozkład błędów:

| Kod | Możliwa przyczyna |
| --- | --- |
| 500 | Błędy aplikacji, wyjątki |
| 502 | Problemy z upstreamem |
| 503 | Niedostępność lub przeciążenie |
| 504 | Timeout |

Szczególnie interesujące byłoby sprawdzenie, czy błędy występują w momentach maksymalnego wykorzystania pamięci i CPU.

Rekomendacje:

- Przeanalizować logi wszystkich 120 błędów.
- Sprawdzić korelację błędów z czasem odpowiedzi.
- Zweryfikować timeouty.
- Sprawdzić dostępność bazy danych i usług zewnętrznych.
- Dodać monitoring wyjątków i przyczyn błędów.

## 3. Co zrobiłbym, żeby poprawić wydajność?

Ustawiłbym następującą kolejność działań:

1. Profilowanie wolnych endpointów
   Zidentyfikować endpointy odpowiedzialne za P99 = 1200 ms.
   Sprawdzić:
   - Czas wykonywania kodu.
   - Czas zapytań SQL.
   - Czas komunikacji z innymi usługami.
   - Liczbę zapytań wykonywanych na jeden request.
2. Optymalizacja bazy danych
   Sprawdzić:
   - Brakujące indeksy.
   - Slow Query Log.
   - N+1 queries.
   - Connection Pool.
   - Długotrwałe transakcje.
   To jeden z pierwszych obszarów, które warto zweryfikować.
3. Optymalizacja zarządzania pamięcią
   - Wprowadzić limity cache.
   - Ograniczyć wielkość odpowiedzi API.
   - Sprawdzić wycieki pamięci.
   - Przeanalizować liczbę równoległych operacji.
4. Poprawa obsługi błędów
   - Dodać szczegółowe logowanie wyjątków.
   - Wprowadzić odpowiednie timeouty.
   - Stosować retry z exponential backoff dla operacji, które można bezpiecznie ponawiać.
   - Zastosować circuit breaker dla niestabilnych usług zewnętrznych.
5. Wprowadzenie cache
   Jeśli API obsługuje często pobierane, rzadko zmieniające się dane, warto rozważyć Redis lub cache aplikacyjny.
   Pozwoli to ograniczyć liczbę zapytań do bazy danych.
6. Testy obciążeniowe
   Przeprowadzić testy za pomocą k6, Locust lub JMeter.
   Sprawdzić zachowanie API przy 2x i 3x obecnego obciążenia.

## 4. Proponowane cele optymalizacyjne

Ustawiłbym następujące cele jako punkt wyjścia, a następnie dostosował je do wymagań biznesowych i SLA.

| Metryka | Obecnie | Cel |
| --- | --- | --- |
| Średni czas | 230 ms | poniżej 180 ms |
| P95 | 450 ms | poniżej 300 ms |
| P99 | 1200 ms | poniżej 600 ms |
| Błędy 5xx | 0,8% | poniżej 0,1% |
| Średnie CPU | 45% | poniżej 60% |
| Maksymalne RAM | 87,5% | poniżej 75% |

Warto zauważyć, że nie należy optymalizować CPU wyłącznie po to, aby uzyskać niższy procent wykorzystania. Ważniejsze jest utrzymanie stabilności i odpowiedniego zapasu zasobów przy rosnącym ruchu.

## 5. Jakie dodatkowe dane chciałbym zobaczyć?

Obecne metryki pozwalają wskazać potencjalne problemy, ale nie wystarczają do ustalenia ich rzeczywistej przyczyny.

Najbardziej przydatne byłyby:

- Ruch w czasie: liczba requestów na sekundę (RPS), najlepiej w interwałach 1-minutowych.
- RAM w czasie: czy pamięć stale rośnie, czy tylko chwilowo skacze?
- CPU w czasie: czy skoki CPU pokrywają się z wysokim P99?
- Baza danych: czas zapytań, liczba aktywnych połączeń, locki.
- Błędy: dokładny rozkład kodów 5xx i stack trace.
- Endpointy: P50, P95, P99 dla poszczególnych ścieżek.

## 6. Moja końcowa diagnoza

## Priorytety działań

P1Pamięć RAM – ryzyko wyczerpania zasobów

P1Błędy 5xx – ustalenie przyczyn 120 błędów

P2P99 – identyfikacja wolnych zapytań

P2CPU – analiza okresowych skoków obciążenia

P3Średni czas odpowiedzi – dalsza optymalizacja

Najważniejszy wniosek: nie zaczynałbym od skalowania infrastruktury ani optymalizacji kodu na ślepo. Najpierw zbadałbym pamięć RAM, błędy 5xx i najwolniejsze requesty. Istnieje możliwość, że wszystkie trzy problemy mają wspólną przyczynę, np. zbyt dużą liczbę równoległych operacji lub problemy z bazą danych.