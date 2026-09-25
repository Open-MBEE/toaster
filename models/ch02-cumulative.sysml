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
        subject toaster : Toaster;
        require constraint { toaster.cycleTime <= 180.0 [SI::s] }
    }

    part nominal : Toaster;
    part slow : Toaster {
        attribute :>> cycleTime = 200.0 [SI::s];
    }
}
