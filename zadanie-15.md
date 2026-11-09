Najlepszym rozwiązaniem będzie zastosowanie obiektu konfiguracyjnego (mapy środowisk) zamiast wielu instrukcji if...else.

Co zostało poprawione?

    Czytelność – zamiast wielu warunków mamy prostą mapę konfiguracji.

    Łatwiejsza rozbudowa – dodanie nowego środowiska wymaga dopisania tylko jednego wpisu.

    Brak powielania kodu – domyślna konfiguracja jest zdefiniowana tylko raz.

    Prostsza obsługa nieznanych środowisk – operator ?? zapewnia konfigurację domyślną.

    Łatwiejsze testowanie – można niezależnie sprawdzać konfigurację każdego środowiska.