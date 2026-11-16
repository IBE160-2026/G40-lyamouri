# QA-logg

QA-loggen oppfyller DR-9 og NFR-4 i PRD-en:
- Hver feil i KI-generert kode eller tekst som en test, referanseregnearket, en gjennomgang eller en manuell test finner, føres med hvordan den ble funnet, rettingen og commiten eller pull requesten.
- Personvernkontrollen av hele Git-historikken føres her, og den gjentas på siste commit før innlevering.
- Den manuelle sjekklisten på siste commit føres her.

**Plassering.** PRD-en lar arkitektursteget fastsette mappene (DR-2). Fila ligger i `docs/` sammen med de andre prosessdokumentene, slik den arkiverte arkitekturen fra 8. november bestemte. Den nye arkitekturen bekrefter plasseringen.

**Tidligere funn.** Feil i KI-generert tekst i planleggingsfasen står under «Kvalitetssikring» i `docs/arbeidslogg.md` og gjentas ikke her.

## 2026-11-16 – Git-forfatteridentiteter i historikken (NFR-4)

**Hvordan det ble funnet.** Mangelen ble først oppdaget i UX-arbeidet 15.–16. november: Git hadde ikke navn og e-post satt i skallet Claude brukte, så commitene fikk identiteten macOS lager automatisk. 16. november kartla Claude forfatteridentitetene på alle grener, `main` og taggen `archive/story-1-1-project-skeleton`.

**Funn.** Forfatteridentitetene i historikken 16. november 2026:

| Identitet | Commits | Vurdering |
|---|---|---|
| Automatisk fra macOS: fullt navn, macOS-brukernavn og maskinnavn. Ett av de to maskinnavnene inneholder fornavnet. | 61 | Bryter NFR-4: fullt navn og lokale maskindata |
| Flettingen av PR #2 på GitHub: GitHub-navnet og skoleadressen | 1 | Bryter NFR-4: e-postadresse |
| Lærerens egne commits, med lærerens navn og skoleadresse | 6 | Tillatt: lærerens egen identitet |
| `Mounia-03` med GitHubs noreply-adresse | alle fra `6245a0a` | I orden |

Adressene og maskinnavnene står ikke her, fordi filene ikke skal ha personopplysninger (NFR-4).

Filene på alle grener og i hele historikken har ingen lokale stier, e-postadresser, nøkler eller tokens. Navnet i medlemslisten i README, personaen «Mounia» og «Mounia-03» i BMAD-konfigurasjonen er vurdert som tillatt. Det gamle brukernavnet i sesjonsloggene, som er første del av en privat e-postadresse, er fjernet fra filene. Det står fortsatt i eldre versjoner av loggene og i commit-meldingen til `6245a0a`.

**Retting.**
- Git-identiteten er satt lokalt i repoet til `Mounia-03` med GitHubs noreply-adresse. Alle commits fra og med `6245a0a` har den.
- Sesjonsloggene er flyttet til `.logs/mounia-03/`, og det gamle brukernavnet er fjernet fra overskriftene (`6245a0a`).

**Beslutning: historikken bevares.** Gamle commits er ikke endret, av fire grunner:
1. Omskriving krever force-push av `main` og de andre grenene, også av flettingen av PR #2 og lærerens commits.
2. Alle commit-hashene som PRD-en, UX-en, arkivet, arbeidsloggen og sesjonsloggene viser til, ville slutte å virke. Det bryter sporbarheten som DR-5 og DR-8 krever.
3. Taggen `archive/story-1-1-project-skeleton` og pull requestene #1 og #2 på GitHub viser til de gamle commitene.
4. Opplysningene er lite sensitive. Navnet står allerede i medlemslisten i README, og ingen passord, nøkler eller tokens er eksponert.

Beslutningen ble tatt 16. november 2026, etter Claudes anbefaling.

**Gjenstår.**
- Slå på «Keep my email addresses private» på GitHub, så flettinger på GitHub ikke bruker skoleadressen igjen.
- Sette samme Git-identitet i andre kloner av repoet.
- Gjenta personvernkontrollen av hele historikken på siste commit før innlevering, og føre resultatet her (NFR-4).
