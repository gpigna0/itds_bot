#!/usr/bin/env python3.10
from pdffields import write_pdf
from itdschargen import creazione, deletepers
from os import remove

if __name__ == "__main__":
    p = creazione(True)
    try:
        write_pdf(p)
    except Exception:
        exit("ERROR")
    print("OK")
    remove(f"pdf/{p.nome}.pdf")
    deletepers(p.nome)
