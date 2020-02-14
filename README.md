# Romrez
Automated room reservation solution at NTNU

# ----------------
# Forberedelse
# ----------------

-----  1. Setter opp AWS for å slippe å ha PCen på 24/7

Gå inn på amazon.com. Opprett bruker på amazon AWS, lag en T2 instance med gratisperiode på 1 år.
Installer nyeste versjon av Ubuntu på den. 
Når det kommer til lagringsplass --> husk å velge maks når du setter opp instance. 


# -- $$$ --
-----  2. Lag en mappe på Pcen, (Linux eller Mac OSX), lagre .pem nøkkel der


# -- $$$ --
-----  3. Gjenbruk SSH tilkoblingen som finnes under fanen "Connect" inne på Amazon Instance Manger

Bare test at det går faktisk an å koble seg til AWSen


# -- $$$ -- 
-----  4. Oppdater linux på AWS

sudo apt get upgrade
sudo apt get update 


# -- $$$ --
-----  5. Installer python3 på AWS 

sudo apt get install python3

Progammet bruker python3, og ikke 2, vil dermed ikke fungere uten dette.


# -- $$$ -- 
-----  6. Kopier repo

Kjør denne kommandoen og erstatt prikkene med en http-adresse av repo
git clone .........


# -- $$$ -- 
-----  7. Installer pip dersom AWSen ikke har det fra før av

sudo apt get install pip
sudo apt get install pip3


# -- $$$ --
-----  8. Koble til requirements.txt filen

enten: 
pip install -r requirements.txt

eller: 
pip3 install -r requirements.txt

-- NB! --> Dersom det dukker opp feilmeldinger, kan det hende fordi Google Chrome er ikke installert på AWSen
	   Installer dermed Google Chrome ved bruk av følgende kommandolinjer:

	   Henter siste versjon av Chrome:
	   wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

	   Installerer Chrome:
	   sudo apt install ./google-chrome-stable_current_amd64.deb


# -- $$$ --
-----  9. Krypter passordet ditt

For at kommandoen skal kunne kjøres må passordet være B64 kryptert.
Gå inn på https://www.base64encode.org
Tast inn passordet ditt der, og kopier ferdig kryptert utgave av det.
Når programmet kjøres må du bruke det som kommer ut som passord. 


# -- $$$ --
-----  10. Koble til Discord for å motta tilbakemeldinger

Lag et chatrom, eller bruk et eksisterende chatrom/server hvor du er admin. Gå deretter inn på instillinger og lag et webhook.
Kopier URLen inn i koden på main.py. Erstatt Webhook Url der. 


# -- $$$ --
-----  11. Endre melding som grupperommet skal bli reservert med

I koden på main.py finn en linje, (nesten helt nederst), "description.send_keys('Bachelor')" og erstatt "Bachelor" teksten med valgfri
tekst. 


# -- $$$ --
-----  12. Sette opp automatisk reservasjon av grupperom

Per nå kjører scriptet kun en gang. Hele poenget med å ha det på en AWS er å kunne ha det kjørendes døgnet rundt uten behov for en 
datamaskin som må stå på hele tiden. 

For å få dette til må følgende gjøres på AWSen:
   1. SSH til AWSen
   2. Kjør følgende kommand:     crontab -e
   3. Les gjerne bruksanvisningen som ligger inne i filen som standard, da den forklarer kodesnutten nedenfor
   4. Lim inn følgende nederst.

	# Mandag
	#2 0 * * 1 python3 ~/book-room/main.py USERNAME PASSWORD S312 S313 09:00 12:30 16:30

	# Tirsdag
	#2 0 * * 2 python3 ~/book-room/main.py USERNAME PASSWORD S312 S313 09:00 12:30 16:30

	# Onsdag
	#2 0 * * 3 python3 ~/book-room/main.py USERNAME PASSWORD S312 S313 09:00 12:30 16:30

	# Torsdag
	#2 0 * * 4 python3 ~/book-room/main.py USERNAME PASSWORD S312 S313 09:00 12:30 16:30

	# Fredag
	#2 0 * * 5 python3 ~/book-room/main.py USERNAME PASSWORD S312 S313 09:00 12:30 16:30
	
	NB! --> fjern "hashtag" før bruk på hver linje. 

   5. Erstatt brukernavn med ntnu brukernavnet
   6. Passord erstattes med en B64 kodet utgave
   7. Det er viktig å passe på at hovedrom og reserverom er nødt til å være i samme bygg!
   8. Velg riktig tidspunkt, og da er du i mål!


# ------------
# Bruk
# ------------

python3 main.py USERNAME B64_PASSWORD ROOM(e.g. S314) BACKUP_ROOM START_TIME FIRST_END_TIME END_TIME



# ------------
# Disclaimer
# ------------

All bruk av dette skriptet er på egen ansvar. Verken forfatter og medforfattere bærer noe form for ansvar og eventuelle/potensielle
konsekvenser som måtte oppstå som følge av bruk av dette skriptet. 

					-------------------------------------
						---------------------
							Enjoy
						---------------------
					-------------------------------------
