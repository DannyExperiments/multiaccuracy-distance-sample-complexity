# Problem and proof

Given labeled IID samples, a fixed predictor and access to k group memberships, estimate its marginally weighted L1 distance to exact multiaccuracy. [Original auditing question](https://arxiv.org/html/2509.16930#S4)

1. Take an ill-conditioned binary matrix and append a coordinate vector as in Alon and Vũ. The rank-k incidence system on k + 1 points has a one-dimensional kernel whose coordinates have large magnitude relative to the last coordinate. Choose the marginal from those magnitudes and use the signs to set the predictor offsets.
2. Change only the last point's label law. The score cap forces a large distance gap while the divergence between the two labeled laws stays small. Testing gives a lower bound proportional to the maximal inverse entry in absolute value.
3. For the upper bound, write the distance as a dual piecewise-affine objective. Delete dependent group rows and choose a maximizing vertex of a pointed cell. Its active constraints form a square binary system with right-hand side in {−1,1}. This bounds an optimal multiplier using the same inverse-entry parameter.
4. Over that multiplier box, a relative Bernstein estimate works at scale linear in the loss range. Compare the two minimum losses, using that each is at most one. Compute the empirical one with an LP on the observations.

When membership atoms are independent, the constraint set separates by atom. The distance is the sum of absolute atom residual means, so one signed counter per observed atom suffices. [Complete argument](../paper/manuscript.pdf)
