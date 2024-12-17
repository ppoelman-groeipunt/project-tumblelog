# Flask-WTF

Flask-WTF is een **extensie voor Flask** die de integratie van webformulieren (Web Template Forms) in een Flask-app vereenvoudigt.

- HTML-formulieren definiëren in Python-klassen.
- Gebruikersinvoer valideren.
- CSRF-beveiliging toevoegen aan een webapplicatie.


## 1. Webformulieren definiëren in klassen

(zie `forms.py`)

## 2. Validatie

Flask-WTF ondersteunt ingebouwde validatieregels, zoals verplichte velden, lengtebeperkingen, e-mailvalidatie en meer.
Bij fouten in validatie kunnen duidelijke foutmeldingen worden weergegeven aan de gebruiker.

De methode `validate_on_submit()` in Flask-WTF combineert twee belangrijke acties om formulieren te verwerken en te valideren:

1. Controleren of het formulier via een POST-verzoek is verzonden.
2. Valideren van het formulier op basis van de opgegeven validatieregels.

Als beide voorwaarden waar zijn, retourneert deze methode **True**. Als een van de twee niet waar is, retourneert het **False**.

**Validate met Flask-WTF gebeurt webserver-side (niet in de browser), maar wel voordat de databaseserver bereikt wordt.**

Dit betekent dat de validatie plaatsvindt nadat de gebruiker het formulier heeft ingediend en 
de gegevens naar de server zijn verzonden.
De gebruiker moet dus wachten op een server-actie om te weten of invoer geldig is.
Dit is veiliger omdat de server niet omzeild kan worden.

Dit betekent niet dat je de validatieregels op database-niveau kunt versoepelen.
Als er een bug in je applicatielogica zit kan foutieve of inconsistente data in de database terechtkomen.

## 3. CSRF-beveiliging

CSRF (Cross-Site Request Forgery) is een aanval waarbij een kwaadwillende een gebruiker misleidt om onbedoeld 
een actie uit te voeren op een website waarop hij is ingelogd, door een vervalst verzoek uit te lokken.

https://www.techdepot.nl/cross-site-request-forgery-csrf/

### Hoe werk CSRF-beveiliging?

- Bij het renderen van een formulier (GET) genereert Flask-WTF een CSRF-token.
- Dit token wordt opgeslagen in de sessie van de gebruiker (server-side) en toegevoegd als een verborgen veld 
in het formulier via `{{ form.hidden_tag() }}`.
- Wanneer het ingevulde formulier wordt ingediend (POST), controleert de server of het CSRF-token 
overeenkomt met het token dat in de sessie is opgeslagen. Als dat niet het geval is, wordt het verzoek geweigerd
met een **403 Forbidden** fout.

### Waarom is dit veilig?

Een kwaadwillende kan geen toegang krijgen tot het CSRF-token dat in de sessie van de gebruiker is opgeslagen, omdat:
- Het token alleen in de server en via het formulier beschikbaar is.
- Een derde partij geen token kan genereren dat overeenkomt met wat de server verwacht.

Zelfs als een aanvaller een verzoek naar de server stuurt met cookies, wordt dit verzoek geweigerd 
omdat het ontbrekende of ongeldige CSRF-token wordt gedetecteerd.


