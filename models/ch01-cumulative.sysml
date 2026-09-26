// GENERATED FIXTURE — do not edit directly.
// Run: python scripts/check_construction.py --check   (to verify)
// Source: notebook cell-02 TOASTER_INCREMENT in chapter 1's construct-introducing notebooks.

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
}