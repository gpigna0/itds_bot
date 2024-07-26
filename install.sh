mkdir pdf
if [ -z "$(command -v redis-cli)" ] # Controlla se Redis è installato
then
  echo "Errore: redis-cli non trovato. Assicurati di avere installato redis sulla tua macchina"
  exit 127
elif [ "$(redis-cli PING)" != "PONG" ] # Controlla se il server è raggiungibile (redis.service è attivo)
then
  echo "Errore: redis-cli è presente, ma il servizio non è raggiungibile. Assicurati che il servizio di Redis sia attivo"
  exit 1
fi
echo "Se non è già presente creo uno user per accedere al database"
if [ -z "$(redis-cli acl getuser ITDSBOT)" ] # Non è presente lo user ITDSBOT
then
  redis-cli acl setuser ITDSBOT \>itds on \~itds:\* +set +get +del +keys +ping
fi
if [ -s config.py ]
then
	echo "config.py deve contenere un token valido e le informazione del database corrette"
	cat config.py
else
	echo "Creato un config.py senza token e con le info di default per la connessione al database."
  echo "Inserire un token valido e modificare gli altri dati se necessario"
	echo "TOKEN=\"\"" > config.py
  echo "DB_ADDRESS=\"localhost\"" >> config.py
  echo "DB_PORT=6379" >> config.py
  cat config.py
fi
python3.10 -m venv venv
. ./venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
patch ./venv/lib/python3.10/site-packages/pypdf/_writer.py pypdf.patch
deactivate
