Z, KAPPA = 1.959964, 0.5
def verdict(D, s, b):
    if D + Z * s < KAPPA * b: return "FAIL"
    if D - Z * s > 0: return "PASS"
    return "INCONCLUSIVE"
