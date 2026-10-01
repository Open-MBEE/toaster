"""Records whether each of the four common-model tools has an allocation-view
or requirement-view kind at all — untested territory the original toy fixture
never exercised. sysml-toolkit's answer is already known (see Step 1's log);
opensysml and pilot are read from their captured --help output (Steps 2-3)."""
import json
from pathlib import Path

EVIDENCE_DIR = Path("decisions/diagram-study-real-fixtures/evidence")


def compile_probe_result(opensysml_supports: dict, pilot_supports: dict) -> dict:
    return {
        "sysml-toolkit": {"allocation": False, "requirement": False,
                           "source": "toolkit-view-help.log (v0.9.1 --help, seven view kinds, neither present)"},
        "opensysml": opensysml_supports,
        "pilot": pilot_supports,
        "sysmld": {"allocation": True, "requirement": True,
                   "source": "sysml2d/src/sysmld/allocation_view.py and requirement_view.py exist; "
                              "see Task 6 for why Phase 0 does not author real-fixture intent for either "
                              "(scoped out — see Review Focus item 5 in the plan)"},
    }


def main() -> None:
    # opensysml_supports / pilot_supports were filled in by hand after reading
    # evidence/opensysml-help.log and evidence/pilot-help.log (Steps 2-3) —
    # there is no automatic parser for either tool's free-text help output.
    result = compile_probe_result(
        opensysml_supports={
            "allocation": False,
            "requirement": False,
            "source": "opensysml-help.log (sysml -help, pinned v0.9.0 binary at "
                       "/private/tmp/functional-toaster-design/sysml): the 'Rendering views' "
                       "section documents -render <view> against a declared View element "
                       "(e.g. Views::vehicleView) with no fixed view-kind enum; no 'allocation' "
                       "or 'requirement' kind/flag appears anywhere in the help text",
        },
        pilot_supports={
            "allocation": False,
            "requirement": False,
            "source": "pilot-help.log (PilotRender.java zero-arg -> s.help(\"viz\")): the seven "
                       "<VIEW> candidates listed are DEFAULT, TREE, INTERCONNECTION, STATE, ACTION, "
                       "SEQUENCE, MIXED; neither ALLOCATION nor REQUIREMENT is present",
        },
    )
    (EVIDENCE_DIR / "view-type-probe.json").write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
