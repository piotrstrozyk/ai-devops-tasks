Oczywiście\! Przejdźmy przez skrypt krok po kroku, zakładając, że dopiero zaczynasz przygodę z Bash i Linuxem.

## 1. Cały skrypt

Najpierw przypomnijmy sobie jego treść:

bash

```bash
#!/bin/bash

SERVICE="docker"

echo "Sprawdzam status usługi Docker..."

if systemctl is-active --quiet "$SERVICE"; then
    echo "Docker działa poprawnie."
else
    echo "Docker nie działa. Próbuję uruchomić usługę..."

    if sudo systemctl start "$SERVICE"; then
        echo "Docker został pomyślnie uruchomiony."
    else
        echo "BŁĄD: Nie udało się uruchomić Dockera."
        exit 1
    fi
fi

exit 0
```

## 2. Wyjaśnienie linia po linii

### Linia 1

bash

```bash
#!/bin/bash
```

To tak zwany shebang.

Informuje system operacyjny, że skrypt powinien zostać wykonany przy użyciu interpretera Bash.

Mówiąc prościej: system wie, że ma użyć Basha do wykonania kolejnych poleceń.

### Linia 2

bash

```bash
SERVICE="docker"
```

Tutaj tworzymy zmienną o nazwie `SERVICE`.

- `SERVICE` – nazwa zmiennej.
- `"docker"` – wartość przypisana do zmiennej.

Od tej chwili wszędzie tam, gdzie użyjemy `$SERVICE`, Bash podstawi tekst `docker`.

Dlaczego tak robimy?

Żeby nie wpisywać wielokrotnie nazwy usługi. Jeśli kiedyś zechcesz sprawdzać inną usługę, wystarczy zmienić wartość zmiennej.

### Linia 3

bash

```bash
echo "Sprawdzam status usługi Docker..."
```

Polecenie `echo` wyświetla tekst w terminalu.

W tym przypadku użytkownik zobaczy:

text

```text
Sprawdzam status usługi Docker...
```

To tylko komunikat informacyjny. Nie wykonuje żadnej operacji na Dockerze.

### Linia 4

bash

```bash
if systemctl is-active --quiet "$SERVICE"; then
```

To jedna z najważniejszych linii skryptu.

Rozłóżmy ją na części:

- `if` – oznacza warunek, czyli „jeżeli”.
- `systemctl` – narzędzie do zarządzania usługami w systemie Linux korzystającym z systemd.
- `is-active` – sprawdza, czy wskazana usługa jest aktywna.
- `--quiet` – wyłącza wyświetlanie dodatkowych komunikatów.
- `"$SERVICE"` – nazwa usługi, w naszym przypadku `docker`.
- `then` – oznacza „to wykonaj”.

Czyli całe polecenie można przeczytać następująco:

Jeżeli usługa Docker jest aktywna, wykonaj polecenia znajdujące się poniżej.

Warto wiedzieć, że `systemctl is-active` zwraca kod zakończenia:

- `0` – usługa jest aktywna.
- Wartość różną od `0` – usługa nie jest aktywna.

Bash wykorzystuje ten kod do oceny warunku `if`.

### Linia 5

bash

```bash
echo "Docker działa poprawnie."
```

Jeśli poprzedni warunek jest prawdziwy, wyświetlany jest komunikat:

text

```text
Docker działa poprawnie.
```

Nie musimy już niczego uruchamiać.

### Linia 6

bash

```bash
else
```

Słowo `else` oznacza „w przeciwnym razie”.

Czyli jeżeli Docker nie działa, Bash przechodzi do tej części skryptu.

### Linia 7

bash

```bash
echo "Docker nie działa. Próbuję uruchomić usługę..."
```

Wyświetlamy informację, że Docker nie działa i skrypt podejmie próbę jego uruchomienia.

### Linia 8

bash

```bash
if sudo systemctl start "$SERVICE"; then
```

Tutaj ponownie mamy instrukcję warunkową `if`.

Tym razem próbujemy uruchomić usługę.

Rozbijmy polecenie:

- `sudo` – wykonuje polecenie z uprawnieniami administratora (root), jeśli użytkownik ma odpowiednie uprawnienia.
- `systemctl` – narzędzie do zarządzania usługami.
- `start` – polecenie uruchamiające usługę.
- `"$SERVICE"` – nazwa usługi, czyli `docker`.

Całość oznacza:

Spróbuj uruchomić usługę Docker z uprawnieniami administratora.

Jeśli polecenie zakończy się powodzeniem, wykonana zostanie część znajdująca się po `then`.

### Linia 9

bash

```bash
echo "Docker został pomyślnie uruchomiony."
```

Jeśli polecenie uruchomienia zakończy się powodzeniem, wyświetli się komunikat:

text

```text
Docker został pomyślnie uruchomiony.
```

### Linia 10

bash

```bash
else
```

Jeżeli uruchomienie Dockera się nie powiedzie, przechodzimy do tej części instrukcji.

### Linia 11

bash

```bash
echo "BŁĄD: Nie udało się uruchomić Dockera."
```

Wyświetlamy komunikat informujący o błędzie.

Przykładowo może się tak stać, jeśli użytkownik nie ma odpowiednich uprawnień lub wystąpi problem z usługą.

### Linia 12

bash

```bash
exit 1
```

To polecenie kończy działanie skryptu.

Liczba `1` oznacza, że skrypt zakończył się błędem.

Warto zapamiętać:

- `exit 0` – wszystko zakończyło się poprawnie.
- `exit 1` – wystąpił błąd.

Kod zakończenia może być później wykorzystany przez inne skrypty lub narzędzia do sprawdzenia, czy operacja się udała.

### Linia 13

bash

```bash
fi
```

Kończy wewnętrzną instrukcję warunkową `if`.

W Bashu każda instrukcja `if` musi zostać zamknięta słowem `fi`.

### Linia 14

bash

```bash
fi
```

Kończy zewnętrzną instrukcję warunkową, która sprawdzała, czy Docker działa.

### Linia 15

bash

```bash
exit 0
```

Kończy skrypt kodem `0`, czyli informacją, że wykonanie zakończyło się poprawnie.

## 3. Schemat działania skryptu

Spójrz na poniższy schemat. Pokazuje on całą logikę programu:

START SKRYPTU

Sprawdź status Dockera

Czy Docker działa?

TAKDocker działa poprawnie

exit 0

NIESpróbuj uruchomić Docker

Czy uruchomienie się udało?

TAKSukces

exit 0

NIEBłąd

exit 1

## 4. Przykładowe rezultaty działania

Przypadek 1: Docker już działa

text

```text
Sprawdzam status usługi Docker...
Docker działa poprawnie.
```

Przypadek 2: Docker nie działa, ale udało się go uruchomić

text

```text
Sprawdzam status usługi Docker...
Docker nie działa. Próbuję uruchomić usługę...
Docker został pomyślnie uruchomiony.
```

Przypadek 3: Nie udało się uruchomić Dockera

text

```text
Sprawdzam status usługi Docker...
Docker nie działa. Próbuję uruchomić usługę...
BŁĄD: Nie udało się uruchomić Dockera.
```

## 5. Co warto zapamiętać z Bash?

| Element | Znaczenie |
| --- | --- |
| `#!/bin/bash` | Wskazuje interpreter |
| `echo` | Wyświetla tekst |
| `SERVICE="docker"` | Tworzy zmienną |
| `$SERVICE` | Odczytuje zmienną |
| `if` | Rozpoczyna warunek |
| `then` | Wykonaj, jeśli warunek jest prawdziwy |
| `else` | W przeciwnym razie |
| `fi` | Kończy warunek |
| `sudo` | Uruchamia polecenie z uprawnieniami administratora |
| `exit 0` | Zakończenie sukcesem |
| `exit 1` | Zakończenie błędem |

Mała wskazówka na koniec: Warto samodzielnie zmodyfikować zmienną `SERVICE` i sprawdzić, jak zachowa się skrypt dla innej usługi, np. `ssh`. To bardzo dobry sposób na naukę zmiennych i instrukcji warunkowych w Bashu.