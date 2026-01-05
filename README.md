Tento balíček obsahuje kostru protokolů pro předmět Fyzikální praktikum.
Dokument je zkompilovatelný těmito čtyřmi příkazy:

```bash
pdflatex main.tex
bibtex main.aux
pdflatex main.tex
pdflatex main.tex
```

Na linuxovém počítači lze tyto čtyři příkazy spustit naráz, a to spuštěním skriptu `compile.sh`:

```bash
source compile.sh
```

Jak vidno, hlavním souborem je `main.tex`.
V něm se do dokumentu vkládají následující části:
  - Titulní stránka. Pokud si ji student potřebuje upravit, tak musí editovat soubor `title_page.tex`. Pravděpodobně bude potřeba upravit tabulku s bodováním tak, aby odpovídala pravidlům nastaveným v daném semestru Fyzikálního praktika.
  - Jednotlivé sekce protokolu. Student pak při psaní protokolu vyplní soubory ze složky `sections/`. Např. teoretický úvod napíše do souboru `sections/teorie.tex`. Student si samozřejmě může libovolně přidávat další soubory, nebo ubírat podle potřeby.
  - Sekce Ukázky, ve které jsou shrnuty základní příkazy potřebné při psaní textu, vkládání obrázků, tabulek apod. Tato sekce je pouze ilustrativní a nesmí být vložena do výsledného odevzdávaného protokolu. Student tedy před kompilací finálního dokumentu musí zakomentovat tyto dva řádky v souboru `main.tex`:
  
```
\section{Ukázky}
\input{sections/ukazky.tex}
```

Soubor `Praktika.bib` obsahuje množství odkazů na literaturu, které se můžou při psaní protokolů hodit.
Některé jsou specifické pro nějakou konkrétní úlohu, ale jiné jsou využitelné u více úloh.
Tyto odkazy jsou ve formátu vyžadovaném nástrojem BibTeX, který v dokumentech LaTeX generuje seznam použité literatury.
Podle mustru odkazů v `Praktika.bib` si student může do tohoto souboru přidat další odkazy na literaturu, kterou při práci na konkrétních úlohách použil.
Soubor `Praktika.bib` klidně může obsahovat i odkazy, které se v daném protokolu nepoužívají.
Používané odkazy se do textu vkládají příkazem \cite{...} a všechny ostatní se ignorují.

