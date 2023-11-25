# Spam-Detection-Web-App

## Praca Inżynierska

Projekt oraz implementacja aplikacji internetowej do rozpoznawania wiadomości typu spam z systemem wyjaśniania decyzji. Realizacja na potrzeby pracy dyplomowej.

## Uruchomienie Aplikacji

Przed próbą uruchomienia aplikacji należy zainstalować wymagane biblioteki:

```bash
pip install -r requirements.txt
```

Aby uruchomić aplikację należy użyć pliku `run.py`:

```bash
python run.py
```

Po wykonaniu komendy, aplikacja będzie dostępna pod adresem [http://localhost:5000/](http://localhost:5000/).

## System Detekcji Spamu

Projekt zawiera implementację systemu detekcji wiadomości typu spam w języku angielskim na podstawie analizy treści wiadomości. Po uruchomieniu apmikacji, w zakładce "Projekt" znajduje się główna część projektu zawierająca interaktywną przestrzeń do dokonywania klasyfikacji wiadomości. Dzięki algorytmom uczenia maszynowego oraz analizie tekstu, tekst klasyfikowany jest jako HAM lub SPAM przy progu klasyfikacji równym 50%. Aplikacja wprowadza innowacyjny element Explainable AI, który wyjaśnia podjętą przez system decyzję.

#### Modele Klasyfikacyjne

| Model | Accuracy | Precision | Recall | F1 Score |
|-------|----------|-----------|--------|----------|
| MNB   | 95.49%   | 94.66%    | 96.63% | 95.62%   |
| SVC   | 96.77%   | 95.18%    | 98.69% | 96.90%   |
| MLP   | 96.78%   | 95.82%    | 97.98% | 96.88%   |

Implementacja modeli MNB, SVC oraz MLP dostarcza funkcjonalność detekcji spamu. Każdy z modeli został wyuczony w procesie uczenia maszynowego na ponad 33 000 wiadomości pochodzących ze zbioru Enron. Modele klasyfikacyjne oceniono w oparciu o technikę walidacji krzyżowej, uzyskując miary wydajności systemu.

## Funkcjonalności

System wzbogacony został o dodatkowe funkcjonalności. W celu prezentacji działania projektu wprowadzono wersję demonstracyjną znajdującą się w zakładce "Demo". Dzięki stworzeniu konta, użytkownik posiada możliwość do zapisania historii klasyfikacji systemu.



