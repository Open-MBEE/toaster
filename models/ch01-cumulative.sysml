package ToasterDemo {
    private import ScalarValues::*;

    abstract part def ToastingSystem {
        doc /* Transform bread into toast acceptable to its user. */
    }

    part def Heater {
        attribute power : Real default = 800.0;
    }

    part def HeatingSystem :> ToastingSystem;
    part def ControlSystem :> ToastingSystem;

    part def Toaster {
        attribute cycleTime : Real default = 120.0;
        part heating : HeatingSystem;
        part control : ControlSystem;
    }
}
