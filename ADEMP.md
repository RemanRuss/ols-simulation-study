# ADEMP: OLS uncertainty under departures from classical assumptions

## A — Aims
Evaluate whether standard OLS slope confidence intervals achieve nominal 95% coverage as sample size increases, and whether heteroskedasticity-consistent HC3 standard errors improve coverage. Hypotheses: conventional intervals work in the correctly specified homoskedastic Gaussian case; HC3 is more reliable under heteroskedasticity, particularly at moderate-to-large sample sizes. Neither method is guaranteed exact small-sample coverage under heavy tails.

## D — Data-generating mechanisms
In each independently generated replicate, draw `x_i ~ N(0,1)` and set `y_i = 0.5 + 1.0*x_i + eps_i`. Three error settings are compared:

1. **Normal:** `eps ~ N(0,1)` independent of `x`.
2. **Heavy tail:** `eps ~ t(df=3)/sqrt(3)` independent of `x`, so variance is one but rare outliers occur.
3. **Heteroskedastic:** conditional on `x`, `eps ~ N(0, (0.5+x²)/1.5)`; marginal variance is one but conditional variance changes with the predictor.

All errors have conditional mean zero; hence OLS remains unbiased in population. No misspecified conditional mean is introduced. Draw new observations on every replicate. Use `SeedSequence([20261021, n, error_index, replicate])`, independent of execution order. Default number of replicates is 2,000 per scenario.

### Complete design matrix

| Error DGP | n=30 | n=100 | n=500 |
|---|---:|---:|---:|
| Independent normal | 2,000 reps | 2,000 reps | 2,000 reps |
| Independent t(3), standardized | 2,000 reps | 2,000 reps | 2,000 reps |
| Heteroskedastic normal | 2,000 reps | 2,000 reps | 2,000 reps |

Each cell uses *both* interval methods on the *same* 2,000 simulated datasets, yielding 9 DGP-by-size conditions and 18 method-by-condition combinations, with 36,000 method-level rows in total. The normal-error cells are theoretical sanity checks.

## E — Estimands/targets
The true population regression slope is `beta_1 = 1`. The target is the repeated-sampling behavior of the estimated slope and nominal 95% confidence intervals.

## M — Methods
**Conventional OLS:** estimate the slope by least squares, use residual variance `RSS/(n-2)`, conventional covariance `s² (X'X)^(-1)`, and a t critical value with `n-2` df. **OLS + HC3:** use the same OLS slope, but covariance `(X'X)^(-1) X' diag[e_i²/(1-h_ii)²] X (X'X)^(-1)` and asymptotic normal 1.96 critical value. Both methods include an intercept. HC3 guards against heteroskedasticity but is not a robust-to-outlier slope estimator.

## P — Performance measures
For each condition and method calculate average slope bias, empirical SD of slope, root mean squared error (RMSE), mean estimated SE, average confidence-interval width, and empirical 95% interval coverage. For coverage `p_hat`, Monte Carlo SE is `sqrt(p_hat*(1-p_hat)/R)`. Error bars use `p_hat ± 1.96*MCSE`, not confidence intervals for the underlying slope. With R=2,000 and coverage about 0.95, the MCSE is approximately 0.0049. The full raw output is saved before aggregation.

## Interpretation scope
This is a simulation of one-predictor, exogenous linear regression. It does not address biased slopes from endogeneity, nonlinear conditional means, correlated observations, contamination of predictors, high-dimensional problems, or alternative bootstrap intervals. Scenarios are intentionally balanced in marginal error variance; any differences reflect distributional shape or conditional heteroskedasticity rather than arbitrary error-scale changes. Results compare uncertainty methods, not point-estimator performance (which is identical between the two methods).
