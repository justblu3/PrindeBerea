# PrindeBerea
# BeerBot v9 (Edge Catching Edition)

Un bot automatizat scris în Python care prinde obiecte (beri) într-un joc folosind recunoașterea imaginilor (`pyautogui`).

Botul folosește logica **"Edge Catching"**: nu se centrează perfect pe obiect, ci se mișcă doar atât cât este necesar pentru a prinde obiectul cu marginea lăzii, maximizând astfel eficiența și permițând prinderea mai multor obiecte simultan.

## 📋 Cerințe

Ai nevoie de Python 3 instalat și următoarele librării:

```bash
pip install pyautogui opencv-python pillow
Nota: opencv-python este necesar pentru parametrul confidence!

⚙️ Configurare
Înainte de rulare, deschide fișierul scriptului și modifică clasa Config de la început:

GAME_REGION: Setează coordonatele zonei de joc (X, Y, Width, Height).

RETINA_SCALE:

Pune 2 dacă ești pe macOS (Retina Display).

Pune 1 dacă ești pe Windows/Linux (Standard Display).

Imaginea: Asigură-te că ai un fișier beer.png (crop mic doar cu berea) în același folder cu scriptul.

🚀 Utilizare
Pornește jocul, asigură-te că zona de joc este vizibilă, apoi rulează:

Bash

python beer_bot.py
Botul va porni după 3 secunde. Pentru a opri botul de urgență, du mouse-ul rapid într-un colț al ecranului (Failsafe) sau apasă Ctrl+C în consolă.

🛠️ Cum funcționează
Scanează regiunea definită pentru imaginea beer.png.

Filtrează berile care sunt prea jos (deja pierdute).

Selectează berea cea mai urgentă (cea mai de jos).

Calculează distanța minimă necesară pentru a intersecta lada cu berea (Edge Catching).

Mută mouse-ul instantaneu.
