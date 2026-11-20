# GRID-1 results: BLOCKED (not run)

Prereg locked at `4820d91` (`grid/PREREG_GRID1.md`). Status Friday 20 November 2026: **not run; no outcome data
downloaded or inspected.**

**Exact blocker.** The world signal D(t) needs the German second-wise NRV (aFRR + mFRR activations). On
netztransparenz.de ("Regelenergie → Daten Regelreserve → Sekündliche Daten") it is served only by an ASP.NET
postback button (`btnHiddenNrvSecondlyValueFileDownload`); the page has static GET links only for the
second-wise frequency zips (2012–2022). No account or sign-in is needed, but fetching the file means submitting
the page's form (a POST of its view state), which under the session rules needs Chad's explicit approval. The
alternatives are closed: the netztransparenz API portal needs credentials; ENTSO-E Transparency needs a token
(account). Frequency alone is INVALID by the prereg's premise (closed-loop; the NRV term is required).

**To unblock (one of):** (1) Chad approves a read-only POST of that download form for the 2022 file; (2) Chad
downloads the 2022 second-wise NRV file himself and places it at `theory/measured/grid/data/`; (3) Chad supplies
an existing API token (not created by me). The GB replication (NESO, open GET) is scored only after the CE
verdict, as preregistered, so it does not run first.
