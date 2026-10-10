import json


def W(s, o):
    open(f'editorial/{s}.json', 'w', encoding='utf-8').write(json.dumps(o, indent=2, ensure_ascii=False))


NS = "Not stated in bullets"
DF = [{"key": "capacity", "label": "Capacity"}, {"key": "coverage", "label": "Room size"}, {"key": "drain", "label": "Drainage"}, {"key": "app", "label": "App"}]
DT = [{"key": "capacity", "label": "Capacity"}, {"key": "coverage", "label": "Room"}, {"key": "drain", "label": "Drainage"}]
MID = ["alexa", "google-home"]

W("wifi-dehumidifiers", {"feature_weights": {"big": 0.25, "pump": 0.25, "voice": 0.25, "energy_star": 0.25},
 "systems_note": "LG ThinQ appliances have an official Home Assistant integration.",
 "spec_fields": DF, "table_columns": DT,
 "awards": [
  {"asin": "B07NRDBBH5", "label": "Best Overall", "kind": "overall", "why": "Rated 4.4 stars by 7,197 buyers, with Wi-Fi, Alexa, Google, and Energy Star."},
  {"asin": "B073VBWKJZ", "label": "Best for Large Basements", "kind": "premium", "why": "50 pints for spaces up to 7,000 sq. ft., with 25,680 reviews."},
  {"asin": "B0GL7R3RJV", "label": "Best With a Pump", "kind": "special", "why": "A built-in pump pushes water up into a sink, so you never empty a bucket."},
  {"asin": "B08ZMY8BC8", "label": "Best Compact", "kind": "budget", "why": "Midea's Cube stacks its bucket underneath to save floor space."}],
 "products": [
  {"asin": "B07NRDBBH5", "brand": "Midea", "model": "22 Pint Dehumidifier", "systems": MID, "systems_label": "SmartHome app",
   "specs": {"capacity": "22 pints/day", "coverage": "Up to 1,500 sq. ft.", "drain": "Bucket or hose", "app": "Midea SmartHome"},
   "features": {"big": False, "pump": False, "voice": True, "energy_star": True},
   "verdict": "The best all-round smart dehumidifier for a bedroom or small basement.",
   "pros": ["7,197 reviews", "Alexa and Google", "Energy Star"],
   "cons": ["22 pints", "No pump", "$194.99"]},
  {"asin": "B073VBWKJZ", "brand": "hOmeLabs", "model": "50 Pint Dehumidifier (7,000 sq. ft.)", "systems": [], "systems_label": "hOmeLabs app",
   "specs": {"capacity": "50 pints (120 max at 95°F)", "coverage": "Up to 7,000 sq. ft.", "drain": "Bucket or hose", "app": "Wi-Fi app"},
   "features": {"big": True, "pump": False, "voice": False, "energy_star": False},
   "verdict": "The most-reviewed large dehumidifier, now with Wi-Fi.",
   "pros": ["25,680 reviews", "Up to 7,000 sq. ft.", "Remote control by app"],
   "cons": ["$269.99", "Voice assistants aren't named in the bullets", "Heavy"]},
  {"asin": "B0GL7QFBJ9", "brand": "Midea", "model": "50 Pint Dehumidifier", "systems": MID, "systems_label": "SmartHome app",
   "specs": {"capacity": "50 pints/day", "coverage": "Up to 4,500 sq. ft.", "drain": "Bucket or hose", "app": "Midea SmartHome"},
   "features": {"big": True, "pump": False, "voice": True, "energy_star": True},
   "verdict": "Midea's large-basement model with voice control.",
   "pros": ["50 pints", "Alexa and Google", "Energy Star"],
   "cons": ["Only 224 reviews", "No pump", "$219.99"]},
  {"asin": "B0GL7R3RJV", "brand": "Midea", "model": "50 Pint Dehumidifier with Pump", "systems": MID, "systems_label": "SmartHome app",
   "specs": {"capacity": "50 pints/day", "coverage": "Up to 4,500 sq. ft.", "drain": "Built-in pump", "app": "Midea SmartHome"},
   "features": {"big": True, "pump": True, "voice": True, "energy_star": True},
   "verdict": "The same Midea with a pump, for basements without a floor drain.",
   "pros": ["Built-in pump", "Alexa and Google", "Energy Star"],
   "cons": ["4.1 stars", "Only 151 reviews", "$220.45"]},
  {"asin": "B0BR7RHQB9", "brand": "GoveeLife", "model": "Dehumidifier (50-137 pints)", "systems": ["alexa", "google-home"], "systems_label": "Govee Home",
   "specs": {"capacity": "Up to 137 pints (test conditions)", "coverage": "Up to 4,500 sq. ft.", "drain": "2-gallon bucket or hose", "app": "Govee Home"},
   "features": {"big": True, "pump": False, "voice": True, "energy_star": False},
   "verdict": "A big-capacity unit with app, voice, and touch control.",
   "pros": ["Alexa and Google", "2-gallon bucket", "1,588 reviews"],
   "cons": ["4.0 stars", "$229.99", "Max pints measured at extreme conditions"]},
  {"asin": "B0GXYD5JBY", "brand": "Dreo", "model": "Smart Dehumidifier (Energy Star 2025)", "systems": [], "systems_label": "Dreo app",
   "specs": {"capacity": NS, "coverage": "Basement", "drain": "1.85-gallon tank or hose", "app": "Dreo, with energy tracking"},
   "features": {"big": True, "pump": False, "voice": False, "energy_star": True},
   "verdict": "Tracks its own energy use in the app.",
   "pros": ["Energy tracking", "Energy Star", "4.3 stars"],
   "cons": ["Only 249 reviews", "Voice control isn't in the bullets", "$199.96"]},
  {"asin": "B0H42G5D34", "brand": "LG", "model": "PuriCare 50-Pint WiFi Dehumidifier", "systems": ["home-assistant"], "systems_label": "LG ThinQ",
   "specs": {"capacity": "50 pints/day", "coverage": NS, "drain": "Bucket or hose", "app": "LG ThinQ"},
   "features": {"big": True, "pump": False, "voice": False, "energy_star": False},
   "verdict": "LG's 50-pint unit, controlled in the ThinQ app with your other LG appliances.",
   "pros": ["LG ThinQ app", "Home Assistant integration", "50 pints"],
   "cons": ["Only 47 reviews", "$260.99", "Voice assistants aren't named in the bullets"]},
  {"asin": "B08ZMY8BC8", "brand": "Midea", "model": "Cube 20 Pint", "systems": MID, "systems_label": "SmartHome app",
   "specs": {"capacity": "20 pints/day", "coverage": "Up to 1,500 sq. ft.", "drain": "Stacked bucket or hose", "app": "Midea SmartHome"},
   "features": {"big": False, "pump": False, "voice": True, "energy_star": True},
   "verdict": "A compact cube that tucks its bucket underneath.",
   "pros": ["Compact", "Alexa and Google", "2,536 reviews"],
   "cons": ["4.0 stars", "20 pints", "$179.99"]},
  {"asin": "B0DFZHBSZX", "brand": "Frigidaire", "model": "22-Pint Wi-Fi Dehumidifier", "systems": ["alexa"], "systems_label": "Frigidaire app",
   "specs": {"capacity": "22 pints/day", "coverage": "Small to medium rooms", "drain": NS, "app": "Frigidaire"},
   "features": {"big": False, "pump": False, "voice": True, "energy_star": True},
   "verdict": "A small Wi-Fi dehumidifier from a big appliance brand.",
   "pros": ["Energy Star", "Wi-Fi", "Alexa"],
   "cons": ["Only 159 reviews", "$199", "22 pints"]},
  {"asin": "B0GWQDR1PK", "brand": "ALORAIR", "model": "Smart Wi-Fi 70 Pint Crawlspace", "systems": [], "systems_label": "ALORAIR app",
   "specs": {"capacity": "70 pints/day", "coverage": "Crawlspace or basement", "drain": "Built-in pump", "app": "Wi-Fi app"},
   "features": {"big": True, "pump": True, "voice": False, "energy_star": False},
   "verdict": "A low-profile crawlspace dehumidifier with a pump and remote monitoring.",
   "pros": ["Built for crawlspaces", "Built-in pump", "70 pints"],
   "cons": ["$422.93", "Only 158 reviews", "4.1 stars"]}],
 "avoid": []})
print("ok")
