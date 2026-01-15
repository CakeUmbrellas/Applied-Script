#!/usr/bin/env python3

import requests
import hashlib
import os

# Läs filen med lösenord
with open('passwords.txt', 'r') as f:
	for line in f:

		# Dela på linjen för att tilldela/skapa  username och password
		username, password = line.strip().split(',')

		# Hasha lösenorder via SHA-1 algoritm
		password_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()

		# Gör en förfrågan till "HaveIBeenPwnd" API för att se om lösenordet har läckts
		response = requests.get(f"https://api.pwnedpasswords.com/range/{password_hash[:5]}")

	#FEATURE1 = Kolla om lösenorden finns i rockyou.txt
		is_in_rockyou = False
		if os.path.exists('/usr/share/wordslists/rockyou.txt.gz'):
			with open('/usr/share/wordslists/rockyou.txt.gz', 'r', encoding='latin-1') as rock_file:
				for rock_line in rock_file:
					if rock_line.strip() == password:
						is_in_rockyou = True
						break
		if is_in_rockyou:
			print(f"Lösenordet för {username} hittades hos rockyou.txt.")



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

# Snyggt jobbat! /Tomas