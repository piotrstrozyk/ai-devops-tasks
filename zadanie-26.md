W przedstawionym `Jenkinsfile` znajdują się 4 główne problemy, w tym jeden błąd składniowy, który uniemożliwi poprawne wykonanie pipeline'u, oraz błędy związane z poleceniami npm i Dockerem.

## 1. Zidentyfikowane błędy

| Miejsce | Problem | Rozwiązanie |
| --- | --- | --- |
| `stesp` | Literówka w nazwie sekcji | Zmiana na `steps` |
| `npm build` | Nieprawidłowe polecenie npm | Zmiana na `npm run build` |
| `docker push myapp:latest` | Niespójność tagowania obrazu | Jawne oznaczenie obrazu tagiem `latest` podczas budowania |
| `when { branch 'master' }` | Warunek działa tylko w odpowiednim kontekście SCM, np. Multibranch Pipeline | Upewnienie się, że pipeline korzysta z Multibranch Pipeline i sprawdzanie właściwej nazwy gałęzi |

Dodatkowo warto zamienić `npm install` na `npm ci`, jeśli projekt posiada plik `package-lock.json`. Zapewnia to bardziej powtarzalne instalowanie zależności w środowisku CI.

## 3. Wyjaśnienie wprowadzonych poprawek

1. `stesp` → `steps`

Oryginalny kod zawierał literówkę:

groovy

```groovy
stesp {
```

Jenkins oczekuje sekcji `steps`, która definiuje polecenia wykonywane w danym etapie. Literówka powodowała błąd interpretacji pipeline'u.

2. `npm build` → `npm run build`

Polecenie:

bash

```bash
npm build
```

nie uruchamia standardowego skryptu `build` z pliku `package.json`.

Prawidłowa forma to:

bash

```bash
npm run build
```

Zakładając, że w `package.json` istnieje odpowiedni skrypt:

json

```json
{
  "scripts": {
    "build": "..."
  }
}
```

3. `docker build` – dodanie tagu `latest`

Oryginalnie:

bash

```bash
docker build -t myapp .
```

Poprawiona wersja:

bash

```bash
docker build -t myapp:latest .
```

Jawnie określamy tag obrazu. Dzięki temu polecenie `docker push myapp:latest` publikuje dokładnie obraz zbudowany w poprzednim kroku.

4. Warunek `when`

Oryginalny warunek:

groovy

```groovy
when {
    branch 'master'
}
```

Jest poprawny składniowo, ale działa w kontekście pipeline'u korzystającego z informacji o gałęzi SCM, typowo Multibranch Pipeline.

Jeżeli Jenkins używa zwykłego Pipeline, warunek może nie działać zgodnie z oczekiwaniami. W takim przypadku należy odpowiednio skonfigurować pobieranie nazwy gałęzi lub zastosować inne sprawdzanie, np. na podstawie zmiennej środowiskowej `BRANCH_NAME` albo `GIT_BRANCH`.

## 4. Dodatkowe zalecenia

W środowisku produkcyjnym warto rozważyć jeszcze:

- Docker Registry: podanie pełnego adresu rejestru, np. `registry.example.com/myapp:latest`.
- Uwierzytelnianie: użycie Jenkins Credentials do bezpiecznego logowania do Docker Registry.
- Kontrola błędów: upewnienie się, że etap Deploy wykonuje się tylko po pomyślnym zakończeniu Build i Test (jest to domyślne zachowanie).
- Wersjonowanie obrazów: zamiast polegać wyłącznie na `latest`, stosowanie tagów opartych na numerze buildu lub identyfikatorze commita.

Podsumowanie: Najważniejsze poprawki to zmiana `stesp` na `steps`, użycie `npm run build` oraz jawne tagowanie obrazu Docker. Dzięki nim pipeline będzie poprawnie budował aplikację, uruchamiał testy i wdrażał obraz tylko dla gałęzi `master` (przy odpowiedniej konfiguracji typu pipeline'u).