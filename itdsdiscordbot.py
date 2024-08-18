#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-

__author__ = "Giampaolo Agosta"
__version__ = "1.0"
__doc__ = """Bot per Discord che implementa le seguenti funzioni:
  Generazione guidata o casuale di personaggi e compilazione delle schede PDF
  Generazione casuale di nomi medievaleggianti
  Lancio dei dadi per le prove
"""

# impiega secret come fonte di randomicità se disponibile, altrimenti random (che è solo pseudo-casuale)
try:
    from secrets import randbelow as rand

    print("Using secrets")
except ImportError:
    from random import randint

    print("Using random")
    rand = lambda x: randint(0, x - 1)


# gestione dei tiri di dado
def d(n, faces):
    """Lancio di dadi base
    n     numero di dadi da lanciare
    faces numero di facce del dado
    returns lista di risultati
    """
    try:
        return [rand(faces) + 1 for i in range(n)]
    except TypeError:
        print(faces, n)
        return [rand(int(faces)) + 1 for i in range(int(n))]


def choice(l):
    return l[sum(d(1, len(l))) - 1]


def d6(n=1):
    """Lancio di dadi a 6 facce
    n     numero di dadi da lanciare [default 1]
    returns lista di risultati
    """
    return d(n, 6)


def roll_itds(dice=2, extra=0, score=0, skill=0, bonus_penalty=0, difficulty=1):
    """Lancio di dadi per una prova de Il Tempo della Spada
    dice    numero di dadi a 6 facce [default 2d6]
    extra   numero di dadi extra [default 0] (qui i dadi extra sono da aggiungere al numero base)
    score   punteggio di caratteristica [default non indicato, non verrà calcolato il successo]
    skill   punteggio di abilità [default 0]
    bonus_penalty  successi bonus o penalità [default 0]
    difficulty    difficoltà (al momento non impiegato) [default 1]
    returns   stringa di testo che descrive il risultato
    """
    r = sorted(d6(dice + extra))  # ordina i risultati in senso crescente
    print(r)
    # Applica il punteggio di abilità in modo da ridurre a 1 più dadi possibile
    r_reduced = []
    i = 0
    while skill and i < len(r):
        if r[i] <= 1:
            r_reduced.append(r[i])
            i += 1
        else:
            r_reduced.append(r[i] - min(r[i] - 1, skill))
            skill -= min(r[i] - 1, skill)
            i += 1
    r_reduced += r[i:]
    # due trattamenti separati a seconda che score sia impostato o meno
    drop = []
    if score:
        # in questo caso, ottimizza il numero di successi
        remaining_extra = extra
        while (
            remaining_extra > 0 and sum(r_reduced) > score
        ):  # Non scarta in caso in cui il risultato minimo necessario sia già raggiunto
            drop.append(r_reduced[-1])
            r_reduced = r_reduced[:-1]
            remaining_extra -= 1
        result = f' tira {dice+extra}d6 {f"vs {score}" if score else ""}: {r} {f"e scarta {drop}" if len(drop) else ""}, ridotti con {skill} punti abilità a {r_reduced}, per un totale di {sum(r_reduced)}'
        successes = r_reduced.count(1)
        success = (
            sum(r_reduced) <= score and successes + 1 + bonus_penalty >= difficulty
        )
        if success:
            return result + f", ottenendo **{successes+1} successi**"
        else:
            return result + f", ottenendo un fallimento"
    else:
        # in questo caso, ottimizza il risultato totale scartando il massimo numero di dadi possibile
        if extra > 0:
            drop = r_reduced[-extra:]
            r_reduced = r_reduced[:-extra]
        result = f' tira {dice+extra}d6 {f"vs {score}" if score else ""}: {r} {f"e scarta {drop}" if len(drop) else ""} ridotti con {skill} punti abilità a {r_reduced} per un totale di {sum(r_reduced)}'
        successes = r_reduced.count(1)
        return (
            result
            + f", ottenendo **{successes+1} successi**, se il tiro è inferiore al punteggio di caratteristica"
        )


# Parsing dei messaggi discord che richiedono il tiro di dadi
import re

# roll parse
rg = r"(?P<dice>\d+)d\s*(?P<drop>\d*)(\s*a(?P<skill>\d+)){0,1}(\s*(?P<bonus_sign>\+|\-)(?P<bonus_value>\d+)){0,1}(\s*vs\s*(?P<score>\d+)){0,1}"
rgc = re.compile(rg, re.IGNORECASE)
# buttons parse
rb = r"(?: ?\([0-9]+\))? ?([0-9a-zà-ùá-ú ]+)"
rbc = re.compile(rb, re.IGNORECASE)
# creation process parse
rc = r"[Hh][ao] scelto: "
rcc = re.compile(rc)


def parse_and_roll(msg):
    """Interpreta un messaggio discord che contiene una specifica per il lancio di dadi ed esegue il lancio
    msg      contenuto di un messaggio discord
    returns  stringa di testo che descrive il risultato
    """
    res = rgc.search(msg)  # esegue il match
    if not res:
        return None  # match fallito
    d = res.groupdict()  # estrae i dati
    for x in d:  # imposta i default
        if not d[x]:
            d[x] = 0
    print(d)
    return roll_itds(
        dice=int(d["dice"]) - int(d["drop"]),  # qui rimuove i dadi extra dal totale, poiché roll li considera in automatico
        extra=int(d["drop"]),
        score=int(d["score"]),
        skill=int(d["skill"]),
        bonus_penalty=int(d["bonus_value"]) * (-1 if d["bonus_sign"] == "-" else 1),  # converte il segno +/-
    )


import discord
import json


# Modal che contiene le caselle di testo per i vari campi da inserire
class TxtInput(discord.ui.Modal):
    def __init__(self, author: str, title: str, boxes: list[str]):
        super().__init__(title=title)
        self.author = author
        for box in boxes:
            self.add_item(
                discord.ui.TextInput(
                    label=box,
                    required=True
                )
            )

    async def on_submit(self, interaction: discord.Interaction):
        msg = ", ".join([c.value for c in self.children])
        await interaction.response.send_message(f"**{self.author}** ha scelto: {msg}")

# Classe che genera il bottone per aprire il Modal con le caselle di testo
class ModalBtn(discord.ui.View):
    def __init__(self, author: str, title: str, boxes: list[str]):
        super().__init__()
        self.author = author
        self.title = title
        self.boxes = boxes
    @discord.ui.button(label="Inserisci", style=discord.ButtonStyle.blurple)
    async def spawn_modal(self, interaction: discord.Interaction, button: discord.ui.Button):
        if str(interaction.user).split("#")[0] != self.author: # accetta l'interazione solo se è del creatore del personaggio
            await interaction.response.send_message(f"Solo {self.author} può interagire con questo messaggio")
            return
        await interaction.response.send_modal(TxtInput(self.author, self.title, self.boxes))
        button.disabled = True # evita altre interazioni
        await interaction.message.edit(view=self)

# Classe per gli input da bottone
class Btn(discord.ui.Button):
    def __init__(self, name: str, author):
        super().__init__(label=name)
        self.author = author

    async def callback(self, interaction: discord.Interaction):
        if str(interaction.user).split("#")[0] != self.author: # accetta l'interazione solo se è del creatore del personaggio
            await interaction.response.send_message(f"Solo {self.author} può interagire con questo messaggio")
            return
        for child in self.view.children:
            child.disabled = True
        # Aggiorna la view disabilitando i components
        await interaction.response.edit_message(view=self.view)
        # Invia il messaggio con le scelte effettuate
        await interaction.followup.send(content=f"**{self.author}** ha scelto: {self.label}")


# Classi per gli input a selezione multipla
class Menu(discord.ui.Select):
    def __init__(self, opts, auhtor, qta=1, qta_max=None, placeholder=None):
        if len(opts) == 0:
            opts = [ discord.SelectOption(label="Non ci sono elementi da selezionare") ]
        if qta > len(opts):
            qta = len(opts)
        if qta_max is None:
            qta_max = qta
        super().__init__(min_values=qta, max_values=qta_max, options=opts, placeholder=placeholder)
        self.author = auhtor

    async def callback(self, interaction: discord.Interaction):
        if str(interaction.user).split("#")[0] != self.author: # accetta l'interazione solo se è del creatore del personaggio
            await interaction.response.send_message(f"Solo {self.author} può interagire con questo messaggio")
            return
        for child in self.view.children:
            child.disabled = True
        # Aggiorna la view disabilitando i components
        await interaction.response.edit_message(view=self.view)
        # Invia il messaggio con le scelte effettuate
        await interaction.followup.send(content=f"**{self.author}** ha scelto: {', '.join(self.values)}")


class MainMenu(Menu):
    """Un Menu che permette di selezionare quale set di opzioni è da visualizzare
       in un secondo Menu, basandosi sui contenuti del dizionario passato al costruttore.
       Ogni volta che viene selezionata un'opzione in MainMenu, il "sottomenu" viene rimosso per poi inserirne
       uno nuovo con il set di opzioni aggiornato.
       Eventualmente è possibile espandere fino a quattro la quantità di set da visualizzare"""
    def __init__(self, opts, author, dic, qta=1, qta_max=None, placeholder=None):
        super().__init__(opts, author, qta, qta_max, placeholder)
        self.dic = dic

    async def callback(self, interaction: discord.Interaction):
        if str(interaction.user).split("#")[0] != self.author: # accetta l'interazione solo se è del creatore del personaggio
            await interaction.response.send_message(f"Solo {self.author} può interagire con questo messaggio")
            return
        # Costruisce le opzioni per il nuovo select
        opts = [ discord.SelectOption(label=val) for val in self.dic[self.values[0]] ]
        # Rimuove tutti gli elementi della view a parte sé stesso (i buttons)
        for child in self.view.children:
            if child is self:
                self.placeholder = f"Categoria selezionata: {self.values[0]}"
                continue
            self.view.remove_item(child)
        # Aggiorna la view inserendo il nuovo menu
        self.view.add_item(Menu(opts, self.author))
        await interaction.response.edit_message(view=self.view)


async def chargen(msg, author: str, comp_type: int, response: str):
    """Funzione per il processo di creazione del personaggio.
Sulla base del prompt trovato da pexpect sceglie il tipo di component da utilizzare"""
    if comp_type == 0:  # Button
        btn_str = response.split("\n")[-1]  # Estrazione delle scelte
        btn_labels = rbc.findall(btn_str)  # Parsing delle scelte
        vw = discord.ui.View()  # Costruzione della view
        for b in btn_labels:  # Ogni possibilità di scelta viene associata ad un bottone
            vw.add_item(Btn(b, author))
        await msg.channel.send(f"## {author}\n{response}", view=vw)

    if comp_type == 1:  # Text input
        resp= response.split("\n")
        title = resp[-2]
        boxes = resp[-1].replace(":", "").split(", ")
        vw = ModalBtn(author, title, boxes)
        await msg.channel.send(f"## {author}\n{response}", view=vw)

    if comp_type == 2: # Selezione multipla
        resp = response.split("\n")
        # Parsing della penultima riga di response dove è contenuto il numero di elementi da selezionare
        qta = int(re.findall(r"\d+", resp[-2])[0])
        opts_str = resp[-1]
        opts_val = rbc.findall(opts_str)
        opts = [ discord.SelectOption(label=o) for o in opts_val ]
        vw = discord.ui.View()
        vw.add_item(Menu(opts, author, qta))
        await msg.channel.send(f"## {author}\n{response}", view=vw)

    if comp_type == 3: # Selezione ad albero
        resp = str(response).split("\n")
        # Parsing JSON del dizionario creato in itdschargen
        sel_dict = json.loads(resp[-3])
        vw = discord.ui.View()
        opts = [ discord.SelectOption(label=key) for key in list(sel_dict.keys()) ]
        vw.add_item(
            MainMenu(
                opts,
                author,
                sel_dict,
                placeholder="Scegli una categoria da visualizzare",
            )
        )
        await msg.channel.send(f"## {author}\n" + "\n".join(resp[-2:]), view=vw)


# Il resto dell'applicazione è più o meno adattata da bot.py
from os import remove
from config import PDF
import pexpect
import namegen

# setup di discord
print(f"Discord version: {discord.__version__}")
intents = discord.Intents.default()
client = discord.Client(intents=intents)
intents.message_content = True  # Il bot deve poter leggere almeno i messaggi

# setup delle variabili globali del bot
pexpect_process = {}  # Se è attiva una shell aperta da pexpect, va salvato l'oggetto corrispondente qui, con lo username dell'autore come chiave; questo consente di eseguire comandi che sfruttano pexpect in contemporanea da parte di utenti diversi
# il prompt di base per le azioni diverse dalla creazione di personaggi: in questi casi \n>>>\t indica la corretta esecuzione
prompt = ["\n>>>\t", pexpect.EOF]
# il prompt atteso dal programma di creazione dei personaggi, indica che la stampa del messaggio è pronta
creator_prompt = ["\n>>>\t"]
# il prompt che indica qual è la prossima azione che il bot deve eseguire
action_prompt = ["<button>", "<txt_input>", "<choice>", "<tree-select>", "Operazione completata", pexpect.EOF]
# prompt ricevuti nel caso di creazione casuale
random_prompt = ["Operazione completata", pexpect.EOF]


# gestione degli eventi webcor
@client.event
async def on_ready():
    """Stampa di controllo: identità del bot e del server su cui è attivo"""
    print(client.user)
    print(client.guilds)


@client.event
async def on_message(msg):
    """Evento principale, gestisce tutti i messaggi"""
    global pexpect_process
    author = str(msg.author).split("#")[0]  # estrae il nome dell'autore del messaggio
    content = msg.content
    if msg.author == client.user:
        author = None
        for a in pexpect_process: # cerca se il messaggio contiene un utente in pexpect_process
            if a in content:
                author = a
        if not author: # il messaggio va ignorato
            return
    # interruzione di un processo pexpect
    if "!itdsinterrupt" in content:
        if author in pexpect_process:
            pexpect_process[author].close()
            del pexpect_process[author]
            await msg.channel.send(f"Operazione terminata da {author}!")
        else:
            await msg.channel.send(f"Non c'è alcun processo associato a {author}!")
        return
    # creazione di un personaggio già iniziata
    if author in pexpect_process and pexpect_process[author].name == "<./itdschargen.py -c>": # questo blocco è da eseguire solo per la creazione manuale
        if rcc.search(content): # Se l'utente vuole scrivere la risposta a mano il messaggio deve contenere 'H(h)o(a) scelto: ' seguito dalle scelte
            pexpect_process[author].sendline(rcc.split(content, maxsplit=1)[-1])
            pexpect_process[author].expect(creator_prompt)
        else:
            return
        comp_type = pexpect_process[author].expect(action_prompt)
        response = pexpect_process[author].before
        if comp_type == 4: # Creazione del personaggio terminata
            nome = response.split("\n")[-2].strip() # estrae il nome del personaggio dall'output del programma
            pexpect_process[author] = pexpect.spawnu(f"./pdffields.py -e '{nome}'") # chiama il convertitore a PDF
            pexpect_process[author].expect(pexpect.EOF) # attende il completamento della conversione
            await msg.channel.send(f"**{author}** ha creato {nome}", file=discord.File(f"./pdf/{nome}.{'pdf' if PDF else 'txt'}")) # invia il file PDF sulla chat
            remove(f"./pdf/{nome}.{'pdf' if PDF else 'txt'}pdf")
            del pexpect_process[author] # rimuove il creator_process, riabilitando gli altri comandi
        elif comp_type == 5: # EOF: si è verificato un errore
            await msg.channel.send(f"### Si è verificato un errore: *{response.strip()}*")
            del pexpect_process[author]
        else:
            await chargen(msg, author, comp_type, response)
        return
    # tutti i comandi successivi sono vincolati a creator_process == None: durante la creazione del personaggio non è possibile eseguire altri comandi
    # prova a parsare il messaggio come lancio di dadi ed eseguirlo
    res = parse_and_roll(content)
    if res and author not in pexpect_process:
        await msg.channel.send(f"**{author}**" + res)
    # creazione di un personaggio casuale; questo comando è autocontenuto, quindi creator_process viene creato e poi distrutto
    if "!itdsr" in content and author not in pexpect_process:
        # attiva il programma di creazione dei personaggi
        pexpect_process[author] = pexpect.spawnu("./itdschargen.py -c r")
        status = pexpect_process[author].expect(random_prompt)
        response = pexpect_process[author].before
        if status == 0: # La creazione del personaggio è terminata con successo
            nome = response.split("\n")[-2].strip() # estrae il nome del personaggio dall'output del programma
            print(f"randomly created {nome}")
            pexpect_process[author] = pexpect.spawnu(f"./pdffields.py -e '{nome}'")
            status = pexpect_process[author].expect(prompt)
            await msg.channel.send(f"**{author}** ha creato {nome}", file=discord.File(f"./pdf/{nome}.{'pdf' if PDF else 'txt'}"))
            remove(f"./pdf/{nome}.{'pdf' if PDF else 'txt'}pdf")
        else: # Si è verificato un errore
            await msg.channel.send(f"### Si è verificato un errore: *{response.strip()}*")
        del pexpect_process[author]  # rimuove il creator_process
        return
    # creazione guidata di un personaggio, inizializzazione
    if "!itdsc" in content and author not in pexpect_process:
        # attiva il programma di creazione dei personaggi
        pexpect_process[author] = pexpect.spawnu("./itdschargen.py -c")
        print("Creating character")
        comp_type = pexpect_process[author].expect(action_prompt)
        response = pexpect_process[author].before
        if comp_type != 5: # Se la connessione a Redis non avviene, itdschargen termina subito
            await chargen(msg, author, comp_type, response)
        else:
            await msg.channel.send(f"### Si è verificato un errore: *{response.strip()}*")
            del pexpect_process[author]
        return
    # visualizzazione dei nomi di tutti i personaggi salvati
    if "!itdss" in content and author not in pexpect_process:
        pexpect_process[author] = pexpect.spawnu("./itdschargen.py -s")
        err = pexpect_process[author].expect(prompt)
        response = pexpect_process[author].before
        if err == 0: # Non si sono verificati errori
            await msg.channel.send(response)
        else:
            await msg.channel.send(f"### Si è verificato un errore: *{response.strip()}*")
        del pexpect_process[author]
        return
    # cancellazione di un personaggio
    if "!itdsd" in content and author not in pexpect_process:
        nome = " ".join(content.split()[1:])
        if nome == '':
            await msg.channel.send("Non è stato fornito alcun nome")
        else:
            pexpect_process[author] = pexpect.spawnu(f"./itdschargen.py -d '{nome}'")
            err = pexpect_process[author].expect(prompt)
            response = pexpect_process[author].before
            if err == 0: # Non si sono verificati errori
                await msg.channel.send(f"### {nome} rimosso dalla memoria")
            else:
                await msg.channel.send(f"### Si è verificato un errore: *{response.strip()}*")
            del pexpect_process[author]
        return
    # generazione della scheda personaggio
    if "!itdse" in content and author not in pexpect_process:
        nome = " ".join(content.split()[1:])
        if nome == '':
            await msg.channel.send("Non è stato fornito alcun nome")
        else:
            pexpect_process[author] = pexpect.spawnu(f"./pdffields.py -e '{nome}'")
            err = pexpect_process[author].expect(prompt)
            response = pexpect_process[author].before
            if err == 0: # Non si sono verificati errori
                await msg.channel.send(f"### Scheda di {nome}", file=discord.File(f"./pdf/{nome}.{'pdf' if PDF else 'txt'}pdf"))
                remove(f"./pdf/{nome}.{'pdf' if PDF else 'txt'}pdf") # cancella la copia locale del file generato
            else:
                await msg.channel.send(f"### Si è verificato un errore: *{response.strip()}*")
            del pexpect_process[author]
        return
    # importazione del personaggio da file
    if "!itdsi" in content and author not in pexpect_process:
        if len(msg.attachments) > 0: # considera solo il primo attachment se esiste
            allegato = msg.attachments[0]
        else:
            await msg.channel.send("File non trovato. Assicurati di averlo inserito nel messaggio")
            return
        if not (".pdf" in allegato or ".txt" in allegato):
            await msg.channel.send("Il file inviato deve essere una scheda personaggio in formato pdf o txt")
            return
        await allegato.save(f"./pdf/{allegato.filename}") # salva l'allegato nella cartella pdf
        pexpect_process[author] = pexpect.spawnu(f"./pdffields.py -i './pdf/{allegato.filename}'")
        err = pexpect_process[author].expect(prompt)
        response = pexpect_process[author].before
        if err == 0: # Non si sono verificati errori
            await msg.channel.send("### Personaggio importato")
        else:
            await msg.channel.send(f"### Si è verificato un errore: *{response.strip()}*")
        remove(f"./pdf/{allegato.filename}")
        del pexpect_process[author]
        return
    # generazione di nomi
    if ("!n" in content or "!nomi" in content) and author not in pexpect_process:
        # impostazioni di default
        n = 1
        language = "Latin"
        gender = "male"
        # lettura dei parametri dal messaggio
        for p in content.split():
            if p in ["female", "f"]:
                gender = "female"
            if p in namegen.regions:
                language = namegen.regions[p]
            if p in namegen.names["male"]:
                language = [p]
            try:
                n = int(p)
            except ValueError:
                pass
        # generazione casuale
        response = "\n".join([ namegen.get_name(gender, choice(language), True, "random") for i in range(n) ])
        await msg.channel.send(response)
        return
    # messaggio d'aiuto
    if "!h" in content and author not in pexpect_process:
        response = f"""Messaggio di aiuto:
 Creazione dei personaggi:
    !itdsc[reate]          Creazione del personaggio interattiva
    !itdsr[and]            Creazione di un personaggio casuale
    !itdsinterrupt         Annulla il processo di creazione del personaggio (o anche quelli per la gestione dei personaggi)
 Gestione dei personaggi:
    !itdss[how]            Mostra i nomi di tutti i personaggi salvati in memoria
    !itdsd[elete] [Nome]   Elimina un personaggio dalla memoria
    !itdsi[mport]          Importa un personaggio allegando la sua scheda
    !itdse[xport] [Nome]   Genera la scheda di un personaggio
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
        return


# main, lancia il bot
from config import TOKEN

client.run(TOKEN)
