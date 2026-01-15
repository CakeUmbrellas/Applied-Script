#!/usr/bin/env python3

import platform
import time 

system = platform.system()

if system == "Windows":
    # Fortsätt med Windows-specifik kod
    print("Windows upptäckt. Scriptet fortsätter..")

elif system == "Linux":
    print("Linux upptäckt. Detta script är avsett för Windows.")
    exit()

elif system == "Darwin":
    print("macOS upptäckt. Detta script är avsett för Windows.")
    exit()

else:
    print(f"Okänt operativsystem ({system}). Detta script är avsett för Windows. Avbryter körning.")
    exit()


# Skriv AV test signaturen baserad på EICAR-testfil, innehållet är helt ofarligt och kommer inte att skada systemet.
eicar_str = "X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*"


with open ("AV-TEST-NOT-DANGEROUS.txt", "w") as f:
    f.write(eicar_str)
    print("Skriver EICAR testsignatur till fil...", end="")

time.sleep(3) #Vänta lite på  AV/EDR respons.
print(" Klar.")

print("Kontrollerar fil för EICAR testsignatur...")
try:
    with open ("AV-TEST-NOT-DANGEROUS.txt", "r") as f:
        file_contents = f.read()

    #Kollar om filen matchar EICAR signaturen
    if file_contents == eicar_str:
        print("Filen innehåller testsignatur, vilket betyder att det inte setts av ditt antivirus eller EDR.")
        input("Tryck RETURN för att avsluta.")

#Exception om filen har flyttats eller tagits bort, dvs. antivirus/EDR fungerar.
except Exception as e:
    print("""Filen kunde inte läsas! 
        Antivirusprogrammet har troligen tagit bort eller satt filen i karantän.
        Ditt antivirus eller EDR verkar fungera samt identifierar kända virussignaturer!
        
        Om du använder Windows Defender och vill verifiera upptäckten:
        
        - Tryck Win+R och skriv eventvwr.msc
        - Öppna Program- och Tjänstloggar
        - Navigera till Microsoft/Windows/Windows Defender/Operational.
        
        I den här loggen bör du se händelse-ID 1116 för upptäckt av skadlig kod och 1117 för antivirus som vidtar åtgärder som karantän eller borttagning.""")
    input("Tryck RETURN för att avsluta.")
