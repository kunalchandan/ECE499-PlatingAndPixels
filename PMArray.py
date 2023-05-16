import colored_traceback.auto

import PySpice.Logging.Logging as Logging
logger = Logging.setup_logging()

from PySpice.Spice.Library import SpiceLibrary
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import u_us, u_ms, u_V
from PySpice.Unit import *


# Define the circuit
circuit = Circuit('Diode Circuit')

# Add the voltage source
circuit.V('input', '+', circuit.gnd, 1@u_V)

# Add the diode
circuit.X('D1', 'D', 'input', circuit.gnd)

print(circuit)

# Set up the simulation
simulator = circuit.simulator(temperature=25, nominal_temperature=25)
simulator.initial_condition(input=u_V(0))


# Run the transient analysis
analysis = simulator.transient(step_time=u_ms(1), end_time=u_ms(10))

# Plot the results
analysis.plot()

# # Define the circuit
# led_circuit = Circuit('LED Array')
# led_library = SpiceLibrary('./led.lib')  # include the new library file

# # Add the LEDs to the circuit
# for i in range(8):
#     led_circuit.X('LED{}'.format(i+1), led_library['LED'], 'LED{}'.format(i+1), '0')

# # Simulate the circuit
# led_simulator = led_circuit.simulator()
# led_simulator.transient(step_time=1@u_us,
#                         end_time=1@u_ms)


# # Plot the results (not necessary for LED array)
# led_analysis = led_simulator.transient_analysis
# led_analysis.plot()