# Manifest: verbatim copy of the 26 November 2026 R&D notes (Forge)

*Snapshot taken Thursday 26 November 2026 at 19:17 ET from the box folder `<local>/gtao-notes/rnd/` (and `<local>/gtao-notes/WORKLOG.md`). Copied byte for byte; nothing in this folder was edited. Every copied file is listed with its SHA-256 in `SHA256SUMS` beside this file (`sha256sum -c SHA256SUMS` from this folder). Those lock lines are also what keeps the repo's word check from reading these notes as new prose: they are a record, written under the day's working vocabulary, and are kept as they were.*

## 1. What was copied

- **535 files**, about 15.9 MB.
- `stepback/**` from `<local>/gtao-notes/rnd/stepback/` (the step-back notes, every route note, scripts and outputs).
- `review_*/**` from `<local>/gtao-notes/rnd/review_*/` (19 review folders, including `review_worldtrack/`, which held reviewer scripts only at the snapshot).
- `overnight/`: `HOSTILE_REVIEW_FOUNDATIONS.md` (from `rnd/`), `entangle/*.md` with `PREREG_P.sha256` and `PREREG_C.sha256` (both verify), `forces-gravity/*.md`, `selfref/HOSTILE_REVIEW_M11.md` with `PREREG_ROUND13_M.md` and its `.sha256` (verifies), `WORKLOG.md` (from `<local>/gtao-notes/WORKLOG.md`), and the two gate reads under `gate_reads/` (copies of `review_qmsel3/GATE_READ_QMSEL3.md` and `review_fix36/GATE_READ_qmsel2.md`).
- Skipped as not notes: folders named `clone*` (fresh repo clones used by reviewers), `__pycache__`, `.lake`, `.git`.

## 2. In progress at the snapshot

- `stepback/WORLD_TRACK.md`: SHA-256 `084ea69e409645ba1a3a5069ff77a4bc99bb442adf465be9c86a33487779b473` (590 lines), equal to the last WORKLOG entry (19:09 ET, Step 3 STORED-PEAK pre-statement appended, nothing computed). Steps 0–2 scored; Step 3 not run; independent review not finished.
- `stepback/TRACKING_FIRST.md`: SHA-256 `edd9bb00866cfd5d127d8b62c4921301929f23a83bd2680f6e6c65c484e3497f` (563 lines), equal to the last WORKLOG entry (19:13 ET, T1 BLANK-PRICE pre-statement appended, nothing computed). `stepback/trackfirst/` holds its scripts and DOI checks.
- Anything written after 19:17 ET is not in this folder. A final update goes in `NOTES/INDEX-2026-11-27.md` §3.1 (append there), and a later copy of either file should go in a new dated folder rather than over these bytes.

## 3. Withheld (60 files; on the box, not committed)

Reasons: compiled binaries (rebuildable from the `.c` beside them), third-party paper copies (cited by DOI or arXiv id in the notes), binary numeric caches and data files over 5 MB (regenerable by the scripts beside them), and scripts or outputs that contain an email address (a mailbox in a Crossref User-Agent string), withheld so that no address goes into the public repo. Hashes are given so a later copy can be checked.

| path (under `<local>/gtao-notes/rnd/`) | bytes | SHA-256 | reason |
|---|---|---|---|
| `review_c1/rv_crossref.py` | 1468 | `d02dfdd5fdda103c9217bab4c44231803fb867be324744244c154da82f3dca27` | contains an email address (a mailbox in a User-Agent or contact string); withheld to keep addresses out of the public repo |
| `review_c12b/crossref_review.py` | 1124 | `7bae84e2ab23133199e487aeddfcfdac0b68de6d0c804b9d4e0acd80db30dbe9` | contains an email address (a mailbox in a User-Agent or contact string); withheld to keep addresses out of the public repo |
| `review_c12c/still2020.pdf` | 576188 | `c943689722b01828368c2add216bb725a3af6fa42cc54bc2ff807cbbd505cbc3` | third-party paper copy (PDF or full-text extraction); cite by DOI/arXiv instead |
| `review_c12c/still2020.txt` | 42598 | `ea79e3946985e66e8fdbbb4f516616bf80e5e5eb9ebf77ecdc77882a96802c28` | third-party paper copy (PDF or full-text extraction); cite by DOI/arXiv instead |
| `review_c12cg/rv_capacity.py` | 1297 | `7e15a3b8bb3340bff7f01f5bc716e41930a422a23ef7b26166da6577054cdd42` | contains an email address (a mailbox in a User-Agent or contact string); withheld to keep addresses out of the public repo |
| `review_c12cg/rv_encoder_search.py` | 2476 | `eee67ba50aa4dede7ececc71d65e535cd9fb51b501ee022b3e05bf6cb007859b` | contains an email address (a mailbox in a User-Agent or contact string); withheld to keep addresses out of the public repo |
| `review_c12cg/rv_encoder_struct.py` | 2240 | `5a3c437067245743bce8e453568fabacff7965b1050d3f3ed9e3b81c8a3e95ab` | contains an email address (a mailbox in a User-Agent or contact string); withheld to keep addresses out of the public repo |
| `review_c12cg/rv_err.py` | 2068 | `1452aa102fbc17aa646a7ac7ebb520403dc356d677523ed91a7d51db970e7b85` | contains an email address (a mailbox in a User-Agent or contact string); withheld to keep addresses out of the public repo |
| `review_c4/c4_lpp` | 16232 | `a8b29596f86ae5587373807e74701873d365d6bf9d04090fd2be23b09ba288e6` | compiled binary (rebuildable from the .c source beside it) |
| `review_lean6/harary1958.pdf` | 1385406 | `0603939e42a18b3d7d6acf551dcbd3a130dcb81e9b9c3f129ed4efd59e0e5bce` | third-party paper copy (PDF or full-text extraction); cite by DOI/arXiv instead |
| `review_lean6/harary1958.txt` | 28876 | `9487f65bd100e501c0abc26e7c5240af9cad247bc9ba3f15345dfbea26e423f9` | third-party paper copy (PDF or full-text extraction); cite by DOI/arXiv instead |
| `review_lemma_r/rsa2017.pdf` | 590134 | `0696f7c66e0dacf71a18f9d28dc013a8ace8f02ef9e1666b96e3a44b0f125e3a` | third-party paper copy (PDF or full-text extraction); cite by DOI/arXiv instead |
| `review_lemma_r/rsa2017.txt` | 46638 | `32d8699a799e8a27880f79a4e4a08c552a181cc8ecac403a205e5e5f21127a26` | third-party paper copy (PDF or full-text extraction); cite by DOI/arXiv instead |
| `review_srb/crossref_review.py` | 593 | `0eae8aad7f2a68861b9c568a31971636d283ec358ff99e2f0db4d2d1a31eb1f6` | contains an email address (a mailbox in a User-Agent or contact string); withheld to keep addresses out of the public repo |
| `review_srb/dpeven` | 16152 | `c1f2e7cf357e83f2ce2af5c64bd19dc8347d3ff18a483224db0245254d81ea88` | compiled binary (rebuildable from the .c source beside it) |
| `review_srb/dpfast` | 16152 | `5570305c715ebac4bdec4bdb12ecbf5dcc52950cf2337c0f264b28b3c6ff00bb` | compiled binary (rebuildable from the .c source beside it) |
| `review_srb/dpmix` | 16232 | `af2f0243d0345df2af7c72e4d0e8b03aef7b60423cf10d00840d665349d7147e` | compiled binary (rebuildable from the .c source beside it) |
| `review_srb4/rv_core.py` | 2135 | `3541572a4c680745799486e1f2308efb7cbeefed141ff5fa1c8986d6706d652c` | contains an email address (a mailbox in a User-Agent or contact string); withheld to keep addresses out of the public repo |
| `review_srb4/rv_crossref.py` | 1640 | `eb4710dbbd53ee11104d9fa39656afc440e8c64f78cfa8950bc8e9a57c10edb7` | contains an email address (a mailbox in a User-Agent or contact string); withheld to keep addresses out of the public repo |
| `review_srb4/rv_crossref2.py` | 1579 | `579019e8a1e025ecdac41b2009d4ba08e3c37cfdaff19ef54973e61a4182b43f` | contains an email address (a mailbox in a User-Agent or contact string); withheld to keep addresses out of the public repo |
| `review_srb4/rv_curves.npy` | 3397400 | `cb105351c5fa6f22b897cb8e3ea499fb1ea3a695b4d1f49686fd6fd43930b744` | binary numeric cache (regenerable by the script beside it) |
| `review_srb4/rv_curves_antipode.npy` | 1600920 | `1b60dcdf3f0ab24ed18223940b92f1beb7109df789456937d4910e515ffcab53` | binary numeric cache (regenerable by the script beside it) |
| `review_srb4/rv_dp` | 16160 | `9f684deee2f921d16eada628b0d7002a98c16d17a2a5c23f1fe9fd86188645b2` | compiled binary (rebuildable from the .c source beside it) |
| `review_worldtrack/rv_tl.py` | 2476 | `2f50b9b48802def28b8b253d1622a0f128e4ddaadcc8b9e7f0e10b7ae95ce566` | contains an email address (a mailbox in a User-Agent or contact string); withheld to keep addresses out of the public repo |
| `stepback/bgw2020_arxiv1606.09331v3.txt` | 170705 | `e7dfb1de7a1c92f1743cdeaaee3f8643c3128222b8c69c571dc783d42f0fa633` | third-party paper copy (PDF or full-text extraction); cite by DOI/arXiv instead |
| `stepback/c1/crossref_c1.py` | 1062 | `b2b6b38e50ec7ca19b3e2e0d4f2473da33ac23d6ef390d834fd7a43d69a8accf` | contains an email address (a mailbox in a User-Agent or contact string); withheld to keep addresses out of the public repo |
| `stepback/c12cg/crossref_c12cg.py` | 971 | `d6eb20944ba9b98f43946d4cdf4d148713523ed3f766696731cccde7be8c5e7f` | contains an email address (a mailbox in a User-Agent or contact string); withheld to keep addresses out of the public repo |
| `stepback/c12cg/enc_search.py` | 3967 | `81f17fffe856f47d90f910980c8bacd6cbe8201098d0fb9fc839576c0090a533` | contains an email address (a mailbox in a User-Agent or contact string); withheld to keep addresses out of the public repo |
| `stepback/c12cg/exact_err.py` | 1883 | `aac4fec705970b58f70edfb6ee0d39408e88e8e97f0b4d9768e84ff605217dfc` | contains an email address (a mailbox in a User-Agent or contact string); withheld to keep addresses out of the public repo |
| `stepback/c12cg/polygons_committed.py` | 6729 | `1d0cbfcb4b20d5c7a15f46e8b5df2fa413bff86e494aaa9a7ae7783c3e3bd371` | contains an email address (a mailbox in a User-Agent or contact string); withheld to keep addresses out of the public repo |
| `stepback/c12cg/prec.py` | 3840 | `2607edd35508a836cf70c08cb3f2600be17c9ad19526b53d4d2908707b7978b0` | contains an email address (a mailbox in a User-Agent or contact string); withheld to keep addresses out of the public repo |
| `stepback/c4run/c4r_lattice` | 16384 | `6a5ae60f90108b0dd0d8f43673aa03f2db5b7e8223c7a3f9871ae0d48ab1461f` | compiled binary (rebuildable from the .c source beside it) |
| `stepback/c4run/c4r_sprinkle` | 16520 | `f3d355978be9bce57c701a0ad5ca31b1241f07485d645f98de134e14776ac024` | compiled binary (rebuildable from the .c source beside it) |
| `stepback/clue/crossref_clue.py` | 1222 | `eb89e11ebd105ee367c6e674cb76a7c09295020ab6aa1be048cad2b06331ba80` | contains an email address (a mailbox in a User-Agent or contact string); withheld to keep addresses out of the public repo |
| `stepback/clue/flex_check.py` | 1888 | `c94c99188889c181d1a1d461e1be2da816a1c7958e8496f4947648e5bcccb4fa` | contains an email address (a mailbox in a User-Agent or contact string); withheld to keep addresses out of the public repo |
| `stepback/crossref_c12c.py` | 925 | `343bea102329a6a8e50a61e6748e015318e530497a0749ae5bb38eb394acedd5` | contains an email address (a mailbox in a User-Agent or contact string); withheld to keep addresses out of the public repo |
| `stepback/crossref_stepback.py` | 1464 | `5ec07ab4030527a9e29ae5bac5873aa044cab8afc81c8cc9a8aaff9f0c5c80f1` | contains an email address (a mailbox in a User-Agent or contact string); withheld to keep addresses out of the public repo |
| `stepback/crossref_stepback2.py` | 1600 | `24a1efbda6600b333463d5a88e8852f15b4d6969c33191fa9c7a7d1c91a51cb3` | contains an email address (a mailbox in a User-Agent or contact string); withheld to keep addresses out of the public repo |
| `stepback/crossref_stepback3.py` | 869 | `175f69849bc0d5258c72fb781155a149cc8d54cdfbf0bdf4ef6bb00bd1aa376b` | contains an email address (a mailbox in a User-Agent or contact string); withheld to keep addresses out of the public repo |
| `stepback/crossref_stepback4.py` | 871 | `8164de32043d37c423a406b5925691b3ed35046e4c79a26109a790789986c5b3` | contains an email address (a mailbox in a User-Agent or contact string); withheld to keep addresses out of the public repo |
| `stepback/crossref_stepback6.py` | 773 | `64eab1b0b9c7ae2de0acd3e7ba95f8446a3cb37c31df45a9029c599977dff422` | contains an email address (a mailbox in a User-Agent or contact string); withheld to keep addresses out of the public repo |
| `stepback/crossref_stepback7.py` | 703 | `88f579527cd2788ea3e109caf4b24465a21d909dbe9c1ce3207d60fbe5a9653a` | contains an email address (a mailbox in a User-Agent or contact string); withheld to keep addresses out of the public repo |
| `stepback/crossref_stepback8.py` | 671 | `570bca5d5a8e71a253fa8051bc971dd4f77d52d6026a9809e98c0697c6a64e35` | contains an email address (a mailbox in a User-Agent or contact string); withheld to keep addresses out of the public repo |
| `stepback/lemma_r/crossref_lemma_r.py` | 916 | `ed6e9c5900b7cf4cf2c2abec4f3a26de916d095a4ef682d6fc9fc0cdc7b3997c` | contains an email address (a mailbox in a User-Agent or contact string); withheld to keep addresses out of the public repo |
| `stepback/lemma_r/lemma_r_check.py` | 3521 | `7d091c5b6b33b316c11fab07c9337482551580f76d76d9a6fe326b76a26f00b5` | contains an email address (a mailbox in a User-Agent or contact string); withheld to keep addresses out of the public repo |
| `stepback/paper_cv/abs.html` | 42282 | `549b45a31f7ed8984337a29b7b5dd5cae753e78fd135d97a7445cd50b16c2af9` | contains an email address (a mailbox in a User-Agent or contact string); withheld to keep addresses out of the public repo |
| `stepback/paper_cv/paper.pdf` | 1979526 | `d17caccbee57cfbee6fc2eeed2e5a53467c9401be979fd2952aa2bf92d5443af` | third-party paper copy (PDF or full-text extraction); cite by DOI/arXiv instead |
| `stepback/paper_cv/paper.txt` | 421668 | `a1182d98fcc372e5ce4ae7b5807cf2e4bf42f56911d0e2cd7a5f1050e9d60845` | third-party paper copy (PDF or full-text extraction); cite by DOI/arXiv instead |
| `stepback/selfhorizon/crossref_sh.py` | 978 | `55efaa925d0653fc549a65cb4bdc9a9a5cea4698943f8118a9fd963cd4af6a28` | contains an email address (a mailbox in a User-Agent or contact string); withheld to keep addresses out of the public repo |
| `stepback/selfhorizon/crossref_shn.py` | 806 | `fc78a6aef79807f9086aba444374ac5e7fa95c32cb13aaf41fbee08dd9e93e2f` | contains an email address (a mailbox in a User-Agent or contact string); withheld to keep addresses out of the public repo |
| `stepback/selfhorizon/curves_sh.npz` | 26074884 | `2cb7a64168ba40dec3fbeb8d87bbe2992439ed1e469068b0be33d044d2da67f6` | binary numeric cache (regenerable by the script beside it) |
| `stepback/selfhorizon/sh_heat_modes.json` | 37563086 | `1050313a343081ac83dcb56e887a3b14fe9bc623cd635fdd8af5b8ac66e7c870` | data file over 5 MB (regenerable by the script beside it) |
| `stepback/selfhorizon/sh_read_modes.json` | 62366815 | `ad7958fbc76dce17dac53914c71ad34321b2c36754341ca811099e91d0f126c1` | data file over 5 MB (regenerable by the script beside it) |
| `stepback/selfhorizon/sh_read_modes.pkl` | 34979537 | `81315df430ff1f77d991a019e1f35379429910075f67d00d4fbc4b23b406e7b7` | binary numeric cache (regenerable by the script beside it) |
| `stepback/selfhorizon/shdp` | 16280 | `0d60c7d0560f162cf9bd7f6af5dff3dc493ff02d848f4ec279b9dac7188a528b` | compiled binary (rebuildable from the .c source beside it) |
| `stepback/sr_b/crossref_srb.py` | 797 | `f94d21aac7c47d308d9506a33233b1f2dd06808477026af1dc9f9d3380d4e441` | contains an email address (a mailbox in a User-Agent or contact string); withheld to keep addresses out of the public repo |
| `stepback/sr_b4/crossref_srb4.py` | 836 | `e517823ab07a07995331f132bd091ac9b9d7b71f5ee25b51ed06afde138a0030` | contains an email address (a mailbox in a User-Agent or contact string); withheld to keep addresses out of the public repo |
| `stepback/sr_b4/curves_even.npy` | 7311160 | `82cc7d0830e4b375ab67cc9110f4698e81b3305fdfea2c42d5903bba738a341d` | binary numeric cache (regenerable by the script beside it) |
| `stepback/sr_b4/dp4` | 16200 | `2d8352a90e845076bac41b56b787b80a32164602ae3f36cc1830c7d07ebd9156` | compiled binary (rebuildable from the .c source beside it) |
| `stepback/worldtrack/tl_core.py` | 1101 | `5d14c0b8661513a04f07cf005f313812ba328640393e1a81c298a10fe35af075` | contains an email address (a mailbox in a User-Agent or contact string); withheld to keep addresses out of the public repo |

