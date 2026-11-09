## Opis procesu konwersji JSON do CSV

Konwersja danych z formatu JSON do CSV polega na przekształceniu struktury danych zapisanej w postaci obiektów i tablic na płaską tabelę składającą się z wierszy i kolumn.

W podanym przykładzie JSON zawiera obiekt główny z tablicą `users`, w której znajdują się dwa obiekty reprezentujące użytkowników.

### 1. Analiza struktury JSON

Na początku należy przeanalizować strukturę danych i zidentyfikować pola, które mają zostać przeniesione do CSV.

W naszym przypadku są to:

- `id` – identyfikator użytkownika.
- `name` – imię i nazwisko.
- `email` – adres e-mail.
- `roles` – tablica ról przypisanych użytkownikowi.

Każdy obiekt z tablicy `users` będzie reprezentowany jako jeden wiersz w pliku CSV.

### 2. Mapowanie pól na kolumny CSV

Następnie przypisujemy poszczególne właściwości JSON do kolumn CSV.

| Pole JSON | Kolumna CSV | Typ danych |
| --- | --- | --- |
| id | id | Liczba |
| name | name | Tekst |
| email | email | Tekst |
| roles | roles | Tablica |

Wiersz nagłówkowy CSV będzie wyglądał następująco:

csv

```csv
id,name,email,roles
```

### 3. Reprezentacja tablicy `roles`

To jeden z najważniejszych aspektów transformacji.

CSV nie obsługuje natywnie tablic ani zagnieżdżonych struktur danych. Dlatego należy wybrać sposób reprezentacji tablicy `roles`.

Możliwe są trzy popularne rozwiązania:

Opcja A – Połączenie wartości w jednej kolumnie (zalecane dla prostych przypadków)

Elementy tablicy łączymy przecinkiem, a całą wartość umieszczamy w cudzysłowie.

csv

```csv
id,name,email,roles
1,Jan Kowalski,jan@example.com,"admin,user"
2,Anna Nowak,anna@example.com,user
```

Zalety:

- Prosta implementacja.
- Zachowanie jednego wiersza na użytkownika.
- Łatwe odczytywanie danych.

Wady:

- Trzeba znać separator użyty do rozdzielania ról.
- Wartości zawierające przecinki wymagają dodatkowego zabezpieczenia.
- Trudniejsze filtrowanie pojedynczych ról w arkuszach kalkulacyjnych.

Opcja B – Rozdzielenie ról na osobne kolumny

Każda rola otrzymuje osobną kolumnę.

csv

```csv
id,name,email,role_1,role_2
1,Jan Kowalski,jan@example.com,admin,user
2,Anna Nowak,anna@example.com,user,
```

Zalety:

- Łatwiejsza analiza danych w arkuszach kalkulacyjnych.
- Role są widoczne w osobnych komórkach.

Wady:

- Liczba kolumn zależy od maksymalnej liczby ról.
- Struktura CSV może się zmieniać wraz z pojawieniem się nowych ról.

Opcja C – Osobny wiersz dla każdej roli

Każda rola jest reprezentowana jako osobny rekord.

csv

```csv
id,name,email,role
1,Jan Kowalski,jan@example.com,admin
1,Jan Kowalski,jan@example.com,user
2,Anna Nowak,anna@example.com,user
```

Zalety:

- Łatwe filtrowanie i grupowanie ról.
- Dobre rozwiązanie do analizy danych i importu do baz danych.
- Brak konieczności przechowywania tablic w jednej komórce.

Wady:

- Powielanie danych użytkownika.
- Jeden użytkownik może występować w wielu wierszach.

### 4. Potencjalne wyzwania podczas konwersji

| Wyzwanie | Opis | Możliwe rozwiązanie |
| --- | --- | --- |
| Tablice | CSV nie obsługuje tablic natywnie | Łączenie elementów separatorem |
| Znaki specjalne | Przecinki, cudzysłowy i znaki nowej linii mogą zaburzyć strukturę | Stosowanie cudzysłowów i poprawnego escapowania |
| Brakujące wartości | Niektóre pola mogą nie występować w JSON | Puste komórki |
| Typy danych | JSON obsługuje liczby, tekst, wartości logiczne i null | Konwersja do reprezentacji tekstowej |
| Zagnieżdżone obiekty | CSV jest formatem płaskim | Spłaszczenie struktury lub osobne pliki |
| Kodowanie znaków | Polskie znaki mogą być niepoprawnie wyświetlane | Kodowanie UTF-8 |

### 5. Dodatkowe kwestie techniczne

Podczas implementacji konwertera warto zwrócić uwagę na kilka szczegółów:

- Escapowanie cudzysłowów: jeśli wartość zawiera cudzysłów, należy go podwoić. Przykładowo `Jan "Admin"` powinno zostać zapisane jako `"Jan ""Admin"""`.
- Separator: najczęściej używany jest przecinek, ale w polskich arkuszach kalkulacyjnych często spotyka się średnik.
- Puste tablice: należy ustalić, czy będą reprezentowane jako pusta komórka, czy np. pusty tekst.
- Wartości null: warto odróżnić brak wartości od pustego ciągu znaków, jeśli ma to znaczenie biznesowe.
- Kolejność kolumn: powinna być stała i zgodna z ustalonym schematem.

### 6. Rekomendowane podejście

W przypadku przedstawionych danych rekomenduję opcję A, czyli przechowywanie wszystkich ról w jednej kolumnie, rozdzielonych przecinkami i ujętych w cudzysłów, jeśli jest to wymagane przez składnię CSV.

Końcowy plik:

csv

```csv
id,name,email,roles
1,Jan Kowalski,jan@example.com,"admin,user"
2,Anna Nowak,anna@example.com,user
```

Takie rozwiązanie jest proste, czytelne i zachowuje zasadę jednego użytkownika na jeden wiersz.

Jeżeli jednak dane będą wykorzystywane do dalszego przetwarzania, filtrowania lub importowania do relacyjnej bazy danych, warto rozważyć opcję C.

Najważniejszy wniosek: CSV nie ma natywnego typu tablicowego, dlatego sposób reprezentacji `roles` należy dobrać do sposobu, w jaki dane będą później wykorzystywane.