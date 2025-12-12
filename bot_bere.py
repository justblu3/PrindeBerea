import pyautogui
import time
import sys

# === CONFIGURARE BOT ===

class Config:
    # Coordonatele regiunii de joc (X, Y, Width, Height)
    GAME_REGION = (936, 1000, 954, 700)
    
    # Imaginea de căutat
    IMAGE_PATH = 'beer.png'
    
    # Setări detecție vizuală
    CONFIDENCE_LEVEL = 0.5
    GRAYSCALE = True
    
    # Setări fizică ladă (Cât de "lacomă" este)
    # 1.3 înseamnă că prindem berea și dacă e puțin în afara centrului lăzii
    RAZA_SIGURA_MULTIPLICATOR = 1.30
    
    # Limita de jos (ignorăm berile care sunt prea aproape de fundul ecranului)
    OFFSET_LIMITA_JOS = 50
    DEADLINE_Y = GAME_REGION[1] + GAME_REGION[3] - OFFSET_LIMITA_JOS
    
    # Factor scalare pentru ecrane Retina (Mac). Pune 1 pentru Windows standard.
    RETINA_SCALE = 2 

# === CLASA PRINCIPALĂ ===

class BeerBot:
    def __init__(self):
        self.running = True
        self._setup_pyautogui()
        
    def _setup_pyautogui(self):
        """Configurează setările de bază pentru pyautogui."""
        pyautogui.PAUSE = 0
        pyautogui.FAILSAFE = True
        print("--- BOT BERE v9 (Edge Catching Refactored) ---")
        print(f"Regiune: {Config.GAME_REGION}")
        print("Mă mișc minimul necesar. Prind și cu marginea.")
        print("Pornesc în 3 secunde... (Apasa Ctrl+C pentru stop)")
        time.sleep(3)

    def get_mouse_x(self):
        """Returnează poziția X a mouse-ului."""
        return pyautogui.position().x

    def calculate_logic_coords(self, box):
        """
        Transformă coordonatele pixelilor în coordonate logice 
        (necesar pentru ecrane Retina/HighDPI).
        """
        width = box.width / Config.RETINA_SCALE
        left = box.left / Config.RETINA_SCALE
        center_x = left + (width / 2)
        return center_x, width

    def scan_screen(self):
        """Caută toate instanțele imaginii pe ecran."""
        try:
            return list(pyautogui.locateAllOnScreen(
                Config.IMAGE_PATH,
                region=Config.GAME_REGION,
                confidence=Config.CONFIDENCE_LEVEL,
                grayscale=Config.GRAYSCALE
            ))
        except pyautogui.ImageNotFoundException:
            return []
        except Exception as e:
            # Opțional: print(f"Eroare la scanare: {e}")
            return []

    def run(self):
        """Bucla principală a botului."""
        try:
            while self.running:
                berile = self.scan_screen()
                
                if not berile:
                    continue

                # 1. Filtrare: Păstrăm doar berile care sunt deasupra liniei de deadline
                berile_prindibile = [b for b in berile if b.top < Config.DEADLINE_Y]

                if not berile_prindibile:
                    continue

                # 2. Prioritizare: Alegem berea cea mai de jos (cea mai urgentă)
                tinta = max(berile_prindibile, key=lambda b: b.top)

                # 3. Calcule Geometrice
                bere_x, latime_bere = self.calculate_logic_coords(tinta)
                mouse_x = self.get_mouse_x()
                
                # Cât de departe poate fi berea față de centru lăzii?
                limita_distanta = latime_bere * Config.RAZA_SIGURA_MULTIPLICATOR
                diferenta = bere_x - mouse_x

                current_y = pyautogui.position().y
                target_x = None

                # 4. Logica de Mișcare Minimă (Edge Catching)
                if diferenta > limita_distanta:
                    # Berea e prea în DREAPTA -> Ne ducem spre dreapta
                    target_x = bere_x - limita_distanta
                    
                elif diferenta < -limita_distanta:
                    # Berea e prea în STÂNGA -> Ne ducem spre stânga
                    target_x = bere_x + limita_distanta

                # Dacă target_x a fost setat, ne mișcăm. Altfel, stăm pe loc (zona sigură).
                if target_x is not None:
                    pyautogui.moveTo(target_x, current_y, duration=0)

        except KeyboardInterrupt:
            print('\n[STOP] Bot oprit manual de utilizator.')
            sys.exit()

# === PUNCT DE INTRARE ===

if __name__ == "__main__":
    bot = BeerBot()
    bot.run()