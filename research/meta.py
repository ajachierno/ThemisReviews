"""Shared page-level copy for the light-switch pages: titles, intros, scoring, guides."""
COMMON = {
    "family": "light-switches", "family_title": "Light switches", "noun": "switch",
    "data_captured": "2026-10-04",
    "weights": {"rating": 0.45, "reviews": 0.30, "features": 0.25},
}
SHARED = {
    "NEUTRAL": {"q": "Do I need a neutral wire?",
                "a": "Most smart switches need one because the electronics stay powered when the light is off. Open the box and look for a bundle of white wires tied together at the back. If it's there, you have a neutral. Older homes, especially those built before the mid-1980s, often don't. If yours doesn't, pick a switch listed as no-neutral."},
    "3WAY": {"q": "Will a smart switch work on a 3-way circuit?",
             "a": "Only if it says so. A 3-way circuit controls one light from two switches. Some smart switches handle that on their own and keep the existing switch at the other end. Others need a matching add-on or companion switch, and some only work on single-pole circuits."},
    "SAFETY": {"q": "Can I install it myself?",
               "a": "If you're comfortable replacing an ordinary switch, the job is similar: power off at the breaker, confirm it's dead with a tester, and match the wires. Check local code, and hire an electrician if the box is crowded, the wiring is aluminum, or you're not sure which wire is which."},
}

PAGES = {
    "z-wave-switches": {
        "title": "The 10 Best Z-Wave Light Switches",
        "subtitle": "In-wall on/off switches for Z-Wave hubs, ranked from live Amazon data.",
        "intro": "We pulled the in-wall Z-Wave on/off switches selling on Amazon, checked each listing's specs, and scored them on rating, review volume, and the features that matter on a Z-Wave network: 800 Series Long Range radios, 3-way support without extra hardware, and S2 security. Dimmers get their own page.",
        "reviews_ceiling": 1500,
        "guide": [
            {"q": "What's the difference between 500, 700, and 800 Series Z-Wave?",
             "a": "The series is the generation of Silicon Labs chip inside. 800 Series switches support Z-Wave Long Range, use less power, and have better range than 500 and 700 Series. All of them work together on the same network, so older switches still run fine next to new ones."},
            {"q": "Do Z-Wave switches need a hub?",
             "a": "Yes. They pair to a Z-Wave controller such as Home Assistant with a USB stick, Hubitat, SmartThings, or a Zooz Z-Box. Alexa and Google Home can't talk to Z-Wave directly."},
            {"q": "What does Z-Wave Long Range mean for a light switch?",
             "a": "Long Range is a separate star network that talks straight to the hub over a much longer distance. Switches listed as 800LR can join either the regular mesh or Long Range, depending on what your controller supports."},
            "NEUTRAL", "3WAY", "SAFETY"]},
    "zigbee-switches": {
        "title": "The 10 Best Zigbee Light Switches",
        "subtitle": "In-wall Zigbee switches for SmartThings, Echo, Hubitat, and Home Assistant.",
        "intro": "We pulled the in-wall Zigbee switches selling on Amazon, checked each listing, and scored them on rating, review volume, and features that matter on Zigbee: no-neutral support, 3-way support, and whether a brand-specific hub is required. Wall-mount remotes and in-wall relays aren't on this list.",
        "reviews_ceiling": 1000,
        "guide": [
            {"q": "Will any Zigbee switch work with my hub?",
             "a": "Usually, but not always. Zigbee 3.0 devices pair with most coordinators, including Home Assistant (ZHA or Zigbee2MQTT), SmartThings, Hubitat, and Echo devices with a built-in Zigbee hub. Some brands, such as Aqara, MOES, and SONOFF, sell switches marketed for their own hub, and features like button modes may only show up there."},
            {"q": "Do Zigbee switches strengthen the mesh?",
             "a": "Switches wired to a neutral usually act as Zigbee routers and pass signals along for other devices. No-neutral switches usually run as end devices and don't route, so they don't help your mesh."},
            "NEUTRAL", "3WAY", "SAFETY"]},
    "wifi-switches": {
        "title": "The 10 Best Wi-Fi Light Switches",
        "subtitle": "No-hub smart switches that connect straight to your router.",
        "intro": "We pulled the best-selling Wi-Fi light switches on Amazon and scored them on rating, review volume, and features: 3-way support, no-neutral options, and Apple Home support. Wi-Fi switches with Matter have their own page, so this list covers the app-based ones.",
        "reviews_ceiling": 40000,
        "guide": [
            {"q": "Will a Wi-Fi switch work on a 5 GHz network?",
             "a": "Almost every Wi-Fi switch here needs 2.4 GHz. Most routers broadcast both bands under one name, and that usually works. If setup fails, turn on a separate 2.4 GHz network temporarily or stand near the router."},
            {"q": "What happens when the internet goes down?",
             "a": "The switch still works as a wall switch. App control and voice control often stop, because many Wi-Fi switches route commands through the maker's cloud. Matter and Apple Home models can keep working locally on your network."},
            {"q": "How many Wi-Fi switches can my router handle?",
             "a": "It depends on the router. Many consumer models cope with 30 to 50 devices, and some cheaper ones struggle earlier. If you plan to put a switch in every room, a mesh Wi-Fi system or a hub-based protocol such as Z-Wave, Zigbee, or Thread puts less load on your network."},
            "NEUTRAL", "3WAY", "SAFETY"]},
    "matter-switches": {
        "title": "The 10 Best Matter Light Switches",
        "subtitle": "Switches that work with Apple Home, Google Home, Alexa, SmartThings, and Home Assistant.",
        "intro": "We pulled the Matter light switches selling on Amazon and scored them on rating, review volume, and features: 3-way support, Thread versus Wi-Fi, and no-neutral options. The comparison table shows whether each switch runs Matter over Wi-Fi or over Thread.",
        "reviews_ceiling": 2000,
        "guide": [
            {"q": "Matter over Wi-Fi or Matter over Thread?",
             "a": "Matter over Wi-Fi switches connect to your router like any Wi-Fi device and need nothing else. Matter over Thread switches need a Thread border router, such as a HomePod mini, Apple TV 4K, Nest Hub (2nd gen), or a recent Echo, but they form a low-power mesh that doesn't load your Wi-Fi."},
            {"q": "Do I need a hub for a Matter switch?",
             "a": "You need a Matter controller, which is usually a smart speaker or streaming box you already own. Apple, Google, Amazon, and Samsung all ship Matter controllers in their current hubs and speakers."},
            {"q": "Can I use a Matter switch with Alexa and Apple Home at the same time?",
             "a": "Yes. Matter's multi-admin feature lets you add the same switch to more than one ecosystem. Add it to the first app, then generate a pairing code from that app to share it with the second."},
            "NEUTRAL", "3WAY", "SAFETY"]},
    "thread-switches": {
        "title": "The Best Thread Light Switches",
        "subtitle": "Every in-wall Thread switch we could find on Amazon, ranked.",
        "intro": "Thread light switches are still uncommon, so this list is short. We pulled the Thread switches and dimmers selling on Amazon and scored them on rating, review volume, and features. Every switch here needs a Thread border router.",
        "reviews_ceiling": 500,
        "guide": [
            {"q": "What's a Thread border router and do I have one?",
             "a": "It's the device that connects Thread gear to your home network. HomePod mini, HomePod (2nd gen), Apple TV 4K with Ethernet, Nest Hub (2nd gen), Nest Hub Max, and some Echo models have one built in. Home Assistant can also run one with a compatible radio."},
            {"q": "Why are there so few Thread switches?",
             "a": "Most switch makers launched Matter over Wi-Fi first because it needs no extra hardware. Thread versions are arriving more slowly."},
            "NEUTRAL", "SAFETY"]},
    "bluetooth-switches": {
        "title": "The Best Bluetooth Light Switches",
        "subtitle": "The few in-wall switches that use Bluetooth, ranked from live Amazon data.",
        "intro": "Pure Bluetooth wall switches are rare. Most switches that list Bluetooth use it for setup or for a mesh alongside Wi-Fi. We pulled what's selling on Amazon and scored it on rating, review volume, and features. The list is short because the market is.",
        "reviews_ceiling": 500,
        "guide": [
            {"q": "Can I control a Bluetooth switch when I'm away from home?",
             "a": "Only if something in the house bridges it to the internet. GE Cync switches use built-in Wi-Fi for that. Pure Bluetooth switches need a phone, hub, or gateway in range."},
            {"q": "What is GE Cync's Bluetooth used for?",
             "a": "Cync switches use Bluetooth for setup and to talk to nearby Cync devices, and Wi-Fi for app and voice control. They behave like Wi-Fi switches with a Bluetooth helper."},
            "NEUTRAL", "SAFETY"]},
    "lutron-caseta-dimmers": {
        "title": "The 10 Best Lutron Caseta Switches and Dimmers",
        "subtitle": "Caseta switches and dimmers on Lutron's Clear Connect RF, ranked.",
        "intro": "We pulled the Lutron Caseta switches, dimmers, and kits selling on Amazon and scored them on rating, review volume, and features. Caseta switches need a Lutron Smart Bridge for app, voice, and automation control. Without one, a Caseta switch still works at the wall and with a paired Pico remote.",
        "reviews_ceiling": 6000,
        "guide": [
            {"q": "Do Caseta switches need a neutral wire?",
             "a": "Most Caseta dimmers don't, which is the main reason people pick them for older houses. The on/off switch and the fan control need a neutral, so check the model before you buy."},
            {"q": "Do I need the Smart Bridge?",
             "a": "For app control, schedules, voice assistants, Apple Home, or Home Assistant, yes. A Caseta switch with a Pico remote works without one. Several kits on this list include the bridge."},
            {"q": "How do Caseta switches handle 3-way circuits?",
             "a": "Lutron uses a Pico remote in place of the second switch. You cap the traveler wire at the other box and mount a Pico in a wallplate bracket there. No extra wiring is needed."},
            "SAFETY"]},
    "rf-light-switches": {
        "title": "The 10 Best RF Wireless Light Switch Kits",
        "subtitle": "Stick-on RF switches and receivers that add a light switch without running wires.",
        "intro": "These kits pair a battery or self-powered wall switch with a receiver wired in at the light. They use simple radio (RF), not Wi-Fi or a hub. Most makers don't publish the exact frequency; the ones here that do list 433 MHz. We pulled the best-selling kits on Amazon and scored them on rating, review volume, and features.",
        "reviews_ceiling": 5000,
        "guide": [
            {"q": "Can I connect a 433 MHz switch to my smart home?",
             "a": "Not directly. A few kits add Wi-Fi to the receiver. Otherwise you need an RF bridge or a software-defined radio running rtl_433, and even then many kits use codes those tools can't decode."},
            {"q": "Is 433 MHz secure?",
             "a": "Basic 433 MHz kits send a fixed code without encryption, so anyone nearby with a cheap receiver can record and replay it. That's fine for a closet light and a bad idea for anything that unlocks or opens."},
            {"q": "Where does the receiver go?",
             "a": "It wires in between the power and the light, in the ceiling box, the fixture canopy, or the existing switch box. Some kits use a plug-in receiver for lamps instead."},
            "SAFETY"]},
}

DIM_GUIDE = [
    {"q": "Will a smart dimmer work with my LED bulbs?",
     "a": "Only with bulbs marked dimmable, and even then some combinations flicker or buzz at low levels. Dimmers with an adjustable minimum brightness (sometimes called low-end trim) let you raise the bottom of the range until the flicker stops."},
    {"q": "What's the wattage rating about?",
     "a": "Smart dimmers list a maximum load, often around 150 W of LED and 600 W of incandescent. Add up the bulbs on the circuit. If you're close to the limit, pick a higher-rated model or split the load."},
    {"q": "Can I use a smart dimmer on a ceiling fan?",
     "a": "No. Dimmers are for lights. Fans need a fan speed control or an on/off switch rated for motors."},
]
PAGES.update({
    "z-wave-dimmers": {
        "family": "dimmers", "family_title": "Dimmers", "noun": "dimmer",
        "title": "The 10 Best Z-Wave Dimmer Switches",
        "subtitle": "In-wall dimmers for Z-Wave hubs, ranked from live Amazon data.",
        "intro": "We pulled the in-wall Z-Wave dimmers selling on Amazon, checked each listing, and scored them on rating, review volume, and features: 800 Series Long Range radios, 3-way support without add-on switches, and adjustable dimming. On/off switches are on our Z-Wave light switches page.",
        "reviews_ceiling": 1000,
        "guide": DIM_GUIDE + [
            {"q": "Do Z-Wave dimmers need a hub?",
             "a": "Yes. They pair to a Z-Wave controller such as Home Assistant with a Z-Wave adapter, Hubitat, SmartThings with a Z-Wave hub, or Homey Pro. Smart speakers can't talk to Z-Wave directly."},
            "NEUTRAL", "3WAY", "SAFETY"]},
    "zigbee-dimmers": {
        "family": "dimmers", "family_title": "Dimmers", "noun": "dimmer",
        "title": "The Best Zigbee Dimmer Switches",
        "subtitle": "Every in-wall Zigbee dimmer we could find on Amazon, ranked.",
        "intro": "In-wall Zigbee dimmers are uncommon in the US, so this list is short. Most of what turns up in a search is a hidden module or a 0-10 V controller, which we left out. We scored the wall dimmers on rating, review volume, and features.",
        "reviews_ceiling": 500,
        "guide": DIM_GUIDE + [
            {"q": "Why are there so few Zigbee dimmers?",
             "a": "In the US, most wall-switch makers chose Z-Wave, Wi-Fi, or Matter. Zigbee is common for bulbs and sensors, and its dimmers are mostly sold as hidden modules rather than wall switches."},
            "NEUTRAL", "SAFETY"]},
    "wifi-dimmers": {
        "family": "dimmers", "family_title": "Dimmers", "noun": "dimmer",
        "title": "The 10 Best Wi-Fi Dimmer Switches",
        "subtitle": "No-hub smart dimmers that connect straight to your router.",
        "intro": "We pulled the best-selling Wi-Fi dimmers on Amazon and scored them on rating, review volume, and features: 3-way support, no-neutral options, and adjustable dimming. Wi-Fi dimmers with Matter are on our Matter dimmers page, so this list covers the app-based ones.",
        "reviews_ceiling": 35000,
        "guide": DIM_GUIDE + ["NEUTRAL", "3WAY", "SAFETY"]},
    "matter-dimmers": {
        "family": "dimmers", "family_title": "Dimmers", "noun": "dimmer",
        "title": "The 10 Best Matter Dimmer Switches",
        "subtitle": "Dimmers that work with Apple Home, Google Home, Alexa, SmartThings, and Home Assistant.",
        "intro": "We pulled the Matter dimmers selling on Amazon and scored them on rating, review volume, and features: 3-way support, no-neutral options, and adjustable dimming. The table shows whether each one runs Matter over Wi-Fi or over Thread.",
        "reviews_ceiling": 1500,
        "guide": DIM_GUIDE + [
            {"q": "Matter over Wi-Fi or Matter over Thread?",
             "a": "Matter over Wi-Fi dimmers connect to your router and need nothing else. Matter over Thread dimmers need a Thread border router, such as a HomePod mini, Apple TV 4K, Nest Hub (2nd gen), or Echo Hub, but they don't add load to your Wi-Fi."},
            "NEUTRAL", "3WAY", "SAFETY"]},
})
