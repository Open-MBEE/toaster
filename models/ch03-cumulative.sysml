// GENERATED FIXTURE — do not edit directly.
// Run: python scripts/check_construction.py --check   (to verify)
// Source: notebook cell-02 TOASTER_INCREMENT in chapter 3's construct-introducing notebooks.

package ToasterDemo {
    private import ScalarValues::*;
    private import SI::*;
    private import ISQ::*;
    private import MeasurementReferences::*;  // DimensionOneValue (dim 1); D-003: move to ISQ::* when opensysml ships it

    abstract part def ToastingSystem {
        doc /* Transform bread into toast acceptable to its user. */
    }
    part def Heater { attribute power : ISQ::PowerValue default = 800.0 [SI::W]; }
    part def HeatingSystem :> ToastingSystem;
    part def ControlSystem :> ToastingSystem;
    part def Toaster {
        attribute cycleTime : ISQ::DurationValue default = 120.0 [SI::s];
        part heating : HeatingSystem;
        part control : ControlSystem;
    }
    part nominal : Toaster;
    part slow : Toaster { attribute :>> cycleTime = 200.0 [SI::s]; }
    requirement def TimelyToast {
        doc /*
         * The toaster shall complete a toasting cycle in at most 180 seconds.
         * Rationale: kitchen workflows typically span 5-15 minutes; a cycle
         * exceeding 3 minutes delays meal preparation and falls outside the
         * usability envelope for a countertop appliance.
         */
        subject toaster : Toaster;
        require constraint { toaster.cycleTime <= 180.0 [SI::s] }
    }
    requirement timely : TimelyToast;
    verification def TimelyToastTest {
        doc /*
         * Verification method: timed test of three consecutive toasting cycles at
         * nominal input power; all must complete within 180 seconds.
         * Method type: test (VerificationMethodKind::test, SysML v2 §7.24 Table 22).
         * Note: #verificationMethod metadata not yet supported in OpenSysML v0.9.0
         * — toaster#19 / OpenSysML#608.
         * spec: SysML v2 formal/2026-03-02 §7.24.2 (VerificationCaseDefinition).
         */
        subject toaster : Toaster;
        objective {
            verify timely;
        }
    }
    part evidence {
        assert satisfy timely by nominal;
        assert satisfy timely by slow;
    }
    calc def DeliveredEnergy {
        in power : ISQ::PowerValue;
        in duration : ISQ::DurationValue;
        in efficiency : DimensionOneValue;
        return : ISQ::EnergyValue = power * duration * efficiency;
    }
}