# Scope and limitations

The observation model is a finite full-support domain, labeled IID samples, a fixed predictor with values in [0,1], and access to membership queries for k specified groups. The metric is weighted L1 distance to the simultaneous exact moment constraints. The statistical lower bound holds even on a known marginal over k + 1 points.

For additive error in (0, 1/64], the main bounds give the optimal leading exponent in k at fixed error. Polynomial and logarithmic factors between the finite-parameter bounds remain. The empirical LP has polynomial cost in the sample count, groups and arithmetic precision, so the worst-case superpolynomial sample requirement persists in the overall task.

The streaming estimator applies when the nonzero membership columns are linearly independent. Its elementary testing bound holds on singleton groups and is included along with established discrete L1 connections. The paper makes no claim of unrestricted polynomial auditing, restricted minimax sharpness, or corresponding distance rates for multicalibration.
