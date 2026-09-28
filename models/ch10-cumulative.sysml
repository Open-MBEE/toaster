// GENERATED FIXTURE: do not edit directly.
// Run: python scripts/check_construction.py --check   (to verify)
// Source: unchanged from models/ch08-cumulative.sysml. Chapter 10 (Traceability and
// Sign-off) adds no new named model element: its own notebooks build a traceability
// graph and a judgment ledger over the model exactly as Chapter 8 left it, the same
// deliberate design choice Chapter 9 made (decisions/pass4-run-009.md), not a fixture
// that would carry nothing new. Unlike Chapter 9, this chapter DOES commit its own
// models/ch10-cumulative.sysml (byte-identical in body to ch08's, only this header
// comment differs), so that scripts/check_construction.py's own predecessor-
// containment check has a real ch10 file of its own to compare ch08's named elements
// against, resolving decisions/next-passes.md item 21 (check_predecessor_containment
// falls back to the nearest earlier chapter with a real fixture -- ch08 -- when the
// immediate predecessor, ch09, has none), and so this chapter's own notebooks have a
// current, committed fixture of their own to name rather than reaching back across a
// chapter boundary to cite ch08's file directly.

package ToasterDemo {
    private import ScalarValues::*;
    private import SI::*;
    private import ISQ::*;
    private import MeasurementReferences::*;  // DimensionOneValue

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
        exhibit state cycle : Cycle;
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
        attribute efficiency : DimensionOneValue;
        assert constraint efficiencyBounded {
            doc /* Efficiency is the fraction of supplied energy delivered as
                 * heat: it cannot be negative and cannot exceed 1. */
            0.0 <= efficiency and efficiency <= 1.0
        }
        calc deliveredEnergy {
            doc /* Characterizes the energy this carrier actually delivers: a
                 * queried power and duration, scaled by this carrier's own
                 * bound efficiency. efficiency is this carrier's own feature
                 * here, not a separate parameter, so the relation can never
                 * be evaluated against an efficiency the model's own bound
                 * does not cover: only a real candidate's own value is ever
                 * used, and that value is exactly what efficiencyBounded
                 * checks. This conversion is a property of the mechanism a
                 * concrete realization chooses, so it lives on this logical
                 * carrier, not on the functional action. */
            in power : ISQ::PowerValue;
            in duration : ISQ::DurationValue;
            return : ISQ::EnergyValue = power * duration * efficiency;
        }
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
        attribute :>> efficiency = 0.7;
        assert satisfy heatGenerationReq by rated;
    }
    part weak : ResistanceCoil {
        attribute :>> power = 400.0 [SI::W];
        assert not satisfy heatGenerationReq by weak;
    }

    state def Cycle {
        entry; then idle;
        state idle;
        state heating {
            do action generateHeat : GenerateHeat {
                doc /* Invokes the heat-generation step of the chain Chapters
                     * 4 and 6 already built. It invokes GenerateHeat
                     * directly, not the full ApplyHeat action: ApplyHeat's
                     * own bread input has no value at this level of
                     * decomposition, and only its already-[0..*] parameters
                     * (D-026) stay executable when left unbound. */
            }
        }
        state ready;
        state cancelled;
        transition first idle accept Start then heating;
        transition first heating accept Finish then ready;
        transition first heating accept Cancel then cancelled;
        transition first ready then idle;
        transition first cancelled then idle;
    }

    part heatGenCheck : HeatGenerator;
    attribute heatGenCheckDuration : ISQ::DurationValue;

    assert constraint deliveredEnergyBoundedBySupply {
        doc /* A real-arithmetic lemma of the same shape as the relation
             * efficiencyBounded (0 <= efficiency <= 1) and deliveredEnergy's own
             * definition (power * duration * efficiency) together would imply:
             * given efficiency in [0,1] and non-negative power and duration,
             * power * duration * efficiency never exceeds power * duration.
             * Restated by hand on a fresh, unbound usage (heatGenCheck) rather
             * than a solver-checked reference to HeatGenerator's own
             * efficiencyBounded and deliveredEnergy: this toolchain's Z3 backend
             * does not compose two separately declared assert constraints,
             * whether sibling or inherited (D-030), and cannot reason through a
             * chained calc invocation such as heatGenCheck.deliveredEnergy(...)
             * (D-031). Proved by Z3 over the unbound heatGenCheck.efficiency,
             * heatGenCheck.power and heatGenCheckDuration features
             * (verify --solve): this restated lemma holds for all such values,
             * but the proof does not track HeatGenerator's own efficiencyBounded
             * or deliveredEnergy if either changes; a content-hash-based record
             * against this file does go stale when either changes (any edit to
             * the file changes the hash), which is a partial safeguard, not a
             * check that the restated copy stays in sync. */
        (heatGenCheck.efficiency >= 0.0 and heatGenCheck.efficiency <= 1.0
         and heatGenCheck.power >= 0.0 [SI::W] and heatGenCheckDuration >= 0.0 [SI::s])
        implies (heatGenCheck.power * heatGenCheckDuration * heatGenCheck.efficiency)
                <= heatGenCheck.power * heatGenCheckDuration
    }
}
