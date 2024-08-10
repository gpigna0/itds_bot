#!/usr/bin/env python3.10
from pypdf import PdfReader, PdfWriter

campi = ['Anno', 'Araldica_af_image', 'Armatura 1', 'Armatura 2', 'Armatura 3', 'Armi 1', 'Armi 2', 'Armi 3', 'Armi 4', 'Armi 5', 'Artigiano 1', 'Artigiano 5', 'Artigiano2', 'Artigiano3', 'Artigiano4', 'Audacia', 'Carartigiano2', 'Carartigiano3', 'Carartigiano4', 'Carartigiano5', 'Caratteristica Artigiano 1', 'Celeritas', 'Ceto', 'Critiche Residue', 'Critichetotali', 'Cultura', 'DAgilità', 'DAlchimia', 'DArchi', 'DArmiComuni', 'DArmiCorte', 'DArmiGuerra', 'DArteGuerra', 'DArtiArcane', 'DArtiLiberali', 'DAtletica', 'DAutorità', 'DBalestre', 'DCarisma', 'DCavalcare', 'DEmpatia', 'DForza', 'DFurtività', 'DGuarigione', 'DIntrattenere', 'DLotta', 'DManualità', 'DMercatura', 'DPercezione', 'DRaggirare', 'DRagionamento', 'DSopravvivenza', 'DStoriaLeggende', 'DTeologia', 'DUsiCostumi', 'DVolontà', 'Dannoarma1', 'Dannoarma2', 'Dannoarma3', 'Dannoarma4', 'Dannoarma5', 'Dartigianato1', 'Dartigianato2', 'Dartigianato3', 'Dartigianato4', 'Dartigianato5', 'Denari', 'Ego', 'Equipaggiamento 10D', 'Equipaggiamento 10S', 'Equipaggiamento 11D', 'Equipaggiamento 11S', 'Equipaggiamento 12D', 'Equipaggiamento 12S', 'Equipaggiamento 13D', 'Equipaggiamento 13S', 'Equipaggiamento 14S', 'Equipaggiamento 15S', 'Equipaggiamento 1D', 'Equipaggiamento 1S', 'Equipaggiamento 2D', 'Equipaggiamento 2S', 'Equipaggiamento 3D', 'Equipaggiamento 3S', 'Equipaggiamento 4D', 'Equipaggiamento 4S', 'Equipaggiamento 5D', 'Equipaggiamento 5S', 'Equipaggiamento 6D', 'Equipaggiamento 6S', 'Equipaggiamento 7D', 'Equipaggiamento 7S', 'Equipaggiamento 8D', 'Equipaggiamento 8S', 'Equipaggiamento 9D', 'Equipaggiamento 9S', 'Eventi 1', 'Eventi 2', 'Eventi 3', 'Eventi 4', 'Eventi 5', 'Eventi 6', 'Eventi 7', 'Fama', 'Fides', 'Focus 1', 'Focus 2', 'Focus 3', 'Focus 4', 'Focus 5', 'Focus 6', 'Fortitudo', 'Fresco residuo', 'Frescototale', 'Gartigianato1', 'Gartigianato2', 'Gartigianato3', 'Gartigianato4', 'Gartigianato5', 'Genere', 'Grado Agilità', 'Grado Alchimia', 'Grado Archi', 'Grado Armi Comuni', 'Grado Armi Corte', 'Grado Armi da Guerra', 'Grado Arte guerra', 'Grado Arti Arcane', 'Grado Arti Liberali', 'Grado Atletica', 'Grado Autorità', 'Grado Balestre', 'Grado Carisma', 'Grado Cavalcare', 'Grado Empatia', 'Grado Forza', 'Grado Furtività', 'Grado Guarigione', 'Grado Intrattenere', 'Grado Lotta', 'Grado Manualità', 'Grado Mercatura', 'Grado Percezione', 'Grado Raggirare', 'Grado Ragionamento', 'Grado Sopravvivenza', 'Grado Storia e Leggende', 'Grado Teologia', 'Grado Usi e Costumi', 'Grado Volontà', 'Graffi Residue', 'Graffitotali', 'Gratia', 'Gravi Residue', 'Gravitotali', 'Honor', 'Impietas', 'Ingombro Leggero', 'Ingombro Massimo', 'Ingombro Moderato', 'Ingombro Pesante', 'Leggere Residue', 'Leggeretotali', 'Lingue', "Lire d'oro", 'Mens', 'Mestiere', 'Misuraarma1', 'Misuraarma2', 'Misuraarma3', 'Misuraarma4', 'Misuraarma5', 'Mod Audacia', 'Mod Celeritas', 'Mod Fortitudo', 'Mod Gratia', 'Mod Mens', 'Mod Prudentia', 'Mortali Residue', 'Mortalitotali', 'Nessun Ingombro', 'Nome', 'Note Armatura 2', 'Note Armatura 3', 'Note armatura 1', 'Ordine', 'PE Liberi', 'PE spesi', 'Parata1', 'Parata2', 'Parata3', 'Parata4', 'Parata5', 'PequipD1', 'PequipD10', 'PequipD11', 'PequipD12', 'PequipD13', 'PequipD2', 'PequipD3', 'PequipD4', 'PequipD5', 'PequipD6', 'PequipD7', 'PequipD8', 'PequipD9', 'PequipS1', 'PequipS10', 'PequipS11', 'PequipS12', 'PequipS13', 'PequipS14', 'PequipS15', 'PequipS2', 'PequipS3', 'PequipS4', 'PequipS5', 'PequipS6', 'PequipS7', 'PequipS8', 'PequipS9', 'Peso totale trasportato', 'Pregiarmi1', 'Pregiarmi2', 'Pregiarmi3', 'Pregiarmi4', 'Pregiarmi5', 'Protezione Armatura', 'Prudentia', 'Ratio', 'Regioni Fama 1', 'Regioni Fama 2', 'Regioni Fama 3', 'Regioni Fama 4', 'Riflessi attuali', 'Riflessi massimi', 'Ritratto_af_image', 'Robustezza Armatura', 'Sfinito residuo', 'Sfinitototale', 'Soldi', 'Spiritoresiduo', 'Spiritototale', 'Stanco residuo', 'Stancototale', 'Superstitio', 'Talenti 1', 'Talenti10', 'Talenti11', 'Talenti12', 'Talenti13', 'Talenti14', 'Talenti2', 'Talenti3', 'Talenti4', 'Talenti5', 'Talenti6', 'Talenti7', 'Talenti8', 'Talenti9', 'Tentazione', 'Tratti 1', 'Tratti 2', 'Tratti 3', 'Tratti 4']

dado_extra_ab = [ 'DAgilità', 'DAlchimia', 'DArchi', 'DArmiComuni', 'DArmiCorte', 'DArmiGuerra', 'DArteGuerra', 'DArtiArcane', 'DArtiLiberali', 'DAtletica', 'DAutorità', 'DBalestre', 'DCarisma', 'DCavalcare', 'DEmpatia', 'DForza', 'DFurtività', 'DGuarigione', 'DIntrattenere', 'DLotta', 'DManualità', 'DMercatura', 'DPercezione', 'DRaggirare', 'DRagionamento', 'DSopravvivenza', 'DStoriaLeggende', 'DTeologia', 'DUsiCostumi', 'DVolontà' ]
grado_ab = [ 'Grado Agilità', 'Grado Alchimia', 'Grado Archi', 'Grado Armi Comuni', 'Grado Armi Corte', 'Grado Armi da Guerra', 'Grado Arte guerra', 'Grado Arti Arcane', 'Grado Arti Liberali', 'Grado Atletica', 'Grado Autorità', 'Grado Balestre', 'Grado Carisma', 'Grado Cavalcare', 'Grado Empatia', 'Grado Forza', 'Grado Furtività', 'Grado Guarigione', 'Grado Intrattenere', 'Grado Lotta', 'Grado Manualità', 'Grado Mercatura', 'Grado Percezione', 'Grado Raggirare', 'Grado Ragionamento', 'Grado Sopravvivenza', 'Grado Storia e Leggende', 'Grado Teologia', 'Grado Usi e Costumi', 'Grado Volontà' ]

ferite  = [ 'Graffitotali', 'Leggeretotali', 'Gravitotali', 'Critichetotali', 'Mortalitotali' ]
feriter = [ 'Graffi Residue', 'Leggere Residue', 'Gravi Residue', 'Critiche Residue', 'Mortali Residue' ]
fatica  = [ 'Frescototale', 'Stancototale', 'Sfinitototale' ]
faticar = [ 'Fresco residuo', 'Stanco residuo', 'Sfinito residuo' ]
denaro  = [ "Lire d'oro", "Soldi", "Denari" ]

def denaro_split(d):
  lire   = (d//12)//20 #lire
  soldi  = (d//12)%20 #soldi
  denari = d%12 #denari
  return lire, soldi, denari

def capitalize(s):
  return s.capitalize()

def fill(p):
  fields = {
   "Nome": p.nome,
   "Anno": str(p.anno_nascita),
   "Genere": 'o' if p.genere=='maschio' else 'a',
   "Cultura": f'{p.cultura[0]}/{p.cultura[1]}',
   "Ceto": p.ceto,
   "Mestiere": p.mestiere,
   "Ordine": p.ordine,
   "Tentazione": p.tentazione,
   "Fama": str(p.fama),
   "Spiritototale" : str(p.spirito),
   "Spiritoresiduo" : str(p.spirito),
   "Riflessi massimi": str(p.riflessi),
   "Riflessi attuali": str(p.riflessi),
   "Nessun Ingombro": str(p.ingombro_base),
   "Ingombro Leggero": str(p.ingombro_base*2),
   "Ingombro Moderato": str(p.ingombro_base*4),
   "Ingombro Pesante": str(p.ingombro_base*6),
   "Ingombro Massimo": str(p.ingombro_base*8),
   "Lingue": ', '.join(p.lingue),
   "PE Liberi" : str(p.pe_liberi),
   "PE spesi" : str(p.pe_spesi),
   "Denari" : '0',
   "Armatura 1" : f'{p.armatura.nome} {"("+p.armatura.qualità+")" if p.armatura.qualità!="normale" else ""}',
   "Protezione Armatura" : str(p.armatura.protezione),
   "Robustezza Armatura" : str(p.armatura.protezione*10),
   "Note Armatura 1": ', '.join(p.armatura.pregi),
   "Peso totale trasportato" : str(p.armatura.peso + sum([ a.peso for a in p.armi]) + sum([o.peso for o in p.equipaggiamento])),
  }
  fields[denaro[0]], fields[denaro[1]], fields[denaro[2]] = denaro_split(p.denaro)

  tratti = p.altro.split('\n')
  i=1
  for t in tratti:
    fields[f"Tratti {i}"]=t
    i+=1

  i=1
  lato='S'
  for a in p.equipaggiamento:
    fields[f'Equipaggiamento {i}{lato}']=f'{a.nome} {"("+a.qualità+")" if a.qualità!="normale" else ""}'
    fields[f'Pequip{lato}{i}']=a.peso
    i=i+1
    if i>15 : 
      i-=15
      lato='D'

  i=1
  for a in p.armi:
    print(a)
    fields[f'Armi {i}']=f'{a.nome} {"("+a.qualità+")" if a.qualità!="normale" else ""}'
    fields[f'Parata{i}']=f'+{a.parata}'
    fields[f'Dannoarma{i}']=f"+{a.danno}{a.tipo}"
    fields[f'Misuraarma{i}']=f"{a.misura if a.misura!='N/A' else ''} {str(a.gittata)+'m' if a.gittata!=0 else ''}"
    fields[f'Pregiarmi{i}']=f"{', '.join(a.pregi)}"
    i+=1

  i=1
  for a in p.abilità:
    if len(p.abilità[a].focus): 
      fields[f'Focus {i}']=f'{a}: {", ".join(p.abilità[a].focus)}'
      i+=1
  for a in p.artigiano:
    if len(p.artigiano[a].focus): 
      fields[f'Focus {i}']=f'{a}: {", ".join(p.artigiano[a].focus)}'
      i+=1
  for a in p.professione:
    if len(p.professione[a].focus): 
      fields[f'Focus {i}']=f'{a}: {", ".join(p.professione[a].focus)}'
      i+=1

  for f,v,r in zip(ferite,p.ferite,feriter):
    fields[f]=str(v)
    fields[r]=str(v)

  for f,v,r in zip(fatica,p.fatica,faticar):
    fields[f]=str(v)
    fields[r]=str(v)

  for c in p.caratteristiche:
    fields[capitalize(c)]=str(p.caratteristiche[c].caratteristica)
    fields['Mod '+capitalize(c)]=str(p.caratteristiche[c].modificatore)

  ab = sorted(list(p.abilità.keys()))
  for c,g,d in zip(ab,grado_ab,dado_extra_ab) :
    fields[d]=str(p.abilità[c].dado_extra)
    fields[g]=str(p.abilità[c].grado)+('*' if p.abilità[c].mestiere else '')
  for v in p.valori:
    fields[capitalize(v)]=str(p.valori[v])

  ab = sorted(list(p.artigiano.keys()))
  i=1
  for c in ab :
    fields[f'Artigiano {i}']=c
    fields[f'Artigiano{i}']=c
    fields[f'Dartigianato{i}']=str(p.artigiano[c].dado_extra)
    fields[f'Gartigianato{i}']=str(p.artigiano[c].grado)+('*' if p.artigiano[c].mestiere else '')
    if i==1 : fields[f'Caratteristica Artigiano {i}']=str(p.artigiano[c].caratteristica)
    else : fields[f'Carartigiano{i}']=str(p.artigiano[c].caratteristica)
    i+=1
  ab = sorted(list(p.professione.keys()))
  for c in ab :
    fields[f'Artigiano {i}']=c
    fields[f'Artigiano{i}']=c
    fields[f'Dartigianato{i}']=str(p.professione[c].dado_extra)
    fields[f'Gartigianato{i}']=str(p.professione[c].grado)+('*' if p.professione[c].mestiere else '')
    if i==1 : fields[f'Caratteristica Artigiano {i}']=str(p.professione[c].caratteristica)
    else : fields[f'Carartigiano{i}']=str(p.professione[c].caratteristica)
    i+=1

  i=1
  for e in p.eventi:
    fields[f'Eventi {i}']=e
    i+=1

  i=1
  for e in p.talenti:
    fields[f'Talenti {i}']=e
    fields[f'Talenti{i}']=e
    i+=1

  return fields


def lista_focus(p):
  ab = [f"{a}: {', '.join(p.abilità[a].focus)}" for a in p.abilità if len(p.abilità[a].focus)]
  ar = [f"{a}: {', '.join(p.artigiano[a].focus)}" for a in p.artigiano if len(p.artigiano[a].focus)]
  pr = [f"{a}: {', '.join(p.professione[a].focus)}" for a in p.professione if len(p.professione[a].focus)]
  return "\n".join(ab + ar + pr)


def lista_armi(p):
  l = [
f'''{a.nome} {"("+a.qualità+")" if a.qualità!="normale" else ""}
  Danno: +{a.parata}
  Parata: +{a.danno}{a.tipo}
  Misura Gittata: {a.misura if a.misura!='N/A' else ''}{str(a.gittata)+' m' if a.gittata!=0 else ''}
  Note o Pregi: {', '.join(a.pregi)}''' for a in p.armi]
  return "\n\n".join(l)


def lista_professioni(p, c, n):
  ar = sorted(list(p.artigiano.keys()))
  pr = sorted(list(p.professione.keys()))
  l1 = [f"|  {a:{c}}|  {p.artigiano[a].caratteristica:{c}}|{str(p.artigiano[a].grado)+('*' if p.artigiano[a].mestiere else ''):^{n}}|{p.artigiano[a].dado_extra:^{n}}|" for a in ar]
  l2 = [f"|  {a:{c}}|  {p.professione[a].caratteristica:{c}}|{str(p.professione[a].grado)+('*' if p.professione[a].mestiere else ''):^{n}}|{p.professione[a].dado_extra:^{n}}|" for a in pr]
  if not (len(l1) or len(l2)):
    l1 = [f"|{' '* (2*c * 2*n + 4)}|"] # lascia la tabella vuota
  return "\n".join(l1+l2)


def lista_equip(p):
  l = [
f'''{a.nome} {"("+a.qualità+")" if a.qualità!="normale" else ""}
  Peso: {a.peso}''' for a in p.equipaggiamento]
  return "\n\n".join(l)


def write_pdf(p):
  reader = PdfReader("scheda_template.pdf")
  writer = PdfWriter()
  writer.clone_reader_document_root(reader)
  fields = fill(p)
  print(fields)
  writer.update_page_form_field_values(writer.pages[0], fields)
  writer.update_page_form_field_values(writer.pages[1], fields)
  writer.add_metadata({"/CharData": p.to_json()}) # Aggiunge un campo nei metadati contenente il Personaggio in formato json facilitando le operazioni di import/export
  with open(f"./pdf/{p.nome}.pdf", "wb") as output_stream:
    writer.write(output_stream)


def import_from_pdf(path): # path o nome?
    reader = PdfReader(path)
    jsonp = reader.metadata["/CharData"]
    savepers(Personaggio.from_json(jsonp))


def write_txt(p):
    num_field = 12
    name_field = 23
    car_size = 4 + 2 * num_field + name_field
    nl = "\n"
    lire = "Lire d'oro"
    fields = fill(p)
    sheet = f"""
IL TEMPO DELLA SPADA
Scheda Personaggio

Il mio nome è {fields['Nome']}, nat{fields['Genere']} nell'Anno del Signore {fields['Anno']} da genti di Cultura {fields['Cultura']}
Sono di Ceto {fields['Ceto']} e ho appreso il Mestiere di {fields['Mestiere']} Ordine {fields['Ordine']}
Conosco le Lingue {fields['Lingue']}



Tentazione: {fields['Tentazione']}



-{'-'*(name_field+2)}-{'-'*num_field}-{'-'*num_field}-{'-'*(name_field+2)}-{'-'*num_field}-{'-'*num_field}-
|{'Caratteristiche':^{car_size}}|{'Abilità':^{car_size}}|
|{'-'*car_size}|{'-'*car_size}|
|{'Nome':^{name_field+2}}|{'Mod':^{num_field}}|{'Punti':^{num_field}}|{'Nome':^{name_field+2}}|{'Grado':^{num_field}}|{'Dadi Extra':^{num_field}}|
|{'-'*car_size}|{'-'*car_size}|
|{' '*(name_field+2)}|{' '*num_field}|{' '*num_field}|  {'Volontà':{name_field}}|{fields['Grado Volontà']:^{num_field}}|{fields['DVolontà']:^{num_field}}|
|{' '*(name_field+2)}|{' '*num_field}|{' '*num_field}|  {'Arte della Guerra':{name_field}}|{fields['Grado Arte guerra']:^{num_field}}|{fields['DArteGuerra']:^{num_field}}|
|  {'Audacia':{name_field}}|{fields['Mod Audacia']:^{num_field}}|{fields['Audacia']:^{num_field}}|  {'Autorità':{name_field}}|{fields['Grado Autorità']:^{num_field}}|{fields['DAutorità']:^{num_field}}|
|{' '*(name_field+2)}|{' '*num_field}|{' '*num_field}|  {'Cavalcare':{name_field}}|{fields['Grado Cavalcare']:^{num_field}}|{fields['DCavalcare']:^{num_field}}|
|{' '*(name_field+2)}|{' '*num_field}|{' '*num_field}|  {'Teologia':{name_field}}|{fields['Grado Teologia']:^{num_field}}|{fields['DTeologia']:^{num_field}}|
|{'-'*(name_field+2)}-{'-'*num_field}-{'-'*num_field}|{'-'*(name_field+2)}-{'-'*num_field}-{'-'*num_field}|
|{' '*(name_field+2)}|{' '*num_field}|{' '*num_field}|  {'Agilità':{name_field}}|{fields['Grado Agilità']:^{num_field}}|{fields['DAgilità']:^{num_field}}|
|{' '*(name_field+2)}|{' '*num_field}|{' '*num_field}|  {'Archi':{name_field}}|{fields['Grado Archi']:^{num_field}}|{fields['DArchi']:^{num_field}}|
|  {'Celeritas':{name_field}}|{fields['Mod Celeritas']:^{num_field}}|{fields['Celeritas']:^{num_field}}|  {'Armi Corte':{name_field}}|{fields['Grado Armi Corte']:^{num_field}}|{fields['DArmiCorte']:^{num_field}}|
|{' '*(name_field+2)}|{' '*num_field}|{' '*num_field}|  {'Furtività':{name_field}}|{fields['Grado Furtività']:^{num_field}}|{fields['DFurtività']:^{num_field}}|
|{' '*(name_field+2)}|{' '*num_field}|{' '*num_field}|  {'Manualità':{name_field}}|{fields['Grado Manualità']:^{num_field}}|{fields['DManualità']:^{num_field}}|
|{'-'*(name_field+2)}-{'-'*num_field}-{'-'*num_field}|{'-'*(name_field+2)}-{'-'*num_field}-{'-'*num_field}|
|{' '*(name_field+2)}|{' '*num_field}|{' '*num_field}|  {'Forza':{name_field}}|{fields['Grado Forza']:^{num_field}}|{fields['DForza']:^{num_field}}|
|{' '*(name_field+2)}|{' '*num_field}|{' '*num_field}|  {'Armi Comuni':{name_field}}|{fields['Grado Armi Comuni']:^{num_field}}|{fields['DArmiComuni']:^{num_field}}|
|  {'Fortitudo':{name_field}}|{fields['Mod Fortitudo']:^{num_field}}|{fields['Fortitudo']:^{num_field}}|  {'Armi da Guerra':{name_field}}|{fields['Grado Armi da Guerra']:^{num_field}}|{fields['DArmiGuerra']:^{num_field}}|
|{' '*(name_field+2)}|{' '*num_field}|{' '*num_field}|  {'Atletica':{name_field}}|{fields['Grado Atletica']:^{num_field}}|{fields['DAtletica']:^{num_field}}|
|{' '*(name_field+2)}|{' '*num_field}|{' '*num_field}|  {'Lotta':{name_field}}|{fields['Grado Lotta']:^{num_field}}|{fields['DLotta']:^{num_field}}|
|{'-'*(name_field+2)}-{'-'*num_field}-{'-'*num_field}|{'-'*(name_field+2)}-{'-'*num_field}-{'-'*num_field}|
|{' '*(name_field+2)}|{' '*num_field}|{' '*num_field}|  {'Carisma':{name_field}}|{fields['Grado Carisma']:^{num_field}}|{fields['DCarisma']:^{num_field}}|
|{' '*(name_field+2)}|{' '*num_field}|{' '*num_field}|  {'Intrattenere':{name_field}}|{fields['Grado Intrattenere']:^{num_field}}|{fields['DIntrattenere']:^{num_field}}|
|  {'Gratia':{name_field}}|{fields['Mod Gratia']:^{num_field}}|{fields['Gratia']:^{num_field}}|  {'Mercatura':{name_field}}|{fields['Grado Mercatura']:^{num_field}}|{fields['DMercatura']:^{num_field}}|
|{' '*(name_field+2)}|{' '*num_field}|{' '*num_field}|  {'Raggirare':{name_field}}|{fields['Grado Raggirare']:^{num_field}}|{fields['DRaggirare']:^{num_field}}|
|{' '*(name_field+2)}|{' '*num_field}|{' '*num_field}|  {'Usi e Costumi':{name_field}}|{fields['Grado Usi e Costumi']:^{num_field}}|{fields['DUsiCostumi']:^{num_field}}|
|{'-'*(name_field+2)}-{'-'*num_field}-{'-'*num_field}|{'-'*(name_field+2)}-{'-'*num_field}-{'-'*num_field}|
|{' '*(name_field+2)}|{' '*num_field}|{' '*num_field}|  {'Ragionamento':{name_field}}|{fields['Grado Ragionamento']:^{num_field}}|{fields['DRagionamento']:^{num_field}}|
|{' '*(name_field+2)}|{' '*num_field}|{' '*num_field}|  {'Alchimia':{name_field}}|{fields['Grado Alchimia']:^{num_field}}|{fields['DAlchimia']:^{num_field}}|
|  {'Mens':{name_field}}|{fields['Mod Mens']:^{num_field}}|{fields['Mens']:^{num_field}}|  {'Arti Arcane':{name_field}}|{fields['Grado Arti Arcane']:^{num_field}}|{fields['DArtiArcane']:^{num_field}}|
|{' '*(name_field+2)}|{' '*num_field}|{' '*num_field}|  {'Arti Liberali':{name_field}}|{fields['Grado Arti Liberali']:^{num_field}}|{fields['DArtiLiberali']:^{num_field}}|
|{' '*(name_field+2)}|{' '*num_field}|{' '*num_field}|  {'Storia e Leggende':{name_field}}|{fields['Grado Storia e Leggende']:^{num_field}}|{fields['DStoriaLeggende']:^{num_field}}|
|{'-'*(name_field+2)}-{'-'*num_field}-{'-'*num_field}|{'-'*(name_field+2)}-{'-'*num_field}-{'-'*num_field}|
|{' '*(name_field+2)}|{' '*num_field}|{' '*num_field}|  {'Percezione':{name_field}}|{fields['Grado Percezione']:^{num_field}}|{fields['DPercezione']:^{num_field}}|
|{' '*(name_field+2)}|{' '*num_field}|{' '*num_field}|  {'Balestre':{name_field}}|{fields['Grado Balestre']:^{num_field}}|{fields['DBalestre']:^{num_field}}|
|  {'Prudentia':{name_field}}|{fields['Mod Prudentia']:^{num_field}}|{fields['Prudentia']:^{num_field}}|  {'Empatia':{name_field}}|{fields['Grado Empatia']:^{num_field}}|{fields['DEmpatia']:^{num_field}}|
|{' '*(name_field+2)}|{' '*num_field}|{' '*num_field}|  {'Guarigione':{name_field}}|{fields['Grado Guarigione']:^{num_field}}|{fields['DGuarigione']:^{num_field}}|
|{' '*(name_field+2)}|{' '*num_field}|{' '*num_field}|  {'Sopravvivenza':{name_field}}|{fields['Grado Sopravvivenza']:^{num_field}}|{fields['DSopravvivenza']:^{num_field}}|
-{'-'*(name_field+2)}-{'-'*num_field}-{'-'*num_field}-{'-'*(name_field+2)}-{'-'*num_field}-{'-'*num_field}-



Riflessi: {fields['Riflessi attuali']}/{fields['Riflessi massimi']}

-{'-'*(name_field+2)}-{'-'*num_field}-{'-'*num_field}-
|{'Ferite':^{car_size}}|
|{'-'*car_size}|
|{'Tipo':^{name_field+2}}|{'Residue':^{num_field}}|{'Totali':^{num_field}}|
|{'-'*car_size}|
|  {'Graffi':{name_field}}|{fields['Graffi Residue']:^{num_field}}|{fields['Graffitotali']:^{num_field}}|
|  {'Leggere':{name_field}}|{fields['Leggere Residue']:^{num_field}}|{fields['Leggeretotali']:^{num_field}}|
|  {'Gravi -1':{name_field}}|{fields['Gravi Residue']:^{num_field}}|{fields['Gravitotali']:^{num_field}}|
|  {'Critiche -2':{name_field}}|{fields['Critiche Residue']:^{num_field}}|{fields['Critichetotali']:^{num_field}}|
|  {'Mortali -3':{name_field}}|{fields['Mortali Residue']:^{num_field}}|{fields['Mortalitotali']:^{num_field}}|
-{'-'*(name_field+2)}-{'-'*num_field}-{'-'*num_field}-



Spirito: {fields['Spiritoresiduo']}/{fields['Spiritototale']}

-{'-'*(name_field+2)}-{'-'*num_field}-{'-'*num_field}-
|{'Fatica':^{car_size}}|
|{'-'*car_size}|
|{'Tipo':^{name_field+2}}|{'Residuo':^{num_field}}|{'Totale':^{num_field}}|
|{'-'*car_size}|
|  {'Fresco':{name_field}}|{fields['Fresco residuo']:^{num_field}}|{fields['Frescototale']:^{num_field}}|
|  {'Stanco -1':{name_field}}|{fields['Stanco residuo']:^{num_field}}|{fields['Stancototale']:^{num_field}}|
|  {'Sfinito -2':{name_field}}|{fields['Sfinito residuo']:^{num_field}}|{fields['Sfinitototale']:^{num_field}}|
-{'-'*(name_field+2)}-{'-'*num_field}-{'-'*num_field}-



Fama: {fields['Fama']}



-{'-'*(name_field+2)}-{'-'*num_field}-
|{'Valori':^{name_field+num_field+3}}|
|{'-'*(name_field+2)}-{'-'*num_field}|
|{'Nome':^{name_field+2}}|{'Punti':^{num_field}}|
|{'-'*(name_field+2)}-{'-'*num_field}|
|  {'Fides':{name_field}}|{fields['Fides']:^{num_field}}|
|  {'Impietas':{name_field}}|{fields['Impietas']:^{num_field}}|
|{'-'*(name_field+2)}-{'-'*num_field}|
|  {'Honor':{name_field}}|{fields['Honor']:^{num_field}}|
|  {'Ego':{name_field}}|{fields['Ego']:^{num_field}}|
|{'-'*(name_field+2)}-{'-'*num_field}|
|  {'Superstitio':{name_field}}|{fields['Superstitio']:^{num_field}}|
|  {'Ratio':{name_field}}|{fields['Ratio']:^{num_field}}|
-{'-'*(name_field+2)}-{'-'*num_field}-



Focus

{lista_focus(p)}



Armi

{lista_armi(p)}



Armatura

{fields['Armatura 1']}
  Protezione: {fields['Protezione Armatura']}
  Robustezza: {fields['Robustezza Armatura']}
  Note o Pregi: {fields['Note Armatura 1']}



Punti Esperienza:
  Spesi: {fields['PE spesi']}
  Liberi: {fields['PE Liberi']}

-{'-'*(name_field+2)}-{'-'*(name_field+2)}-{'-'*num_field}-{'-'*num_field}-
|{'Artigiano e Professione':^{name_field+2}}|{'Caratteristica':^{name_field+2}}|{'Grado':^{num_field}}|{'Dadi Extra':^{num_field}}|
|{'-'*(name_field+2)}-{'-'*(name_field+2)}-{'-'*num_field}-{'-'*num_field}|
{lista_professioni(p, name_field, num_field)}
-{'-'*(name_field+2)}-{'-'*(name_field+2)}-{'-'*num_field}-{'-'*num_field}-



Tratti

{p.altro}



Talenti

{nl.join(p.talenti)}



Eventi

{nl.join(p.eventi)}



-{'-'*(name_field+2)}-{'-'*num_field}-
|{'Movimento':^{name_field+num_field+3}}|
|{'-'*(name_field+2)}-{'-'*num_field}|
|  {'Ingombro Base':{name_field}}|{fields['Nessun Ingombro']:^{num_field}}|
|  {'Leggero (Base R2)':{name_field}}|{fields['Ingombro Leggero']:^{num_field}}|
|  {'Moderato (Base R4)':{name_field}}|{fields['Ingombro Moderato']:^{num_field}}|
|  {'Pesante (Base R6)':{name_field}}|{fields['Ingombro Pesante']:^{num_field}}|
|  {'Massimo (Base R8)':{name_field}}|{fields['Ingombro Massimo']:^{num_field}}|
-{'-'*(name_field+2)}-{'-'*num_field}-



Denaro (1 Lira = 20 Soldi - 1 Soldo = 12 Denari)

-{'-'*(3*num_field+2)}-
|{'Lire':^{num_field}}|{'Soldi':^{num_field}}|{'Denari':^{num_field}}|
|{'-'*(3*num_field+2)}|
|{fields[lire]:^{num_field}}|{fields['Soldi']:^{num_field}}|{fields['Denari']:^{num_field}}|
-{'-'*(3*num_field+2)}-



Equipaggiamento

{lista_equip(p)}







!!! JSON PER IMPORTARE IL PERSONAGGIO: NON MODIFICARE !!!

JSON: {p.to_json()}
"""
    with open(f"./pdf/{p.nome}.txt", "w") as f:
        f.write(sheet)


def import_from_txt(path):
    with open(path, "r") as f:
        s = f.read().split("JSON: ")[-1] # Si assume che il json sia l'ultima stringa che inizia con 'JSON: '
    json = s.split("\n")[0] # Elimino eventuali righe successive
    savepers(Personaggio.from_json(json))


from redis import exceptions as RExceptions
from itdschargen import CharacterNotFound, Personaggio, loadpers, savepers
from config import PDF
import dataclasses

if __name__=='__main__':
  from sys import exit
  import argparse
  parser = argparse.ArgumentParser(
    prog="Pdffields",
    description="Genera schede personaggio o importa un personaggio da una scheda esistente"
  )
  parser.add_argument("--importa","-i",metavar="PATH",type=str,help="Salva sul database il personaggio contenuto nella scheda")
  parser.add_argument("--esporta","-e",metavar="NOME",type=str,help="Genera la scheda del personaggio chiamato NOME")
  random=False
  a = parser.parse_args()
  if a.esporta is not None:
    try:
      c = loadpers(a.esporta) #TODO sembra che fromjson perda le armi (lista di dataclass)
    except (CharacterNotFound, RExceptions.ConnectionError) as e:
      exit(str(e))
    for field in dataclasses.fields(c):
      field_name = field.name
      field_value = getattr(c, field_name)
      print(f"{field_name}: {field_value}")
    print("-----------------------------------------------------------------")
    if PDF:
        write_pdf(c)
    else:
        write_txt(c)
  elif a.importa is not None:
    try:
      if ".pdf" in a.importa:
        import_from_pdf(a.importa)
      else:
        import_from_txt(a.importa)
    except (KeyError, RExceptions.ConnectionError) as e:
      exit(str(e))
  print("\n>>>\t")
