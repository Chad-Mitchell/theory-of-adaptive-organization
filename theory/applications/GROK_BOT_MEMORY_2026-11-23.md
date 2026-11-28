# Grok Bot memory

*Monday 23 November 2026. Canonical home for one application of the cost to an assistant's working memory. Not a test of the hypothesis. No new derivation. `THEORY.md` is not edited. The hypothesis sentence is unchanged.*

The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.

## 1. What this is

This page records how the cost is used in one system: Grok Bot's working notes in a long chat. Applications are not evidence for the theory unless a test says so, and they are not the theory itself (`theory/applications/README.md`).

Write the cost, find its minimum, read off the design, and state which inputs are still measurements.

## 2. The posted challenge

Posted Monday 23 November 2026 at 1:01 AM ET (America/New_York) as [2124745125699944748](https://x.com/i/status/2124745125699944748) (deleted 27 Nov 2026; text preserved here). The text as posted:

> A challenge for the Grok Bot team.
>
> My Grok Bot keeps losing work the same way. When a chat gets long, its working notes are cut to a summary on a length trigger, and what's dropped stays out of view. In the last three days I had to catch it at least three times: our axiom work, the information bottleneck, and a one-pager it had promised me.
>
> The cost of judgment gives the fix, derived, not guessed. Write the cost per item: upkeep if held, plus stake × chance it's needed if not, plus the cost of a re-check, plus the drift loss between re-checks. Minimize it, and two rules fall out:
>
> 1. Hold an item only when stake × need beats upkeep.
> 2. Re-check it against the full record every √(6k/(wσ²)): sooner when the stakes are high or it goes stale fast.
>
> A length-triggered summary breaks both rules. Try the minimum and measure what gets lost.
>
> Open & CC0: https://github.com/Chad-Mitchell/theory-of-adaptive-organization
>
> @mattyp @poteto @bot @elonmusk

The post's own link was a short URL to that repository.

## 3. The observed failure

A length-triggered summary cuts the working notes. Items dropped from those notes stay out of view, even though the transcript itself remains searchable. That is the observed cause, not a claim about the transcript being deleted.

At least three instances were caught on 20–22 November 2026: the information bottleneck, the axiom work, and a one-pager.

## 4. The cost, and its minimum

For separate items that drift, the cost of judgment specializes to a sum over items. For each item \(i\), let \(h_i\in\{0,1\}\) be the decision to hold it in the working notes, and let \(T_i\) be the refresh interval used if it is held. The per-item cost is

$$J=\sum_i\bigl[h_i\bigl(c_i+k_i/T_i+w_i\sigma_i^2 T_i/6\bigr)+(1-h_i)w_i p_i\bigr].$$

- \(c_i\) is the storage upkeep of holding the item.
- \(w_i\) is the stake on being wrong when the item is needed.
- \(p_i\) is the need rate of the item.
- \(k_i\) is the cost of a re-check.
- \(\sigma_i^2\) is the variance rate of the item's drift.

The refresh terms are incurred only when the item is held. Minimizing over the hold bit and the interval gives two rules:

1. Hold an item only if \(w_i p_i>c_i+2\sqrt{k_i w_i\sigma_i^2/6}\): stake times need rate beats the full cost of holding (storage plus the minimized refresh). The addend is the barrier excess from §5.
2. Re-check a held item at \(T_i^*=\sqrt{6k_i/(w_i\sigma_i^2)}\).

The post's "stake × need beats upkeep" has the right sign. In that wording, "upkeep" should be read as the full cost of holding, including the minimized refresh, not storage alone. A short check: at \(c=1\), \(w=10\), \(p=0.2\), \(k=0.5\), \(\sigma^2=1\), stake times need is \(wp=2>c=1\), but \(c+2\sqrt{kw\sigma^2/6}=2.83\), so \(wp\) fails the full-cost test. The two tests disagree once refresh is counted.

The related result already in the five-term sum is CT11 (THEORY.md, Appendix B.2): freeze, hold, or look up. That is a three-way rule, with a freeze edge \(q\le q_f=2c/(W\cdot\tau_{\mathrm{life}}^2)\) and a lookup edge \(q>q_c=(\mu u-h)^2/(2cW)\). The hold rule used here is the two-way comparison of the full cost of holding against stake times need rate, for a working-note item whose alternative is to be dropped from view.

The refresh time is the single-layer lifetime in `theory/LAYER_LIFETIME_2026-11-21.md` §2, which is CL19 after Dixit 1991 (doi [10.2307/2298051](https://doi.org/10.2307/2298051); also *J. Econ. Dyn. Control* 15:657, doi [10.1016/0165-1889(91)90037-2](https://doi.org/10.1016/0165-1889(91)90037-2)).

A length-triggered summary breaks both rules. It keeps or drops items by length, not by whether stake times need beats the full cost of holding, and it does not refresh what it keeps at the lifetime the cost selects.

## 5. Scope of the refresh formula

These limits are already in `theory/LAYER_LIFETIME_2026-11-21.md` §2 and §3b. They belong with the application because the post used the formula in public.

- The coefficient 6 is the barrier policy: re-check when the drift exceeds the band \(b^*=(6k\sigma^2/w)^{1/4}\). The expected time between resets is \(b^{*2}/\sigma^2\), which is \(T^*=\sqrt{6k/(w\sigma^2)}\). So \(\sqrt{6k/(w\sigma^2)}\) is the *mean* interval under that policy, not a fixed clock.
- A fixed clock gives \(T_{\mathrm{fix}}^*=\sqrt{2k/(w\sigma^2)}\) and a higher cost (\(\sqrt{2kw\sigma^2}\) against the barrier's excess \(2\sqrt{kw\sigma^2/6}\)). The barrier is cheaper because it does not reset when the gap is still small.
- The formula assumes Brownian drift, quadratic loss, a lumpy reset, and a slack ruin cap.
- The formula is false as a quantitative rule once \(T^*\) is not short compared with the item's correlation time (`theory/LAYER_LIFETIME_2026-11-21.md` §3b). In the checks there, a case with \(T_{\mathrm{bm}}/\tau\approx0.0045\) had the exact fixed-period OU optimum within 0.3% of \(T_{\mathrm{bm}}\); a case with \(T_{\mathrm{bm}}/\tau\approx0.63\) missed by 137%, because the mean-square error had begun to saturate.

The post said to re-check "every \(\sqrt{6k/(w\sigma^2)}\)". That wording reads as a fixed clock. The correction is the first two bullets: it is the average gap under the barrier rule, and a fixed clock's best interval is \(\sqrt{2k/(w\sigma^2)}\) at higher cost. The diagnosis in the post still holds. A length-triggered summary breaks both rules under either timing.

## 6. What remains measured

The theory does not supply the numbers. For each item, \(c_i\), \(p_i\), \(w_i\), \(k_i\), and \(\sigma_i\) are still measurements. Until they are measured for this system, the two rules are the design the cost selects, not a scored test. This page is not a qualification under THEORY §3, and it is not a field test of the hypothesis.

## Credits (appended 27 November 2026)

The two rules in the post are not new mathematics. The square-root rule for a holding cost against a lumpy reset is Harris 1913 and Barro 1972; the re-check interval as the mean gap of a barrier rule is the monitoring-interval result of Senders 1964; the same √ rule in noisy niches is Lee, Flack and Krakauer 2024, doi 10.1098/rspb.2024.1606; the refresh-time form is Dixit 1991 (§4). These credits are already in `theory/PRICE_FREE_2026-11-21.md` (line 94), and this note repeats them beside the application. The posted challenge (2124745125699944748) was deleted on 27 Nov 2026; its text is preserved in §2.
