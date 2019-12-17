# Bachelor Scriptie
Dit is een verzameling van alle code en data gebruikt voor het onderzoek
De geannoteerde Google 5-grams zijn te vinden in de map 'Annotated Data'.
Om deze te gebruiken, dienen ze eerst uitgepakt te worden.

De code die gebruikt is voor het annoteren van de data is te vinden in 5gramannotator.py.

De eerste stap is het uitvoeren van patternchecker.py op de geannoteerde data, om de gezochte patronen in de data te vinden. hiervoor dient het script in dezelfde map aanwezig te zijn als de data (de Google 5-grams). 

Dit script zal de input creëren voor het programma persontagger.py. Dit in de vorm van nieuwe bestanden eindigend op _gender en _animacy.

De laatste stap is het uitvoeren van persontagger.py. Dit script dient hiervoor in dezelfde map te staan als de door patterchecker.py gecreëerde bestanden. 

Bron Krantenartikelen: Algemeen Dagblad
