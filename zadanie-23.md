## 1. Analiza złożoności pierwotnego algorytmu

Algorytm wykorzystuje dwie zagnieżdżone pętle `for`, które sprawdzają wszystkie możliwe pary elementów tablicy.

Złożoność czasowa: O(n²)

- Pętla zewnętrzna wykonuje się `n` razy.
- Pętla wewnętrzna sprawdza kolejne elementy od indeksu `i + 1`.
- Łączna liczba porównań wynosi:

$$
\frac{n(n-1)}{2}
$$

Po pominięciu stałych otrzymujemy O(n²).

Złożoność pamięciowa: O(k)

- Tablica `pairs` przechowuje znalezione pary.
- `k` oznacza liczbę znalezionych par.
- Pozostałe zmienne zajmują stałą ilość pamięci O(1).

W najgorszym przypadku liczba par wynosi O(n²), więc maksymalna złożoność pamięciowa również wynosi O(n²).

## 2. Optymalizacja algorytmu

Możemy zoptymalizować rozwiązanie, wykorzystując strukturę danych `Set`.

Zamiast porównywać każdy element z pozostałymi elementami tablicy, zapamiętujemy wcześniej odwiedzone wartości.

Dla każdego elementu:

1. Obliczamy wartość uzupełniającą (complement), czyli `targetSum - num`.
2. Sprawdzamy, czy ta wartość znajduje się już w `Set`.
3. Jeśli tak, zapisujemy znalezioną parę.
4. Dodajemy aktualny element do `Set`.

Dzięki temu eliminujemy zagnieżdżoną pętlę.

Zoptymalizowany kod:

javascript

```javascript
function findPairs(arr, targetSum) {
  const pairs = [];
  const seen = new Set();

  for (const num of arr) {
    const complement = targetSum - num;

    if (seen.has(complement)) {
      pairs.push([complement, num]);
    }

    seen.add(num);
  }

  return pairs;
}
```

## 3. Złożoność zoptymalizowanego algorytmu

Złożoność czasowa: O(n + k)

- Przechodzimy przez tablicę tylko raz: O(n).
- Operacje `Set.has()` i `Set.add()` mają średnią złożoność O(1).
- Zapisywanie znalezionych par wymaga O(k).

Złożoność pamięciowa: O(n + k)

- `Set` przechowuje odwiedzone wartości: maksymalnie O(n).
- Tablica `pairs` przechowuje znalezione pary: O(k).

## 4. Porównanie rozwiązań

| Kryterium | Pierwotny algorytm | Zoptymalizowany algorytm |
| --- | --- | --- |
| Czasowa | O(n²) | O(n + k) |
| Pamięciowa | O(k) | O(n + k) |
| Liczba pętli | 2 | 1 |
| Dodatkowa struktura | Brak | Set |
| Skalowalność | Niższa | Wyższa |

## 5. Wnioski

Zastosowanie `Set` pozwala znacząco zoptymalizować algorytm, ponieważ eliminuje konieczność sprawdzania wszystkich możliwych kombinacji elementów.

W typowym przypadku, gdy liczba znalezionych par jest niewielka, złożoność czasowa zbliża się do O(n), zamiast O(n²).

Należy jednak pamiętać, że jeśli liczba znalezionych par wynosi O(n²), algorytm nie może działać w czasie O(n), ponieważ samo wygenerowanie wszystkich wyników wymaga O(n²) operacji.

Najważniejszy kompromis: zoptymalizowane rozwiązanie zużywa więcej pamięci, ale znacząco zmniejsza liczbę operacji potrzebnych do wyszukiwania par.