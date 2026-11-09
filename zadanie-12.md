### oryginalna:

def find_duplicates(list_of_items):
    duplicates = []
    for i in range(len(list_of_items)):
        for j in range(i+1, len(list_of_items)):
            if list_of_items[i] == list_of_items[j] and list_of_items[i] not in duplicates:
                duplicates.append(list_of_items[i])
    return duplicates

### zoptymalizowana

Tak\! Twój kod można znacząco zoptymalizować. Obecna implementacja działa poprawnie, ale ma złożoność czasową O(n²) ze względu na dwie zagnieżdżone pętle.

Można osiągnąć O(n), wykorzystując strukturę danych `set` (zbiór).

## 1. Zoptymalizowana wersja

python

```python
def find_duplicates(list_of_items):
    seen = set()
    duplicates = set()

    for item in list_of_items:
        if item in seen:
            duplicates.add(item)
        else:
            seen.add(item)

    return list(duplicates)
```

### Jak to działa?

- `seen` przechowuje elementy, które już wystąpiły.
- `duplicates` przechowuje elementy wykryte jako duplikaty.
- Jeśli element znajduje się już w `seen`, dodajemy go do `duplicates`.
- W przeciwnym razie dodajemy go do `seen`.

## 2. Złożoność obliczeniowa

| Wersja | Złożoność czasowa | Złożoność pamięciowa |
| --- | --- | --- |
| Oryginalna | O(n²) | O(n) |
| Zoptymalizowana | O(n) średnio | O(n) |

Operacje sprawdzania obecności elementu w `set` mają średnią złożoność O(1).

## 3. Ważna uwaga – zachowanie kolejności

Wersja powyżej wykorzystuje zbiór do przechowywania duplikatów, dlatego nie gwarantuje kolejności ich występowania.

Jeśli chcesz zachować kolejność pierwszego wykrycia duplikatów, lepsza będzie taka implementacja:

python

```python
def find_duplicates(list_of_items):
    seen = set()
    duplicates = []
    duplicates_set = set()

    for item in list_of_items:
        if item in seen:
            if item not in duplicates_set:
                duplicates.append(item)
                duplicates_set.add(item)
        else:
            seen.add(item)

    return duplicates
```

Przykład:

python

```python
items = [1, 2, 3, 2, 4, 1, 5, 3, 3]

print(find_duplicates(items))
```

Wynik:

python

```python
[2, 1, 3]
```

## 4. Którą wersję wybrać?

Polecam drugą wersję, ponieważ:

- Zachowuje kolejność wykrywania duplikatów.
- Nie dodaje wielokrotnie tego samego duplikatu.
- Ma średnią złożoność czasową O(n).
- Jest wydajna i czytelna.

Uwaga: Obie zoptymalizowane wersje zakładają, że elementy listy są hashowalne (np. liczby, napisy czy krotki). Jeśli lista zawiera słowniki lub inne listy, potrzebne będzie inne rozwiązanie.