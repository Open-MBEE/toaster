# Probe script (2026-09-26): re-runs the OpenSysML v0.9.0 constructs recorded in decisions/probes.md.
# Run: uv run python scripts/probes/reprobe_opensysml.py [test-name ...]
import json, warnings, opensysml
conn = opensysml.connect(version="v0.9.0")
def load(src):
    m = conn.load_from_content(src, strict=False)
    return m, [f"{d.severity}: {d.message} @{d.start_line}" for d in m.diagnostics]
def api(m):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return json.loads(m.to_api_json().content)
def types(m):
    return sorted({e["@type"] for e in api(m) if e.get("qualifiedName","").startswith("P")} )

BASE = """
package P {
  import ScalarValues::*; import ParametersOfInterestMetadata::*;
  item def Bread; item def Toast;
  action def ToastBread { in item b : Bread; out item t : Toast; }
  port def PowerPort; port def FuelPort;
"""
tests = {}
# G3: spec 7.15.2 form, allocation def with typed ends + nested sub-allocation, and allocation usage
tests["G3-typed-ends"] = BASE + """
  part def LogicalSystem { part component : LogicalComponent; }
  part def LogicalComponent;
  part def PhysicalAssembly;
  part def PhysicalDevice { part assembly : PhysicalAssembly; }
  allocation def LogicalToPhysicalAllocation {
     end part logical : LogicalSystem;
     end part physical : PhysicalDevice;
     allocate logical.component to physical.assembly;
  }
  part system : LogicalSystem;
  part device : PhysicalDevice;
  allocation a : LogicalToPhysicalAllocation allocate system to device;
}"""
tests["G3-allocation-usage-only"] = BASE + """
  part def L; part def Ph;
  part l : L; part p : Ph;
  allocate l to p;
  allocation named_alloc allocate l to p;
}"""
# G4: mismatched port types through an interface / connect
tests["G4-mismatched-ports"] = BASE + """
  part def Outlet { port o : PowerPort; }
  part def Tank { port f : FuelPort; }
  part def Torch { port fuelIn : FuelPort; }
  part outlet : Outlet; part torch : Torch;
  connect outlet.o to torch.fuelIn;
}"""
tests["G4-mismatched-interface-def"] = BASE + """
  part def Outlet { port o : PowerPort; }
  part def Torch { port fuelIn : FuelPort; }
  interface def PowerLink { end a : PowerPort; end b : PowerPort; }
  part outlet : Outlet; part torch : Torch;
  interface link : PowerLink connect a ::> outlet.o to b ::> torch.fuelIn;
}"""
# perform inheritance
tests["perform-inherit"] = BASE + """
  abstract part def Heater { perform action heat : ToastBread; }
  part def CoilHeater :> Heater { attribute watts : Real = 800; }
  part def Toaster { part h : CoilHeater; }
  part t : Toaster;
}"""
tests["perform-bare"] = BASE + """
  abstract part def Heater { perform ToastBread; }
}"""
tests["perform-ref-usage"] = BASE + """
  action heatUse : ToastBread;
  abstract part def Heater { perform heatUse; }
}"""
# named connectors
tests["named-flow-satisfy-perform"] = BASE + """
  requirement def R { doc /* r */ }
  part def H { perform action heat : ToastBread; port o : PowerPort; }
  part h : H; part h2 : H;
  requirement r1 : R;
  satisfy r1 by h;
  allocation named_alloc allocate h to h2;
  connection named_conn connect h.o to h2.o;
  flow named_flow of Bread from h.o to h2.o;
}"""
tests["moe-mop-metadata"] = BASE + """
  part def T { 
    attribute quality : Real; attribute cycleTime : Real;
    }
  metadata MeasureOfEffectiveness about T::quality;
}"""
import sys
for k, s in tests.items():
    if len(sys.argv)>1 and k not in sys.argv[1:]: continue
    try:
        m, d = load(s)
        print(f"\n## {k}: ok={m.ok}"); [print("   ", x) for x in d[:5]]
        if m.ok:
            t = [ (e["@type"], e.get("qualifiedName") or e.get("name")) for e in api(m) if e["@type"] in ("AllocationUsage","AllocationDefinition","PerformActionUsage","ConnectionUsage","InterfaceUsage","FlowUsage","SatisfyRequirementUsage")]
            print("    ", t)
    except Exception as e:
        print(f"\n## {k}: EXC {type(e).__name__}: {str(e)[:200]}")

print("\n## G1: which named elements does model.query() see?")
m,_ = load(tests["named-flow-satisfy-perform"])
print("ok", m.ok, [x for x in _])
T = lambda t: {"@type":"PrimitiveConstraint","property":"@type","operator":"=","value":[t]}
for t in ["AllocationUsage","ConnectionUsage","FlowUsage","PerformActionUsage","SatisfyRequirementUsage","MetadataUsage"]:
    r = m.query(where=T(t), select=["name"])
    print(t, [(e.id, e.properties.get("name")) for e in r])
m2,_=load(tests["perform-inherit"]); 
print("perform-inherit query PerformActionUsage:", [(e.id) for e in m2.query(where=T("PerformActionUsage"))])
m3,_=load(tests["moe-mop-metadata"]); print("mop meta query:", [(e.id,e.type) for e in m3.query(where=T("MetadataUsage"))], [e["@type"] for e in api(m3) if "etadata" in e["@type"]])
print("\n## perform queryability")
m,_=load(tests["perform-inherit"])
for sc in (["P::Heater"],["P::CoilHeater"],["P::Toaster"],["P::t"],["P"]):
    try: print(sc, [(e.id,e.type) for e in m.query(scope=sc)])
    except Exception as e: print(sc,"ERR",str(e)[:100])
print([ (e["@type"],e.get("qualifiedName")) for e in api(m) if "erform" in e["@type"] or e.get("qualifiedName","").endswith("heat")])
sym=m.find("P::Heater"); print("Symbol.members?", [a for a in dir(sym) if not a.startswith("_")])
