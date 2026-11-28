# Exact three-atom repair

Over the rational unit cube for the three-atom example, the two group constraints force mean absolute repair distance at least 1/12. The repair (5/8, 3/8, 1) attains that bound.

This is the worked example. The general estimation algorithm and statistical upper and lower bounds remain in the manuscript.

[Lean source](Q572Repair.lean) · [Mathematical source](../paper/manuscript.tex) · [Expected axiom report](expected-axioms.txt)

Replay from this directory with Lean 4.30.0 and its standard library.

```sh
lean -DwarningAsError=true Q572Repair.lean > axioms.actual
diff -u expected-axioms.txt axioms.actual
```
