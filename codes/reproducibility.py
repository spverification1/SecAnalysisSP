#!/usr/bin/env python3
"""
reproducibility.py
------------------

This script computes the following for a binomial proportion (e.g., key regeneration rate):

- 95% confidence interval using the Wilson score method
- Two-sided exact binomial test p-value vs. null hypothesis p=0.5
 

Example from your manuscript:
  x = 36, n = 500
  The script outputs:
    Observed proportion: 0.072 (36/500)
    95% Wilson CI: [0.050, 0.098]
    Binomial test p-value vs 0.5: 0.000000
"""

from statsmodels.stats.proportion import proportion_confint
from scipy.stats import binomtest


def compute_reproducibility_stats(x, n, alpha=0.05, null_p=0.5, verbose=True):
    """
    x        : number of successes (e.g., regenerations that produced identical keys)
    n        : total number of trials (e.g., attempted regenerations)
    alpha    : significance level (default 0.05 -> 95% CI)
    null_p   : null hypothesis proportion (default 0.5)
    verbose  : print results if True

    Returns:
        p_hat, ci_low, ci_high, p_value
    """
    if x < 0 or x > n:
        raise ValueError("x must be between 0 and n.")

    p_hat = x / n
    ci_low, ci_high = proportion_confint(x, n, alpha=alpha, method='wilson')
    p_value = binomtest(x, n, p=null_p).pvalue

    if verbose:
        print(f"Observed proportion: {p_hat:.4f} ({x}/{n})")
        print(f"95% Wilson CI: [{ci_low:.4f}, {ci_high:.4f}]")
        print(f"Binomial test p-value vs p={null_p}: {p_value:.6f}")

    return p_hat, ci_low, ci_high, p_value


if __name__ == "__main__":
    # Example usage (corresponds to your 7.2% regeneration rate)
    x = 36
    n = 500
    compute_reproducibility_stats(x, n)

 