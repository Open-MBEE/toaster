# Chapter 7 Conclusion

## What we built

The cumulative model now includes a `state Cycle` with four substates and three transitions. The `DeliveredEnergy` calc def is bound to a sympy expression and evaluated by lambdify, confirming the 67200 J reference value. A parameter sweep over heater power (500–1200 W) produces a matplotlib figure with the design threshold marked.

## What this establishes

The execution and simulation results show that the toaster model is behaviourally consistent: normal and cancel scenarios follow distinct state paths, and the nominal heater (800 W) delivers well above the 50 kJ threshold. The sympy binding proves that the calc def formula is correctly expressed — lambdify and `model.eval()` agree to within 1 J.

## What comes next

Chapter 8 turns the simulation results into formal engineering verdicts by calling `verify_satisfaction()` on the model's `assert satisfy` declarations and recording violation witnesses as ReviewRecords.

## Exercise

See `exercises/ch07/exercise.ipynb`: bind the coffee maker's brew energy formula to sympy, sweep duration, and find the minimum duration that meets a 40 kJ threshold.
