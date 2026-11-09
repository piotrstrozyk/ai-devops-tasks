Zastosowane tagi JSDoc:

    @async – oznacza funkcję asynchroniczną.

    @function – określa nazwę dokumentowanej funkcji.

    @param – opisuje parametr wejściowy.

    @returns – opisuje typ i wartość zwracaną.

    @throws – dokumentuje możliwy wyjątek.

    @example – przedstawia przykład użycia funkcji.


JSDoc to standard dokumentowania kodu JavaScript za pomocą specjalnych komentarzy umieszczanych bezpośrednio nad funkcjami, klasami, metodami lub zmiennymi.

Pozwala opisać:

- `@param` – parametry funkcji.
- `@returns` – wartość zwracaną.
- `@type` – typ zmiennej.
- `@throws` – możliwe wyjątki.
- `@example` – przykład użycia.
- `@deprecated` – oznaczenie przestarzałego elementu.

Przykład:

javascript

```javascript
/**
 * Dodaje dwie liczby.
 * @param {number} a - Pierwsza liczba.
 * @param {number} b - Druga liczba.
 * @returns {number} Suma liczb.
 */
function add(a, b) {
  return a + b;
}
```

Główne zalety JSDoc:

- Ułatwia zrozumienie i utrzymanie kodu.
- Generuje automatyczną dokumentację.
- Poprawia podpowiedzi w edytorach, np. VS Code.
- Pomaga wykrywać błędy związane z typami danych.