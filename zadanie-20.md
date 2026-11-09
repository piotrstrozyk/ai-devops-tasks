### Regex

^(?:(?:25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\.){3}(?:25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])$

Wyrażenie regularne:

regex

```regex
^(?:(?:25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\.){3}(?:25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])$
```

służy do sprawdzania, czy tekst jest poprawnym adresem IPv4 zapisanym w standardowej postaci dziesiętnej, np. `192.168.1.1`.

## 1. Budowa wyrażenia regularnego

Rozłóżmy regex na poszczególne elementy.

### Początek i koniec tekstu

regex

```regex
^
```

Oznacza początek tekstu.

regex

```regex
$
```

Oznacza koniec tekstu.

Dzięki temu regex sprawdza cały ciąg znaków, a nie tylko jego fragment.

Przykładowo `abc192.168.1.1xyz` nie zostanie zaakceptowany.

### Zakres pojedynczego oktetu (0–255)

Najważniejsza część wyrażenia to:

regex

```regex
(?:25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])
```

Odpowiada ona za sprawdzenie, czy pojedyncza liczba mieści się w zakresie od 0 do 255.

Składa się z czterech alternatyw (`|` oznacza LUB):

| Fragment regex | Zakres | Przykłady |
| --- | --- | --- |
| `25[0-5]` | 250–255 | 250, 253, 255 |
| `2[0-4][0-9]` | 200–249 | 200, 225, 249 |
| `1[0-9]{2}` | 100–199 | 100, 150, 199 |
| `[1-9]?[0-9]` | 0–99 | 0, 9, 45, 99 |

Wyjaśnienie dodatkowych symboli:

- [ ]– określa zbiór dopuszczalnych znaków.
- `[0-9]` – dowolna cyfra od 0 do 9.
- `[1-9]` – cyfra od 1 do 9.
- `?` – poprzedni element może wystąpić zero lub jeden raz.
- `{2}` – poprzedni element musi wystąpić dokładnie dwa razy.
- `|` – alternatywa logiczna OR.
- `(?:...)` – grupa nieprzechwytująca, służąca do grupowania fragmentów regex.

### Trzy pierwsze oktety i kropki

regex

```regex
(?:(?:25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\.){3}
```

Ten fragment odpowiada za trzy pierwsze części adresu IPv4.

Elementy:

- `(?:...)` – grupuje wzorzec pojedynczego oktetu wraz z kropką.
- `\.` – oznacza dosłowną kropkę. Backslash jest potrzebny, ponieważ sama kropka w regex oznacza dowolny znak.
- `{3}` – powtarza cały wzorzec dokładnie trzy razy.

Przykładowo dopasowuje:

text

```text
192.
168.
1.
```

### Ostatni oktet

regex

```regex
(?:25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])
```

Ostatni fragment sprawdza czwarty oktet. Nie ma już po nim kropki.

W ten sposób otrzymujemy dokładnie cztery liczby oddzielone trzema kropkami.

## 2. Testowanie wyrażenia regularnego

Sprawdźmy kilka przykładów.

Poprawne adresy| Adres IPv4 | Dlaczego jest poprawny? |
| --- | --- |
| `192.168.1.1` | Wszystkie oktety mieszczą się w zakresie 0–255 |
| `10.0.0.1` | Wszystkie liczby są poprawne |
| `255.255.255.255` | Maksymalna wartość każdego oktetu |
| `0.0.0.0` | Minimalna wartość każdego oktetu |
| `172.16.254.3` | Wszystkie oktety są poprawne |
| `192.168.100.200` | Wszystkie oktety są poprawne |
| `8.8.8.8` | Wszystkie oktety są poprawne |

Niepoprawne adresy| Adres IPv4 | Dlaczego jest niepoprawny? |
| --- | --- |
| `256.168.1.1` | 256 przekracza maksymalną wartość 255 |
| `192.168.1.999` | 999 przekracza zakres |
| `192.168.1` | Brakuje czwartego oktetu |
| `192.168.1.1.1` | Występuje pięć oktetów |
| `192.168..1` | Brakuje wartości jednego oktetu |
| `192.168.01.1` | Niedozwolone zero wiodące |
| `abc.168.1.1` | Zawiera litery zamiast cyfr |
| `192-168-1-1` | Użyto myślników zamiast kropek |
| `192.168.1.256` | Ostatni oktet przekracza 255 |

## 3. Przykładowy test w JavaScript

Możesz przetestować regex bezpośrednio w JavaScript:

javascript

```javascript
const ipv4Regex = /^(?:(?:25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\.){3}(?:25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])$/;

const addresses = [
    "192.168.1.1",
    "255.255.255.255",
    "0.0.0.0",
    "10.0.0.1",
    "256.168.1.1",
    "192.168.1",
    "192.168.01.1",
    "192.168.1.999"
];

addresses.forEach(ip => {
    console.log(ip, ipv4Regex.test(ip));
});
```

Wynik:

text

```text
192.168.1.1 true
255.255.255.255 true
0.0.0.0 true
10.0.0.1 true
256.168.1.1 false
192.168.1 false
192.168.01.1 false
192.168.1.999 false
```

## 4. Interaktywny tester IPv4

Możesz również sprawdzić działanie regexu poniżej.

Wpisz adres IPv4:

192.168.1.1

Poprawny format IPv4

Walidacja wykorzystuje dokładnie omawiane wyrażenie regularne.

192.168.1.1  255.255.255.255  256.1.1.1  192.168.01.1

## 5. Ważna uwaga

Ten regex sprawdza poprawność składniową adresu IPv4, ale nie sprawdza, czy adres jest faktycznie przypisany do urządzenia, dostępny w sieci lub możliwy do routowania.

Na przykład `0.0.0.0` i `255.255.255.255` przechodzą walidację składniową, ale mają specjalne znaczenie w sieciach komputerowych.

Podsumowanie: Regex gwarantuje cztery oktety, trzy kropki, wartości od 0 do 255 i brak zer wiodących. To dobre rozwiązanie do podstawowej walidacji formatu IPv4 w formularzach i aplikacjach.