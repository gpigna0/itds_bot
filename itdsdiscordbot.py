#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-

__author__ = 'Giampaolo Agosta'
__version__= '1.0'
__doc__ = """Bot per Discord che implementa le seguenti funzioni:
  Generazione guidata o casuale di personaggi e compilazione delle schede PDF
  Generazione casuale di nomi medievaleggianti
  Lancio dei dadi per le prove
"""

# impiega secret come fonte di randomicità se disponibile, altrimenti random (che è solo pseudo-casuale)
try : 
  from secrets import randbelow as rand
  print("Using secrets")
except ImportError : 
  from random import randint
  print("Using random")
  rand = lambda x : randint(0,x-1)

try : from secrets import random as rnd
except ImportError : 
  from random import random as rnd

# gestione dei tiri di dado
def d(n,faces):
  '''Lancio di dadi base
  n     numero di dadi da lanciare
  faces numero di facce del dado
  returns lista di risultati
  '''
  try : return [ rand(faces)+1 for i in range(n) ]
  except TypeError : 
    print(faces,n)
    return [ rand(int(faces))+1 for i in range(int(n)) ]

def choice(l):
  return l[sum(d(1,len(l)))-1]

def d6(n=1):
  '''Lancio di dadi a 6 facce
  n     numero di dadi da lanciare [default 1]
  returns lista di risultati
  '''
  return d(n,6)

def roll_itds(dice=2, extra=0, score=0, skill=0, bonus_penalty=0, difficulty=1):
  '''Lancio di dadi per una prova de Il Tempo della Spada
  dice    numero di dadi a 6 facce [default 2d6]
  extra   numero di dadi extra [default 0] (qui i dadi extra sono da aggiungere al numero base)
  score   punteggio di caratteristica [default non indicato, non verrà calcolato il successo]
  skill   punteggio di abilità [default 0]
  bonus_penalty  successi bonus o penalità [default 0]
  difficulty    difficoltà (al momento non impiegato) [default 1]
  returns   stringa di testo che descrive il risultato
  '''
  r = sorted(d6(dice+extra))  # ordina i risultati in senso crescente
  print(r)
  # Applica il punteggio di abilità in modo da ridurre a 1 più dadi possibile
  r_reduced = []
  i=0
  while skill and i<len(r): 
    if r[i]<=1: 
      r_reduced.append(r[i])
      i+=1
    else :
      r_reduced.append(r[i]-min(r[i]-1,skill))
      skill-=min(r[i]-1,skill)
      i+=1
  r_reduced+=r[i:]
  # due trattamenti separati a seconda che score sia impostato o meno
  drop = []
  if score: 
    # in questo caso, ottimizza il numero di successi
    remaining_extra = extra
    while remaining_extra>0 and sum(r_reduced)>score: # Non scarta in caso in cui il risultato minimo necessario sia già raggiunto
      drop.append(r_reduced[-1])
      r_reduced=r_reduced[:-1]
      remaining_extra-=1
    result = f' tira {dice+extra}d6 {f"vs {score}" if score else ""}: {r} {f"e scarta {drop}" if len(drop) else ""}, ridotti con {skill} punti abilità a {r_reduced}, per un totale di {sum(r_reduced)}'
    successes=r_reduced.count(1)
    success=sum(r_reduced)<=score and successes+1+bonus_penalty>=difficulty
    if success:
      return result+f', ottenendo **{successes+1} successi**'
    else:
      return result+f', ottenendo un fallimento'
  else:
    # in questo caso, ottimizza il risultato totale scartando il massimo numero di dadi possibile
    if extra>0: 
      drop=r_reduced[-extra:]
      r_reduced=r_reduced[:-extra]
    result = f' tira {dice+extra}d6 {f"vs {score}" if score else ""}: {r} {f"e scarta {drop}" if len(drop) else ""} ridotti con {skill} punti abilità a {r_reduced} per un totale di {sum(r_reduced)}'
    successes=r_reduced.count(1)
    return result+f', ottenendo **{successes+1} successi**, se il tiro è inferiore al punteggio di caratteristica'

# Parsing dei messaggi discord che richiedono il tiro di dadi
import re
rg=r"(?P<dice>\d+)d\s*(?P<drop>\d*)(\s*a(?P<skill>\d+)){0,1}(\s*(?P<bonus_sign>\+|\-)(?P<bonus_value>\d+)){0,1}(\s*vs\s*(?P<score>\d+)){0,1}"
rgc=re.compile(rg, re.IGNORECASE)
rb=r"[a-z]+"
rbc=re.compile(rb, re.IGNORECASE)

def parse_and_roll(msg):
  '''Interpreta un messaggio discord che contiene una specifica per il lancio di dadi ed esegue il lancio
  msg      contenuto di un messaggio discord
  returns  stringa di testo che descrive il risultato
  '''
  res = rgc.search(msg) # esegue il match
  if not res : return None # match fallito
  d = res.groupdict() # estrae i dati
  for x in d : # imposta i default
    if not d[x]: d[x]=0
  print(d) 
  return roll_itds(
    dice  = int(d['dice'])-int(d['drop']), # qui rimuove i dadi extra dal totale, poiché roll li considera in automatico
    extra = int(d['drop']), 
    score = int(d['score']), 
    skill = int(d['skill']), 
    bonus_penalty=int(d['bonus_value'])*(-1 if d['bonus_sign']=='-' else 1) # converte il segno +/-
  )


import discord
# Classe per gli input da bottone
class Btn(discord.ui.Button):
    def __init__(self, name: str, author):
        super().__init__(label=name)
        self.author = author
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(content=f"{self.author} ha scelto: {self.label}")


# Funzione per il processo di creazione del personaggio
# Sulla base del prompt matchato da pexpect sceglie
# il tipo di component da utilizzare
async def chargen(msg, process, author, comp_type, response):
    if comp_type==0: # Button
        btn_str = str(response).split("\n").pop() # Estrazione delle scelte
        btn_labels = rbc.findall(btn_str) # Parsing delle scelte
        vw = discord.ui.View() # Costruzione della view
        for b in btn_labels: # Ogni possibilità di scelta viene associata ad un bottone
            vw.add_item(Btn(b, author))
        await msg.channel.send(response, view=vw)
    if comp_type==1: # Text input
        # si limita a inviare la richiesta. L'input viene letto
        # dal messaggio inviato dall'utente
        await msg.channel.send(response)
    if comp_type==2: # Choice menu (ancora da implementare)
        pass


# Il resto dell'applicazione è più o meno adattata da bot.py
import pexpect
from itdschargen import creazione
import namegen

# setup di discord
print(f'Discord version: {discord.__version__}') 
intents = discord.Intents.default()
client = discord.Client(intents=intents)
intents.message_content = True # Il bot deve poter leggere almeno i messaggi

# setup delle variabili globali del bot
creator_process = {}  # Se è attivo il programma di creazione dei personaggi, va salvato l'oggetto corrispondente qui, con lo username dell'autore come chiave; questo consente di creare più personaggi contemporaneamente
prompt = ["\n>>>\t",pexpect.EOF] # il prompt atteso dal programma di creazione dei personaggi, indica che la stampa del messaggio è pronta
component_prompt = ["<button>", "<txt_input>", "<choice>"]

# gestione degli eventi webcor
@client.event
async def on_ready():
  '''Stampa di controllo: identità del bot e del server su cui è attivo
  '''
  print(client.user)
  print(client.guilds)  


@client.event
async def on_message(msg):
  '''Evento principale, gestisce tutti i messaggi
  '''
  global creator_process
  author = str(msg.author).split("#")[0] # estrae il nome dell'autore del messaggio
  content = msg.content
  isbot = False # serve nel processo di creazione per decidere come parsare content
  if msg.author==client.user:
    isbot = True
    if content.split(" ")[0] not in creator_process:
      return # ignora i propri messaggi
    else:
      content = content.split(" ")
      author = content[0]
  # creazione di un personaggio già iniziata
  if author in creator_process: # se è attivo il processo di creazione, interagisce con esso
        if isbot and len(content) > 1: # qualora fossero necessari ulteriori messaggi del bot si usa come trigger ['ha', 'scelto']
            creator_process[author].sendline(content[3]) # al momento si tiene conto che l'input sia uno solo
            creator_process[author].expect(prompt)
        if not isbot: # gli input da parte dell'utente vengono riconosciuti
            creator_process[author].sendline(content) # al momento si tiene conto che l'input sia uno solo
            creator_process[author].expect(prompt)
        comp_type = creator_process[author].expect(component_prompt)
        resp = creator_process[author].before
        await chargen(msg, creator_process[author], author, comp_type, resp) # WARN: pexpect.EOF ancora da gestire
        return
  # tutti i comandi successivi sono vincolati a creator_process == None: durante la creazione del personaggio non è possibile eseguire altri comandi
  # prova a parsare il messaggio come lancio di dadi ed eseguirlo
  res = parse_and_roll(content)   
  if res and author not in creator_process: 
    await msg.channel.send(f'**{author}**'+res)
  # creazione di un personaggio casuale; questo comando è autocontenuto, quindi creator_process viene creato e poi distrutto
  if '!itdsrand' in content and author not in creator_process:
    creator_process[author] = pexpect.spawnu('./itdschargen.py r') # attiva il programma di creazione dei personaggi
    creator_process[author].expect(pexpect.EOF)
    response = creator_process[author].before
    nome  = response.split("\n")[-2].strip()
    print(f"randomly created {re.escape(nome)}")
    creator_process[author] = pexpect.spawnu(f'./pdffields.py json/{re.escape(nome)}.json')
    creator_process[author].expect(pexpect.EOF)
    await msg.channel.send(f"**{author}** ha creato {nome}", file=discord.File(f'./pdf/{nome}.pdf'))
    del creator_process[author] # rimuove il creator_process
  # creazione guidata di un personaggio, inizializzazione
  if '!itdsc' in content and author not in creator_process:
    # TODO: Definire una funzione che gestisca dall'inizio alla fine
    # il processo di creazione del personaggio utilizzando solamente
    # i message components inviati dal bot
    creator_process[author] = pexpect.spawnu(['./itdschargen.py']) # attiva il programma di creazione dei personaggi
    # creator_process[author].expect(prompt)
    # response = creator_process[author].before
    print("Creating character")
    comp_type = creator_process[author].expect(component_prompt)
    resp = creator_process[author].before
    await chargen(msg, creator_process[author], author, comp_type, resp)
  # generazione di nomi
  if ('!n' in content or '!nomi' in content) and author not in creator_process:
    # impostazioni di default
    n=1 
    language='Latin'
    gender='male'
    # lettura dei parametri dal messaggio
    for p in content.split():
      if p in ['female', 'f'] : gender = 'female'
      if p in namegen.regions :
        language=namegen.regions[p]
      if p in namegen.names['male'] : language=[p]
      try : n=int(p)
      except ValueError : pass
    # generazione casuale
    response = '\n'.join([ namegen.get_name(gender,choice(language),True,'random') for i in range(n) ])
    await msg.channel.send(response)
  # messaggio d'aiuto
  if '!h' in content and author not in creator_process:
    response = f"""Messaggio di aiuto:
 Creazione dei personaggi giocanti:
    !itdsc       Creazione del personaggio interattiva
    !itdsrand    Creazione di un personaggio casuale
 Generazione casuale di nomi:
    !n[omi] [m|f] [N] [regione|lingua]
      [m|f]     default: maschile
      [N]       default: 1 nome
      [regione|lingua] default: Latino
        regioni {list(namegen.regions.keys())}
        lingue  {list(namegen.names['male'].keys())}
 Lancio dei dadi:
    Nd[X] [aN] [+N|-N] [vs N]
      Nd[X] lancia Nd6, scarta gli X più alti
      [aN] applica ai dadi residui un punteggio di abilità pari a N
      [+N|-N] applica N successi bonus o penalità
      [vs N] confronta il risultato con un punteggio di caratteristica pari a N
    """
    await msg.channel.send(response)

# main, lancia il bot
from config import TOKEN
client.run(TOKEN)


