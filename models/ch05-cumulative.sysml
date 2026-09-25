package ToasterDemo {
    private import ScalarValues::*;

    abstract part def ToastingSystem {
        doc /* Transform bread into toast acceptable to its user. */
    }
    part def Heater { attribute power : Real default = 800.0; }
    part def HeatingSystem :> ToastingSystem;
    part def ControlSystem :> ToastingSystem;
    part def Toaster {
        attribute cycleTime : Real default = 120.0;
        part heating : HeatingSystem;
        part control : ControlSystem;
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
        then action calculate {
            assign energy := DeliveredEnergy(power, duration, efficiency);
        }
        then done;
    }
    item def Start;
    item def Finish;
    item def Cancel;
    allocate ApplyHeat to HeatingSystem;
    part def BreadLoader { part bread : Start; }
    part def BreadEjector { part bread : Finish; }
    part def BreadHandling {
        part loader : BreadLoader;
        part ejector : BreadEjector;
        flow loader.bread to ejector.bread;
    }
}
