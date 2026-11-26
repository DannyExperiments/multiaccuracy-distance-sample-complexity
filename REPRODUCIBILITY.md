# Reproducibility

From the repository root, with Python 3.11 or later and Git:

~~~sh
python3 -I scripts/verify_repository.py
python3 -I verification/src/replay.py
~~~

The standard-library replay uses exact fractions. It tests 1,605 lower-bound law pairs over all 181 invertible binary matrices of dimensions one through three, 345 small primal–dual LPs with rank reduction, and 2,728 independent-sign likelihood-ratio comparisons. It checks all nine illustrated repairs and an independent crossing-atom case of the discrete sign-flip identity. [Expected output](verification/logs/replay.txt)

The small primal and dual computations enumerate breakpoints as a diagnostic. The manuscript describes the general sample-polynomial LP estimator and proves the confidence bounds. [Build the manuscript](paper/BUILD.md) · [Rebuild the animation and explorer](visualization/README.md)
