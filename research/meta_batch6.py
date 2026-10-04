"""Page copy for batch 6: temperature and humidity sensors, and buttons and remotes.
Imported at the bottom of meta.py."""
from meta_batch3 import _p, SENSOR_BATT

TEMP_GUIDE = [
    {"q": "How accurate are these sensors?",
     "a": "Most smart sensors are within about 1°F and 3 to 5% relative humidity, which is fine for rooms, nurseries, and basements. For fridges, freezers, or reptile tanks, pick one with a probe or a stated tighter accuracy, and check it against a reference thermometer once."},
    {"q": "What can I automate with one?",
     "a": "Turn on a fan or dehumidifier when humidity climbs, get an alert when a freezer warms up or pipes risk freezing, or let a smart thermostat average temperatures across rooms."},
    SENSOR_BATT,
]
RF_TEMP_GUIDE = [
    {"q": "Can a 433 MHz sensor work with a smart home?",
     "a": "Not on its own. These sensors talk to their own display. With a cheap USB SDR receiver and the rtl_433 software, Home Assistant can read many AcuRite, La Crosse, and Ambient Weather sensors, but that's a do-it-yourself project, not a supported feature."},
    {"q": "Will a replacement sensor work with my display?",
     "a": "Only if the listing names your display's model. 433 MHz sensors use brand-specific formats, so an AcuRite sensor won't pair with a La Crosse display."},
    {"q": "Where should an outdoor sensor go?",
     "a": "In the shade, out of direct sun and rain, and a few feet off the ground. A sensor in the sun can read 10°F or more too high."},
]
BUTTON_GUIDE = [
    {"q": "What can a smart button do?",
     "a": "Anything your hub can run: turn on a scene, toggle a lamp, start a routine, or arm an alarm. Many buttons recognize single, double, and long presses, so one button can run three actions."},
    {"q": "Do buttons need a hub?",
     "a": "Yes, for Zigbee and Z-Wave. The button sends a press to the hub, and the hub runs the automation. Some Zigbee buttons can bind directly to a bulb or plug, but most setups go through the hub."},
    SENSOR_BATT,
]
PICO_GUIDE = [
    {"q": "Do Pico remotes need the Smart Hub?",
     "a": "No, not for basic use. A Pico can pair directly to a Caseta dimmer or switch and control it with no hub at all. You need the Smart Hub to use a Pico for scenes, multiple lights, or other smart home devices."},
    {"q": "Can I mount a Pico on the wall?",
     "a": "Yes. A wallplate bracket lets it sit in a standard Decora wallplate, so it looks like a real switch. That's how most people add a 3-way switch without running new wires."},
    {"q": "How long does the battery last?",
     "a": "Lutron rates the coin cell at up to 10 years of typical use."},
]

PAGES = {
    "zigbee-temperature-sensors": _p("temperature-sensors", "Temperature sensors", "sensor", "The 10 Best Zigbee Temperature and Humidity Sensors",
        "Cheap Zigbee climate sensors for every room, ranked from live Amazon data.",
        "We pulled the Zigbee temperature and humidity sensors selling on Amazon and scored them on rating, review volume, and features: built-in displays, probes, and open Zigbee 3.0 pairing.",
        6000, TEMP_GUIDE),
    "z-wave-temperature-sensors": _p("temperature-sensors", "Temperature sensors", "sensor", "The Best Z-Wave Temperature and Humidity Sensors",
        "Z-Wave climate sensors and multisensors, ranked.",
        "Dedicated Z-Wave temperature sensors are rare, so this list includes multisensors that also report temperature. We scored them on rating, review volume, and features: humidity, Long Range, and extra sensing.",
        500, TEMP_GUIDE),
    "wifi-temperature-sensors": _p("temperature-sensors", "Temperature sensors", "sensor", "The 10 Best Wi-Fi Temperature and Humidity Sensors",
        "Sensors and kits that send alerts to your phone, no smart home hub needed.",
        "We pulled the Wi-Fi temperature and humidity monitors selling on Amazon and scored them on rating, review volume, and features: alerts, data history, and probes. Several popular kits use Bluetooth or their own radio to a Wi-Fi gateway; the table shows which.",
        10000, TEMP_GUIDE),
    "bluetooth-temperature-sensors": _p("temperature-sensors", "Temperature sensors", "sensor", "The 10 Best Bluetooth Temperature and Humidity Sensors",
        "Cheap Bluetooth thermometer-hygrometers you can read on your phone, ranked.",
        "We pulled the Bluetooth temperature and humidity sensors selling on Amazon and scored them on rating, review volume, and features: displays, range, and how easily Home Assistant can read them with a Bluetooth adapter or proxy.",
        50000, TEMP_GUIDE),
    "rf-temperature-sensors": _p("temperature-sensors", "Temperature sensors", "sensor", "The Best 433 MHz Wireless Temperature Sensors",
        "Indoor-outdoor thermometers and replacement sensors on the 433 MHz band.",
        "We pulled the 433 MHz wireless temperature sensors selling on Amazon and scored them on rating, review volume, and features. These are standalone sensors and displays; the guide below explains how hobbyists read them in Home Assistant.",
        40000, RF_TEMP_GUIDE),
    "zigbee-buttons": _p("buttons", "Buttons and remotes", "button", "The 10 Best Zigbee Smart Buttons and Remotes",
        "Zigbee buttons, remotes, and dimmer switches for scenes and shortcuts.",
        "We pulled the Zigbee smart buttons and remotes selling on Amazon and scored them on rating, review volume, and features: multiple press types, extra buttons, and open Zigbee 3.0 pairing.",
        15000, BUTTON_GUIDE),
    "z-wave-buttons": _p("buttons", "Buttons and remotes", "remote", "The Best Z-Wave Scene Controllers and Remotes",
        "Battery remotes and wired scene controllers for Z-Wave hubs, ranked.",
        "We pulled the Z-Wave remotes and scene controllers selling on Amazon and scored them on rating, review volume, and features: number of buttons, Long Range, and battery or wired power.",
        500, BUTTON_GUIDE),
    "lutron-pico-remotes": _p("buttons", "Buttons and remotes", "remote", "The Best Lutron Pico Remotes",
        "Every Pico remote and Pico kit we found on Amazon, ranked.",
        "We pulled the Lutron Pico remotes selling on Amazon and scored them on rating, review volume, and what's included, like wall brackets and pedestals.",
        3000, PICO_GUIDE),
}
