# Toaster

An executable tutorial on recursive system decomposition using SysML v2 and OpenSysML.

**Didactic purpose:** Learn to develop and recursively decompose a system model, use executable analyses to test specific claims, and exercise engineering judgment about assumptions and evidence. The tutorial uses a domestic toaster as a teaching example: concrete enough to reason about, simple enough not to obscure the method.

**Audience:** Engineers with basic systems knowledge and introductory Python.

**After completing this tutorial you will be able to:**
- Build a SysML v2 model incrementally from an abstract definition through requirements, functions, and allocated architecture
- Execute model analyses using OpenSysML and interpret the results
- Construct and evaluate engineering judgment records following Hawkins et al. 2011

## Chapter outline

| Chapter | Question | Constructs / Operations |
|---|---|---|
| 1: System and Purpose | What is the system? | abstract part def, part def, specialization, composition |
| 2: Requirements and Assumptions | What must it do? | requirement def, attribute override, asserted_context |
| 3: Measures of Success | How do we know it succeeds? | requirement usage, assert satisfy / assert not satisfy, verification def, asserted_solution |
| 4: Functional Decomposition | What functions must it perform? | action def, constraint, item def, asserted_inference |
| 5: Architecture and Allocation | Which component performs it, and how do components connect? | model navigation, allocate, perform, port, interface |
| 6: Recursive Decomposition | What does one branch of the recursion show, one level down? | nested action, abstract logical carrier, port, allocate, specialization, asserted_solution |
| 7: Execution and Experiments | What does it do? | bounded calc, assert constraint, exhibit state, do action, execute_state, parameter sweep |
| 8: Constraint Checking | Does one claim hold at one point, or does a property hold for every value? | assert constraint, verify_satisfaction, verify_holds (Z3), stale records |
| 9: Coverage and Sufficiency | Are all requirements covered? | requirement coverage, evidence sufficiency, stale detection at scale |
| 10: Traceability and Sign-off | Is the argument complete? | traceability graph, judgment ledger, asserted_inference synthesis |

[Setup and installation](setup.md) | [Glossary](glossary.md) | [References](references.md) | [Case studies](case-studies/)
