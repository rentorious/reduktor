# Reduktor
## Projekat iz praktične astronomije na Matematičkom fakultetu u Beogradu

### Ovaj projekat je program za redukciju kordinata sa ciljem za što kvalitetnije posmatranje nebeskih tela.

#### Program trenutno podržava:
- Nebesko ekvatorski, mesno ekvatorski i horizontski koordinatni sistem kao i prelaske sa bilo kog na bilo koji
- Prelazak za geocentričnih na topocentrične koordinate, kao i obrnut prelaz
- Uticaj nutacije na koordinate
- Uticaj precesije na koordinate

#### Pokretanje koda:
1. git clone https://github.com/rentorious/reduktor.git
2. cd reduktor
3. python3 -m venv reduktor
4. source reduktor/bin/activate
5. pip install -r requirements.txt
6. export FLASK_APP=reduktor
7. flask run