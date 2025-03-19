<!-- Update font to Times New Roman :) -->
<span style="font-family: 'times New Roman', sans-serif;">

*Note: This user manual was created using the software markdown structure format (.md) as part of the overall user guide. Once complete, the entire GitHub respository will be made public and intended to be used as the complete User Manual.*

<!-- Title and background information -->
# Raspberry Pi Mesh Network for Environmental Sensor Data Monitoring User Manual
**Course:** SEE 410W | SEE411 *(Septmeber 2024 - April 2025)*
**Created by:** Pi-oneers Team (Micheal Chen, Nathaniel King, William Le, Tianna Sequeira)
**Submitted on:** March 30, 2025

**Client:** Stephen Makonin, SFU Computational Sustainability Lab
**Capstone Advisor:** Mina Xu, SEE Professor

<!-- Table of Contents -->
## Table of Contents
- [Raspberry Pi Mesh Network for Environmental Sensor Data Monitoring User Manual](#raspberry-pi-mesh-network-for-environmental-sensor-data-monitoring-user-manual)
  - [Table of Contents](#table-of-contents)
    - [User Guide Overview ](#user-guide-overview-)
    - [Safety Considerations ](#safety-considerations-)
    - [Technical Specifications ](#technical-specifications-)
    - [Prototype at a Glance ](#prototype-at-a-glance-)
    - [Operating the Prototype ](#operating-the-prototype-)
    - [Maintenance ](#maintenance-)
    - [Troubleshooting ](#troubleshooting-)
        - [Wi-Fi Disconnection](#wi-fi-disconnection)
        - [Electrical Wiring Disconnection](#electrical-wiring-disconnection)
        - [Data Overload](#data-overload)
        - [Sensor Malfunctions](#sensor-malfunctions)
        - [Microcontroller Boot](#microcontroller-boot)
    - [Team Member Contribution ](#team-member-contribution-)
    - [References ](#references-)

<!-- Section 1: Overview -->
### User Guide Overview <a name="userguide"></a>
Our capstone project, an environmental data monitoring system, is an open-source software platform designed for users seeking to analyze their surroundings for sustainable development, health monitoring, or weather forecasting. The system is versatile and can be deployed indoors in residential or commercial spaces, as well as in outdoor or extreme environments such as greenhouses. Whether you are a beginner exploring home electronics or an experienced designer, this guide will help you develop and implement your own system.

This user guide provides an overview of the completed capstone prototype, as well as how you can adapt it to your own needs. It outlines key safety considerations, technical and operating specifications, and step-by-step instructions for setup and operation. Additionally, this guide includes troubleshooting procedures and maintenance guidelines to ensure optimal performance and reliability.

<!-- Section 2: Safety Section -->
### Safety Considerations <a name="safety"></a>
<!-- Safety First – A list of safety features; any cautions that must be exercised by the user and operator -->
When operating the environmental data monitoring system, users must follow basic safety precautions to ensure both personal safety and the longevity of the prototype. As the system involves electrical components, proper handling of wiring and power connections is essential to prevent short circuits, electrical shocks, or potential fire hazards. Users should ensure all components are properly insulated and avoid exposing the system to moisture unless it has been adequately weatherproofed for outdoor deployment. Additionally, if the system is installed in an industrial or extreme environment, care must be taken to secure components against physical damage, overheating, or exposure to harsh elements. Regular inspections of wiring, sensors, and power supplies should be conducted to prevent failures. Lastly, when modifying or expanding the system, users should follow best practices for electronic assembly and software security to avoid damage or data breaches.

<!-- Section 3: Technical Specifications -->
### Technical Specifications <a name="techspec"></a>
<!-- Technical Specifications – Details of the design, including dimensions, weight, energy input/outputs -->

<!-- Section 4: Prototype -->
### Prototype at a Glance <a name="prototype"></a>
<!-- Prototype at a Glance – Orienting the user to the main features of the design; basic functions and considerations; instrumentation -->
[Maybe add: 3D model, PCB Design, Electrical Schematic and all the backend storage stuff]

<!-- Section 5: Prototype Operation -->
### Operating the Prototype <a name="operation"></a>
<!-- Operating the Prototype – Detailed description of how each sub-component can be operated -->
[Maybe add: web interface design and how to operate from a user perspective?]

<!-- Section 6: Maintenance -->
### Maintenance <a name="maintenance"></a>
<!-- Maintenance – Frequency of service; elements needing service -->
The maintenance requirements for this prototype largely depend on the lifespan and durability of the physical components used. Since the core of the system is software-based, minimal upkeep is required as long as the hardware remains in proper working condition.

However, the environment in which the prototype is deployed plays a significant role in determining maintenance needs. For indoor applications, such as residential or commercial spaces, maintenance is relatively low. Routine checks should include ensuring proper power supply, securing sensor connections, and keeping components free from dust or debris that could affect performance.

In contrast, deployments in harsher environments—such as greenhouses, outdoor fields, or industrial settings may require more frequent maintenance. Exposure to varying weather conditions, humidity, dust, and potential physical impacts can degrade materials over time. Metal components may be susceptible to corrosion, enclosures may require additional sealing to prevent moisture ingress, and sensors may need regular calibration to maintain accuracy. In these cases, periodic inspections should be performed to check for wear and tear, clean or replace damaged parts, and ensure continued reliability.

Regular software updates and data integrity checks should also be part of the maintenance routine to prevent performance issues. Ensuring proper ventilation, securing cable connections, and protecting the system from power surges will further extend the lifespan of the prototype. By following these maintenance guidelines, users can maximize the efficiency and longevity of their environmental data monitoring system, regardless of where it is deployed.

<!-- Section 7: Troubleshooting -->
### Troubleshooting <a name="troubleshoot"></a>
<!-- Troubleshooting – Describe common faults anticipated and ways of overcoming them -->
With many systems, it is expected for some faults to occur throughout the design process, and it is important to know how to address them. Below are some of the potential faults our team has identified:

##### Wi-Fi Disconnection
In some cases, users could experience a Wi-Fi disconnection, which can prevent data transmission. This may be caused by a weak or unstable Wi-Fi signal, incorrect network credentials, or the Raspberry Pi failing to detect the network. To resolve this, check if the Wi-Fi network is operational by testing with another device. Ensure the Raspberry Pi is within range of the router, repositioning it or using a Wi-Fi extender if necessary. Verify that the correct SSID and password are entered, and restart both the Raspberry Pi and the router to reset the connection. If using a static IP, confirm that the configuration settings are correct.
##### Electrical Wiring Disconnection
In some environments (especially those that are more humid), users may encounter is electrical wiring disconnection, which can result in the system failing to power on or sensors not receiving power. This may be due to loose or disconnected power cables, a faulty power adapter, or damaged wiring. To fix this, inspect all power connections and ensure they are securely plugged in. Test the power adapter with an alternate one if available and check the Raspberry Pi’s LED indicators to confirm it is receiving power. If external sensors are not functioning, ensure their power connections are intact. Additionally, using a multimeter can help detect voltage inconsistencies in the power lines.
##### Data Overload
If users are storing large data files or have expanded the system to include multiple sensors, the excessive data processing can cause slow performance or unresponsiveness. This typically occurs when too many sensors are active, the Raspberry Pi has limited RAM or storage, or high-frequency data logging is overwhelming the system. To address this, reduce the data collection rate to lower processing demands, limit the number of active sensors, or distribute processing across multiple Raspberry Pis. Regularly clearing unnecessary data logs can free up storage space, while using a high-endurance microSD card or external storage can prevent write fatigue. Optimizing the software to filter and process only necessary data can also improve performance.
##### Sensor Malfunctions
If the sensors are not initialized properly, users may also encounter sensor malfunctions or incorrect readings, where sensor outputs fluctuate, display errors, or stop working entirely. This can be due to loose or incorrect wiring connections, calibration drift, or exposure to extreme environmental conditions. To resolve this, verify that all sensor connections match the wiring diagram and check for physical damage, replacing faulty sensors as needed. Recalibrating sensors according to the manufacturer’s instructions can improve accuracy. Additionally, ensuring sensors are not exposed to conditions beyond their rated specifications and restarting the system to refresh sensor readings may help.
##### Microcontroller Boot
In rare cases, the Raspberry Pi may not display or respond. This can result in an insufficient power supply, or hardware failure. To troubleshoot, try booting with a the Raspberry Pi again by using the *BOOTSEL button*. Ensure the power supply meets the recommended voltage and current requirements, as an underpowered device may fail to start properly. If the Raspberry Pi appears physically damaged, such as having broken ports or burned components, replacing the board may be necessary. If the issue persists, testing with another Raspberry Pi unit can help determine if the problem lies with the hardware.

### Team Member Contribution <a name="contribution"></a>
Below is a list of each members contributions for this portion of the capstone project. 

<!-- Table for Team Member Contributions -->
| Team Member | Contributions |
| ------------|----------------|
|Micheal| <li> Finalized PCB Design <br> <li> Ordered Final Components |
|Nathaniel | <li> Developed database, storage and collector node software <br> <li> Documentation and Writing User Manual |
| Tianna | <li> Developed User Website Interface (front end code) <br> <li> Documentation and Writing User Manual |
| William | <li> Finalized 3D Model & Printing |

### References <a name="references"></a>

</span>