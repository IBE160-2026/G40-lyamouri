# Prognose: brainstorming før PRD

## 2026-10-31 kl. 17:43 — mounia.tech03

### Oppgave
Forberede PRD-en for Prognose (G40-lyamouri) ved å avklare hullene i Product Brief og lærerens tilbakemelding. Brukeren ba om forslag til research- og brainstorming-temaer, og kjørte deretter en BMAD-brainstorming om planleggerflyt, periodeenhet og kantfall i beregningene, fulgt av konvergering med MoSCoW.

### Plan
- Sjekket at prosjektmappen og BMAD er på plass, og kjørte `git pull` (to nye commits: `CLAUDE.md` og `sesjonslogg`-skillen).
- Leste `brief.md` og `tilbakemelding-product-brief.md` og foreslo research- og brainstorming-temaer.
- Kjørte `bmad-brainstorming` i stilen Creative Partner, med teknikkene Job to Be Done, Persona Journey, Morphological Analysis og Worst Possible Idea.
- Konvergerte med MoSCoW og sjekket prioriteringene mot briefens suksesskriterier og lærerens krav.
- Lagde et kort intent-dokument til PRD-en.

### Resultat
Opprettet i `_bmad-output/brainstorming/brainstorm-prognose-pre-prd-2026-10-31/`:
- `.memlog.md`: full økt-logg med 74 oppføringer (status `complete`).
- `brainstorm-intent.md`: beslutninger og MoSCoW, skrevet på engelsk som inndata til `/bmad-prd`.

Viktigste beslutninger:
- Jobben er «hvor mye skal jeg bestille neste uke». Bestillingsmengde = `max(0, rund opp(prognose uke 1 + sikkerhetsmargin − lager))`, basert på normalscenario. Optimistisk og pessimistisk vises som alternativer.
- Periodeenhet er uke, horisont 3 uker, 104 uker syntetiske data per produkt pluss noen korte testprodukter. Lager og utsolgt-flagg ligger i dataene.
- Utsolgte uker holdes utenfor, og glidende gjennomsnitt bruker de 3 siste gyldige ukene. 3 eller flere høye uker på rad regnes som mulig nytt normalnivå, ikke avvik.
- Terskler: minst 3 gyldige uker for prognose, varsel ved data eldre enn 8 uker. Lav tillit under 12 gyldige uker, høy ved 104 eller flere uker uten varsler. Vindu større enn gyldige uker gir melding og ingen prognose.
- MoSCoW: sesongjustering flyttet fra Must til Should for å nå fristen. Forklaring uten betalt API er Must. Prosess og repo-ting (dokumentert KI-bruk, `.env.example`, plass for seed-data) lagt til som Must.
- Briefen sier sesong er med i v1, så kuttet må begrunnes i PRD-en.

Ingenting er committet eller pushet i denne økten, etter brukerens uttrykkelige ønske. BMAD-filene (`_bmad/`, `.claude/skills/bmad-*`) var untracked fra før.

### Åpne punkter
- Velge sesongmetode (indeks per uke, estimering fra to år, samspill med avvik og utsolgt-regler) gjennom research.
- Bekrefte «snart må bestilles» som lagerdekning (lager ÷ forventet salg per uke).
- Bekrefte dato for lagerbeholdning som trigger for «usikker lagerbeholdning».
- Avklare avviksjekk i de første ukene og median 0 uten utsolgt-flagg.
- Avklare om manuelle justeringer av bestillingsmengden lagres mellom økter.
- Avklare innholdet i den malbaserte forklaringen og reserven for forklaring med språkmodell.
- Velge teknologistakk og sette innleveringsfristen.
- Oppdatere Product Brief med beslutningene fra økten, slik at historikken viser utviklingen (lærerens råd).
