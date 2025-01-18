**Projekt: Aplikacja okienkowa do przetwarzania obrazów**

**Opis:**

Aplikacja umożliwia wczytywanie obrazów i ich przetwarzanie z wykorzystaniem interfejsu graficznego (GUI). Obsługiwane funkcje obejmują m.in. konwersję do skali szarości, odwracanie kolorów, regulację saturacji oraz przetwarzanie wielowątkowe. Projekt jest inspirowany narzędziami takimi jak ImageJ i CVIPtools.

**Funkcjonalności:**

-Wczytywanie obrazów: Użytkownik może załadować obraz z dysku.

-Przetwarzanie obrazów:

  --Konwersja do skali szarości (Grayscale).
  
  --Odwracanie kolorów (Invert).
  
  --Regulacja saturacji (Saturation) z suwakiem (0%-200%).

-Podgląd obrazów: Wyświetlanie oryginalnego i przetworzonego obrazu w oknie aplikacji.

-Zapisywanie wyników: Możliwość zapisania przetworzonych obrazów na dysku.

-Przetwarzanie wielowątkowe: Optymalizacja wydajności poprzez równoległe przetwarzanie obrazów.

**Struktura katalogów**
project-folder/
├── main.py                 # Główna aplikacja GUI
├── image_processing.py     # Funkcje przetwarzania obrazu
├── multiprocessing_utils.py # Funkcje wielowątkowości
├── testing.py              # Testowanie przetwarzania obrazu
├── sandbox.py              # Eksperymenty i testy
├── img/                    # Katalog roboczy na segmenty obrazów
├── requirements.txt        # Lista zależności
└── README.md               # Dokumentacja projektu

**main.py** Główny plik aplikacji, który uruchamia GUI.
**image_processing.py** Plik z funkcjami do przetwarzania obrazu, które mogą być używane również w innych miejscach.
**multiprocessing_utils.py** Plik z funkcjami obsługującymi przetwarzanie wielowątkowe.
**testing.py** Plik do testowania funkcji wielowątkowych.
**sandbox.py** Ten plik można użyć do testowania kodu na żywo i eksperymentów, np. z funkcją imgcrop lub szybkimi modyfikacjami.

**Instalacja**

Skopiuj repozytorium:
  git clone <link-do-repozytorium>
  cd project-folder

Zainstaluj wymagane zależności:
Upewnij się, że masz zainstalowanego Pythona (>= 3.7). Następnie wykonaj:
  pip install -r requirements.txt

Uruchom aplikację:
  python main.py

**Wymagania**
-Python 3.7 lub wyższy
-Biblioteki wymienione w requirements.txt

**Technologie użyte w projekcie**
-Tkinter: Tworzenie interfejsu graficznego.
-OpenCV: Przetwarzanie obrazów.
-Pillow: Obsługa obrazów w GUI.
-NumPy: Operacje na danych numerycznych.
-Multiprocessing: Optymalizacja wydajności.

