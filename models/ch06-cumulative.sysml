// GENERATED FIXTURE: do not edit directly.
// Run: python scripts/check_construction.py --check   (to verify)
// Source: notebook cell-02 TOASTER_INCREMENT in chapter 6's construct-introducing notebooks.

package ToasterDemo {
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

        first start;
        then action generateHeat : GenerateHeat {
            in energyIn = ApplyHeat::energy;
        }
        then done;
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

    port def DurationPort {
        doc /* Carries a duration signal: how long to apply heat. */
        out duration : ISQ::DurationValue[0..*];
    }

    abstract part def HeatingSystem {
        doc /* The logical carrier of the heating mechanism: performs ApplyHeat
             * and exposes a port for a duration signal from a control component. */
        perform action applyHeat : ApplyHeat;
        port durationIn : ~DurationPort;
    }
    part def ControlSystem {
        port durationOut : DurationPort;
    }

    part def Toaster :> ToastingSystem {
        attribute cycleTime : ISQ::DurationValue;
        part heating : HeatingSystem;
        part control : ControlSystem;
        interface durationInterface connect control.durationOut to heating.durationIn;
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

    part nominal : Toaster;
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

    allocation heatAllocation allocate ToastBread::applyHeat to Toaster::heating;

    port def EnergyPort {
        doc /* Carries an energy signal delivered to a heat generator, not
             * committed to any particular energy form. */
        out energy : ISQ::EnergyValue[0..*];
    }

    action def GenerateHeat {
        doc /* Converts a supplied energy input into a thermal energy output.
             * No mechanism, and no energy form, is committed yet: a resistive
             * coil and a gas flame both take some supplied energy and deliver
             * heat, so any device that does this satisfies the function. */
        in energyIn : ISQ::EnergyValue[0..*];
        out heatOut : ISQ::EnergyValue;
    }

    abstract part def HeatGenerator {
        doc /* The logical carrier of heat generation, one level below
             * HeatingSystem: performs GenerateHeat and exposes a port for an
             * energy signal, not yet connected to a producer. Named for the
             * function it carries, not for a mechanism: which mechanism
             * realizes it is a selection among alternatives, recorded once a
             * concrete part specializes this carrier. */
        perform action generateHeat : GenerateHeat;
        port energyIn : ~EnergyPort;
        attribute power : ISQ::PowerValue;
    }

    part def HeatingAssembly :> HeatingSystem {
        part heatGen : HeatGenerator;
    }

    allocation heatGenAllocation allocate ApplyHeat::generateHeat to HeatingAssembly::heatGen;

    requirement def HeatGenerationReq {
        doc /*
         * A heat generator shall be rated for at least 600 W.
         * This is an engineering performance threshold on a component rating,
         * not yet derived from a stated measure of effectiveness through the
         * energy relation: no supply and no coil are modeled together yet, so
         * there is nothing to derive it from. Recorded openly, not faked.
         */
        subject heatGen : HeatGenerator;
        require constraint { heatGen.power >= 600.0 [SI::W] }
    }

    requirement heatGenerationReq : HeatGenerationReq;

    part def ResistanceCoil :> HeatGenerator {
        doc /* An electrically switched resistive element: converts electrical
             * energy to heat by Joule heating. The mechanism selection this
             * specialization commits to is recorded against the alternative
             * it was chosen over, argued from a domain premise about how the
             * two mechanisms work, not from anything the model connects. */
        attribute :>> power default = 800.0 [SI::W];
        attribute resistance : ISQ::ResistanceValue default = 12.0 [SI::ohm];
    }

    part rated : ResistanceCoil {
        assert satisfy heatGenerationReq by rated;
    }
    part weak : ResistanceCoil {
        attribute :>> power = 400.0 [SI::W];
        assert not satisfy heatGenerationReq by weak;
    }
}
