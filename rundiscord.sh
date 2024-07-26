if [ -z "$(redis-cli acl getuser ITDSBOT)" ] # Non è presente lo user ITDSBOT
then
  redis-cli acl setuser ITDSBOT \>itds on \~itds:\* +set +get +del +keys +ping
fi
. ./venv/bin/activate
./itdsdiscordbot.py
