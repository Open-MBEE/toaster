// GENERATED FIXTURE — do not edit directly.
// Run: python scripts/check_construction.py --check   (to verify)
// Source: notebook cell-02 TOASTER_INCREMENT in chapter 2's construct-introducing notebooks.

package ToasterDemo {
    private import ScalarValues::*;
    private import SI::*;
    private import ISQ::*;

    abstract part def ToastingSystem {
        doc /* Transform bread into toast acceptable to its user. */
    }

    part def Heater {
        attribute power : ISQ::PowerValue default = 800.0 [SI::W];
    }

    part def HeatingSystem :> ToastingSystem;
    part def ControlSystem :> ToastingSystem;

    part def Toaster {
        attribute cycleTime : ISQ::DurationValue default = 120.0 [SI::s];
        part heating : HeatingSystem;
        part control : ControlSystem;
    }

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

    part nominal : Toaster;
    part slow : Toaster {
        attribute :>> cycleTime = 200.0 [SI::s];
    }
}