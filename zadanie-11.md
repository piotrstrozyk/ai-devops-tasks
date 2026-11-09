Poniżej znajdziesz prosty przykład testu jednostkowego dla funkcji `sum(a, b)` z wykorzystaniem Jest – popularnego frameworka do testowania kodu JavaScript.

## 1. Czym jest Jest?

Jest to framework do testowania kodu JavaScript i TypeScript, rozwijany pierwotnie przez Facebook (Meta).

Pozwala między innymi na:

- Pisanie testów jednostkowych (unit tests).
- Sprawdzanie, czy funkcje zwracają oczekiwane wyniki.
- Wykrywanie błędów w kodzie.
- Tworzenie mocków (symulowanie działania innych funkcji lub modułów).
- Generowanie raportów pokrycia kodu testami (code coverage).

Jest jest szczególnie popularny w projektach JavaScript i React.

## 2. Struktura plików projektu

Przykładowa struktura projektu:

text

```text
moj-projekt/
│
├── src/
│   └── sum.js
│
├── tests/
│   └── sum.test.js
│
├── package.json
└── node_modules/
```

Opis plików:

- `src/sum.js` – plik zawierający testowaną funkcję.
- `tests/sum.test.js` – plik zawierający test jednostkowy.
- `package.json` – konfiguracja projektu i zależności.
- `node_modules/` – katalog z zainstalowanymi bibliotekami.

## 3. Instalacja Jest

Najpierw upewnij się, że masz zainstalowany Node.js i npm.

W terminalu przejdź do katalogu projektu i wykonaj:

bash

```bash
npm init -y
```

Następnie zainstaluj Jest jako zależność deweloperską:

bash

```bash
npm install --save-dev jest
```

Dodaj do pliku `package.json` skrypt uruchamiający testy:

json

```json
{
  "scripts": {
    "test": "jest"
  }
}
```

Pozostałe pola wygenerowane przez `npm init` pozostaw bez zmian.

## 4. Kod testowanej funkcji

Plik: `src/sum.js`

javascript

```javascript
function sum(a, b) {
  return a + b;
}

module.exports = sum;
```

Używamy `module.exports`, aby umożliwić importowanie funkcji w pliku testowym.

## 5. Napisanie testu jednostkowego

Plik: `tests/sum.test.js`

javascript

```javascript
const sum = require('../src/sum');

describe('Funkcja sum()', () => {
  test('powinna zwrócić sumę dwóch liczb', () => {
    expect(sum(2, 3)).toBe(5);
  });

  test('powinna poprawnie dodawać liczby ujemne', () => {
    expect(sum(-2, -3)).toBe(-5);
  });

  test('powinna zwrócić 0 dla dwóch zer', () => {
    expect(sum(0, 0)).toBe(0);
  });
});
```

### Wyjaśnienie użytych metod

- `describe()` – grupuje testy dotyczące określonej funkcji.
- `test()` – definiuje pojedynczy przypadek testowy.
- `expect()` – określa wartość, którą chcemy sprawdzić.
- `toBe()` – sprawdza, czy otrzymany wynik jest równy oczekiwanej wartości.

Przykład:

javascript

```javascript
expect(sum(2, 3)).toBe(5);
```

Oznacza to: wywołaj funkcję `sum(2, 3)` i sprawdź, czy zwróciła `5`.

## 6. Uruchomienie testów

W terminalu, w głównym katalogu projektu, wpisz:

bash

```bash
npm test
```

Jest automatycznie wyszuka pliki testowe, między innymi te, których nazwy kończą się na `.test.js`.

Przykładowy wynik:

text

```text
PASS  tests/sum.test.js

  Funkcja sum()
    ✓ powinna zwrócić sumę dwóch liczb
    ✓ powinna poprawnie dodawać liczby ujemne
    ✓ powinna zwrócić 0 dla dwóch zer

Test Suites: 1 passed, 1 total
Tests:       3 passed, 3 total
```

Wszystkie 3 testy zakończone powodzeniem## 7. Podsumowanie

Wykonaliśmy następujące kroki:

1. Zainicjalizowaliśmy projekt za pomocą `npm init -y`.
2. Zainstalowaliśmy Jest za pomocą `npm install --save-dev jest`.
3. Utworzyliśmy funkcję `sum()` w pliku `sum.js`.
4. Utworzyliśmy testy jednostkowe w pliku `sum.test.js`.
5. Uruchomiliśmy testy poleceniem `npm test`.

Najważniejsze: test jednostkowy sprawdza działanie pojedynczego, niewielkiego fragmentu kodu – w tym przypadku funkcji `sum()`. Dzięki Jest możemy automatycznie sprawdzać, czy kod działa zgodnie z oczekiwaniami, bez konieczności ręcznego uruchamiania funkcji i sprawdzania wyników.