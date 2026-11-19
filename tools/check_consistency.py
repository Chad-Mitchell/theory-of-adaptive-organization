#!/usr/bin/env python3
"""Consistency check for the GTAO repository (stdlib only).

Run from the repo root:  python3 tools/check_consistency.py
Exit code 0 = no FAIL in the maintained (canonical) documents.

What it checks
  1. Versions: THEORY.md's title version and CLAIM_MAP_v2.md's latest "vN note"
     agree with every maintained pointer (README, STATUS, THEORY header, BRIEF).
  2. Banned wording in maintained docs:
       - "law" used of GTAO (any bare 'law' not in an allow-listed compound
         such as 'power law', 'area law', 'law firm', a named physical law,
         or a negation such as 'not a law' / never 'law');
       - "theory of everything" unless negated ('not a theory of everything');
       - a field-test name next to passed/failed/confirmed/refuted/killed in
         the same sentence without a proxy / in-model / gate / tier label;
       - the MV gates described as awaiting Chad's sign-off (they bind as of
         18 Nov 2026, Chad t1927).
       - stale scope phrases ('silent on black holes', 'nothing is keeping
         score', 'no predictions about black holes').
  3. CLAIM_MAP N-rows: every 'N<k>' cited with a CLAIM_MAP context in a
     maintained doc exists in CLAIM_MAP section N, and wherever a maintained
     doc states a status right after a CLAIM_MAP N-number, the base status
     matches the CLAIM_MAP row.
  4. Process rules (lock pass, 18 Nov 2026; reviews/lock_2026-11-18/PROCESS.md):
     R1 no self-review is called independent; R2 the CLAIM_MAP current tally
     equals the rows; R3 table rows have as many cells as their header; R4 no
     named GTAO relation is called a 'law'; R5 the repo is not called private.
Frozen history (locked tests, preregs, review records, night-1/2 working
files, older theory notes) is scanned for the same wording and reported as
INFO only: those files are dated records and are not edited.
"""
import glob, os, re, sys


def main(argv=None):
    """Run every check from the repo root; return the exit code (0 = no FAIL).
    Kept inside main() so importing this module (e.g. pytest collection) has no
    side effects: no chdir, no output, no sys.exit."""
    argv = sys.argv if argv is None else argv
    ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(ROOT)

    MAINTAINED = [
        "README.md", "STATUS.md", "THEORY.md", "QUEUE.md", "BRIEF.md",
        "measurement/FRAMEWORK.md", "measurement/CLAIM_MAP_v2.md",
        "theory/README.md", "theory/SCALE_ENDS.md", "theory/SCALE_ENDS_SUMMARY_FOR_CHAD.md",
        "applications/README.md", "tests/README.md", "reviews/README.md",
        "litmap/LITMAP.md", "litmap/PRIOR_ART.md", "litmap/THREATS.md",
        "litmap/LEFT_ON_THE_TABLE.md", "theory/BOOKENDS.md",
        "theory/REACH.md", "theory/COSMIC_WEB.md", "theory/WORMHOLES.md", "theory/TORUS.md",
    ]
    MAINTAINED = [f for f in MAINTAINED if os.path.exists(f)]
    ALL_MD = sorted(p for p in glob.glob("**/*.md", recursive=True))
    FROZEN = [p for p in ALL_MD if p not in MAINTAINED and not p.startswith("history/")]

    fails, infos = [], []

    def read(p):
        with open(p, encoding="utf-8") as fh:
            return fh.read()

    def lines(p):
        return read(p).split("\n")

    # ---------------------------------------------------------------- 1. versions
    theory = read("THEORY.md")
    m = re.search(r"^# .*? v(1\.4\.\d+[a-z]?) draft", theory, re.M)
    THEORY_V = m.group(1) if m else None
    cm = read("measurement/CLAIM_MAP_v2.md")
    notes = [tuple(int(x) for x in v.split(".")) for v in re.findall(r"^\*\*v(2\.\d+) note", cm, re.M)]
    CM_V = "%d.%d" % max(notes) if notes else None
    print("== 1. Versions")
    print("THEORY.md title: v%s; CLAIM_MAP latest note: v%s" % (THEORY_V, CM_V))
    if not THEORY_V or not CM_V:
        fails.append("versions: could not read THEORY or CLAIM_MAP version")

    # Pointer patterns: (file, regex, which) -- each must match at least once and every match must agree.
    POINTERS = [
        ("README.md", r"canonical statement of the theory \(v(1\.4\.\d+[a-z]?)", "T"),
        ("README.md", r"THEORY\.md\s+The theory, v(1\.4\.\d+[a-z]?)", "T"),
        ("README.md", r"CLAIM_MAP_v2\.md` \(v(2\.\d+)\)", "C"),
        ("STATUS.md", r"\*\*As of:\*\*.*?`THEORY\.md` v(1\.4\.\d+[a-z]?)", "T"),
        ("STATUS.md", r"\*\*As of:\*\*.*?`measurement/CLAIM_MAP_v2\.md` v(2\.\d+)", "C"),
        ("STATUS.md", r"`THEORY\.md` — the theory \(v(1\.4\.\d+[a-z]?)\)", "T"),
        ("STATUS.md", r"`measurement/CLAIM_MAP_v2\.md` \(v(2\.\d+);", "C"),
        ("THEORY.md", r"Claim statuses: `measurement/CLAIM_MAP_v2\.md` \(v(2\.\d+)\)", "C"),
        ("BRIEF.md", r"\*\*Checked against:\*\* THEORY\.md v(1\.4\.\d+[a-z]?)", "T"),
        ("BRIEF.md", r"\*\*Checked against:\*\*[^\n]*?CLAIM_MAP v(2\.\d+)", "C"),
    ]
    for f, rx, which in POINTERS:
        if not os.path.exists(f):
            fails.append("versions: %s missing" % f); continue
        want = THEORY_V if which == "T" else CM_V
        found = re.findall(rx, read(f), re.S if "As of" in rx else 0)
        if not found:
            fails.append("versions: %s has no pointer matching /%s/" % (f, rx)); continue
        bad = [v for v in found if v != want]
        status = "OK" if not bad else "FAIL"
        print("  %-4s %-26s %s -> %s (want v%s)" % (status, f, "THEORY" if which == "T" else "CLAIM_MAP", ",".join("v" + v for v in found), want))
        if bad:
            fails.append("versions: %s points to %s, current is v%s" % (f, ",".join(bad), want))

    # ---------------------------------------------------------------- 2. wording
    LAW_OK = re.compile(
        r"(power[- ]laws?|area[- ]laws?|law firms?|second law|first law|laws? of (thermodynamics|motion|physics|large numbers|their interaction|nature)|"
        r"(Moore|Kleiber|Zipf|Little|Ohm|Hooke|Fick|Weber|Fechner|Hick|Taylor|Heaps|Benford|Lotka|Bergmann|Cope|Haldane|Newton|Wolff|Landauer|Ashby|Goodhart|Conway|Pareto|Allee|Fitts|Weber.Fechner|Kepler|Planck|Stefan.Boltzmann|Wien|Hubble|Curie|Gibrat|Okun|Wagner|Brooks|Parkinson|Murphy)'?s? laws?|"
        r"case law|by law|in-?laws?|lawyers?|lawful|lawsuit|law-like|legal)", re.I)
    NEG_LAW = re.compile(r"(not (a |called a |presented as a )?['\"“‘]?laws?|never (a |be called a |called a )?['\"“‘]?laws?|no ['\"“‘]?laws?['\"”’]?|['\"“‘]law['\"”’]|“law”|‘law’|\"law\"|'law')", re.I)
    GTAO_LAW = re.compile(r"((GTAO|the theory|this theory|our theory|A Theory of Adaptive Organization)('s)?\b[^.;|]{0,40}\b(is|as|becomes|called|calls itself|a|the)\b[^.;|]{0,15}\b(universal |general |new |fundamental )?laws?\b|\b(universal|fundamental|general) laws? of (adaptive|organi[sz]ation|life|persistence)|\blaw of adaptive organi[sz]ation)", re.I)
    TOE = re.compile(r"theor(y|ies) of everything", re.I)
    TOE_NEG = re.compile(r"(not|never|isn't|is not|no)[^.]{0,40}theor(y|ies) of everything|theor(y|ies) of everything['\"”’]?\)?[^.]{0,30}(imposter|banned|withdrawn)", re.I)
    FIELD = re.compile(r"\b(MATCH1|DECISIVE|banks?|glucose|populations|F1|C3b?|BIO1|COLLAPSE1|DRIFT1|measles|PIAAC|Enron|VIGIL[_-]ONA|GITHUB-UPSTREAM|WIKIDATA-BAND|CAISO|SPF|VIX|SENSE-CELL|LANG1|MEASURE-SELF|news(-| )recall|D3S?)\b")
    VERDICT = re.compile(r"(\b(passed|failed|confirmed|refuted|killed|kill fired)\b|\bHIT\b)")
    LABEL = re.compile(r"(proxy|PROXY|in-model|in model|SIM-|simulat|synthetic|dry run|gate|MV\d|Tier|known-groups|prereg|locked|lock |kill rule|joint (kill )?rule|literal|referee|review|power|not a (theory-specific )?hit|sign-only|INCONCLUSIVE|NOT EVIDENCE|MATH-CORRECTED|withdrawn|premise|by construction|reproduce|replicate|own code|own MC|Monte Carlo|pass rule|wrong-pass|[\"“][^\"”]{0,12}(hit|passed|failed)[^\"”]{0,3}[\"”])", re.I)
    SIGNOFF = re.compile(r"(sign[- ]?off|signs off|signed off|once Chad|until Chad|await(s|ing)? Chad)", re.I)
    GATECTX = re.compile(r"(gate|MV\d|M2\b|binding)", re.I)
    STALE = re.compile(r"(silent on black holes|nothing (is )?keeping score|no predictions? about black holes|makes no predictions about black holes)", re.I)
    STALE_OK = re.compile(r"(superseded|\*\*wrong\*\*|was wrong|Ace told Chad|Ace's line|contradicts the record|Never say|never say|withdrawn|stale)", re.I)

    def sentences(text):
        # crude sentence split that keeps table cells apart
        for para in re.split(r"\n|\|", text):
            for s in re.split(r"(?<=[.;!?])\s+(?=[A-Z*(\"“])", para):
                if s.strip():
                    yield s

    def scan_wording(path, sink, tag):
        hits = 0
        for i, ln in enumerate(lines(path), 1):
            if ln.lstrip().startswith(("http", "<!--")):
                continue
            for s in sentences(ln):
                # law: only 'law' used of GTAO / the theory (probability laws,
                # conservation laws, published scaling laws are not GTAO claims)
                for mm in GTAO_LAW.finditer(s):
                    ctx = s[max(0, mm.start() - 20): mm.end() + 40]
                    lawword = s[max(0, mm.end() - 30): mm.end()]
                    if LAW_OK.search(lawword) or NEG_LAW.search(s) or re.search(r"WITHDRAWN", ln):
                        continue
                    sink.append("%s %s:%d law: …%s…" % (tag, path, i, ctx.strip())); hits += 1
                if TOE.search(s) and not TOE_NEG.search(s):
                    sink.append("%s %s:%d theory-of-everything: …%s…" % (tag, path, i, s.strip()[:160])); hits += 1
                if FIELD.search(s) and VERDICT.search(s) and not LABEL.search(s):
                    sink.append("%s %s:%d unlabeled field verdict: …%s…" % (tag, path, i, s.strip()[:200])); hits += 1
                if SIGNOFF.search(s) and GATECTX.search(s) and not re.search(r"(no longer|superseded|bind(s|ing)? as of|was:|before 18 Nov|binding since|nothing awaits|treated as binding)", s, re.I):
                    sink.append("%s %s:%d gates-await-sign-off: …%s…" % (tag, path, i, s.strip()[:200])); hits += 1
                if STALE.search(s) and not STALE_OK.search(s):
                    sink.append("%s %s:%d stale-scope: …%s…" % (tag, path, i, s.strip()[:200])); hits += 1
        return hits

    print("\n== 2. Wording (maintained docs: FAIL; frozen records: INFO)")
    wf = []
    for p in MAINTAINED:
        scan_wording(p, wf, "FAIL")
    fails.extend(wf)
    for x in wf:
        print("  " + x)
    print("  maintained docs scanned: %d; wording FAILs: %d" % (len(MAINTAINED), len(wf)))
    fi = []
    for p in FROZEN:
        scan_wording(p, fi, "INFO")
    infos.extend(fi)
    print("  frozen records scanned: %d; INFO hits (not edited, dated records): %d" % (len(FROZEN), len(fi)))

    # ---------------------------------------------------------------- 3. N rows
    print("\n== 3. CLAIM_MAP section N")
    rows = {}
    for ln in cm.split("\n"):
        mm = re.match(r"^\| (N\d+) \|", ln)
        if mm:
            cells = [c.strip() for c in re.split(r"(?<!\\)\|", ln)]
            rows[mm.group(1)] = cells[4] if len(cells) > 4 else ""
    BASES = ["PROXY-PASS", "PROXY-FAIL", "MATH-CORRECTED", "NOT EVIDENCE", "PRIOR ART", "INCONCLUSIVE", "WITHDRAWN", "DECIDED", "PROVED", "OPEN", "SIM-FAIL", "SIM-PASS", "BINDING"]
    def base(s):
        s = s.replace("*", "")
        for b in BASES:
            if re.search(r"\b" + re.escape(b) + r"\b", s):
                return b
        return None
    print("  rows in CLAIM_MAP section N: %d (%s..%s)" % (len(rows), min(rows, key=lambda k: int(k[1:])), max(rows, key=lambda k: int(k[1:]))))
    cm_ctx = re.compile(r"(CLAIM_MAP|CM)\s*(v2\.\d+\s*)?(rows?\s*)?$")
    nref = re.compile(r"\b(N(\d{1,2}))\b(?:\s*(?:/|,|and|–|-)\s*N\d{1,2})*\s*(?:\(|is |stays |now |moved to |→ |=|:)?\s*\**\s*(PROXY-PASS|PROXY-FAIL|MATH-CORRECTED|NOT EVIDENCE|PRIOR ART|INCONCLUSIVE|WITHDRAWN|DECIDED|PROVED|OPEN|SIM-FAIL)\b")
    nchecked, nfail = 0, 0
    for p in MAINTAINED:
        if p == "measurement/CLAIM_MAP_v2.md":
            continue
        in_theory_s1 = False
        for i, ln in enumerate(lines(p), 1):
            if p == "THEORY.md":
                if ln.startswith("## 1."):
                    in_theory_s1 = True
                elif ln.startswith("## ") and not ln.startswith("## 1."):
                    in_theory_s1 = False
                if in_theory_s1 and ln.startswith("| N"):
                    continue  # THEORY §1 rows N1-N6 are that file's own numbering
            for mm in re.finditer(r"(CLAIM_MAP|CM)[^|.;]{0,25}?\b(N\d{1,2})\b", ln):
                nchecked += 1
                if mm.group(2) not in rows:
                    fails.append("N-ref: %s:%d cites CLAIM_MAP %s, which has no row" % (p, i, mm.group(2))); nfail += 1
            # explicit "N<k> STATUS" statements, including grouped forms like N25/N26 PROVED
            for mm in re.finditer(r"\b((?:N\d{1,2}\s*(?:/|,|and)\s*)*N\d{1,2})\s*(?:stays |is |now |\(|:)?\s*\**(PROXY-PASS|PROXY-FAIL|MATH-CORRECTED|NOT EVIDENCE|PRIOR ART|INCONCLUSIVE|WITHDRAWN|DECIDED|PROVED|OPEN|SIM-FAIL)\b", ln):
                pre = ln[max(0, mm.start() - 4):mm.start()]
                post = ln[mm.end():mm.end() + 40]
                if "§1 " in pre or "§1" == pre.strip():
                    continue
                if re.match(r"[^→.;|]{0,30}→", post) or re.search(r"(was|Was|from)\s*\**\s*$", ln[max(0, mm.start() - 12):mm.start()]):
                    continue  # a recorded transition (old → new), not a current statement
                ids = re.findall(r"N\d{1,2}", mm.group(1))
                st = mm.group(2)
                for nid in ids:
                    nchecked += 1
                    if nid not in rows:
                        fails.append("N-status: %s:%d says %s %s but CLAIM_MAP has no %s" % (p, i, nid, st, nid)); nfail += 1
                    elif base(rows[nid]) != st:
                        fails.append("N-status: %s:%d says %s %s; CLAIM_MAP says %s" % (p, i, nid, st, rows[nid])); nfail += 1
    print("  N references checked: %d; mismatches: %d" % (nchecked, nfail))


    # ---------------------------------------------------------------- 4. process rules
    # Added in the lock pass (reviews/lock_2026-11-18/PROCESS.md, rules R1-R5):
    # each encodes an error type that recurred in the repo's history.
    print("\n== 4. Process rules (reviews/lock_2026-11-18/PROCESS.md)")
    pf = []

    def split_cells(ln):
        """GitHub splits a table row on every unescaped pipe, even inside backticks."""
        t = ln.strip()
        parts = re.split(r"(?<!\\)\|", t)
        if t.startswith("|"):
            parts = parts[1:]
        if t.endswith("|") and not t.endswith("\\|"):
            parts = parts[:-1]
        return parts

    # R1: a self-review must never be called independent.
    # Header marks of a self-review. Widened in the independent review of the lock
    # pass: "**Not independent**" mid-line and "This audit ... is not independent"
    # were missed, so the four lock-pass files were not treated as self-reviews.
    SELF_MARK = re.compile(r"(Independence:\s*\**\s*NOT independent|This pass is not independent|\(NOT independent\)|same executor that wrote|same executor, reread|^\s*\**Not independent\b|\*\*Not independent\b|\bThis (pass|audit|review|file|self-review|self-check)\b[^.]{0,40}\bis not independent\b)", re.I | re.M)
    self_reviews = []
    for p in sorted(glob.glob("reviews/**/*.md", recursive=True)):
        if SELF_MARK.search("\n".join(lines(p)[:15])):
            self_reviews.append(p)
    INDEP = re.compile(r"\bindependent(ly)?\b", re.I)
    INDEP_OK = re.compile(r"(\bnot\s+(an?\s+)?(fully\s+)?independent|\bno(n-?| )independent|self-review|self-check|was called|called it|isn't independent|same executor)", re.I)
    # words between "independent" and the citation that mean the self-review is
    # being contrasted with, not called, an independent review
    BETWEEN_OK = re.compile(r"(supersed|replac|correct|instead of|unlike|\bthan\b|earlier|re-?deriv|checked|reviewed)", re.I)
    pats = [(sr, re.compile(r"(?<![\w-])(?:reviews/)?" + re.escape(sr[len("reviews/"):]))) for sr in self_reviews]
    for p in MAINTAINED:
        for i, ln in enumerate(lines(p), 1):
            for s_ in sentences(ln):
                if not INDEP.search(s_) or INDEP_OK.search(s_):
                    continue
                for sr, rx in pats:
                    # Flag only when "independent" sits next to the citation
                    # ("the independent review `X`", "`X` is independent"), so a
                    # sentence that merely mentions an independent review and a
                    # self-review side by side is not a false positive.
                    def near(m_):
                        w = s_[max(0, m_.start() - 60):m_.start()]
                        k = [x for x in INDEP.finditer(w)]
                        return bool(k) and not BETWEEN_OK.search(w[k[-1].end():])
                    hit = any(near(m_) or
                              re.match(r"[`)\]]*\s*(\([^)]*\)\s*)?,?\s*((which|that)\s+)?(is|was|are|were)\s+(an?\s+)?(fully\s+)?independent", s_[m_.end():])
                              for m_ in rx.finditer(s_))
                    if hit:
                        pf.append("self-review-called-independent: %s:%d calls %s independent (its header says it is not)" % (p, i, sr))
    print("  self-reviews found by header: %d" % len(self_reviews))

    # R2: the CLAIM_MAP current tally must equal the rows.
    TB = ["PROXY-PASS", "PROXY-FAIL", "MATH-CORRECTED", "NOT EVIDENCE", "PRIOR ART", "SIM-INCONCLUSIVE", "INCONCLUSIVE", "WITHDRAWN", "DECIDED", "PROVED", "OPEN", "SIM-FAIL", "SIM-PASS"]
    counted, sec, unknown = {}, None, []
    for ln in cm.split("\n"):
        mm = re.match(r"^## ([A-Z])\.", ln)
        if mm:
            sec = mm.group(1)
        if ln.startswith("## Counts"):
            sec = None
        mm = re.match(r"^\| ([A-Z]{1,2}\d+[′']?[a-z]?) \|", ln)  # two-letter IDs: section O (CT/CL/CX); alias rows "CTk → X" are not counted
        if mm and sec:
            c = split_cells(ln)
            t = c[3].replace("*", "").strip() if len(c) > 3 else ""
            st = next((b for b in TB if t.startswith(b)), None) or next((b for b in TB if b in t), None)
            if not st:
                unknown.append(mm.group(1)); continue
            counted[st] = counted.get(st, 0) + 1
    mm = re.search(r"<!-- tally:begin -->(.*?)<!-- tally:end -->", cm, re.S)
    if not mm:
        pf.append("tally: CLAIM_MAP has no <!-- tally:begin --> block")
    else:
        stated, total = {}, None
        for ln in mm.group(1).split("\n"):
            c = [x.replace("*", "").strip() for x in split_cells(ln)] if ln.startswith("|") else []
            if len(c) == 2 and c[1].isdigit():
                if c[0] == "Total":
                    total = int(c[1])
                else:
                    stated[next((b for b in TB if c[0].startswith(b)), c[0])] = int(c[1])
        if stated != counted:
            pf.append("tally: CLAIM_MAP current tally %s differs from the rows %s" % (stated, counted))
        if total != sum(counted.values()):
            pf.append("tally: CLAIM_MAP tally total %s, rows %d" % (total, sum(counted.values())))
        print("  CLAIM_MAP rows counted: %d (tally total %s)" % (sum(counted.values()), total))
    for u in unknown:
        pf.append("tally: CLAIM_MAP row %s has no recognised status" % u)

    # R3: every table row in a maintained doc has as many cells as its header
    # (an unescaped pipe silently drops the last cell on GitHub).
    nt = 0
    for p in MAINTAINED:
        L = lines(p); fence = False; n = None
        for i, ln in enumerate(L, 1):
            if ln.lstrip().startswith("```"):
                fence = not fence; n = None; continue
            if fence or not ln.lstrip().startswith("|"):
                n = None; continue
            if n is None:
                if i < len(L) and re.match(r"^\s*\|?\s*:?-{3,}", L[i]):
                    n = len(split_cells(ln)); nt += 1
                continue
            if re.match(r"^\s*\|?\s*:?-{3,}", ln):
                continue
            k = len(split_cells(ln))
            if k != n:
                pf.append("table-cells: %s:%d has %d cells, header has %d (escape a pipe as \\|)" % (p, i, k, n))
    print("  tables checked: %d" % nt)

    # R4: no named GTAO relation is called a 'law' ('the sqrt N law'); use 'rule'.
    NAMED_LAW = re.compile(r"(√N|sqrt\(?N\)?|square[- ]root|trail[- ]fade|fade|shared[- ]memory|freeze[- ]or[- ]hold|read[- ]rate|three[- ]cost)\s+(scaling\s+)?laws?\b", re.I)
    # Published names that contain one of those words are prior art, not GTAO claims
    # (e.g. the inventory "square-root law", Maister 1976).
    NAMED_LAW_OK = re.compile(r"(inventor|Maister|pooling of stock|safety stock)", re.I)
    # R5: the repository is public since 18 Nov 2026; never call it private in the present tense.
    PRIVATE = re.compile(r"\b(repo|repository) (is|remains|stays) (still |currently )?private\b|\bthis private (repo|repository)\b", re.I)
    for p in MAINTAINED:
        for i, ln in enumerate(lines(p), 1):
            for s_ in sentences(ln):
                if NAMED_LAW.search(s_) and not NEG_LAW.search(s_) and not NAMED_LAW_OK.search(s_) and "WITHDRAWN" not in ln:
                    pf.append("law-named: %s:%d …%s…" % (p, i, s_.strip()[:160]))
                mp = PRIVATE.search(s_)
                if mp and not (s_[max(0, mp.start() - 1):mp.start()] in "\"“'" or "→" in s_):  # quoted old wording in a changelog is history
                    pf.append("stale-private: %s:%d …%s…" % (p, i, s_.strip()[:160]))
    for x in pf:
        print("  FAIL " + x)
    print("  process-rule FAILs: %d" % len(pf))
    fails.extend("FAIL " + x for x in pf)

    # ---------------------------------------------------------------- summary
    print("\n== Summary")
    print("FAIL: %d   INFO (frozen records): %d" % (len(fails), len(infos)))
    if "-v" in argv:
        for x in infos:
            print("  " + x)
    for x in fails:
        if not x.startswith("FAIL "):
            print("  FAIL " + x)
    print("RESULT:", "PASS" if not fails else "FAIL")
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
