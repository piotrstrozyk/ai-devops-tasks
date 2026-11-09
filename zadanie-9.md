### YAML

services:
  web:
    image: nginx
    ports:
      - "80:80"
  app:
    build: .
    ports
      - "3000:3000"
    depends_on:
      - db
  db:
    image: postgres
    environment:
      POSTGRES_PASSWORD=password

Nie, ten YAML zawiera jeden błąd składniowy.

W sekcji `app` brakuje dwukropka (`:`) po `ports`.

### Błędny fragment

yaml

```yaml
    ports
      - "3000:3000"
```

### Poprawiona wersja

yaml

```yaml

services:
  web:
    image: nginx
    ports:
      - "80:80"

  app:
    build: .
    ports:
      - "3000:3000"
    depends_on:
      - db

  db:
    image: postgres
    environment:
      POSTGRES_PASSWORD: password
```

Poprawny YAML### Dodatkowe uwagi

1. `ports:` musi kończyć się dwukropkiem.
2. Wcięcia są istotne – YAML używa ich do określania struktury.
3. `depends_on: - db` określa zależność aplikacji od kontenera bazy danych.
4. `POSTGRES_PASSWORD` jest poprawnie zapisane jako zmienna środowiskowa.

Ważne: `depends_on` domyślnie nie gwarantuje, że PostgreSQL będzie już gotowy do przyjmowania połączeń, a jedynie określa kolejność uruchamiania kontenerów.

Możesz też sprawdzić plik poleceniem:

bash

```bash
docker compose config
```

Jeśli konfiguracja jest poprawna, Docker Compose wyświetli jej znormalizowaną wersję.