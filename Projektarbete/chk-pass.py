#!/usr/bin/env python3

import requests
import hashlib

# Läs filen med lösenord
with open('passwords.txt', 'r') as f:
	for line in f:

		# Dela på linjen för att tilldela/skapa  username och password
		username, password = line.strip().split(',')

		# Hasha lösenorder via SHA-1 algoritm
		password_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()

		# Gör en förfrågan till "HaveIBeenPwnd" API för att se om lösenordet har läckts
		response = requests.get(f"https://api.pwnedpasswords.com/range/{password_hash[:5]}")

		# Om responsstatuskoden är 200 betyder det att lösenordet har läckts
		if response.status_code == 200:
			# Få listan med hashes från läckta lösenord som börjar med samma 5 symboler som angivet lösenord
			hashes = [line.split(':') for line in response.text.splitlines()]

			# Kolla om hashen från det angivna lösenordet matchar någon av de som läckts
			for h, count in hashes:
				if password_hash[5:] == h:
					print(f"Lösenordet för {username} har läckts {count} gånger.")
					break
			else:
				print (f"Kunde inte kolla lösenordet för {username}.")
