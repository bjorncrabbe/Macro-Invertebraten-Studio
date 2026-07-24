# Macro-Invertebraten Studio

Macro-Invertebraten Studio is een Python-applicatie voor het verwerken, herkennen
en determineren van aquatische macro-invertebraten.

Het project combineert beeldherkenning met interactieve determinatiesleutels om
de identificatie van macro-invertebraten te ondersteunen.

> **Status:** Dit project is momenteel in actieve ontwikkeling.

## Doel van het project

Het doel van Macro-Invertebraten Studio is om een praktische desktopapplicatie
te ontwikkelen waarmee macro-invertebraten op een gestructureerde manier kunnen
worden onderzocht en gedetermineerd.

De applicatie combineert:

- AI-gebaseerde beeldherkenning
- interactieve determinatiesleutels
- verwerking van foto's/camerabeelden
- registratie van waarnemingen
- opslag van sessie- en determinatiegegevens
- een grafische gebruikersinterface

## Functionaliteiten

### AI-herkenning

De applicatie bevat een TensorFlow/Keras-model waarmee beelden van
macro-invertebraten kunnen worden geanalyseerd.

Het AI-model geeft een voorspelling van de vermoedelijke groep. Deze informatie
kan vervolgens gebruikt worden om de juiste determinatiesleutel te selecteren.

### Determinatie

Macro-Invertebraten Studio bevat een eigen determination engine.

Determinatiesleutels worden opgeslagen als gegevensbestanden en door de
applicatie ingelezen. De gebruiker wordt vervolgens via vragen en kenmerken
door de determinatie geleid.

Momenteel zijn onder andere determinatiegegevens aanwezig voor groepen zoals:

- Odonata
- Coleoptera
- Diptera
- Ephemeroptera
- Hemiptera
- Hirudinea
- Mollusca
- Oligochaeta
- Plecoptera
- Trichoptera
- Crustacea

De beschikbare sleutels worden verder uitgebreid tijdens de ontwikkeling.

### Grafische interface

De desktopinterface is opgebouwd in Python en bevat onder andere componenten
voor:

- camerabeelden
- determinatie
- sessiebeheer
- staalbeheer
- statusinformatie
- bediening van de applicatie

## Projectstructuur

```text
Macro-Invertebraten-Studio/
│
├── backend/          # Applicatielogica en engines
├── controllers/      # Controllers tussen GUI en backend
├── Data/             # Determinatiesleutels en applicatiegegevens
├── gui/              # Grafische gebruikersinterface
├── test_files/       # Tests en testdata
├── threads/          # Achtergrondtaken
├── Tools/            # Hulpmiddelen voor o.a. Excel/determinatiesleutels
│
├── Main.py           # Startpunt van de applicatie
├── config.py         # Configuratie
├── keras_model.h5    # AI-model
└── labels.txt        # Labels voor het AI-model