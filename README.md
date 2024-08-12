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
 - Per creare nuovi personaggi e gestire quelli esistenti basta usare `itdschargen.py`, anch'esso dotato di un help che descrive tutte le possibili operazioni.
 - Il compito di generare le schede personaggio e importare i personaggi è svolto da `pdffields.py`, con i comandi `--esporta` e `--importa`, documentati nello help
 
### Note
 - La generazione di PDF si basa su pypdf, che ha qualche problema -- ho prodotto una patch che viene installata automaticamente nell'ambiente virtuale.
 
### Funzionalità aggiunte
 - Processo di creazione dei personaggi guidato, sfruttando elementi come bottoni e menù a tendina che permettono di selezionare le opzioni senza doverle scrivere a mano. Per scelte come le informazioni di base del personaggio viene utilizzato un form che permette di inserire con un'unica interazione tutte le info necessarie. Rimane comunque compatibile la selezione delle scelte tramite messaggio semplice: perché le scelte vengano riconosciute esse devono essere scritte nei seguenti modi:
   - Per scelte singole `Ho scelto: <scelta>`
   - Per scelte multiple `Ho scelto: <scelta 1>, <scelta 2>`

   Al posto di `Ho` sono accettati anche `ho`, `Ha`, `ha`.
 - Salvataggio dei personaggi persistente tramite Redis. Alcuni dati usati per la connessione al database sono definiti in `config.py`, pertanto è consigliabile cancellare e rigenerare il file tramite `install.sh` o aggiornarlo con i dati necessari.
 - Il durante la creazione viene controllato che il nome del personaggio contenga solo lettere, numeri, spazi o apostrofi. Vengono accettate anche diverse lettere accentate.
 - In fase di installazione viene testato il corretto funzionamento di pypdf. Se ci sono errori un flag in `config.py` fa sì che le schede vengano generate usando file in formato testuale.
 - Per l'importazione possono essere usati tutti e due i formati: come gestire l'operazione è deciso sulla base dell'estensione contenuta nel path del file (.pdf o .txt). Le informazioni per importare il personaggio sono contenute in un apposito campo nei metadati del pdf e nell'ultima parte della scheda txt.
 - I personaggi sono salvati sul database. Quando viene creata una scheda per l'esportazione, essa viene cancellata dopo l'invio sul server. Quando si usa lo script singolo la scheda rimane salvata nella directory `pdf`. Anche le schede usate per l'importazione vengono eliminate dopo l'utilizzo dal bot.

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

 - Sanitizzare l'input dal bot, in particolare le stringhe di testo libero.

#### Portabilità e facilità di installazione
Modifiche per semplificare l'installazione

 - Verificare funzionalità sotto Windows e MacOS
 - Quasi sicuramente sotto Windows ci saranno da fare piccoli aggiustamenti, in primis usare le primitive portabili di os.path
 - Comprendere la natura del problema nella scheda e, se è il caso, fare un bug report per `pypdf` con un MVE
 - Generare dei test di unità e integrazione
 
