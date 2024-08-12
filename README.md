## Bot di Supporto per "Il Tempo della Spada"

Gli script contenuti in questa cartella implementano quattro funzionalità utili per il GdR "Il Tempo della Spada":
 - Lancio dei dadi, con risoluzione dei successi (da bot Discord)
 - Generazione di nomi medioevali (da bot Discord o direttamente da `namegen.py`)
 - Generazione di personaggi casuali (da bot Discord o usando i due script `itdschargen.py` e `pdffields.py`)
 - Generazione guidata di personaggi (da bot Discord o usando i due script `itdschargen.py` e `pdffields.py`)

### Installazione
L'installazione non è, purtroppo, del tutto elementare.
Innanzitutto è necessario avere installato [Redis](https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/), disponibile sia per Linux che per MacOS. Per Windows, invece, sarà necessario installare il database tramite **WSL**. In questo caso è possibile utilizzare il bot direttamente dalla macchina virtuale seguendo le istruzioni per Linux.  
In un ambiente Linux con Python 3.10, dovrebbe essere sufficiente eseguire lo script `install.sh`.
Con un po' di fortuna, le stesse cose potrebbero funzionare anche su altri sistemi operativi compatibili con lo standard POSIX.

### Esecuzione

#### Bot Discord
 - Per il bot Discord, bisogna quindi procurarsi un token dal Discord Developer Portal e inserirlo in `config.py`
 - Dopodiché, è sufficiente eseguire il comando `./rundiscord.py`
 - Il bot dispone di un suo help, ottenibile con `!h`
 - Il bot permette di creare e gestire i personaggi a più utenti in contemporanea.

#### Script singoli
 - Una volta completata l'installazione, è anche possibile eseguire i singoli script.
 - Attivare preliminarmente l'ambiente virtuale con `. ./venv/bin/activate`
 - `namegen.py` dispone di un help abbastanza completo, ottenibile con `./namegen.py --help`
 - La generazione di personaggi casuali si ottiene con `./itdschargen.py r`. Lo script produce un file testuale nella cartella `json` con nome uguale al nome del personaggio, più l'estensione `.json`. Questo può essere convertito in PDF con `./pdffields.py json/{nome del personaggio}.json`
 - Per la creazione guidata, la procedura è identica, ma va omesso il parametro `r` nell'invocazione di `./itdschargen`
 
### Note
 - La generazione di PDF si basa su pypdf, che ha qualche problema -- ho prodotto una patch che viene installata automaticamente nell'ambiente virtuale.
 
### Funzionalità aggiunte
 - Processo di creazione dei personaggi guidato, sfruttando elementi come bottoni e menù a tendina che permettono
 di selezionare le opzioni senza doverle scrivere a mano. Per scelte come le informazioni di base del personaggio
 viene utilizzato un form che permette di inserire con un'unica interazione tutte le info necessarie. Rimane comunque compatibile
 la selezione delle scelte tramite messaggio semplice, con la differenza che nel caso di scelte multiple le le opzioni
 selezionate vanno separate con `, ` (virgola spazio)
 - Salvataggio dei personaggi persistente tramite Redis. Alcuni dati usati per la connessione al database sono definiti in `config.py`, pertanto è consigliabile cancellare e rigenerare il file tramite `install.sh` o aggiornarlo con i dati necessari.
### TODO
Idee per estensioni, divise per argomento.

#### Funzionalità del generatore
Nuove funzionalità o miglioramenti e feature mancanti per il generatore di personaggi

 - Gestire l'equipaggiamento consentendo la scelta dei pregi associati alla qualità degli oggetti
 - Gestire l'equipaggiamento in funzione dell'epoca
 - Gestire l'avanzamento (e talenti e ordini)
 - Armonizzare la generazione dei nomi con quella del personaggio (soprattutto dal punto di vista della professione)
 - Generare gli eventi in funzione della professione

#### Supporto bot/hosting/etc.
Funzionalità necessarie per consentire l'hosting del bot ed il suo corretto funzionamento

 - Verificare il corretto funzionamento della creazione contemporanea da più giocatori/magistri.
 - Generare la scheda in un formato diverso se `pypdf` non funziona (banalmente in formato testuale?), eseguendo la verifica in modo automatico (tentando di creare un PG casuale subito dopo l'installazione).
 - Sanitizzare l'input dal bot, in particolare le stringhe di testo libero.
 - Non memorizzare permanentemente i pdf. Consentire agli utenti di scaricare la scheda in json in modo da limitare la necessità di mantenere i file (per limitare lo spazio impiegato dal bot). In alternativa, si potrebbero ricaricare i personaggi dal PDF (più complicato, ma credo fattibile).

#### Portabilità e facilità di installazione
Modifiche per semplificare l'installazione

 - Verificare funzionalità sotto Windows e MacOS
 - Quasi sicuramente sotto Windows ci saranno da fare piccoli aggiustamenti, in primis usare le primitive portabili di os.path
 - Comprendere la natura del problema nella scheda e, se è il caso, fare un bug report per `pypdf` con un MVE
 - Generare dei test di unità e integrazione
 
