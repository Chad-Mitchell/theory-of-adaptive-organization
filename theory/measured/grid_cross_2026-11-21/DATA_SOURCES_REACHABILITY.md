# GRID-CROSS reachability log (before lock)

Fetched Saturday 21 November 2026, America/New_York, from this environment, without accounts, forms, or API keys. Large archives were checked with HTTP HEAD (status, content-type, content-length) and were not downloaded. Official PDFs that are eligible for Pass 1 scoring were confirmed by HEAD or a capped GET; **no newly reachable PDF was opened for numbers before the lock.**

A "LOGIN_HINT" in an earlier raw crawl meant only that the word "login" or "sign in" appeared somewhere in the page or headers (often a header chrome link). It is not a wall unless the official content was withheld.

## Fetched and eligible (HTTP 200, no account)

| URL | Status | Type | Bytes | Role |
|---|---|---|---|---|
| https://api.neso.energy/api/3/action/datapackage_show?id=system-frequency-data | 200 | JSON | 18,256 | GB 1-s frequency catalog (GRID-2 source; not re-pulled for a new spectrum) |
| https://api.neso.energy/api/3/action/package_show?id=system-inertia | 200 | JSON | 2,593 | GB inertia catalog |
| https://www.neso.energy/data-portal/system-frequency-data | 200 | HTML | (capped) | Landing page for the same package |
| https://www.ofgem.gov.uk/sites/default/files/2023-03/ESORI%20Guidance%20Document%202023-2025.pdf | 200 | PDF | 509,297 | GB operator incentive (S_pen / S_own) |
| https://www.ofgem.gov.uk/sites/default/files/docs/2017/03/final_proposals_for_electricity_system_operator_incentives_from_april_2017.pdf | 200 | PDF | 785,613 | GB BSIS proposals already cited in QUALIFICATION.md |
| https://www.neso.energy/document/356356/download | 200 | PDF | 1,142,444 | FRCR 2025 (S_rel; GB ruin input already used in GRID-DX) |
| https://www.aemc.gov.au/sites/default/files/2026-02/Schedule%20of%20reliability%20settings%20-%202026-27%20financial%20year.pdf | 200 | PDF | 235,556 | Australia reliability settings (was HTTP 403 in GRID-DX). **Not opened for numbers before lock.** |
| https://www.aemc.gov.au/news-centre/media-releases/final-rule-better-control-power-system-frequency | 200 | HTML | 8,439 | AEMC PFR media release |
| https://www.aemc.gov.au/rule-changes/primary-frequency-response-requirement | 200 | HTML | 8,065 | AEMC PFR rule change |
| https://www.aemo.com.au/-/media/files/electricity/nem/security_and_reliability/ancillary_services/frequency-and-time-error-reports/quarterly-reports/2026/frequency-monitoring-q1-2026.pdf | 200 | PDF | 3,004,168 | AEMO Q1 2026 frequency-monitoring report (not a verified 4-s series) |
| https://www.aemo.com.au/-/media/files/electricity/nem/security_and_reliability/ancillary_services/frequency-and-time-error-reports/quarterly-reports/2026/frequency-monitoring-q2-2026.pdf | 200 | PDF | 2,711,586 | AEMO Q2 2026 report |
| https://www.aemo.com.au/-/media/files/electricity/nem/security_and_reliability/ancillary_services/frequency-and-time-error-reports/quarterly-reports/2026/frequency-monitoring-q3-2026.pdf | 200 | PDF | 2,666,439 | AEMO Q3 2026 report |
| https://www.ercot.com/files/docs/2022/10/31/2022%20Biennial%20ERCOT%20Report%20on%20the%20ORDC%20-%20Final_corr.pdf | 200 | PDF | 1,251,273 | ERCOT ORDC / VOLL |
| https://www.ercot.com/news/release/2023-06-12-ercot-adds-new | 200 | HTML | 14,385 | ECRS go-live notice |
| https://www.ercot.com/services/mdt/data-portal | 200 | HTML | 16,358 | States that the Public API requires registration (excluded) |
| https://www.ercot.com/gridinfo | 200 | HTML | 15,750 | ERCOT grid-info landing |
| https://www.eirgrid.ie/ds3-programme-delivering-secure-sustainable-electricity-system | 200 | HTML | 41,623 | DS3 programme |
| https://www.eirgrid.ie/sites/default/files/publications/DS3-SS-Protocol-v4.1-October-2024.pdf | 200 | PDF | 1,042,484 | DS3 System Services Protocol v4.1 (class of source that was 403 in GRID-DX) |
| https://www.eirgrid.ie/sites/default/files/publications/DS3_System_Services_Current_System_Services_Volume_Requirements_Information_Paper.pdf | 200 | PDF | 487,820 | System Services volume requirements |
| https://www.eirgrid.ie/sites/default/files/publications/DS3-Bidders-Information-Session-Volume-Uncapped-Gate-10-9-January-2024.pdf | 200 | PDF | 1,192,561 | Gate 10, 9 Jan 2024 |
| https://www.eirgrid.ie/sites/default/files/publications/DS3-Bidders-Information-Session-26-June-2025.pdf | 200 | PDF | 1,276,763 | Gate 13, 26 June 2025 (via cms.eirgrid.ie 301) |
| https://www.eirgrid.ie/grid/real-time-system-information | 200 | HTML | 82,986 | Real-time dashboard landing; historical CSV/API not verified |
| https://www.eirgrid.ie/ | 200 | HTML | 25,620 | EirGrid home |
| https://www.soni.ltd.uk/ | 200 | HTML | 28,683 | SONI home |
| https://data.fingrid.fi/en/datasets/339 | 200 | HTML | 17,972 | Nordic 10 Hz frequency dataset page (CC BY 4.0) |
| https://data.fingrid.fi/files/339/2026/2026-09.7z | 200 | 7z | 65,757,645 | Direct monthly archive, no API key (HEAD only; closed-loop frequency) |
| https://data.fingrid.fi/en/instructions | 200 | HTML | 9,405 | States that the REST API requires a registered key (excluded) |
| https://www.fingrid.fi/en/grid/power-transmission/maintenance-of-power-balance/ | 200 | HTML | 55,284 | Points to the same frequency archives |
| https://www.svk.se/press-och-nyheter/nyheter/nbm/2022/den-nordiska-kapacitetsmarknaden-afrr-startar-som-planerat-den-7-december-2022/ | 200 | HTML | 24,093 | Nordic aFRR capacity market start |
| https://www.entsoe.eu/network_codes/eb/fcr/ | 200 | HTML | 13,984 | FCR Cooperation |
| https://www.entsoe.eu/news/2022/06/01/go-live-of-picasso-the-pan-european-platform-for-the-international-coordination-of-automatic-frequency-restoration-reserves-and-stable-system-operation/ | 200 | HTML | 7,998 | PICASSO go-live |
| https://www.nerc.com/globalassets/standards/reliability-standards/bal/bal-003-2.pdf | 200 | PDF | 1,107,601 | NERC BAL-003-2 |
| https://www.nerc.com/pa/Stand/Pages/default.aspx | 200 | HTML | 11,494 | Redirects to nerc.com/standards/reliability-standards |
| https://www.eia.gov/electricity/gridmonitor/ | 200 | HTML | 11,681 | EIA Grid Monitor landing (no sub-hourly series retrieved) |
| https://www.eia.gov/electricity/gridmonitor/dashboard/electric_overview/US48/US48 | 200 | HTML | 11,681 | US48 dashboard landing |
| https://www.ofgem.gov.uk/ | 200 | HTML | 25,721 | Ofgem home |
| https://www.hawaiianelectric.com/ | 200 | HTML | 20,700 | Hawaii operator home |
| https://www.hawaiianelectric.com/about-us/performance-scorecards-and-metrics/renewable-energy/rswg-monthly-reports | 200 | HTML | 123,248 | RSWG monthly reports landing |
| https://www.transpower.co.nz/system-operator | 200 | HTML | 6,678 | NZ system operator landing |
| https://www.transpower.co.nz/system-operator/notices-and-reporting/quarterly-system-performance-report | 200 | HTML | (HEAD 200) | NZ quarterly performance reports |
| https://tsoc.org.cy/ | 200 | HTML | 45,300 | Cyprus TSO home |
| https://www.netztransparenz.de/xspproxy/api/staticfiles/ntp-relaunch/dokumente/regelenergie/sek%C3%BCndliche%20frequenz/2022_frequenz.zip | 200 | zip | 48,053,151 | CE 2022 1-s frequency (HEAD only; closed-loop; already in DATA_SOURCES.md) |
| https://www.netztransparenz.de/de-de/Regelenergie/Daten-Regelreserve/Sek%C3%BCndliche-Daten | 200 | HTML | (HEAD 200) | Landing; 1-s aFRR setpoint remains form-gated |

AEMO "What we do" and the frequency-and-time-deviation-monitoring landing page were also retrieved as HTML text by a separate HTTP fetch (WebFetch), without an account, after curl from this environment received HTTP 403 on those HTML paths. Quarterly PDFs under `/-/media/files/...` returned 200 to curl.

Elexon BMRS `https://data.elexon.co.uk/bmrs/api/v1/datasets/BOALF` responds without an account (HTTP 400 JSON, missing From/To). A new multi-day series was not downloaded.

## Fetched and not eligible, or unsuccessful

| URL | Status | Why it is not used |
|---|---|---|
| AEMO HTML paths `/about/what-we-do`, Fast Frequency Response, frequency-monitoring (curl) | 403 | Bot/WAF block to curl; content on the first and third was obtained only via a different fetch, as noted above |
| Guessed AEMO annual "Mainland frequency data 2026" csv/xlsx paths | 302 → 404/403 | Direct file not obtained; 4-s annual series **not included** |
| https://www.ercot.com/services/mdt/data-portal (API section) | 200 page, registration required for the API | Public API excluded |
| Fingrid REST API (described on /en/instructions) | key required | Excluded; static 7z files above are eligible |
| https://transparency.entsoe.eu/ and generation/r2/.../show | 200 JS shell (~4–14 KB HTML) | No data table; API/SFTP need registration; form-gated export unavailable |
| https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32017R1485 | WAF 202 / fetch 403 | SOGL text **not included** |
| https://www.eia.gov/opendata/ | 200 HTML | Page discusses API keys; no keyless series fetched |
| https://www.eia.gov/electricity/930/ | 503 | Not retrieved |
| https://www.eia.gov/electricity/gridmonitor/knownissues/xls/Interchange_latest.xlsx | 200 HTML, not a spreadsheet | Not a data file |
| https://www.elia.be/en/grid-data | 403 | Excluded |
| https://www.tennet.eu/electricity-market/system-information | 403 | Excluded |
| https://www.nationalgrideso.com/ | failed | Successor is neso.energy |
| https://www.aemc.gov.au/energy-system/electricity/electricity-system/reliability-panel | 404 | Guessed path |
| Two guessed historical EirGrid "site-files/library" PDF paths | 404 | Replaced by the 200 PDFs listed above |
| https://www.hawaiianelectric.com/about-us/our-commitment/renewable-energy | 404 | Guessed path |
| https://www.transpower.co.nz/system-operator/operational-information/system-frequency | 404 | Guessed path |
| https://www.ercot.com/mpdatagrid | 404 | Guessed path |

## What this log implies for Pass 2

Institutional sources for Pass 1 are sufficient to attempt S scores for GB, Australia NEM, ERCOT, Ireland/NI, Nordic, and Continental Europe, and to attempt Hawaii or a named substitute. That is not the same as a d1.

No official *pre-control imbalance* series, and no complete DV-GB1.2-style reconstruction kit (frequency + inertia + delivered response/dispatch) for a non-GB grid, was successfully fetched as a data file in this pass. Reachable high-resolution *frequency* archives (Fingrid 10 Hz, NESO 1 s, Netztransparenz 2022 1 s) are closed-loop and, by the locked d1 rule, are not enough. AEMO's 4-s annual frequency files were not fetched. ERCOT high-resolution series sit behind a registration API. ENTSO-E imbalance, where public at all without an account, is not shown here at a resolution that includes 1 min. EIA Grid Monitor pages are reachable but no sub-hourly official series was retrieved.

Unless Pass 2 later finds an official open-loop series or a complete reconstruction kit without an account, the rank test will be **UNTESTED** (n = 1 complete d1, GB only, as in P25).

## Addendum, Saturday 21 November 2026, 2:18 AM EST (after lock; independent review S6)

The independent review of PR #128 noted three missed no-account sources. They were checked again in this environment at about 2:16 AM EST on Saturday 21 November 2026, without accounts, forms, or API keys. Directory listings and dataset pages were fetched with a capped GET for classification only. No zip or archive body was downloaded, and no series was opened for numbers. No official S or d score is computed from this addendum. Closed-loop frequency, a form-gated download, and an API-key route are not treated as a rescue. The conclusion that no-account public sources are insufficient for n ≥ 5 complete (S, d1) pairs is not overturned.

**NEMWEB** (`https://www.nemweb.com.au/Reports/Current/`, HTTP 200, no account). The public report portal is reachable. `FPPDAILY` (`https://www.nemweb.com.au/Reports/Current/FPPDAILY/`, HTTP 200) lists public daily zips (`PUBLIC_NEXT_DAY_FPP_*.zip`). The historical pack that is currently posted is at `https://www.nemweb.com.au/Reports/ARCHIVE/FPPDAILY/` (HTTP 200; monthly `PUBLIC_NEXT_DAY_FPP_*.zip` and weekly `PUBLIC_NEXT_DAY_FPPMW_*.zip`). The path `.../Current/ARCHIVE/FPPDAILY/` returns 404. These FPP / FPPMW zips are listed as unit-level 4-s FPP / MW files, not a system pre-control imbalance series; the zip bodies were not downloaded. `Causer_Pays` and `Causer_Pays_Scada` under `Reports/Current/` return HTTP 200 with no file listing (parent link only). `https://www.nemweb.com.au/Reports/ARCHIVE/Causer_Pays/` returns 404. `https://www.nemweb.com.au/Reports/ARCHIVE/Causer_Pays_Scada/` returns HTTP 200 with no file listing (parent link only). The historical Causer Pays 4-s feed, which official AEMO documentation describes as including Area Control Error, is not currently posted as a fetchable archive at these paths. This is a missed *portal*, not a missed ready d1 series.

**Fingrid dataset 397**, "Calculated imbalance," page `https://data.fingrid.fi/en/datasets/397` (HTTP 200, Content-Length 54,375). The page describes "the momentary calculated net imbalance (ACE open loop) without activated reserves in Finland," 1-minute sampling, dataset ID 397, CC BY 4.0, valid from 25 June 2025 (written 25.6.2025). This is the closest official open-loop imbalance series found in the review, and it sits on the same portal already used for dataset 339. There is no static `/files/397/` archive (`https://data.fingrid.fi/files/397/` returns 404). The REST API requires a registered key, as already recorded for this portal, and is excluded. The `/en/data?datasets=397` route (HTTP 200) is a JavaScript "Download datasets" UI (start/end time fields); the prereg treats a form-gated route as unavailable unless a keyless static file is shown. The series is Finland-only, not a Nordic-area series, and a 1-min sampling interval is a tight fit to a band that must include 1 min. It does not, by itself, create n ≥ 5 complete pairs.

**ERCOT EMIL catalog** (`https://www.ercot.com/mp/data-products`, HTTP 200 without an account). The public catalog page is reachable. The product list is loaded by a JavaScript application and was not retrieved as a static table in this pass; no product zip was downloaded. The independent review classified public frequency products found there as weekly/monthly event or performance zips and a real-time dashboard, not a sub-minute pre-control imbalance series. The registration-required Public API / Data Access Portal remains excluded, as in the pre-lock log. This catalog does not supply a no-account d1 for ERCOT.

