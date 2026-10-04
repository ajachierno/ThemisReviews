"""Page copy for batch 7: trackers, Bluetooth proxies, Thread blinds, 433 MHz weather stations, RF bridges.
Imported at the bottom of meta.py."""
from meta_batch3 import _p

TRACKER_GUIDE = [
    {"q": "Which tracker works with my phone?",
     "a": "AirTags and other Find My trackers work only with iPhones. Samsung SmartTags work best with Galaxy phones. Trackers built for Google's Find Hub network work with Android. A few newer tags support both Apple and Google; the table says which."},
    {"q": "How far away can I find it?",
     "a": "Bluetooth reaches roughly 100 to 400 ft. Beyond that, trackers rely on other people's phones in the same network passing by and reporting the location, so they work best in busy areas."},
    {"q": "Do trackers work with my smart home?",
     "a": "Mostly no. Trackers report to their phone network, not to Apple Home, Alexa, or Google Home. Home Assistant can see some of them nearby as Bluetooth devices for presence detection, but that's a workaround, not a feature."},
]
PROXY_GUIDE = [
    {"q": "What is a Bluetooth proxy?",
     "a": "A small ESP32 board running ESPHome that listens for Bluetooth devices and forwards them to Home Assistant over Wi-Fi or Ethernet. Put one in each part of the house and Home Assistant can read Bluetooth sensors, locks, and lights far from the server."},
    {"q": "How do I set one up?",
     "a": "Plug the board into a computer, open ESPHome's Bluetooth proxy page in Chrome or Edge, and install the ready-made firmware in a few clicks. Home Assistant finds the proxy automatically."},
    {"q": "Ethernet or Wi-Fi?",
     "a": "Ethernet is more reliable because the ESP32 uses the same 2.4 GHz radio for Wi-Fi and Bluetooth. If you have lots of Bluetooth devices, a PoE board is worth the extra few dollars."},
]
BLINDS_GUIDE = [
    {"q": "Motor kit or complete shade?",
     "a": "A motor kit fits inside a roller shade you already own, if the tube size matches. A complete shade arrives with the motor installed, cut to your window. Measure the tube or window carefully before ordering either."},
    {"q": "Why Thread for blinds?",
     "a": "Thread is low power, so battery motors last months between charges, and Matter over Thread works with Apple Home, Google Home, Alexa, SmartThings, and Home Assistant. You need a Thread border router."},
    {"q": "How are they powered?",
     "a": "Most use a built-in rechargeable battery charged over USB-C or by an optional solar panel. Expect a few months per charge depending on how often the shade moves."},
]
WEATHER_GUIDE = [
    {"q": "Can a 433 MHz weather station join my smart home?",
     "a": "Not by itself. These stations send to their own console. Some models add Wi-Fi to upload to weather services, and Home Assistant can read many of their sensors with a USB SDR and rtl_433, which is a do-it-yourself project."},
    {"q": "Where should the outdoor sensor go?",
     "a": "In open air, away from roofs, walls, and pavement that radiate heat, ideally 5 ft. or more above the ground. Wind sensors need to be above nearby obstacles to read accurately."},
    {"q": "What does 5-in-1 or 7-in-1 mean?",
     "a": "The number of measurements the outdoor sensor takes: usually temperature, humidity, wind speed, wind direction, and rainfall, with light and UV added in 7-in-1 models."},
]
RFBRIDGE_GUIDE = [
    {"q": "What does an RF bridge do?",
     "a": "It learns the signals from 433 MHz remotes, doorbells, and sensors so you can trigger them from an app or a smart home hub. Most handle only fixed-code remotes, not the rolling-code remotes used by garage doors and car fobs."},
    {"q": "What is an SDR receiver for?",
     "a": "A software-defined radio USB stick can listen to many 433 MHz and 915 MHz weather sensors at once. With rtl_433 and Home Assistant, it turns cheap weather and temperature sensors into smart home data. It only receives; it can't send commands."},
    {"q": "Is any of this plug and play?",
     "a": "The Wi-Fi IR/RF hubs are app-based and fairly easy. SDR sticks and custom firmware are hobbyist projects that need some comfort with Linux or Home Assistant add-ons."},
]

PAGES = {
    "bluetooth-trackers": _p("trackers", "Trackers", "tracker", "The 10 Best Bluetooth Trackers",
        "AirTags, Tiles, SmartTags, and the cheaper alternatives, ranked from live Amazon data.",
        "We pulled the Bluetooth item trackers selling on Amazon and scored them on rating, review volume, and features: Apple or Google network support, replaceable batteries, and multi-packs.",
        15000, TRACKER_GUIDE),
    "bluetooth-proxies": _p("hubs", "Hubs and controllers", "board", "The Best Boards for Home Assistant Bluetooth Proxies",
        "ESP32 boards that extend Home Assistant's Bluetooth range, ranked.",
        "We pulled the ESP32 boards on Amazon that work as ESPHome Bluetooth proxies and scored them on rating, review volume, and features: a case, Ethernet or PoE, and USB-C.",
        1500, PROXY_GUIDE),
    "thread-blinds": _p("blinds", "Blinds and shades", "shade", "The Best Thread and Matter Smart Blinds",
        "Matter-over-Thread shade motors and motorized shades, ranked.",
        "Thread blinds are new, so most have few reviews. We scored the Matter-over-Thread motors and shades on Amazon on rating, review volume, and features: retrofit fit, battery or solar power, and app support.",
        100, BLINDS_GUIDE),
    "rf-weather-stations": _p("weather-stations", "Weather stations", "station", "The 10 Best Wireless Home Weather Stations",
        "Indoor-outdoor weather stations with wireless sensors, ranked from live Amazon data.",
        "We pulled the wireless home weather stations selling on Amazon and scored them on rating, review volume, and features: wind and rain sensing, color displays, and Wi-Fi uploads. Most use 433 MHz or 915 MHz sensors; the table shows what each listing states.",
        20000, WEATHER_GUIDE),
    "rf-bridges": _p("hubs", "Hubs and controllers", "device", "The Best RF Bridges and SDR Receivers",
        "Devices that bring 433 MHz remotes and sensors into a smart home.",
        "We pulled the RF bridges, IR/RF hubs, and SDR receivers selling on Amazon and scored them on rating, review volume, and features. The table shows which can send commands and which only listen.",
        6000, RFBRIDGE_GUIDE),
}
