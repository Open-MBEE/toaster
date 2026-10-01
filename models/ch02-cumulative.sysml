// GENERATED FIXTURE — do not edit directly.
// Run: python scripts/check_construction.py --check   (to verify)
// Source: notebook cell-02 TOASTER_INCREMENT in chapter 2's construct-introducing notebooks.

package ToasterDemo {
    metadata def ReviewRecordRef {
        attribute identifier : ScalarValues::String;
    }

    private import ScalarValues::*;
    private import SI::*;
    private import ISQ::*;

    item def Bread;
    item def Toast;

    action def ToastBread {
        doc /* Transform bread into toast acceptable to its user. */
        in bread : Bread;
        out toast : Toast;
    }

    abstract part def ToastingSystem {
        perform action toastBread : ToastBread;
    }

    part def HeatingSystem;
    part def ControlSystem;

    part def Toaster :> ToastingSystem {
        attribute cycleTime : ISQ::DurationValue;
        part heating : HeatingSystem;
        part control : ControlSystem;
    }

    requirement def TimelyToast {
        doc /*
         * The toaster shall complete a toasting cycle in at most 180 seconds.
         * Rationale: kitchen workflows typically span 5-15 minutes; a cycle
         * exceeding 3 minutes delays meal preparation and falls outside where
         * and how a user prepares a meal.
         */
        subject toaster : Toaster;
        require constraint { toaster.cycleTime <= 180.0 [SI::s] }
    }

    part nominal : Toaster;
    metadata ac001Tag : ReviewRecordRef about nominal {
        identifier = "AC-001";
    }

    part slow : Toaster {
        attribute :>> cycleTime = 200.0 [SI::s];
    }
}
