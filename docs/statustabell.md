# Statustabell

Statustabellen oppfyller DR-8 i PRD-en. Den viser hvert funksjonskrav (FR) og DR-10 med prioriteten, statusen ved innlevering, storyene, testene og grunnen til et eventuelt avvik.

**Statusene.** Tabellen bruker bare de fire statusene i DR-8: «bygd», «delvis bygd», «ikke bygd» og «endret». «Ikke bygd» uten en grunn betyr at kravet ikke er bygd ennå.

**Oppdatering.** Hver story oppdaterer tabellen når den er ferdig, fordi Definition of Done krever det (DR-7). Story 4.3 fyller ut alle kolonnene, og story 4.4 setter statusen ved innlevering. Da har hver rad som er «delvis bygd», «endret» eller «ikke bygd», en grunn i den siste kolonnen, også kan-ha-kravene (DR-8). Tabellen skal også vise en epic som ikke er bygd (D-2 i `epics.md`), noe story 4.3 legger til. At oppsettet på Windows ikke kunne testes (D-3), står i et eget avsnitt over tabellen, fordi tabellen bare har rader for FR og DR-10 (story 1.3).

**Kolonnene.**
- **Navn:** overskriften til kravet i PRD-en, oversatt til norsk med ordene fra ordlisten i PRD §3.
- **Prioritet:** prioriteten i [PRD-en](../_bmad-output/planning-artifacts/prds/prd-G40-lyamouri-2026-11-02/prd.md) (§8.5). Må-ha er Must, bør-ha er Should, og kan-ha er Could. DR-10 er ikke med i versjon 1 og har ingen av dem (PRD §8.1).
- **Stories:** storyen som bygger kravet, står først. I parentes står de andre storyene i [`epics.md`](../_bmad-output/planning-artifacts/epics.md) som dekker en del av det.
- **Tester:** fylles ut når testene finnes. Hver test nevner FR-n eller E-n som den kontrollerer (DR-5), og en test som ikke kontrollerer noen FR, nevner NFR-, DR- eller AD-ID-ene sine (D-10).

**Status 23. november 2026.** Bare FR-3 er delvis bygd. Prosjektskjelettet fra story 1.1 del A har brukermodellen `web.Company` og databasen i Docker Compose, som FR-1 og FR-4 bygger på, men kravene bygges i story 1.8 og 1.7. Story 1.4 har laget app-skallet og de norske feilsidene (NFR-10, AD-12). FR-2 skal vise siden «Siden finnes ikke» for andre bedrifters produkter, men kravet bygges i story 1.8. Story 1.5 har laget referanseregnearket i `reference/` (DR-3): fasiten med referanseeksemplene, de fire FR-21-variantene og de forventede verdiene for regeltestproduktene. Story 1.6 har laget generatoren `data/generate_seed.py` og de to testbedriftene i `data/seed/` (FR-3), men datasettet er først ferdig når `load_seed` laster det inn i story 1.7, og epic 2 kontrollerer produktene mot kjernen. FR-21 er ikke bygd, fordi innstillingene lages i epic 3. Testene for regnearket står i FR-3- og FR-21-raden.

**Oppsett på Windows (D-3).** Oppsettet med Docker Desktop og oppstarten uten nett er ikke testet på Windows, fordi gruppen ikke har en Windows x64-PC der uv og Docker Desktop kan installeres. Delen uten Docker testes automatisk på Windows Server 2025 x64 i GitHub Actions for hver pull request som endrer koden eller avhengighetene, og passerte første gang 22. november 2026 (se [QA-loggen](qa-logg.md#2026-11-22--oppsettet-på-windows-story-13-sm-2-nfr-1-dr-1-d-3)).

| Krav | Navn | Prioritet | Status | Stories | Tester | Grunn til avvik |
|---|---|---|---|---|---|---|
| FR-1 | Innlogging med kundenummer og passord | må-ha | ikke bygd | 1.8 | `tests/test_company.py`: `test_company_is_the_user_model_with_customer_number_as_login`, `test_password_is_stored_as_a_pbkdf2_hash` og `test_customer_number_is_required`; `tests/test_seed_data.py`: `test_the_files_hold_hashes_that_accept_the_readme_passwords` | – |
| FR-2 | Isolasjon av bedriftens data | må-ha | ikke bygd | 1.8 (2.7, 2.8, 2.11, 3.1, 3.3, 6.2, 6.3, 8.2, 8.3) | – | – |
| FR-3 | Syntetisk datasett med kjente mønstre | må-ha | delvis bygd | 1.6 (1.5, 1.7, 2.6) | `tests/test_reference_spreadsheet.py`: `test_every_rule_test_product_has_its_series_stock_and_expected_results` og `test_products_use_the_series_of_their_source`; `tests/test_seed_data.py`: `test_two_runs_write_identical_files`, `test_the_script_runs_as_the_readme_says`, `test_the_committed_files_equal_a_fresh_run`, `test_the_rule_test_products_come_from_the_workbook`, `test_a_changed_workbook_changes_a_rule_test_product`, `test_a_missing_rule_test_product_stops_the_generator`, `test_a_workbook_product_that_no_company_places_is_refused`, `test_broken_seed_data_is_refused_before_writing`, `test_edits_that_miss_the_history_are_refused`, `test_the_seed_files_have_the_documented_schema`, `test_the_companies_have_the_documented_size_and_numbers`, `test_each_history_ends_at_the_latest_data_week`, `test_the_histories_cover_the_ranges_of_valid_weeks`, `test_every_pattern_has_a_product_that_shows_it`, `test_the_demo_products_of_testbedrift_a_follow_the_mockup` og `test_denne_uken_for_testbedrift_a_matches_the_mockup_and_the_ux_flow`. Testene av passordhashene, filene og stilen (NFR-3, NFR-4, AD-15) står i samme fil | – |
| FR-4 | Data lagres mellom øktene | må-ha | ikke bygd | 1.7 | – | – |
| FR-5 | Glidende gjennomsnitt | må-ha | ikke bygd | 2.2 | – | – |
| FR-6 | Eksponentiell glatting | må-ha | ikke bygd | 2.2 | – | – |
| FR-7 | Prognosehorisont på tre uker | må-ha | ikke bygd | 2.4 (2.5, 2.9) | – | – |
| FR-8 | For lite data | må-ha | ikke bygd | 2.2 (2.5, 2.7) | – | – |
| FR-9 | Sesongjustering | bør-ha | ikke bygd | 5.1 | – | – |
| FR-10 | Tre scenarioer | må-ha | ikke bygd | 2.4 (2.9) | – | – |
| FR-11 | Foreslått bestillingsmengde | må-ha | ikke bygd | 2.4 (2.7) | – | – |
| FR-12 | Utregning av bestillingsmengde | må-ha | ikke bygd | 2.4 (2.9) | – | – |
| FR-13 | Bestillingsmengde per scenario | bør-ha | ikke bygd | 6.1 | – | – |
| FR-14 | Merknad om overlager | bør-ha | ikke bygd | 6.1 | – | – |
| FR-15 | Utsolgte uker holdes utenfor | må-ha | ikke bygd | 2.1 (2.5, 2.9, 2.10) | – | – |
| FR-16 | Uvanlige uker | må-ha | ikke bygd | 2.1 (2.2, 2.5, 2.9, 2.10; bryteren i 3.3) | – | – |
| FR-17 | Nytt nivå | må-ha | ikke bygd | 2.1 (2.2, 2.5, 2.10, 5.2) | – | – |
| FR-17b | Varseltekst for nytt nivå | bør-ha | ikke bygd | 5.2 | – | – |
| FR-18 | Varsel om gamle data | må-ha | ikke bygd | 2.5 | – | – |
| FR-19 | Tillitsmerke | må-ha | ikke bygd | 2.5 (2.7, 4.2, 5.2) | – | – |
| FR-20 | Felles innstillinger for bedriften | må-ha | ikke bygd | 3.1 (5.1, 8.1) | – | – |
| FR-21 | Endringer gjelder alle produktene med en gang | må-ha | ikke bygd | 3.2 (1.5, 3.3, 5.1, 8.1) | `tests/test_reference_spreadsheet.py`: `test_every_fr21_variant_changes_the_setting_the_prd_names` | – |
| FR-22 | Innstillingene lagres mellom øktene | må-ha | ikke bygd | 3.1 | – | – |
| FR-23 | Innstillinger per produkt | kan-ha | ikke bygd | 8.1 | – | – |
| FR-24 | Produktoversikt | må-ha | ikke bygd | 2.8 (2.6, 2.11; 1.8 viser den første produktlisten) | – | – |
| FR-25 | Produktside | må-ha | ikke bygd | 2.7 (2.10, 4.2, 5.2; innstillingene fra produktsiden i 3.2 og 3.3) | – | – |
| FR-26 | Malbasert forklaring på norsk | må-ha | ikke bygd | 2.12 (5.1, 5.2, 6.1, 8.4) | – | – |
| FR-27 | Forklaringen holdes atskilt fra de beregnede tallene | må-ha | ikke bygd | 2.12 (5.1, 5.2, 6.1, 7.1, 8.4, 8.5) | – | – |
| FR-28 | Valgfri lokal språkmodell | bør-ha | ikke bygd | 7.1 | – | – |
| FR-29 | Justere en bestillingsmengde | bør-ha | ikke bygd | 6.2 (6.3, 8.2) | – | – |
| FR-30 | Samlet bestillingsoversikt | bør-ha | ikke bygd | 6.3 (8.3) | – | – |
| FR-31 | Lagre justeringer og merke produkter som godkjent | kan-ha | ikke bygd | 8.2 | – | – |
| FR-32 | Eksportere den samlede bestillingsoversikten | kan-ha | ikke bygd | 8.3 | – | – |
| FR-33 | Lagerbeholdningen varer ikke gjennom uke 2 og 3 | kan-ha | ikke bygd | 8.4 | – | – |
| FR-34 | Prognosenøyaktighet | kan-ha | ikke bygd | 8.5 | – | – |
| FR-35 | Prognoseutregning | må-ha | ikke bygd | 2.9 (5.1) | – | – |
| FR-36 | Varsel om sesongmønster | bør-ha | ikke bygd | 5.2 | – | – |
| DR-10 | Publisering | ikke i versjon 1 | ikke bygd | – (story 1.9 er fjernet; 4.1 sier det i README-en) | – | Publiseringen på Vercel med Neon ble tatt ut av versjon 1 etter [lærerens avklaring på Canvas 19. november 2026](../_bmad-output/planning-artifacts/prds/prd-G40-lyamouri-2026-11-02/avklaring-publisering-2026-11-19.md). Story 1.9 ble fjernet, og DR-10 står igjen i PRD-en som historikk (D-1 i `epics.md`). |
