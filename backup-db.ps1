
# Prosty skrypt do backupu bazy danych

$DB_NAME = "app_database"
$BACKUP_DIR = "C:\Backups\db"
$DATE = Get-Date -Format "yyyyMMdd_HHmmss"
$FILENAME = Join-Path $BACKUP_DIR "${DB_NAME}_${DATE}.sql.gz"

# Sprawdź czy katalog istnieje
if (-not (Test-Path -Path $BACKUP_DIR -PathType Container)) {
    New-Item -ItemType Directory -Path $BACKUP_DIR -Force | Out-Null
    Write-Host "Utworzono katalog $BACKUP_DIR"
}

# Wykonaj backup
Write-Host "Rozpoczynam backup bazy $DB_NAME..."

# Uruchom mysqldump i zapisz wynik do gzip
try {
    $dump = & mysqldump -u root -p $DB_NAME 2>&1

    if ($LASTEXITCODE -ne 0) {
        throw "Błąd podczas wykonywania mysqldump: $dump"
    }

    $dump | gzip -c > $FILENAME

    if ($LASTEXITCODE -ne 0) {
        throw "Błąd podczas kompresji backupu."
    }

    Write-Host "Backup zakończony sukcesem: $FILENAME"
}
catch {
    Write-Host "Błąd podczas wykonywania backupu!"
    Write-Host $_
    exit 1
}
