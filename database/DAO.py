from database.DB_connect import DBConnect
from model.cliente import Cliente


"""
CHINOOK: GENERI E CLIENTI

Si consideri il database "Chinook", contenente informazioni, fra le altre cose,
su generi musicali (genre), brani (track), fatture (invoice) e righe di fattura
(invoiceline). Ogni brano appartiene a un genere, ogni riga di fattura si
riferisce a un brano e ogni fattura e' intestata a un cliente.
Si intende costruire un'applicazione che permetta di analizzare le relazioni tra
generi musicali in base ai clienti che li hanno acquistati.

PUNTO 1
a. L'utente inserisce in un campo di testo un numero minimo di brani venduti x.

b. Premendo "Crea grafo", l'applicazione costruisce un grafo semplice, non
   orientato e pesato. I vertici sono i generi di cui sono stati venduti almeno
   x brani, cioe' quelli per cui la somma del campo Quantity delle righe di
   fattura relative ai brani di quel genere e' maggiore o uguale a x.
   SUGGERIMENTO. Per ogni genere puo' risultare conveniente aggiungere alla
   relativa classe il numero di brani venduti e l'insieme dei clienti che hanno
   acquistato almeno un brano di quel genere.

c. Esiste un arco tra due generi distinti G1 e G2 se almeno un cliente ha
   acquistato brani di entrambi. Il peso dell'arco e' il numero di clienti
   distinti che hanno acquistato brani di entrambi i generi. Costruito il
   grafo, l'applicazione visualizza il numero di vertici e di archi.

d. L'utente seleziona da un menu a tendina uno dei generi presenti nel grafo.
   Alla pressione del bottone "Generi adiacenti", l'applicazione stampa
   l'elenco dei generi adiacenti a quello selezionato con il peso dell'arco
   corrispondente, in ordine decrescente di peso e, a parita' di peso, in
   ordine alfabetico.

PUNTO 2
Partendo dal grafo del punto precedente, alla pressione del bottone "Percorso"
si implementi una procedura ricorsiva che calcoli un percorso di peso massimo
con queste caratteristiche:
- il punto di partenza e' il genere selezionato al punto 1.d;
- ogni vertice puo' comparire una sola volta;
- il peso degli archi nel percorso deve essere strettamente decrescente.
Al termine della ricerca si stampino l'elenco dei vertici, i pesi degli archi
incontrati e il peso totale del percorso ottimo.

Tutti i possibili errori di immissione, validazione dati, accesso al database
ed algoritmici devono essere gestiti; non sono ammesse eccezioni generate dal
programma.

VALORI DI CONTROLLO
Punto 1
- x = 1:   24 vertici, 219 archi
- x = 20:  14 vertici, 89 archi
- x = 40:  9 vertici, 36 archi
- x = 100: 4 vertici, 6 archi
- x = 40, generi: Alternative & Punk (244 venduti), Blues (61), Classical (41),
  Jazz (80), Latin (386), Metal (264), R&B/Soul (41), Rock (835), TV Shows (47)
- x = 40, adiacenti di Rock: Latin (56), Metal (55), Alternative & Punk (50),
  Jazz (32), Blues (23), TV Shows (19), R&B/Soul (17), Classical (14)
- x = 40, adiacenti di Jazz: Rock (32), Latin (30), Metal (30),
  Alternative & Punk (27), ...

Punto 2
- x = 40, Rock -> peso totale 211, 9 vertici:
    Rock -> Metal (55) -> Latin (53) -> Alternative & Punk (47) -> Jazz (27)
    -> Blues (12) -> TV Shows (7) -> Classical (6) -> R&B/Soul (4)
- x = 40, Jazz -> peso totale 123, 8 vertici
- x = 40, Classical -> peso totale 14, 2 vertici (Classical -> Rock)
- x = 20, Rock -> peso totale 222, 11 vertici
- x = 20, Latin -> peso totale 224, 11 vertici
- x = 100, Rock -> peso totale 155, 4 vertici
- con x = 1 la ricerca impiega alcuni secondi
"""

class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAnni():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
            return result

        cursor = cnx.cursor(dictionary=True)
        query = """
            SELECT DISTINCT YEAR(InvoiceDate) AS anno
            FROM invoice
            ORDER BY anno
        """
        cursor.execute(query)
        for row in cursor:
            result.append(row["anno"])
        cursor.close()
        cnx.close()
        return result

    @staticmethod
    def getNodi(annoDa, annoA):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
            return result

        cursor = cnx.cursor(dictionary=True)
        query = """
            SELECT c.CustomerId AS id, c.FirstName AS nome, c.LastName AS cognome,
                   c.Country AS paese, SUM(i.Total) AS spesa
            FROM invoice i, customer c
            WHERE i.CustomerId = c.CustomerId
              AND YEAR(i.InvoiceDate) BETWEEN %s AND %s
            GROUP BY c.CustomerId, c.FirstName, c.LastName, c.Country
        """
        cursor.execute(query, (annoDa, annoA))
        for row in cursor:
            result.append(Cliente(row["id"], row["nome"], row["cognome"],
                                  row["paese"], float(row["spesa"])))
        cursor.close()
        cnx.close()
        return result

    @staticmethod
    def getArtistiClienti(annoDa, annoA):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
            return result

        cursor = cnx.cursor(dictionary=True)
        query = """
            SELECT DISTINCT i.CustomerId AS idCliente, a.ArtistId AS idArtista
            FROM invoice i, invoiceline il, track t, album a
            WHERE i.InvoiceId = il.InvoiceId
              AND il.TrackId = t.TrackId
              AND t.AlbumId = a.AlbumId
              AND YEAR(i.InvoiceDate) BETWEEN %s AND %s
        """
        cursor.execute(query, (annoDa, annoA))
        for row in cursor:
            result.append((row["idCliente"], row["idArtista"]))
        cursor.close()
        cnx.close()
        return result