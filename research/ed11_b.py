import json


def W(s, o):
    open(f'editorial/{s}.json', 'w', encoding='utf-8').write(json.dumps(o, indent=2, ensure_ascii=False))


NS = "Not stated in bullets"
ALL7 = ["home-assistant", "apple-home", "google-home", "alexa", "smartthings", "hubitat", "homey"]


def P(asin, brand, model, systems, specs, features, verdict, pros, cons, label=None):
    o = {"asin": asin, "brand": brand, "model": model, "systems": systems}
    if label:
        o["systems_label"] = label
    o.update({"specs": specs, "features": features, "verdict": verdict, "pros": pros, "cons": cons})
    return o


# ---------------- pet fountains ----------------
def F(cap, power, filt, track):
    return {"capacity": cap, "power": power, "filter": filt, "tracking": track}


W("wifi-pet-fountains", {"feature_weights": {"intake": 0.35, "cordless": 0.25, "filterless": 0.20, "big": 0.20},
 "systems_note": "Smart fountains run in their makers' apps. None of these listings name a voice assistant or smart home platform.",
 "spec_fields": [{"key": "capacity", "label": "Capacity"}, {"key": "power", "label": "Power"}, {"key": "filter", "label": "Filtration"}, {"key": "tracking", "label": "App tracking"}],
 "table_columns": [{"key": "capacity", "label": "Capacity"}, {"key": "power", "label": "Power"}, {"key": "tracking", "label": "Tracking"}],
 "awards": [
  {"asin": "B0FDKQGRCK", "label": "Best Overall", "kind": "overall", "why": "PETLIBRO's Dockstream 2 weighs every sip, rated 4.3 stars by 20,409 buyers, 4K+ bought last month."},
  {"asin": "B0GX5JWR3P", "label": "Best Budget", "kind": "budget", "why": "Hydration tracking and water-level alerts for $62.80, sold by Amazon."},
  {"asin": "B0FDKVJNXB", "label": "Best Cordless", "kind": "special", "why": "The Dockstream 2 on battery, up to a month per charge, with 5 GHz Wi-Fi."},
  {"asin": "B0GWJ2QWXF", "label": "Best Premium", "kind": "premium", "why": "A 5 L filterless fountain with a built-in AI camera to watch your pet drink."}],
 "products": [
  P("B0FDKQGRCK", "PETLIBRO", "Dockstream 2 (3 L, plug-in)", [], F("3 L", "Plug-in, pump-free design", "4-layer filter", "Water intake by scale"),
    {"intake": True, "cordless": False, "filterless": False, "big": True},
    "The most popular smart fountain, with a scale that measures how much your cat drinks.",
    ["20,409 reviews", "Water intake measured by weight", "2-year warranty", "Sold by Amazon"],
    ["Filters to replace", "Plug-in only", "$79.99"], "PETLIBRO app"),
  P("B0FDKVJNXB", "PETLIBRO", "Dockstream 2 Cordless (3 L)", [], F("3 L", "Battery, up to a month per charge", "4-layer filter", "Water intake by scale"),
    {"intake": True, "cordless": True, "filterless": False, "big": True},
    "The same fountain without the cord, so it can go anywhere.",
    ["Up to a month per charge", "5 GHz Wi-Fi", "4,526 reviews"],
    ["$89.99", "4.2 stars", "Filters to replace"], "PETLIBRO app"),
  P("B0GX5JWR3P", "PETLIBRO", "Dockstream (2.5 L)", [], F("2.5 L", "Plug-in, wireless pump", "Multi-layer filter", "Volume, frequency, and time"),
    {"intake": True, "cordless": False, "filterless": False, "big": False},
    "Hydration goals and filter reminders in the app for about $63.",
    ["$62.80", "Water-level alerts", "Sold by Amazon"],
    ["Only 178 reviews", "2.5 L", "Filters to replace"], "PETLIBRO app"),
  P("B0GQ9MV5R4", "PETLIBRO", "Dog Water Fountain (3 L)", [], F("3 L", "Plug-in, pump-free design", "Multi-layer filter", "Daily intake and habits"),
    {"intake": True, "cordless": False, "filterless": False, "big": True},
    "PETLIBRO's tracking fountain with a wider tray for small dogs.",
    ["Wide tray for dogs", "Dishwasher-safe tray", "4.3 stars"],
    ["Small dogs only at 3 L", "Only 354 reviews", "$79.99"], "PETLIBRO app"),
  P("B0FHQC19RV", "PETKIT", "Eversweet Max 2 Cordless (3 L)", [], F("3 L", "Battery (5,000 mAh)", "Multi-layer filter", "Weekly and monthly drinking reports"),
    {"intake": True, "cordless": True, "filterless": False, "big": True},
    "A cordless fountain whose parts are dishwasher safe, except the battery pack.",
    ["Dishwasher-safe parts", "Motion-sensor mode saves battery", "Under 25 dB"],
    ["4.0 stars", "Only 164 reviews", "$84.99"], "PETKIT app"),
  P("B0GWJ2QWXF", "PETKIT", "Eversweet Ultra (5 L, AI camera)", [], F("5 L clean, 1.8 L waste tank", "Plug-in", "Filterless, wastewater separation", "AI camera, low-water alerts"),
    {"intake": True, "cordless": False, "filterless": True, "big": True},
    "Separate clean and dirty tanks plus a camera with night vision, for two weeks per refill.",
    ["5 L, about two weeks per refill", "No filters to buy", "Built-in camera"],
    ["$249.99", "Only 84 reviews", "4.2 stars"], "PETKIT app"),
  P("B0HGF8BDWD", "ODSD", "Filterless Cat Water Fountain (3 L)", [], F("3 L clean, 1.35 L waste tank", "Plug-in or 5,000 mAh battery", "Filterless, wastewater separation", "Tank levels, drain schedules"),
    {"intake": False, "cordless": True, "filterless": True, "big": True},
    "Filterless and cordless, with clean and wastewater levels in the app.",
    ["No filters to buy", "Battery or plug-in", "4.6 stars"],
    ["Only 34 reviews", "Not for large dogs", "Intake is not measured"], "Companion app"),
  P("B0GXZ1RX3G", "PETGUGU", "AI Cat Water Fountain", [], F(NS, "Plug-in, wireless pump", "8-layer filter", "Daily intake and trends"),
    {"intake": True, "cordless": False, "filterless": False, "big": False},
    "A budget tracking fountain with an 8-layer filter.",
    ["$59.98", "8-layer filter", "Sensor mode"],
    ["Sold by Woot", "Only 30 reviews", "2.4 GHz Wi-Fi only"], "PETGUGU app"),
  P("B0G52BXW5H", "Vacqueen", "Smart Dog Water Fountain (10 L)", [], F("10 L", "Plug-in or 4,000 mAh battery", "5-stage filter", "Water status and drinking habits"),
    {"intake": True, "cordless": True, "filterless": False, "big": True},
    "A 10 L fountain for big dogs or multi-pet homes.",
    ["10 L", "Battery backup", "Low-water alert"],
    ["3.8 stars", "2.4 GHz Wi-Fi only", "Lesser-known brand"], "Companion app")],
 "avoid": []})


# ---------------- garage door openers ----------------
def G(drive, power, cam, extras):
    return {"drive": drive, "power": power, "camera": cam, "extras": extras}


W("wifi-garage-door-openers", {"feature_weights": {"battery": 0.30, "camera": 0.20, "quiet": 0.25, "voice": 0.25},
 "systems_note": "Chamberlain, LiftMaster, and Craftsman openers use the myQ app. Genie openers use Aladdin Connect, which also has an official Home Assistant integration.",
 "spec_fields": [{"key": "drive", "label": "Drive"}, {"key": "power", "label": "Motor"}, {"key": "camera", "label": "Camera"}, {"key": "extras", "label": "Extras"}],
 "table_columns": [{"key": "drive", "label": "Drive"}, {"key": "power", "label": "Motor"}, {"key": "camera", "label": "Camera"}],
 "awards": [
  {"asin": "B07SKCGMY7", "label": "Best Overall", "kind": "overall", "why": "Genie's StealthDrive Connect works with Alexa, Google, and SmartThings, has a battery backup, and has 5,084 reviews."},
  {"asin": "B0CWM6PFP2", "label": "Best Budget", "kind": "budget", "why": "Built-in Wi-Fi with Alexa and Google for $215.99."},
  {"asin": "B0FQYSF58M", "label": "Best with Camera", "kind": "special", "why": "A quiet belt-drive myQ opener with a 130° camera and battery backup."},
  {"asin": "B0C7K97GX2", "label": "Best Premium", "kind": "premium", "why": "Chamberlain's wall-mount opener frees the ceiling and handles tall or heavy doors."}],
 "products": [
  P("B07SKCGMY7", "Genie", "StealthDrive Connect 7155-TKV", ["alexa", "google-home", "smartthings", "home-assistant"],
    G("Belt", "1.25 HPc DC", "No", "Battery backup"),
    {"battery": True, "camera": False, "quiet": True, "voice": True},
    "The best-connected opener here, with Alexa, Google, and SmartThings named on the listing.",
    ["5,084 reviews", "Battery backup", "Works with SmartThings"],
    ["$334.21", "8 ft doors need an extension kit", "No camera"], "Aladdin Connect app"),
  P("B07MV2WHF4", "Genie", "QuietLift Connect (with keypad)", ["alexa", "google-home", "home-assistant"],
    G("Belt", "3/4 HPc DC", "No", "Wireless keypad, two remotes"),
    {"battery": False, "camera": False, "quiet": True, "voice": True},
    "A quiet belt drive that comes with a wireless keypad.",
    ["Keypad included", "2,015 reviews", "Sold by Amazon"],
    ["Battery backup isn't in the bullets", "Doors up to 7 ft without a kit", "$259"], "Aladdin Connect app"),
  P("B0CWM6PFP2", "Genie", "Chain Drive 500 (1135-VM)", ["alexa", "google-home", "home-assistant"],
    G("Chain", "1/2 HPc DC", "No", "Works with HomeLink and Car2U"),
    {"battery": False, "camera": False, "quiet": False, "voice": True},
    "The cheapest smart opener here, with car-remote support built in.",
    ["$215.99", "Car remotes work without a bridge", "4.4 stars"],
    ["Chain drive is louder", "Doors up to 350 lbs", "Only 65 reviews"], "Aladdin Connect app"),
  P("B0FQYSF58M", "Chamberlain", "Belt Drive myQ Opener 3/4 HP with camera", [],
    G("Belt", "3/4 HP DC", "130° built-in", "Battery backup, 2 LED bulb sockets"),
    {"battery": True, "camera": True, "quiet": True, "voice": False},
    "A camera in the opener lets you check the garage from the myQ app.",
    ["Built-in 130° camera", "Battery backup", "1K+ bought in the past month"],
    ["Bulbs sold separately", "$272.77", "Voice assistants aren't named in the bullets"], "myQ app"),
  P("B0FQXRQ561", "Chamberlain", "Chain Drive myQ Opener 3/4 HP with camera", [],
    G("Chain", "3/4 HP DC", "Built-in, wide angle", "Battery backup"),
    {"battery": True, "camera": True, "quiet": False, "voice": False},
    "The camera model with a chain drive for detached garages where noise matters less.",
    ["Built-in camera", "Battery backup", "Sold by Amazon"],
    ["Chain drive", "Bulbs sold separately", "$266.47"], "myQ app"),
  P("B0FQYM9DQS", "Chamberlain", "Belt Drive myQ Opener 1/2 HP", [],
    G("Belt", "1/2 HP DC", "No", "Battery backup, 5-year motor and belt warranty"),
    {"battery": True, "camera": False, "quiet": True, "voice": False},
    "A quiet myQ opener with battery backup for standard doors.",
    ["Battery backup", "5-year motor and belt warranty", "4.3 stars"],
    ["One bulb socket, bulb sold separately", "1/2 HP", "Only 151 reviews"], "myQ app"),
  P("B0G95ZTYDG", "Chamberlain", "1 HP Belt Drive myQ Opener with camera", [],
    G("Belt", "1 HP DC", "Built-in", "Battery backup, 10-year motor and belt warranty"),
    {"battery": True, "camera": True, "quiet": True, "voice": False},
    "A 1 HP motor for heavy doors, with a camera and a 10-year warranty.",
    ["10-year motor and belt warranty", "Built-in camera", "1 HP"],
    ["Only 30 reviews", "$349", "Single light"], "myQ app"),
  P("B0C7K97GX2", "Chamberlain", "Wall Mount myQ Opener", [],
    G("Direct drive, wall mount", NS, "No", "Battery backup, remote LED light"),
    {"battery": True, "camera": False, "quiet": True, "voice": False},
    "Mounts beside the door, so there's no rail on the ceiling and room for high-lift setups.",
    ["No ceiling rail", "Handles tall and heavy doors", "4.5 stars from 617 reviews"],
    ["$519", "Motor rating isn't in the bullets", "No camera"], "myQ app"),
  P("B09B2VHJDL", "Chamberlain", "C2212T", [],
    G("Chain", "1/2 HP", "No", "Battery backup, Bluetooth setup"),
    {"battery": True, "camera": False, "quiet": False, "voice": False},
    "A basic chain-drive myQ opener with battery backup.",
    ["Battery backup", "Bluetooth setup", "4.4 stars"],
    ["Sold by a third party at $309.99", "Chain drive", "Low stock"], "myQ app"),
  P("B0FQYW1Y69", "Craftsman", "Belt Drive Opener 3/4 HP", [],
    G("Belt", "3/4 HP DC", "No", "Battery included, 5-year motor and belt warranty"),
    {"battery": True, "camera": False, "quiet": True, "voice": False},
    "Craftsman's myQ opener, with the battery included.",
    ["Battery included", "5-year warranty", "$247"],
    ["Only 53 reviews", "Bulbs not included", "Low stock"], "Craftsman myQ app")],
 "avoid": [
  {"asin": "B0G1FWWCPT", "brand": "LiftMaster", "model": "6690L", "systems": [], "flag": "Rails sold separately",
   "verdict": "A $542.50 opener that can't be installed out of the box.",
   "reasons": ["The listing says \"Rails are sold separately\"", "Sold by a third-party dealer", "Only 16 reviews"]}]})


# ---------------- air conditioners ----------------
def A(typ, btu, room, extras):
    return {"type": typ, "btu": btu, "room": room, "extras": extras}


W("wifi-air-conditioners", {"feature_weights": {"inverter": 0.30, "google": 0.20, "quiet": 0.25, "heat": 0.25},
 "systems_note": "These ACs connect to their makers' apps; Alexa and Google support is listed per model.",
 "spec_fields": [{"key": "type", "label": "Type"}, {"key": "btu", "label": "Cooling"}, {"key": "room", "label": "Room size"}, {"key": "extras", "label": "Extras"}],
 "table_columns": [{"key": "type", "label": "Type"}, {"key": "btu", "label": "Cooling"}, {"key": "room", "label": "Room size"}],
 "awards": [
  {"asin": "B0G34M7C1M", "label": "Best Overall", "kind": "overall", "why": "Midea's U-shaped inverter AC is quiet, efficient, and leaves the window usable, rated 4.4 stars."},
  {"asin": "B0HKH91VNM", "label": "Best Budget", "kind": "budget", "why": "A 5,000 BTU smart window AC with Alexa for $195.96."},
  {"asin": "B0CVVQWGH2", "label": "Best with Heat", "kind": "special", "why": "An Energy Star inverter AC that also heats, with 2K+ bought last month."},
  {"asin": "B0CRJXS26V", "label": "Best for Big Rooms", "kind": "premium", "why": "10,000 BTU for rooms up to 450 sq ft with Alexa and Google, sold by Amazon."}],
 "products": [
  P("B0G34M7C1M", "Midea", "U Smart Inverter 6,000 BTU", ["alexa", "google-home"], A("U-shaped window, inverter", "6,000 BTU", "Up to 250 sq ft", "Window stays usable"),
    {"inverter": True, "google": True, "quiet": True, "heat": False},
    "The U shape keeps the noisy part outside and lets you still open the window.",
    ["Inverter, 37%+ energy savings", "Window opens with it installed", "Sold by Amazon"],
    ["$314.99 for 6,000 BTU", "Small rooms only", "Bracket install"], "SmartHome app"),
  P("B0FDQGPCG7", "Midea", "U Smart Inverter 8,000 BTU", ["alexa", "google-home"], A("U-shaped window, inverter", "8,000 BTU", "Up to 350 sq ft", "Window stays usable"),
    {"inverter": True, "google": True, "quiet": True, "heat": False},
    "The U design sized for a bedroom or home office.",
    ["Inverter", "906 reviews", "Quiet"],
    ["Sold by a third party", "4.1 stars", "$357.19"], "SmartHome app"),
  P("B0FDQLNGHZ", "Midea", "U Smart Inverter 10,000 BTU", ["alexa", "google-home"], A("U-shaped window, inverter", "10,000 BTU", "Up to 450 sq ft", "Window stays usable"),
    {"inverter": True, "google": True, "quiet": True, "heat": False},
    "The U design for living rooms.",
    ["450 sq ft", "Inverter", "800+ bought in the past month"],
    ["Sold by a third party", "$396.62", "Heavy to install"], "SmartHome app"),
  P("B0CVVQWGH2", "Midea", "8,000 BTU Smart Inverter with Heat", ["alexa", "google-home"], A("Window, inverter", "8,000 BTU", "Up to 350 sq ft", "Heat, dehumidify, 45 dBA"),
    {"inverter": True, "google": True, "quiet": True, "heat": True},
    "Cools in summer and heats in winter, so one unit covers a room year-round.",
    ["Heat mode", "Energy Star", "2K+ bought in the past month"],
    ["4.1 stars", "Fits windows 24 to 38.5 in", "$339.99"], "Midea app"),
  P("B0CRJXS26V", "TCL", "10,000 BTU Smart Window AC", ["alexa", "google-home"], A("Window", "10,000 BTU", "Up to 450 sq ft", "Fan and dehumidifier modes"),
    {"inverter": False, "google": True, "quiet": False, "heat": False},
    "A big-room window AC with Alexa and Google, sold by Amazon.",
    ["450 sq ft", "Alexa and Google", "Sold by Amazon"],
    ["Not inverter", "Only 102 reviews", "Noise level isn't in the bullets"], "TCL Home app"),
  P("B0CFYFCNBW", "Frigidaire", "8,000 BTU Smart Inverter", ["alexa", "google-home"], A("Window, inverter", "8,000 BTU", "Up to 350 sq ft", "Clean-filter alerts, 6-way airflow"),
    {"inverter": True, "google": True, "quiet": True, "heat": False},
    "An Energy Star inverter AC with filter reminders in the app.",
    ["Energy Star inverter", "Clean-filter alerts", "Sold by Amazon"],
    ["Only 36 reviews", "$380.57", "Low stock"], "Frigidaire app"),
  P("B0BVGF5RBB", "GE Profile", "ClearView 10,300 BTU", ["alexa", "google-home"], A("Saddle window, inverter", "10,300 BTU", "Up to 450 sq ft", "Full window view, 40 dB"),
    {"inverter": True, "google": True, "quiet": True, "heat": False},
    "Sits over the sill so the window keeps its full view, and runs as low as 40 dB.",
    ["As low as 40 dB", "Full window view", "Energy Star"],
    ["3.5 stars", "Sold by a third party", "$319.95"], "SmartHQ app"),
  P("B0HDNK1QND", "DELLA", "6,000 BTU Smart Window AC", ["alexa"], A("Window", "6,000 BTU", "Up to 250 sq ft", "Geo-location, 51 dB"),
    {"inverter": False, "google": False, "quiet": False, "heat": False},
    "A cheap smart window unit that can turn on as you head home.",
    ["$209.96", "Geo-location control", "Small and light, 38.6 lbs"],
    ["Alexa only", "4.0 stars", "Not inverter"], "Della+ app"),
  P("B0HKH91VNM", "DELLA", "5,000 BTU Smart Window AC", ["alexa"], A("Window", "5,000 BTU", "Up to 150 sq ft", "Geo-location, dehumidify"),
    {"inverter": False, "google": False, "quiet": False, "heat": False},
    "The cheapest smart AC here, for a small bedroom.",
    ["$195.96", "Geo-location control", "36.4 lbs"],
    ["150 sq ft", "Alexa only", "4.0 stars"], "Della+ app")],
 "avoid": []})


# ---------------- universal remotes ----------------
def R(hub, devices, screen, extras):
    return {"hub": hub, "devices": devices, "screen": screen, "extras": extras}


W("wifi-universal-remotes", {"feature_weights": {"matter": 0.30, "ha": 0.20, "voice": 0.25, "screen": 0.25},
 "systems_note": "SwitchBot remotes join Matter through the included hub. SofaBaton's X2 has a Home Assistant integration.",
 "spec_fields": [{"key": "hub", "label": "Hub"}, {"key": "devices", "label": "Devices"}, {"key": "screen", "label": "Screen"}, {"key": "extras", "label": "Extras"}],
 "table_columns": [{"key": "hub", "label": "Hub"}, {"key": "devices", "label": "Devices"}, {"key": "screen", "label": "Screen"}],
 "awards": [
  {"asin": "B0CXJC5ZZT", "label": "Best Overall", "kind": "overall", "why": "SwitchBot's remote and Matter hub bundle, rated 4.2 stars by 5,308 buyers."},
  {"asin": "B0FYPR3KLW", "label": "Best for Home Assistant", "kind": "special", "why": "A touchscreen remote that can also control Home Assistant over MQTT."},
  {"asin": "B0CTH5HGGT", "label": "Best for Home Theater", "kind": "premium", "why": "One-touch activities across a 500,000-device code library, with Alexa and Google."}],
 "products": [
  P("B0CXJC5ZZT", "SwitchBot", "Universal Remote with Hub Mini (Matter)", ALL7, R("Hub Mini (Matter)", "25 (10 IR + 15 Bluetooth)", "No", "10 scenes, 2,000 mAh battery"),
    {"matter": True, "ha": True, "voice": True, "screen": False},
    "A remote for TVs, ACs, and SwitchBot gear, bridged to Matter by the included hub.",
    ["5,308 reviews", "Matter through the hub", "$85.49"],
    ["Check IR and Bluetooth compatibility first", "No screen", "10 IR devices max"], "SwitchBot app"),
  P("B0FT3F7ZGZ", "SwitchBot", "Universal Remote with Hub 3", ALL7, R("Hub 3", "25 (10 IR + 15 Bluetooth)", "No", "10 scenes, IR learning"),
    {"matter": True, "ha": True, "voice": True, "screen": False},
    "The same remote bundled with the bigger Hub 3.",
    ["Hub 3 included", "Matter and Apple Home", "1,868 reviews"],
    ["3.8 stars", "$142.49", "Check compatibility first"], "SwitchBot app"),
  P("B0FYPR3KLW", "SofaBaton", "X2", ["home-assistant"], R("X2 hub with charging dock", "500,000+ devices, 6,000+ brands", "2.4 in touchscreen", "Home Assistant control over MQTT"),
    {"matter": False, "ha": True, "voice": False, "screen": True},
    "A touchscreen home theater remote that doubles as a Home Assistant controller.",
    ["Home Assistant integration", "Touchscreen", "Charging dock"],
    ["$359.99", "Only 87 reviews", "Voice assistants aren't named in the bullets"], "SofaBaton app"),
  P("B0CTH5HGGT", "SofaBaton", "X1S", ["alexa", "google-home"], R("X1S hub with 2 wired IR transmitters", "500,000+ devices", "No", "One-touch activities, raise to wake"),
    {"matter": False, "ha": False, "voice": True, "screen": False},
    "Starts the TV, soundbar, and streamer together with one button or one voice command.",
    ["Activities across devices", "Alexa and Google", "IR, Bluetooth, and Wi-Fi devices"],
    ["3.6 stars", "$179.99", "No touchscreen"], "SofaBaton app")],
 "avoid": []})
print("ok")
