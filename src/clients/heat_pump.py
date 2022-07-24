"""
This file holds the heat pump simulation class.
"""
import datetime as dt


class HeatingState:
    ON = 'On'
    OFF = 'Off'


class State:
    def __init__(self, t_inside: float, t_inside_exp: float, t_outside: float):
        # Temperatures
        self.t_inside = t_inside
        self.t_inside_exp = t_inside_exp
        self.t_outside = t_outside

        # Other
        self.timestamp = dt.datetime.utcnow()

    @property
    def t_delta(self):
        """
        Temperature difference between indoor and outdoor.
        """
        return self.t_inside - self.t_outside


class HeatPumpConnect:
    def __init__(self, t_set, t_range, p_compressor, initial_state: State):
        # Thermostat settings
        self.t_set = t_set
        self.t_range = t_range

        # Heat pump variables
        self.p_compressor = p_compressor
        self.cop = 3.5

        self.state = initial_state

    def get_state(self):
        """
        Asks the state of the heat pump system.
        """
        pass


class VaillantConnect(HeatPumpConnect):
    def __init__(self, t_set, t_range, p_compressor, initial_state):
        super(VaillantConnect, self).__init__(t_set, t_range, p_compressor, initial_state)

    def get_state(self):
        """
        Asks the state of a Vaillant heat pump system.
        """
        pass


class DemoConnect(HeatPumpConnect):
    def __init__(self, t_set, t_range, p_compressor, initial_state, k=1e-3):
        self.k = k  # in [
        super(DemoConnect, self).__init__(t_set, t_range, p_compressor, initial_state)
        self.heating_mode = HeatingState.OFF

    def get_state(self):
        """
        Creates a demo state.
        """
        passed_time = dt.datetime.utcnow() - self.state.timestamp
        t_inside_next = self.get_next_t_inside(
            t_inside=self.state.t_inside,
            t_delta=self.state.t_delta,
            time=passed_time.seconds / 60
        )

        self.state = State(
            t_inside=t_inside_next,
            t_inside_exp=t_inside_next,
            t_outside=self.state.t_outside
        )

    def get_next_t_inside(self, t_inside, t_delta, time):
        """
        Calculates the next inside temperature.
        """
        if self.heating_mode == HeatingState.OFF:
            t_next = t_inside - t_delta * self.k * time

            # Turn on heating if the lower bound has be reached
            if t_next < self.t_set - self.t_range:
                self.heating_mode = HeatingState.ON

            return t_next

        elif self.heating_mode == HeatingState.ON:
            t_next = t_inside + t_delta * self.k * time * 3

            # Turn off heating if the upper bound has been reached.
            if t_next > self.t_set + self.t_range:
                self.heating_mode = HeatingState.OFF

            return t_next



class HeatPump:

    def __init__(self, t_set, t_range, p_compressor, demo_mode=False):

        if demo_mode:
            self.connection = DemoConnect(
                t_set=t_set,
                t_range=t_range,
                p_compressor=p_compressor,
                initial_state=State(
                    t_inside=19.2,
                    t_inside_exp=19.2,
                    t_outside=14
                ),
                k=1e-1
            )
        else:
            self.connection = VaillantConnect()

        # System variables
        self.power_consumption = 0  # in [%]

    def get_current_state(self):
        """
        Retrieves the current state from the connected source.
        """
        self.connection.get_state()

    def get_forecast(self):
        """
        Get the forecast.
        """
        pass

    def update_forecast(self):
        """
        Updates the heat pump energy demand forecast.
        """
        pass


if __name__ == "__main__":
    heat_pump = HeatPump(
        t_set=19,
        t_range=0.5,
        p_compressor=2,
        demo_mode=True
    )

    print("t_inside: ", heat_pump.connection.state.t_inside)
    heat_pump.connection.state.timestamp += dt.timedelta(hours=-1)
    heat_pump.connection.get_state()
    print("t_inside: ", heat_pump.connection.state.t_inside)
