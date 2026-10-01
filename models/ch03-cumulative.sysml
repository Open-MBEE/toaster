// GENERATED FIXTURE: do not edit directly.
// Run: python scripts/check_construction.py --check   (to verify)
// Source: notebook cell-02 TOASTER_INCREMENT in chapter 3's construct-introducing notebooks.

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

    requirement timely : TimelyToast;

    metadata acC03Tag : ReviewRecordRef about timely {
        identifier = "AC-C03";
    }

    metadata asC03Tag : ReviewRecordRef about timely {
        identifier = "AS-C03";
    }

    part nominal : Toaster;
    metadata ac001Tag : ReviewRecordRef about nominal {
        identifier = "AC-001";
    }

    part slow : Toaster {
        attribute :>> cycleTime = 200.0 [SI::s];
        assert not satisfy timely by slow;
    }

    verification def TimelyToastTest {
        doc /*
         * Verification method: timed test of three consecutive toasting cycles at
         * nominal input power; all must complete within 180 seconds.
         * Method type: test (VerificationMethodKind::test, SysML v2 §7.24 Table 22).
         * Note: formal #verificationMethod metadata not yet supported in OpenSysML v0.9.0;
         * tracked at toaster#19 / OpenSysML#608.
         * spec: SysML v2 formal/2026-03-02 §7.24.2 (VerificationCaseDefinition).
         */
        subject toaster : Toaster;
        objective {
            verify timely;
        }
    }
}
