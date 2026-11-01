# Digest: per-owner authorisation / data isolation, claim verification (round 2, assistant isolation-r2-verify)

All pages fetched with WebFetch on 2026-11-01. Quotes are as returned by the fetch tool (a small summarising model), so treat wording as near-verbatim, not guaranteed character-exact. 6 distinct sources read, 9 tool calls used by the digest stage.

## Claim status

| claim | status | one-line basis |
|---|---|---|
| I1 | verified | OWASP Top 10:2025 ranks Broken Access Control #1 and lists IDOR; Authorization and IDOR cheat sheets require a server-side check on every request, deny by default. |
| I2 | partly verified | OWASP says to write unit and integration tests for access control, but no page shows the specific "log in as A, request B's record, expect 403/404" test; WSTG describes it as a manual two-account test. |
| I3 | verified for Flask; Django partly disputed | Flask `get_post` has the author check with 404/403; the Django generic-display page shows filtering by URL publisher, and `request.user` appears only in one prose sentence with no code. |

## Findings
| # | claim | source URL | publisher | pub_date | accessed | confidence | class |
|---|---|---|---|---|---|---|---|
| 1 | A01:2025 Broken Access Control is ranked #1 in the OWASP Top 10:2025 ("Maintaining its position at #1 in the Top Ten"). | https://top10.owasp.org/2025/A01_2025-Broken_Access_Control | OWASP Top 10 project | undated (edition 2025; copyright 2021-2025) | 2026-11-01 | high | I1 |
| 2 | The same page lists as a common flaw "Permitting viewing or editing someone else's account by providing its unique identifier (insecure direct object references)". | https://top10.owasp.org/2025/A01_2025-Broken_Access_Control | OWASP Top 10 project | undated (2025 ed.) | 2026-11-01 | high | I1 |
| 3 | It prescribes deny by default ("Except for public resources, deny by default"), server-side enforcement ("Access control is only effective when implemented in trusted server-side code or serverless APIs") and record ownership ("Model access controls should enforce record ownership"). | https://top10.owasp.org/2025/A01_2025-Broken_Access_Control | OWASP Top 10 project | undated (2025 ed.) | 2026-11-01 | high | I1 |
| 4 | The Authorization Cheat Sheet says an application should "deny access by default", that "Permission should be validated correctly on every request", and that validating "on just the majority of requests is insufficient". | https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html | OWASP Cheat Sheet Series | undated (no date on page) | 2026-11-01 | high | I1 |
| 5 | The Authorization Cheat Sheet says to "Perform access control checks on every request for the specific object or functionality being accessed" and notes that having access to one object of a type does not imply access to every object of that type; it links this to IDOR. | https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html | OWASP Cheat Sheet Series | undated | 2026-11-01 | high | I1 |
| 6 | The IDOR Prevention Cheat Sheet says to "implement access control checks for each object that users try to access" and to "Verify the user's permission every time an access attempt is made"; it states "even with complex identifiers, access control checks are essential", so random IDs are defence in depth, not a substitute. | https://cheatsheetseries.owasp.org/cheatsheets/Insecure_Direct_Object_Reference_Prevention_Cheat_Sheet.html | OWASP Cheat Sheet Series | undated | 2026-11-01 | high | I1 |
| 7 | OWASP A01 says "Developers and QA staff should include functional access control in their unit and integration tests". The page does not use the phrase "automated testing". | https://top10.owasp.org/2025/A01_2025-Broken_Access_Control | OWASP Top 10 project | undated (2025 ed.) | 2026-11-01 | high | I2 |
| 8 | The Authorization Cheat Sheet has a section titled "Create Unit and Integration Test Cases for Authorization Logic" (not "Test Authorization Logic"), saying "automated unit and integration testing of access control logic can help reduce" authorization defects, and "Create tests that validate that the permissions mapped out in the design phase are being correctly enforced". It does not mention CI and gives no concrete company-A-versus-company-B 403/404 example (per the fetched text; the full section was not read verbatim). | https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html | OWASP Cheat Sheet Series | undated | 2026-11-01 | medium | I2 |
| 9 | WSTG-ATHZ-04 (IDOR testing) says "The best way to test for direct object references would be by having at least two (often more) users", then modifying the identifier parameter to see whether another user's record, file or function is reachable. This is a manual penetration-test method, not an automated-test recipe, and it does not name expected status codes. | https://wstg.owasp.org/latest/4-Web_Application_Security_Testing/05-Authorization/04-Insecure_Direct_Object_References/ | OWASP Web Security Testing Guide | undated ("Latest", (c) 2026) | 2026-11-01 | medium | I2 |
| 10 | The Flask tutorial's `get_post(id, check_author=True)` fetches the post, calls `abort(404, ...)` if it is missing, and `abort(403)` if `check_author and post['author_id'] != g.user['id']`; `update` and `delete` call it, so each owner-only view checks ownership on the server. | https://flask.palletsprojects.com/en/stable/tutorial/blog/ | Pallets (Flask documentation 3.1.x) | undated (docs 3.1.x, (c) 2010 Pallets) | 2026-11-01 | high | I3 |
| 11 | The same Flask tutorial's `index` view runs `SELECT ... FROM post p JOIN user u ...` with no WHERE on the author, so it lists all users' posts. The tutorial's ownership check is therefore per-record on update/delete, not a general per-owner data partition. | https://flask.palletsprojects.com/en/stable/tutorial/blog/ | Pallets (Flask documentation 3.1.x) | undated | 2026-11-01 | high | I3 |
| 12 | The tutorial explains `404` "Not Found" and `403` "Forbidden"; the code returns 404 for a missing id and 403 for another user's record, so it distinguishes existence from ownership (the page does not discuss that as an information-leak trade-off). | https://flask.palletsprojects.com/en/stable/tutorial/blog/ | Pallets (Flask documentation 3.1.x) | undated | 2026-11-01 | high | I3 |
| 13 | The Django generic-display page (Django 6.1 docs) shows `get_queryset()` filtering `Book.objects.filter(publisher=self.publisher)` from a URL-captured publisher, and only says in prose: "if we wanted, we could use `self.request.user` to filter using the current user, or other more complex logic." It shows no code that filters by `request.user` and does not frame this as an access-control or ownership pattern. | https://docs.djangoproject.com/en/stable/topics/class-based-views/generic-display/ | Django Software Foundation | undated (Django 6.1 docs) | 2026-11-01 | high | I3 |

## Worked example(s) / formulas
None requested.

## Leads worth chasing
- A source that actually shows a per-owner test (log in as user A, request B's record, assert 403/404), for example framework test-client docs (Django test client, Flask test client) or OWASP ASVS requirements on access-control verification. Not read in this round.
- Django docs that explicitly show `request.user` in a queryset filter (for example the authentication topic page or a tutorial); not found on the page checked.
- OWASP Top 10 A01 is documented separately from the cheat sheets; the cheat sheets have no dates, so their freshness cannot be established from the pages themselves.
- 403 versus 404 for another owner's record (existence disclosure): Flask returns 403; no source was read on which is preferred.

## Not found / could not verify
- A concrete "company A requests company B's record and expects 403/404" test example in any OWASP page read (I2 as phrased is not evidenced word-for-word).
- Publication or last-updated dates for both cheat sheets, the Top 10 A01 page and the WSTG page; none shown.
- The first WSTG URL I tried (wstg.owasp.org/latest/.../05-Authorization_Testing/04-Testing_for_Insecure_Direct_Object_References/) returned 404; the page was reached via a search result at the restructured path used in row 9.
- Django `request.user` code example: not on the page checked.
