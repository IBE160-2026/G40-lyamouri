# Testdata

Denne mappa har generatoren [`generate_seed.py`](generate_seed.py) og dataene den skriver i [`seed/`](seed/): de to testbedriftene Testbedrift A og Testbedrift B med produkter, salgshistorikk og lager (FR-3, AD-15). Alt er syntetisk. Ingen virkelig bedrift, kunde eller person er med (NFR-4). Story 1.7 laster filene inn i databasen med `load_seed`, og til da leser ingenting i appen dem.

## Generatoren

```
uv run python data/generate_seed.py
```

Den skriver `seed/testbedrift-a.json` og `seed/testbedrift-b.json`, og gir byte for byte de samme filene hver gang, på macOS, Windows og Linux. Seriene lages med heltallsregning, og tilfeldigheten kommer fra SHA-256 av varenummeret og posisjonen, ikke fra klokka eller en tilfeldighetsgenerator. Testene kjører generatoren på nytt og feiler hvis de innsjekkede filene avviker. Fila `.gitattributes` holder JSON-filene med LF-linjeslutt også på Windows, så de ikke avviker fra utdataene. Endrer du generatoren eller [`reference/reference-examples.xlsx`](../reference/reference-examples.xlsx), kjører du kommandoen og committer filene.

Regeltestproduktene og Strøsand 25 kg henter serie og lager fra regnearket, som er fasiten (AD-17). Leseren er [`reference/answer_key_reader.py`](../reference/answer_key_reader.py), den samme som testene bruker. Alle andre produkter lages av generatoren.

Passordhashene lages med Djangos `PBKDF2PasswordHasher`, et fast salt per bedrift og Djangos standard antall iterasjoner. Filene har bare hashen. Et nytt standardantall i en senere Django-versjon får hash-testen til å feile, og da kjører du generatoren på nytt.

## Skjemaet (versjon 1)

Hver fil har én bedrift:

| Felt | Innhold |
|---|---|
| `schema_version` | 1 |
| `customer_number` | kundenummeret, tekst |
| `name` | bedriftens navn |
| `password_hash` | `pbkdf2_sha256$…`, aldri passordet |
| `products` | produktene, sortert etter varenummer |

Hvert produkt:

| Felt | Innhold |
|---|---|
| `product_number` | 5 sifre, tekst. Bedriftene har ulike varenumre |
| `name` | produktnavnet |
| `first_week` | den eldste uka, ISO-uke som «2024-W46» |
| `units_sold` | solgte enheter per uke, eldste først. Posisjon 1 er første tall |
| `stockout_positions` | posisjonene (fra 1) til de utsolgte ukene. En utsolgt uke har tallet i `units_sold` som salg |
| `stock_on_hand` | lager ved slutten av siste registrerte uke (R-13) |

Historikken er en rekke av påfølgende ISO-uker uten hull. Siste registrerte uke lagres ikke. Den er `first_week` pluss antall uker, og er den samme for alle produktene i en bedrift (AD-8): uke 45 i 2026 for Testbedrift A og uke 44 i 2026 for Testbedrift B. Innstillingene lagres ikke her. `load_seed` lager dem fra standardverdiene i FR-20 (story 1.7).

## Bedriftene

| Bedrift | Kundenummer | Passord | Produkter | Siste uke |
|---|---|---|---|---|
| Testbedrift A, en jernvareforretning | 1001 | `testbedrift-a` | 30, varenr. 10001–10043 | 2026-W45 |
| Testbedrift B, hage og hus | 1002 | `testbedrift-b` | 32, varenr. 20001–20032 | 2026-W44 |

## Produktene fra regnearket

De har serie og lager fra [`reference/reference-examples.xlsx`](../reference/reference-examples.xlsx), og arket `products` har de forventede resultatene (DR-3).

| Varenr. | Produkt | Bedrift | Regnearket | Eksempler |
|---|---|---|---|---|
| 10012 | Strøsand 25 kg | A | Strøsand 25 kg | E1, E3, E4, E13 |
| 10025 | Impregnert planke 48×98 mm, 3 m | A | E8 | E8 |
| 20001 | Plantejord 20 l | B | E1 | E1, E2, E3, E4 |
| 20002 | Plengjødsel 10 kg | B | E7 | E7, E17, E29 a |
| 20003 | Hageslange 25 m | B | E9 | E9 |
| 20004 | Frøpose gulrot | B | E10 | E10 |
| 20005 | Terrakottapotte 30 cm | B | E15 | E15 |
| 20006 | Vannkanne 10 l | B | E16 | E16 |
| 20007 | Sagblad 250 mm | B | E18 a | E18 a |
| 20008 | Hagesaks | B | E18 b | E18 b |
| 20009 | Kompostbeholder | B | E19 | E19 |

E8-produktet (10025) er demoproduktet i UJ-1 steg 4. Det har 50 på lager, så behovet er dekket og «Denne uken» holder seg på 4 produkter som bør bestilles snart.

## Demoproduktene i Testbedrift A (UX-DR46)

Tallene og navnene følger mockupen. De tre siste ukene gir ukeprognosen for uke 1, og to mockuptall kan ikke forekomme under reglene, så reglene gjelder: Skruers ukeprognose er 21,3 (ikke 21,5) og Kabelstrips' uker dekning 3,8 (ikke 3,7).

| Varenr. | Produkt | Lager | Ukeprognose uke 1 | Forslag | Tillit |
|---|---|---|---|---|---|
| 10007 | Isskrape | 2 | 8,0 | 7 | høy |
| 10012 | Strøsand 25 kg | 5 | 14,3 | 11 | middels |
| 10031 | Lyspære LED E27 9 W | 12 | 18,7 | 9 | høy |
| 10004 | Skruer 4×40 mm, 200 stk. | 20 | 21,3 | 4 | middels (nytt nivå) |
| 10040 | Snøskuffe aluminium | 6 | ingen, 2 gyldige uker | – | lav |
| 10001 | Malertape 25 mm | 40 | 9,3 | 0 | høy |
| 10002 | Kabelstrips 200 mm | 25 | 6,7 | 0 | høy |
| 10019 | Tetningslist 6 m | 14 | 3,0 | 0 | middels (80 uker) |

«Denne uken» for Testbedrift A skal gi 4 produkter som bør bestilles snart (Isskrape, Strøsand 25 kg, Lyspære og Skruer), 31 enheter, 1 produkt uten prognose og 4 produkter med varsel (Strøsand 25 kg, Skruer, Snøskuffe aluminium og E8-produktet). De 21 andre produktene har ingen utsolgte, uvanlige eller nye nivåuker og lager som dekker behovet. Gruppen kontrollerte tallene med et uavhengig skript for R-1 til R-16, som ikke er committet. Epic 2 kontrollerer dem med kjernen (story 2.8).

## Mønstrene (FR-3, SM-7)

Hvert mønster har minst ett produkt. Testene leser denne tabellen og sjekker at hvert produkt som står her, har mønsteret.

| Mønster | Varenr. |
|---|---|
| Kjent trend | 20011 |
| Sesongmønster uten trend | 20010 |
| Utsolgte uker | 10012, 20012 |
| Uvanlige uker | 10012, 10025, 20013 |
| Nytt nivå | 10004, 20014 |
| Lang rekke utsolgte uker på slutten | 20015 |
| Lager som dekker neste uke | 10001, 10002, 20016 |
| Historikk for «høy» | 10007, 10031, 20016, 20017 |
| Færre enn 3 gyldige uker | 10040, 20018 |
| 3 til 11 gyldige uker | 10025, 20001, 20020 |
| 12 til 103 gyldige uker | 10019, 20019, 20021 |

- Trenden i 20011 stiger 0,2 enheter per uke, fra 10 til 31. Metodene i Prognose ser ikke trend, så prognosen ligger etter (E28).
- Sesongen i 20010 har toppen i uke 26 og bunnen i uke 52, med en indeks fra omtrent 0,5 til 1,6. Det er ingen trend, og de to årene har samme nivå.
- 20012 har utsolgte uker for lenge siden og i de siste 12 ukene. 20013 har to enkeltstående uvanlige uker i de siste 12 ukene. 20014 og 10004 har et nytt nivå i de siste 12 ukene.
- 20015 har de 10 siste ukene utsolgt, så siste gyldige uke ligger mer enn 8 uker før siste registrerte uke (R-15, varselet om gamle data).
- 20018 har 5 uker, der 3 er utsolgte, så den har 2 gyldige uker. 20019 har 12 gyldige uker, grensen mellom «lav» og «middels», og 20020 har 11.
