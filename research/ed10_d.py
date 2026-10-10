import json


def W(s, o):
    open(f'editorial/{s}.json', 'w', encoding='utf-8').write(json.dumps(o, indent=2, ensure_ascii=False))


NS = "Not stated in bullets"
ALL = ["home-assistant", "apple-home", "google-home", "alexa", "smartthings", "hubitat", "homey"]
SF = [{"key": "outlets", "label": "Outlets"}, {"key": "weather", "label": "Weather rating"}, {"key": "extras", "label": "Extras"}]
TC = [{"key": "outlets", "label": "Outlets"}, {"key": "weather", "label": "Weather"}]

W("wifi-outdoor-plugs", {"feature_weights": {"multi": 0.25, "rated": 0.25, "big_platforms": 0.30, "extra": 0.20},
 "systems_note": "Kasa plugs have an official TP-Link integration in Home Assistant; Smart Life (Tuya) plugs work with its Tuya integration.",
 "spec_fields": SF, "table_columns": TC,
 "awards": [
  {"asin": "B091FXH2FR", "label": "Best Overall", "kind": "overall", "why": "Two independent outlets, rated 4.6 stars by 17,506 buyers, with 10K+ bought last month."},
  {"asin": "B099KLNM24", "label": "Best Budget", "kind": "budget", "why": "A single IP64 outdoor plug with 300 ft Wi-Fi range for $12.99."},
  {"asin": "B0CDYPNS5K", "label": "Best for Apple Home", "kind": "premium", "why": "IP65, -20°F to 122°F, and Matter, so it works in every major system."},
  {"asin": "B08D4RQR1T", "label": "Best for Holiday Lights", "kind": "special", "why": "A six-outlet yard stake with a 6 ft cord for big light displays."}],
 "products": [
  {"asin": "B091FXH2FR", "brand": "Kasa", "model": "EP40 Outdoor Smart Plug", "systems": ["alexa", "google-home", "home-assistant"],
   "specs": {"outlets": "2, independent, 15 A each", "weather": "Cover attached", "extras": "Long Wi-Fi range"},
   "features": {"multi": True, "rated": False, "big_platforms": False, "extra": False},
   "verdict": "The most popular outdoor plug, with two outlets you can name and schedule separately.",
   "pros": ["4.6 stars from 17,506 reviews", "Independent outlets", "10K+ bought in the past month", "Home Assistant integration"],
   "cons": ["No Apple Home", "Weather rating isn't in the bullets", "No energy monitoring"]},
  {"asin": "B099KLNM24", "brand": "Kasa", "model": "KP401 Outdoor Smart Plug", "systems": ["alexa", "google-home", "home-assistant"],
   "specs": {"outlets": "1", "weather": "IP64", "extras": "Wi-Fi range up to 300 ft"},
   "features": {"multi": False, "rated": True, "big_platforms": False, "extra": False},
   "verdict": "A cheap single outdoor plug with long Wi-Fi range.",
   "pros": ["$12.99", "IP64", "4K+ bought in the past month"],
   "cons": ["One outlet", "No Apple Home", "No energy monitoring"]},
  {"asin": "B0CDYPNS5K", "brand": "Leviton", "model": "Decora Smart Outdoor Plug D215O", "systems": ALL,
   "specs": {"outlets": "1", "weather": "IP65, -20°F to 122°F", "extras": "Matter, Sonos"},
   "features": {"multi": False, "rated": True, "big_platforms": True, "extra": True},
   "verdict": "The most rugged and most connected plug here, thanks to Matter.",
   "pros": ["Matter: Apple Home, Google, Alexa, SmartThings", "IP65", "Works down to -20°F"],
   "cons": ["$59.99", "One outlet", "Only 175 reviews"]},
  {"asin": "B08HQ2N235", "brand": "meross", "model": "Outdoor Smart Plug (2 sockets)", "systems": ["apple-home", "alexa", "google-home", "smartthings"],
   "specs": {"outlets": "2, independent", "weather": "IP44", "extras": "HomeKit"},
   "features": {"multi": True, "rated": True, "big_platforms": True, "extra": False},
   "verdict": "Two outlets with HomeKit, Alexa, Google, and SmartThings.",
   "pros": ["Apple HomeKit", "SmartThings", "4.4 stars from 3,956 reviews"],
   "cons": ["IP44 only", "HomeKit remote access needs a home hub", "$25.99"]},
  {"asin": "B08NXY7WWX", "brand": "Wyze", "model": "Plug Outdoor", "systems": ["alexa", "google-home"], "systems_label": "Wyze app",
   "specs": {"outlets": "2, independent", "weather": "IP64", "extras": "Energy monitoring"},
   "features": {"multi": True, "rated": True, "big_platforms": False, "extra": True},
   "verdict": "The only outdoor plug here that tracks energy use.",
   "pros": ["Energy monitoring", "IP64", "4.5 stars"],
   "cons": ["$36.97", "No Apple Home", "Wyze app"]},
  {"asin": "B0BFWMQTZ7", "brand": "ELEGRP", "model": "PQR20 Outdoor Smart Plug", "systems": ["alexa", "google-home"],
   "specs": {"outlets": "2, independent", "weather": "IP66", "extras": "Long-range Wi-Fi"},
   "features": {"multi": True, "rated": True, "big_platforms": False, "extra": False},
   "verdict": "The best weather rating here at IP66.",
   "pros": ["IP66", "Independent outlets", "$26.99"],
   "cons": ["Pumps limited to 1/2 HP", "Only 824 reviews", "2.4 GHz only"]},
  {"asin": "B07JQSX11M", "brand": "BN-LINK", "model": "Outdoor Smart Plug (3 outlets)", "systems": ["alexa", "google-home", "home-assistant"], "systems_label": "Smart Life",
   "specs": {"outlets": "3, switched together", "weather": "IP44", "extras": "6.8 in. cord"},
   "features": {"multi": True, "rated": True, "big_platforms": False, "extra": False},
   "verdict": "Three heavy-duty outlets on a short cord, with 13,773 reviews.",
   "pros": ["3 grounded outlets", "13,773 reviews", "$21.99"],
   "cons": ["Outlets switch together", "IP44", "Smart Life app"]},
  {"asin": "B08D4RQR1T", "brand": "HBN", "model": "Smart Outdoor Power Stake (6 outlets)", "systems": ["alexa", "google-home"],
   "specs": {"outlets": "6, on a yard stake", "weather": NS, "extras": "6 ft cord"},
   "features": {"multi": True, "rated": False, "big_platforms": False, "extra": True},
   "verdict": "Push it into the lawn and power a whole holiday display from one outlet.",
   "pros": ["6 outlets", "6 ft cord", "400+ bought in the past month"],
   "cons": ["4.2 stars", "Weather rating isn't in the bullets", "Outlets switch together"]},
  {"asin": "B094YHJJVG", "brand": "Amazon Basics", "model": "Outdoor Smart Plug", "systems": ["alexa"],
   "specs": {"outlets": "2, independent", "weather": "IP65", "extras": "Alexa groups"},
   "features": {"multi": True, "rated": True, "big_platforms": False, "extra": False},
   "verdict": "An IP65 two-outlet plug for Alexa homes, and only Alexa homes.",
   "pros": ["IP65", "Independent outlets", "3K+ bought in the past month"],
   "cons": ["Alexa only", "No app outside Alexa", "$23.99"]},
  {"asin": "B09DT173R1", "brand": "Kasa", "model": "Outdoor Smart Dimmer Plug", "systems": ["alexa", "google-home", "smartthings", "home-assistant"],
   "specs": {"outlets": "1, dimming", "weather": "IP64", "extras": "Dims string lights (150 W LED max)"},
   "features": {"multi": False, "rated": True, "big_platforms": False, "extra": True},
   "verdict": "Dims dimmable patio string lights from your phone or voice.",
   "pros": ["Dimming", "IP64", "2K+ bought in the past month"],
   "cons": ["Dimmable lights only", "150 W LED limit", "4.3 stars"]}],
 "avoid": []})
print("ok")
