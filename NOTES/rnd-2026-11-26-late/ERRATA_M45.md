# Errata for miss M45 (units of `w` in the hold rule), 27 November 2026

*Friday 27 November 2026, America/New_York. The files below are hash-locked in `NOTES/rnd-2026-11-26-late/SHA256SUMS` and are not edited. This note sits beside them.*

Each copies the per-item rule of `applications/GROK_BOT_MEMORY_2026-11-23.md` §4 as printed on 23 November, with the drift term \(w\sigma^2T/6\) and \(T^*=\sqrt{6k/(w\sigma^2)}\). Under §4's own definitions (\(w\) the stake when the item is needed, \(p\) the need rate) the drift weight is \(wp/g^2\), where \(g\) is the gap at which a held item is as costly as a dropped one (miss M45 in `NOTES/MISSES-LEDGER.md`; independent review `reviews/pr301_2026-11-27/UNITS_REVIEW.md`). Read them with these substitutions:

| file:line | as locked | read as |
|---|---|---|
| `stepback/TRACKABLE_WORLD.md:46` | \(J(T)=c+k/T+w\sigma^2T/6\), \(J^*=c+2\sqrt{kw\sigma^2/6}\), \(T^*=\sqrt{6k/(w\sigma^2)}\) | \(J(T)=c+k/T+wps\,T/6\), \(J^*=c+2\sqrt{kwps/6}\), \(T^*=\sqrt{6k/(wps)}\), with \(s=\sigma^2/g^2\) |
| `context/MEMORY_CHALLENGE.md:38` | hold rule \(w_ip_i>c_i+2\sqrt{k_iw_i\sigma_i^2/6}\) | \(w_ip_i>c_i+2\sqrt{k_iw_ip_is_i/6}\) |
| `context/MEMORY_CHALLENGE.md:39` | \(T^*=\sqrt{6k/(w\sigma^2)}\); fixed clock \(\sqrt{2k/(w\sigma^2)}\) | \(T^*=\sqrt{6k/(wps)}\); fixed clock \(\sqrt{2k/(wps)}\) |
| `stepback/TRACKABLE_WORLD.md:16` | hold rule \(w p > c + 2\sqrt{k w\sigma^2/6}\) | \(w p > c + 2\sqrt{k\,wps/6}\) |
| `stepback/trackable/prestatement_block.md:8` | hold rule \(w p > c + 2\sqrt{k w\sigma^2/6}\) | \(w p > c + 2\sqrt{k\,wps/6}\) |
| `stepback/NEXT_ROUTES_2026-11-26.md:48` | hold rule \(w p > c + 2\sqrt{k w\sigma^2/6}\) | \(w p > c + 2\sqrt{k\,wps/6}\) |
| `stepback/nextroutes/NEXT_ROUTES_main_block.md:48` | hold rule \(w p > c + 2\sqrt{k w\sigma^2/6}\) | \(w p > c + 2\sqrt{k\,wps/6}\) |
| `stepback/trackable/tw_check.py:4-5` | `J0=c+k/T+w*s2*T/6`, `Ts=sp.sqrt(6*k/(w*s2))` | `w*s2` read as `w*p*s2/g**2`; the checks there (C1 stationarity, C4 limits in \(\sigma^2\)) hold for any positive drift weight |

The qualitative rows (the hold test is the full cost of holding, not storage alone; the barrier interval is a mean, not a fixed clock) are unchanged. Machine check of the corrected rule: `formal/lean/GTAO/MemoryRule.lean` (`fixed_hold_rule`).
