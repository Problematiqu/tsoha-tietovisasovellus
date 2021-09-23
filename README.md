# Tietovisasovellus

Harjoitustyön aiheena on tietovisasovellus.
 
* Tietovisa on kymmenen kysymyksen pituinen, ja siinä on neljä vastausvaihtoehtoa 
* Visaa voi pelata ilman kirjautumista
* Kirjautumalla sisään sovellukseen, se ylläpitää tilastoja käyttäjän tuloksista
* Tuloksia voi katsella käyttäjän profiilista
* Sovelluksessa on myös kaikkien käyttäjien välinen scoreboard, joka laittaa käyttäjät paremmuusjärjestykseen tulosten perusteella
* Ylläpitäjä voi lisätä ja poistaa kysymyksiä kysymyspankkiin

## Välipalautus 2 

Sovelluksen ominaisuudet ovat hyvällä mallilla, melkein kaikki on jo tehtynä. Ulkoasussa on vielä paljon tekemistä, sekä käyttökokemuksen parantamisessa. 

Sovellusta pääsee testamaan täällä: https://tsoha-tietovisailu.herokuapp.com/

### Puuttuvat ominaisuudet
* Kysymysten lisäämisen ja poistamisen toiminnallisuus

### Keskeneräiset työt
* Refaktorointi niin, että tietokantakomennot omassa moduulissaan 
* Ulkoasu on keskeneräinen, ja on pelkkä pohja tällä hetkellä 
* Virheidenkäsittely ei ole vielä valmis 
* Infoviestien lähettäminen käyttäjälle on vaiheessa. Esimerkiksi onnistuneen rekisteröinnin jälkeen ei tapahdu mitään
* Mahdollinen divide by zero ongelma tietokannassa, jos käyttäjä ei ole saanut yhtään vastausta oikein, ja menee katsomaan scoreboardia
* Käyttäjä voi karata visasivulta ilman visan tekemistä loppuun tai esimerkiksi päivittää vain sivun uudelleen parempien kysymysten toivossa
* Käyttäjä voi lähettää uudelleen jo kerran tekemänsä visan menemällä selaimen back-ominaisuudella vain takaisin
* Profiilisivun pitäisi näyttää tuloksia, vaikka yhteenkään kysymykseen ei ole vielä vastattu 
* CSRF-estot puuttuvat

