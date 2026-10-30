# External contribution investigation 01: QuantStats price/return ambiguity

**Target:** [ranaroussi/quantstats issue #571](https://github.com/ranaroussi/quantstats/issues/571). This is an **independent reproduction starting point**, not an accepted contribution or upstream PR.

Issue #571 reports a possible flaw in `_prepare_returns`: an input series below $1 may be treated as returns, while the equivalent price series multiplied by ten is converted to returns. Since the library's README describes returns inputs, the maintainers first need to define whether price inputs are actually supported.

## What is here

- `reproduce_quantstats_571.py` creates one deterministic price path, compares a sub-dollar version to an equivalent scaled price series, and uses the issue's documented detection condition.
- With `quantstats` installed, it prints three Sharpes: prices below $1, scaled prices, and actual daily returns.
- `tests/test_repro.py` tests the local synthetic condition, **not** QuantStats itself.

## Run

```bash
pip install pandas numpy pytest quantstats
python -m pytest -q tests
python reproduce_quantstats_571.py
```

**Verification limitation:** QuantStats was not installed in the authoring runtime, so the external-library reproduction has **not** been run. The local deterministic tests do not establish that current upstream releases still exhibit this behavior.

## Before contributing

1. Independently reproduce against the exact current QuantStats release and record versions.
2. Read the issue and related PRs; do not duplicate fixes already in flight.
3. Ask maintainers for clarification of the accepted input contract *in your own words* if still unanswered.
4. Only then write tests and a minimally scoped patch, run the upstream test suite, and disclose AI assistance.

This work is AI-assisted preparation. It is **not** external validation until maintainers independently engage with or accept a contribution.
