Wildcat5e Vision 2022
=====================

Network Table Format
--------------------

    Type: [Ball|Hoop]
    Pitch: radians
    Yaw: radians
    Color: [Blue|Red|Other]
    Distance: meters

What the files are for
--------------------

    Ball-Getter is for ball recognition
    Ball-Getter-Local is for testing on local machines without networktables

Useful Romi Links
-----------------

* [Romi Robot Documentation](https://docs.wpilib.org/en/stable/docs/romi-robot)
* [robotpy Vision](https://robotpy.readthedocs.io/en/stable/vision/)
* [WPILibPi Releases](https://github.com/wpilibsuite/WPILibPi/releases)

Note: The Romi release includes Wi-Fi access forbidden on competition bots, but
useful for debugging and testing.

Robot Lab Pi Addresses
----------------------

    | Name  | IP Address  | Network           | Password    |
    ---------------------------------------------------------
    | Lab   | 10.100.0.20 | WC-WIFI           |             |
    | Table | 10.0.0.2    | WPILibPi-d33d8771 | WPILib2021! |
    | Robot | 10.67.5.11  | 6705-team3        | 88775691    }

Multi-Camera
------------

All devices on the Pi are represented as files in /dev.

    | Name  | Device      | Responsibility                        |
    ---------------------------------------------------------------
    | hoop  | /dev/video0 | distance, pitch, and yaw of top hoop  |
    | ball  | /dev/video2 | distance, pitch, and yaw closest ball |

Assuming both USB cameras are plugged in before starting the Pi, the /dev/video0
is the top left USB port after reboot. The other camera will connect as
/dev/video2.

If camera USBs are plugged into a live Pi, the first one is assigned
/dev/video0. Consequently, ALWAYS plugin the HOOP camera first!
