# Chapter 4: Conclusion

## What we built

The Chapter 4 model adds `ApplyHeat`, an action definition with typed flows: bread and energy in, toast, delivered energy and loss out. A balance constraint (`delivered + loss <= energy`) bounds the two outputs by the energy supplied, without assuming any particular efficiency. `ApplyHeat` is nested inside `ToastBread`, the whole-system function Chapter 1 declared with no body, as its first step: `first start; then action applyHeat : ApplyHeat; then done;`. `Start`, `Finish`, and `Cancel` are item definitions naming the cycle's signals, each carrying a `doc` stating that it names a signal, not the bread or toast material flow. The Python side adds `AI-C04`, an `asserted_inference` ReviewRecord claiming the flows this worked example names are accounted for, with `AS-C03` in its `premises` list.

## What this establishes

The chapter answers its engineering question: the toaster now has one functional step, correctly typed and correctly placed. `ApplyHeat` states what the system *does*, bread and energy in, toast and accounted-for energy out, without committing to how the hardware achieves it. The balance constraint is a real, evaluable relation, not a conversion formula: it holds or fails against concrete values, and no specific efficiency is assumed. `ApplyHeat` is no longer free-floating; it is reachable as `ToastBread`'s own step, which is what makes this a decomposition rather than an isolated action. The inference record states the scope honestly: this is a complete flow accounting for the one function modeled, not for the toaster's full functional architecture of roughly fifteen verb-noun functions.

## What comes next

Chapter 5 asks how this one function, and the rest of the toaster's functions, are allocated to logical components and connected by interfaces. It introduces `allocate` for assignment relationships and `flow` for item flows between parts.

**Exercise:** The [Chapter 4 exercise](../../exercises/ch04/exercise.ipynb) asks you to define a `Brew` action for your coffee maker's `BrewUnit`, name its flows with `item def`, and write an `asserted_inference` record claiming the decomposition is complete. Use the same pattern as `ApplyHeat` and `AI-C04`.
