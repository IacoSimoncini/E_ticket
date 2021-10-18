# Progetto Software Cybersecurity

## Pre-Requisiti
+ Python 3.9.1
+ Web3 5.23.1
+ Pillow 8.3.2
+ Django 3.2.7


## Avvio

Per avviare la Blockchain: 
Linux: avviare lo script ```./start.sh``` all'interno della cartella 3-nodes-quickstart (su Linux).
Windows: Per utenti Windows aprire Docker, entrare dentro WSL e ripetere la procedura sovrastante.

Per avviare il server eseguire questo comando

```bash
python manage.py runserver
```

## Interazioni

Per utilizzare l'applicazione web con privilegi superiori a quelli dell'utente di tipo cliente si possono utilizzare i profili qui messi a disposizione. Profili di tipo cliente si possono creare in ogni momento tramite la pagina di registrazione.
Per muoversi all'interno del sito si possono premere i vari bottoni che permettono di accedere alle pagine preposte allo svolgimento delle varie operazioni richieste. Inoltre sono presenti due bottoni speciali (uno giallo con la scritta "E_Ticket" in alto a sinistra e uno blu col nome dell'utente in alto a destra) che a seconda del tipo di utente permettono di accedere a diffferenti pagine.

Questi sono i livelli di utente presenti nell'applicazione web:

### Amministratore 

Credenziali d'accesso:
utente: admin
password: admin

può creare eliminare o modificare eventi


Sia il bottone giallo che il bottone blu permettono di accedere alla home page dell'admin dove può creare, modificare o eliminare un evento

### Reseller

Credenziali d'accesso:
utente: reseller
password: resel123

può invalidare i biglietti


Sia il bottone giallo che il bottone blu permettono di accedere alla home page del reseller dove può invalidare il biglietto

### Cliente

può comprare o chiedere il rimborso dei biglietti

Il bottone giallo permette di accedere alla home page dell'utente dove può acquistare dei biglietti
Il bottone blu permette di accedere alla pagina contenente la lista degli eventi per i quali l'utente ha comprato il biglietto, da qui potrà vedere i biglietti acquisiti per un evento e, se lo desidera, richiedere il rimborso


## Personalizzazione del sito

Nel caso in cui si vogliano effettuare delle modifiche all'applicazione web, in special modo nella struttura del database, vengono qui lasciati i comandi per effettuare la migrazione

```bash
python manage.py makemigrations
python manage.py migrate
```


## Autori

### Carletti Nicola  
email: s1101135@studenti.univpm.it
### Martino Pio Enrico  
email: s1102862@studenti.univpm.it
### Mezzotero Giulio  
email: s1101006@studenti.univpm.it
### Simoncini Iacopo  
email: s1102874@studenti.univpm.it
### Talento Francesco 
email: s1102540@studenti.univpm.it
