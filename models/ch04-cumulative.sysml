// GENERATED FIXTURE: do not edit directly.
// Run: python scripts/check_construction.py --check   (to verify)
// Source: notebook cell-02 TOASTER_INCREMENT in chapter 4's construct-introducing notebooks.

package ToasterDemo {
    metadata def ReviewRecordRef {
        attribute identifier : ScalarValues::String;
    }

    private import ScalarValues::*;
    private import SI::*;
    private import ISQ::*;

    item def Bread;
    item def Toast;

    action def ApplyHeat {
        in bread : Bread;
        in energy : ISQ::EnergyValue[0..*];
        in duration : ISQ::DurationValue[0..*] {
            doc /* Signal from a control function: how long to apply heat.
             * No control function is modeled in this chapter, so this input
             * is declared and typed but not yet connected to a value. */
        }
        out toast : Toast;
        out delivered : ISQ::EnergyValue;
        out loss : ISQ::EnergyValue;

        assert constraint balance {
            delivered >= 0.0 [SI::J] and loss >= 0.0 [SI::J] and delivered + loss <= energy
        }
    }

    metadata aiC04Tag : ReviewRecordRef about ApplyHeat {
        identifier = "AI-C04";
    }

    action def ToastBread {
        doc /* Transform bread into toast acceptable to its user. */
        in bread : Bread;
        out toast : Toast;
        first start;
        then action applyHeat : ApplyHeat {
            in bread = ToastBread::bread;
        }
        then done;
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

    item def Start {
        doc /* Signal marking the start of a toasting cycle, not the bread itself. */
    }
    item def Finish {
        doc /* Signal marking the finish of a toasting cycle, not the toast itself. */
    }
    item def Cancel {
        doc /* Signal requesting cancellation of an in-progress toasting cycle. */
    }
}
