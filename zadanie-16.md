Na podstawie przedstawionego przykładu można wskazać następujące główne różnice między Bash a PowerShell:

## 1. Deklarowanie zmiennych

- Bash: zmienne deklaruje się bez znaku `$` po lewej stronie przypisania.
- PowerShell: zmienne zawsze poprzedza się znakiem `$`.

bash

```bash
DB_NAME="app_database"
```

powershell

```powershell
$DB_NAME = "app_database"
```

## 2. Pobieranie aktualnej daty

- Bash: wykorzystuje polecenie `date`.
- PowerShell: wykorzystuje polecenie `Get-Date` z parametrem `-Format`.

bash

```bash
DATE=$(date +%Y%m%d_%H%M%S)
```

powershell

```powershell
$DATE = Get-Date -Format "yyyyMMdd_HHmmss"
```

## 3. Operacje na katalogach

- Bash: wykorzystuje polecenia `mkdir -p` oraz test `-d`.
- PowerShell: wykorzystuje `New-Item` i `Test-Path`.

bash

```bash
if [ ! -d "$BACKUP_DIR" ]; then
    mkdir -p "$BACKUP_DIR"
fi
```

powershell

```powershell
if (-not (Test-Path -Path $BACKUP_DIR -PathType Container)) {
    New-Item -ItemType Directory -Path $BACKUP_DIR -Force
}
```

## 4. Wyświetlanie komunikatów

- Bash: używa polecenia `echo`.
- PowerShell: używa najczęściej `Write-Host` do wyświetlania komunikatów.

bash

```bash
echo "Rozpoczynam backup..."
```

powershell

```powershell
Write-Host "Rozpoczynam backup..."
```

## 5. Łączenie ścieżek i zmiennych

- Bash: często wykorzystuje konkatenację tekstu i zmienne w nawiasach klamrowych `${}`.
- PowerShell: umożliwia interpolację zmiennych w ciągach znaków oraz korzystanie z `Join-Path`.

bash

```bash
FILENAME="${BACKUP_DIR}/${DB_NAME}_${DATE}.sql.gz"
```

powershell

```powershell
$FILENAME = Join-Path $BACKUP_DIR "${DB_NAME}_${DATE}.sql.gz"
```

## 6. Uruchamianie zewnętrznych programów

Oba języki mogą uruchamiać programy systemowe, np. `mysqldump` i `gzip`.

- Bash: polecenia można łączyć za pomocą potoku `|`.
- PowerShell: również obsługuje potoki, ale przekazuje nimi obiekty .NET, a nie wyłącznie strumienie tekstowe lub bajtowe.

bash

```bash
mysqldump -u root -p "$DB_NAME" | gzip > "$FILENAME"
```

powershell

```powershell
$dump = & mysqldump -u root -p $DB_NAME
$dump | gzip -c > $FILENAME
```

## 7. Obsługa błędów i kodów zakończenia

- Bash: wykorzystuje `$?` do sprawdzania kodu zakończenia ostatniego polecenia.
- PowerShell: wykorzystuje `$LASTEXITCODE` do sprawdzania kodu zakończenia zewnętrznego programu.

bash

```bash
if [ $? -eq 0 ]; then
    echo "Sukces"
else
    exit 1
fi
```

powershell

```powershell
if ($LASTEXITCODE -eq 0) {
    Write-Host "Sukces"
}
else {
    exit 1
}
```

PowerShell oferuje również mechanizm wyjątków `try/catch`, który ułatwia obsługę błędów.

## 8. Tworzenie i obsługa potoków

- Bash: potoki przekazują dane między procesami za pomocą standardowego wejścia i wyjścia.
- PowerShell: potoki domyślnie przekazują obiekty PowerShell, co może wymagać dodatkowej uwagi przy współpracy z programami zewnętrznymi.

## 9. Obsługa ścieżek

- Bash: standardowo stosuje ukośniki `/`, np. `/var/backups/db`.
- PowerShell: w Windows standardowo stosuje ścieżki z ukośnikami odwrotnymi `\`, np. `C:\Backups\db`.

## Podsumowanie

| Obszar | Bash | PowerShell |
| --- | --- | --- |
| Zmienne | `$NAZWA` | `$NAZWA` |
| Przypisanie | `=` bez spacji jest typowe | `=` ze spacjami jest typowe |
| Data | `date` | `Get-Date` |
| Katalogi | `mkdir -p` | `New-Item` |
| Sprawdzanie katalogu | `-d` | `Test-Path` |
| Komunikaty | `echo` | `Write-Host` |
| Kody błędów | `$?` | `$LASTEXITCODE` |
| Obsługa wyjątków | `if`, `trap` | `try/catch` |
| Ścieżki Windows | `/` lub zależnie od środowiska | `\` |
| Potoki | Strumienie danych | Obiekty PowerShell |

Najważniejszy wniosek: Bash jest przede wszystkim powłoką opartą na poleceniach i strumieniach tekstowych, natomiast PowerShell jest powłoką obiektową, która dodatkowo oferuje rozbudowane mechanizmy automatyzacji i obsługi błędów. Dzięki temu PowerShell jest szczególnie dobrze przystosowany do administracji systemami Windows.