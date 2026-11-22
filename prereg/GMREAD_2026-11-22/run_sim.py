"""Run the locked GMREAD decision code on simulated series only.

Writes JSON to stdout. Does not open a network connection and does not
read a stimulus or spike file.
"""

from __future__ import annotations

import json
import sys

from gmread import demonstrate, power_study


def main(argv):
    n_mc = 200
    if len(argv) > 1:
        n_mc = int(argv[1])
    demo = demonstrate()
    demo["power"] = power_study(n_mc=n_mc)
    labels = sorted({row["label"] for row in demo["scenarios"]})
    demo["labels_produced"] = labels
    demo["every_label"] = all(
        name in labels for name in ("supports", "fails_to_support", "not_a_test")
    )
    json.dump(demo, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    if not demo["every_label"]:
        return 2
    if not demo["power"]["gate_met"]:
        return 3
    if demo["official_real"]["label"] != "not_a_test":
        return 4
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
