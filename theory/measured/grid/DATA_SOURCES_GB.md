# GRID-2 raw data (GB; not in git; deleted after the run)
Fetched 20 Nov 2026, 10:04–10:12 AM ET, by curl, no login.
- NESO 1-s system frequency, Nov 2025–Oct 2026: https://api.neso.energy/dataset/cb1cc925-ecd8-4406-b021-3a3f368196e1/resource/<id>/download/fnew-YYYY-M.csv (resource list: package `system-frequency-data`)
- NESO system inertia 2025-26, 2026-27: package `system-inertia`
- NESO Response-Reserve results summary (current dump 596f29ac-0387-4ba4-a6d3-95c243140707; FY2025 archive be55ee51-b79e-47da-b71e-a0f8865d9d66)
- NESO MFR holding volumes 2025-26 D9 (https://www.neso.energy/document/360561/download), 2026-27 D9 (https://www.neso.energy/document/381851/download)
- Elexon BMRS BOALF and PN streams, https://data.elexon.co.uk/bmrs/api/v1/datasets/{BOALF,PN}/stream?from=…&to=…, days 4–11 Jan, 5–12 Apr, 5–12 Jul, 4–11 Oct 2026 (64 files; SHA-256 of their sorted hash list 038588facb6baac05fb665b76e932d32612f7c5589db07504fe11f77c508663f)

SHA-256 (local file names):
```
901fd1ad49cf9c1d3a5803b0d7c6a1466cbe429bb4a92c5a333bbce60bafb3cf  eac_fy2025.csv
9478aa0693f7e76b50f890ba3bf78cb125b01595af0c2cf7a6b916d9bf267c89  eac_summary.csv
d7f9311bf46549143d5c7ee4c7cee681cbaa639e245a02a20226ad8abb01ec5b  f_2025_11.csv
9ed085bd3627dd1dfa4c308b25883becd9e5551ae0210aceb6641f89f2ca3d4d  f_2025_12.csv
91c50b26014087f1c37d8449a467a501e10987ba5c8fd15cf969977ab834dfec  f_2026_01.csv
3afe6fb8e3526377dfb8f813958ff2517b159c2974dcd82eb53b85b3b3e9ea58  f_2026_02.csv
e7592d058f2df0531987298b8c43ebba641615a36b798c76de38b370e9536df7  f_2026_03.csv
799bd9f78f85d953e6fbf48030742b7a6a558a1451a1241c3657a96d26d3c3ce  f_2026_04.csv
c3677df5b38f9681651d38cbce0b82f4fc1a2a3810a8f13bf1bb11e0de59e315  f_2026_05.csv
400105c258a73532cd212c9d55d95df16434a28ce01379168be7bd49554326c9  f_2026_06.csv
1ca3e9e995c32928b475a2914a2dea1b1ddc738d39942f579931d38aec3b3964  f_2026_07.csv
510b37fd12bf932d4771b83bec63fbdb8e0e2bdca79408d54532909b6f517c8a  f_2026_08.csv
7a897109ffd90740f074be46840cbc642729996f266afd8d0b20352740f9ebde  f_2026_09.csv
f38d9a52ec04de55ebda61f4644e3279fb51716a70131d9487fc3f6c4e29e131  f_2026_10.csv
eeeca9b78370d93e896aa4e6e84936eb3e4417d7b6076d5d078f73619a9226fc  inertia_2025-2026.csv
a35f3073323c08de131343d0865c82d0992cf8905ab01afd0dc24a8af5d2ed57  inertia_2026-2027.csv
17cd447cf4f5a9c216b4b48e0f70e2410a5979c7c11918dca2c60e592beb0cac  mfr_360561.bin
1b800c88c9c91d32524685d79975174148f50b3c623e9e5ccef94f848d2e70ad  mfr_381851.bin
```
