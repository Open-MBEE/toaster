package ToasterDemo {
    private import ScalarValues::*;
    private import SI::*;
    abstract part def ToastingSystem {
        doc /* Transform bread into toast acceptable to its user. */
    }
    part def Heater { attribute power : Real default = 800.0; }
    part def HeatingSystem { part heater : Heater; }
    part def Toaster :> ToastingSystem {
        attribute cycleTime : Real default = 120.0;
        part heating : HeatingSystem;
    }
    part nominal : Toaster;
    part slow : Toaster { attribute :>> cycleTime = 200.0; }
    requirement def TimelyToast {
        subject toaster : Toaster;
        require constraint { toaster.cycleTime <= 180.0 }
    }
    requirement timely : TimelyToast;
    part evidence {
        assert satisfy timely by nominal;
        assert satisfy timely by slow;
    }
    calc def DeliveredEnergy {
        in power : Real;
        in duration : Real;
        in efficiency : Real;
        return : Real = power * duration * efficiency;
    }
    action def ApplyHeat {
        in power : Real;
        in duration : Real;
        in efficiency : Real;
        out energy : Real;
        first start;
        then action calculate { assign energy := DeliveredEnergy(power, duration, efficiency); }
        then done;
    }
    item def Start;
    item def Finish;
    item def Cancel;
    state Cycle {
        entry; then idle;
        state idle;
        state heating;
        state ready;
        state cancelled;
        transition first idle accept Start then heating;
        transition first heating accept Finish then ready;
        transition first heating accept Cancel then cancelled;
    }

    // Construct 11: allocate X to Y
    part def ControlUnit;
    part def ElectricToaster :> ToastingSystem {
        part control : ControlUnit;
        part heatingUnit : HeatingSystem;
    }
    allocate ApplyHeat to ElectricToaster;

    // Construct 12: flow (item flow between parts via items)
    part def LoadStation {
        out item bread : Start;
    }
    part def EjectStation {
        in item bread : Start;
    }
    part def ToasterLine {
        part loader : LoadStation;
        part ejector : EjectStation;
        flow loader.bread to ejector.bread;
    }
}
