"""Page copy for batch 5: hubs and controllers, and Wi-Fi garage door openers.
Imported at the bottom of meta.py."""
from meta_batch3 import _p

HUB_GUIDE = [
    {"q": "USB stick or full hub?",
     "a": "A USB stick (or network coordinator) is just a radio. It needs software running on something else, usually Home Assistant on a mini PC or a Home Assistant Green. A full hub has the radio and the automation software in one box, so it works out of the box but you're tied to its app."},
    {"q": "Can I move my devices to a new hub later?",
     "a": "Usually not without re-pairing each device. Z-Wave controllers can sometimes back up and restore their network, and some Zigbee coordinators can be migrated in Home Assistant, but plan on re-pairing if you switch brands."},
    {"q": "Where should the hub go?",
     "a": "Somewhere central and out in the open, not in a metal cabinet or right next to the router. For USB sticks, use a short USB extension cable to move the stick away from the computer, since USB 3 ports put out interference that hurts 2.4 GHz radios."},
]
THREAD_BR_GUIDE = [
    {"q": "What does a Thread border router do?",
     "a": "It connects your Thread devices to your home network so a Matter controller (Apple Home, Google Home, Alexa, SmartThings, or Home Assistant) can reach them. Without one, Thread devices can't connect to anything."},
    {"q": "Do I already have one?",
     "a": "Possibly. Many recent HomePod minis, Apple TV 4K models, Nest Hubs, Nest Wifi Pro routers, Echo devices, eero routers, and SmartThings hubs have a Thread border router built in. Check your speaker or router before you buy another box."},
    {"q": "Can border routers from different brands share one network?",
     "a": "They're supposed to, and it's getting better, but mixing ecosystems can still create separate Thread networks. Sticking to one brand of border router, or using one that shares credentials with your main platform, avoids most trouble."},
]
LUTRON_GUIDE = [
    {"q": "Which Lutron bridge do I need?",
     "a": "The standard Caseta Smart Hub handles most homes. The Smart Hub Pro adds a telnet integration port that some home automation systems use. RA2 Select is a step up for bigger homes. Check what your hub software supports before choosing."},
    {"q": "Does it work with Home Assistant?",
     "a": "Yes. Home Assistant has an official Lutron Caseta integration that works with both the standard and Pro bridges, and it controls devices locally."},
    {"q": "Is buying a kit cheaper?",
     "a": "Usually. Kits that bundle a Smart Hub with a dimmer and a Pico remote often cost little more than the hub alone."},
]
GARAGE_GUIDE = [
    {"q": "Will it work with my garage door opener?",
     "a": "Most smart controllers wire to the same two terminals your wall button uses, so they work with most openers made since the 1990s. Newer Chamberlain and LiftMaster openers with yellow learn buttons use encrypted wall controls; check the product's compatibility list or plan on an adapter."},
    {"q": "How does it know if the door is open?",
     "a": "A tilt or contact sensor on the door tells the controller whether it's open or closed. Without one, the app can push the button but can't confirm the door actually moved."},
    {"q": "Is it safe to close the door remotely?",
     "a": "Openers sold in the US must stop and reverse if the safety sensors detect something. Most smart controllers also flash a light or beep before closing remotely, as UL 325 requires for unattended operation."},
]

PAGES = {
    "z-wave-controllers": _p("hubs", "Hubs and controllers", "controller", "The Best Z-Wave Hubs and USB Controllers",
        "Z-Wave USB sticks and all-in-one hubs, ranked from live Amazon data.",
        "We pulled the Z-Wave USB controllers and hubs selling on Amazon and scored them on rating, review volume, and features: 800 Series chips with Long Range, all-in-one hubs that need no extra computer, and extra radios. The table shows whether each is a stick or a hub.",
        3000, HUB_GUIDE),
    "zigbee-coordinators": _p("hubs", "Hubs and controllers", "hub", "The 10 Best Zigbee Hubs and Coordinators",
        "Zigbee USB coordinators and standalone hubs, ranked from live Amazon data.",
        "We pulled the Zigbee coordinators and hubs selling on Amazon and scored them on rating, review volume, and features: open Zigbee 3.0 pairing, Thread support on the same radio, and network (Ethernet or PoE) connections. The table shows whether each is a stick or a hub.",
        6000, HUB_GUIDE),
    "matter-controllers": _p("hubs", "Hubs and controllers", "hub", "The 10 Best Matter Hubs and Controllers",
        "Hubs that run Matter devices, many with a Thread border router built in.",
        "We pulled the Matter hubs and controllers selling on Amazon and scored them on rating, review volume, and features: a built-in Thread border router, extra radios like Zigbee or IR, and a screen. Smart speakers that double as controllers are covered on our Thread border router page.",
        3000, HUB_GUIDE),
    "thread-border-routers": _p("hubs", "Hubs and controllers", "border router", "The 10 Best Thread Border Routers",
        "The speakers, routers, hubs, and USB sticks that put Thread devices on your network.",
        "We pulled the Thread border routers selling on Amazon, including mesh routers and hubs that have one built in, and scored them on rating, review volume, and features. You may already own one; the guide below explains how to check.",
        15000, THREAD_BR_GUIDE),
    "lutron-bridges": _p("hubs", "Hubs and controllers", "bridge", "The Best Lutron Caseta Bridges and Kits",
        "Every Lutron Caseta Smart Hub and hub kit we found on Amazon, ranked.",
        "Lutron sells only a few Caseta bridges, so this list includes the starter kits that bundle a bridge with dimmers or remotes. We scored each on rating, review volume, and what's in the box.",
        3000, LUTRON_GUIDE),
    "wifi-garage-openers": _p("garage-openers", "Garage door openers", "opener", "The 10 Best Smart Garage Door Openers",
        "Wi-Fi controllers that add phone and voice control to the opener you already have.",
        "We pulled the best-selling smart garage door controllers on Amazon and scored them on rating, review volume, and features: door position sensors, Apple Home support, and Matter. Matter models here use Wi-Fi, so they belong on this page too.",
        30000, GARAGE_GUIDE),
}
