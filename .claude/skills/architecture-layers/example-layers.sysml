package ToasterLayers {
    import ScalarValues::*;
    import ParametersOfInterestMetadata::*;

    // Functional: what. Typed flows and a phenomena relation; no mechanism.
    item def Bread;
    item def Toast;
    action def ApplyHeat {
        in item bread : Bread;
        in attribute energyIn : Real;
        out item toast : Toast;
        out attribute energyLoss : Real;
    }
    constraint def EnergyBalance {
        in attribute energyIn : Real;
        in attribute energyToBread : Real;
        in attribute energyLoss : Real;
        energyToBread + energyLoss <= energyIn
    }

    // Logical: how. A mechanism's carrier, its interface, and the derived requirement.
    port def PowerPort;
    abstract part def HeatSource {
        port power : PowerPort;
        perform action applyHeat : ApplyHeat;
        attribute efficiency : Real;
    }
    requirement def EfficientHeating {
        doc /* MoP threshold derived from the MoE: efficiency at least 0.6 */
        attribute efficiency : Real;
        require constraint { efficiency >= 0.6 }
    }

    // Physical: where. A concrete part that realizes the logical component and confers values.
    part def NichromeCoil :> HeatSource {
        attribute watts : Real = 800.0;
    }
    part toaster {
        action apply : ApplyHeat;
        part source : NichromeCoil;
        allocate apply to source;
    }
    metadata MeasureOfPerformance about HeatSource::efficiency;
}
