# Chapter 5 — Conclusion

## What we built

The Chapter 5 model adds three constructs to the cumulative model. `model.find()` and `model.get()` are now the standard navigation layer: notebook 01 confirms they return a `Symbol` for any known qualified name and `None` (rather than an exception) for an unknown name. `allocate ApplyHeat to HeatingSystem` creates an `AllocationUsage` element, visible in the JSON export via `sysx:sourceText` on its connector endpoints. `BreadHandling` introduces the `flow` construct, connecting `loader.bread` to `ejector.bread` as a `FlowUsage` element. The `build_interconnection_intent()` and `render_sysmld()` functions extract those endpoints and render an SVG.

## What this establishes

The chapter answers its engineering question: the toaster model now has formal allocation and interface declarations. The `allocate` statement makes explicit what was implicit — that `HeatingSystem` realizes `ApplyHeat`. The `flow` statement makes the bread-handling interface visible: the loader transfers a `Start`-typed item to the ejector, and the ejector handles `Finish`. The interconnection SVG confirms that the structural connectivity is readable and matches the model.

## What comes next

Chapter 6 asks how deep the decomposition should go. It applies the same structural constructs from Chapter 1 one level down — decomposing `HeatingSystem` into its component parts — and records a stopping judgment that ties the child-level evidence back to the parent claims.

**Exercise:** The [Chapter 5 exercise](../../exercises/ch05/exercise.ipynb) asks you to add a `CoffeeFlow` assembly with a `pump` and a `filter`, declare a flow between them, build the interconnection intent, and confirm the endpoint paths appear correctly in the intent dict.
