# Units of w in GROK_BOT_MEMORY §4: independent hostile review (Part A)

*Copied unchanged from the reviewer's box folder `/workspace/units-memrule/` (file name there: `VERDICT.md`, renamed for the wording rule) on 27 Nov 2026.*

Read in full on fresh main de15ab9086128700ae08ff5f3f771bdf1d113d3b:
applications/GROK_BOT_MEMORY_2026-11-23.md (all 82 lines), theory/LAYER_LIFETIME_2026-11-21.md §0–§3
(CL19 at :30, Model LS at :38), CORE.md:27–41 (J = Q̇ + w·E[ℓ]; "w converts the loss into the
currency of the heat"), THEORY.md:87 (CT12) and :384 (CT17).

## 1. What the theory's own definitions force

- CORE.md:27–29: J is a cost *rate*; w is the price of one unit of loss; ℓ is the loss.
- CL19 (LAYER_LIFETIME:30): the gap x costs w·x² per unit time, *all the time*. So there w has
  units currency / (gap² · time). That is a drift weight, and it is right for a layer whose error
  is paid continuously.
- GROK_BOT_MEMORY §4:47–48 defines w_i as "the stake on being wrong **when the item is needed**"
  (currency per need event) and p_i as "the need rate" (1/time). The drop term w_i p_i is then
  currency/time. Correct.
- The drift term w_i σ_i² T_i/6 needs a weight in currency/(gap²·time). With §4's w (currency
  per need) it has units currency·gap² (σ²T is a squared gap): not a cost rate. **The doc uses one symbol
  for two quantities.**

Derivation under §4's own words: the gap is paid only when the item is used. Let g_i be the gap at
which a held item is as bad as a dropped one (loss per need w_i when fully wrong, w_i (x/g_i)² for a
small gap, the quadratic of CL19). Loss rate of a held item = p_i · w_i · E[x²]/g_i². So the drift
weight is

  a_i = w_i p_i / g_i²        (currency per squared gap per time)

and, writing s_i = σ_i²/g_i² (variance rate of the gap in units of g_i; dimension 1/time),

  J = Σ_i [ h_i ( c_i + k_i/T_i + w_i p_i s_i T_i / 6 ) + (1 − h_i) w_i p_i ].

The same w then means the same thing in both terms, which is what CORE's single w requires
(dropped = gap at g, loss w per need; held = gap x, loss w(x/g)² per need).

Correct rules (V_i := w_i p_i, stake × need rate):

1. Hold iff  V > c + 2√(k V s / 6),  equivalently  √V > √(ks/6) + √(ks/6 + c).
2. Re-check interval (mean, barrier rule)  T* = √(6k/(V s)) = √(6k g²/(w p σ²)).
3. Band  b*/g = (6 k s / V)^{1/4},  i.e.  b* = (6 k σ² g² /(w p))^{1/4}.  Mean interval b*²/σ² = T*.
4. Fixed clock: T_fix = √(2k/(V s)), refresh cost √(2kVs) vs barrier 2√(kVs/6).
5. Range: the quadratic loss needs b* ≤ g, i.e. V ≥ 6ks. Past that the loss saturates at the drop
   loss and the formulas are only an upper-bound guide.

So the candidate in the brief is right: T* = √(6kg²/(wpσ²)), hold iff wp > c + 2√(kwpσ²/(6g²)).

## 2. Is there a reading under which §4 is consistent as written?

Not with §4's definitions. Checked readings:

- (R1) w is the drift weight (currency/(gap²·time)). Then the drop term w·p has units
  currency/(gap²·time²): not a cost rate. Consistent only if the drop term is renamed to a separate
  drop loss L_i (= stake × need), and then w is not "the stake when needed" (§4:47 must change),
  and the post's/reply's "stake × need" is a different number from the "stake" in the root.
- (R2) p is a dimensionless fraction of time the item is in use, w a loss rate while in use, gap
  normalized by g. Then w·p is fine, but the drift term w s T/6 charges the gap at full rate even
  when the item is not in use — contradicting "when the item is needed". Consistent only if p = 1.
- (R3) the item misleads continuously while held (gap costs whether needed or not). Not what §4
  says, and then the drop loss should not scale with p either.

So §4 is internally consistent only after a redefinition. Under the definitions it prints, the need
rate must enter T*, the band, and the root in the hold threshold.

## 3. The worked example (§4:57) reverses

c = 1, w = 10, p = 0.2, k = 0.5, σ² = 1 (take g = 1, so s = 1); V = wp = 2.

| | doc (a = w) | consistent (a = wp/g²) |
|---|---|---|
| c + 2√(k a σ²/6) | 2.83 | 1.82 |
| hold? (vs V = 2) | no | **yes** |
| T* | 0.548 | 1.225 |
| b* | 0.740 | 1.107 g (outside b* ≤ g) |

The band exceeds g, so the quadratic is past its range; but capping the band at b = g gives a held
cost c + k s + V/6 = 1.833 < 2, a valid held policy inside the quadratic range. So "hold" stands
under the consistent reading; the doc's "fails the full-cost test" is reversed. (The doc's
qualitative point — storage-only and full-cost tests can disagree — survives with other numbers.)
The answer also depends on g, which is one more input to measure (§6 should list it).

## 4. The public reply

Text judged:
> Keep an item iff stake × need > upkeep + 2√(check cost × stake × drift / 6)
> Re-check it when its drift leaves the band (6 × check cost × drift / stake)^¼
> A role bot bears only part of the loss, so it watches at √(its loss / total loss) of the right rate.

**Classification: (3) wrong as stated under the natural reading.** It is (2) — correct only if
"stake" in the root and band means the drift weight — but that reading makes the same word mean two
different quantities inside one inequality, which is not natural.

- "stake" is fixed by its first use, "stake × need": stake per need (currency). With that meaning,
  the root term √(k · w · σ²) has units currency·gap/√time (or currency/√time with a normalized
  gap); the left side is currency/time. Dimensionally inconsistent. Need must appear inside the
  root: 2√(check cost × stake × need × drift / 6).
- Band: (6 k σ²/w)^{1/4} with w = stake per need has units (gap²/time)^{1/4}, not a gap. Needs
  (6 × check cost × drift / (stake × need))^{1/4}.
- "drift" must mean the drift **variance rate** σ² (squared gap per time), measured in units of the
  gap at which the item is useless (so it is 1/time). Read as a drift speed (gap/time), both lines
  are wrong a second way.
- Line 3 (role-bot √ share) **survives**. The rate is 1/T* ∝ √(drift weight), and the drift weight
  is proportional to the loss the watcher counts under either reading (a = w or a = wp/g²; a share
  of the stake or of the need scales it the same way). A bot that counts fraction f of the loss
  re-checks at √f of the right rate (CT17 (ii) at α = 2; (Λᵢ/Λ)^{1/α} in general). Caveats: same
  check cost and drift for both; it applies to items the bot still holds (the bot's own hold test
  is also stricter, so it may drop items the whole would keep); "rate" is the mean rate under the
  barrier rule.

Corrected reply lines (for the parent; posting needs Chad's approval of exact text):
> Keep an item iff stake × need > upkeep + 2√(check cost × stake × need × drift / 6)
> Re-check it when its gap leaves the band (6 × check cost × drift / (stake × need))^¼
(drift = variance rate of the gap, in units of the gap at which the item is useless.)

## 5. Minimal doc fix (not applied; Part A is read-only)

GROK_BOT_MEMORY §4:
- :44 → J = Σ_i[h_i(c_i + k_i/T_i + w_i p_i s_i T_i/6) + (1 − h_i) w_i p_i].
- :50 → "s_i = σ_i²/g_i² is the variance rate of the item's drift, measured in units of the gap g_i
  at which the held item is as costly as a dropped one (loss per need w_i(x/g_i)² for a small gap)."
- :54 → w_i p_i > c_i + 2√(k_i w_i p_i s_i/6).   :55 → T_i* = √(6k_i/(w_i p_i s_i)).
- :57 → recompute: c + 2√(kwps/6) = 1.82 < wp = 2, so the item is **held**. To keep the point that
  the storage test and the full-cost test can disagree, use numbers inside the quadratic range
  (b* ≤ g): c = 2.5, w = 15, p = 0.2, k = 0.4, σ² = 1, g = 1. Then wp = 3 > c = 2.5, but
  c + 2√(k·wp·s/6) = 2.5 + 2√0.2 = 3.39 > 3, so the item fails the full-cost test; b*/g =
  (6·0.4·1/3)^{1/4} = 0.95 ≤ 1.
- §5:69–70 → b* = (6ks/(wp))^{1/4} g; T_fix* = √(2k/(wps)); fixed cost √(2kwps), barrier 2√(kwps/6).
- §5:74 and §2 quote: the quoted post is preserved text; add a note that its √(6k/(wσ²)) carries the
  same units slip (w there must be stake × need / g²).
- §6:78 → add g_i to the measured inputs.
- Same formula copied at applications/MEMORY_MISS_COST_BOUNDS_2026-11-24.md:52–54,
  NOTES/rnd-2026-11-26-late/stepback/TRACKABLE_WORLD.md:46, NOTES/rnd-2026-11-26-late/context/MEMORY_CHALLENGE.md:38.

Alternative minimal fix (R1): keep the formulas, rename the drift weight a_i, define it as
w_i p_i/g_i², and say so. Either way the need rate enters the root and T*.

Nothing in LAYER_LIFETIME or CT12/CT17 changes: there w is a drift weight on a continuously paid
error, and the formulas are consistent.
