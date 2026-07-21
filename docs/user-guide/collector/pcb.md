# PCB and Enclosure

The optional interface PCB and enclosure provide a tidy way to mount a Raspberry Pi Pico W with the sensors used by the original OpenCollector greenhouse prototype. They are hardware design sources, not a requirement for running the software; supported sensors may also be wired directly or mounted on a custom carrier.

## PCB

The latest design in the repository is `PCBs/Sensor Interface PCB REV4`. It contains the Altium project, schematic (`Sheet1.SchDoc`), board layout (`PCB.PcbDoc`), a STEP model (`PCB.step`), and generated fabrication layers under `Project Outputs for Capstone PCB Project`.

Before ordering or assembling a board:

1. Open the revision 4 project in compatible PCB-design software and review the schematic, footprints, board outline, and design rules.
2. Generate a fresh fabrication package from the source project and compare it with the checked-in output files. The repository does not provide a single, release-qualified manufacturing archive or bill of materials.
3. Confirm connector pin order, voltage levels, and current requirements against the exact Pico W and sensor modules you purchased. Similar modules can use different connectors or pin orders.
4. Assemble and inspect the board before inserting the Pico W or sensors. Check for shorts between power and ground with the board unpowered.
5. Configure the collector GPIO values to match the assembled wiring. The PCB does not automatically configure the software; see [Collector Config](./config.md) and [Supported Sensors](./sensors.md).

Revision 3 is retained for reference. Use revision 4 for new work unless you have already validated revision 3 hardware. These files are prototype engineering artifacts and have not been documented as a certified or production-ready hardware release.

## Enclosure

The `Enclosure_Design` directory contains SolidWorks part and assembly files for the prototype enclosure and models of the PCB and sensors. Open `Assem1.SLDASM` to inspect the complete assembly. The repository does not currently include ready-to-print STL or 3MF exports.

To manufacture an enclosure:

1. Open the assembly in a compatible CAD application and verify that all referenced parts resolve.
2. Check clearances against the assembled revision 4 PCB, connectors, cables, and the exact sensor modules in use.
3. Export the printable enclosure parts—not the PCB or sensor reference models—to STL or 3MF using appropriate mesh tolerances.
4. Print a low-cost fit test before the final enclosure. Confirm access to power, programming, ventilation, and sensor openings.
5. Mount components without stressing the PCB or cables. Keep air-quality, temperature, humidity, and light sensors exposed as required by their manufacturers.

Enclosure material, ventilation, direct sunlight, condensation, and heat from the electronics can bias environmental readings. Place the collector where air can circulate and validate measurements against a trusted reference instrument after installation.
