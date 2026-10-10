import json


def W(s, o):
    open(f'editorial/{s}.json', 'w', encoding='utf-8').write(json.dumps(o, indent=2, ensure_ascii=False))


NS = "Not stated in bullets"
ALL = ["home-assistant", "apple-home", "google-home", "alexa", "smartthings", "hubitat", "homey"]
LV = ["home-assistant"]
HF = [{"key": "tank", "label": "Tank"}, {"key": "coverage", "label": "Room size"}, {"key": "mist", "label": "Mist"}, {"key": "auto", "label": "Auto humidity"}]
HT = [{"key": "tank", "label": "Tank"}, {"key": "coverage", "label": "Room"}, {"key": "mist", "label": "Mist"}]

W("wifi-humidifiers", {"feature_weights": {"auto": 0.25, "voice": 0.25, "warm": 0.25, "big": 0.25},
 "systems_note": "Levoit (VeSync) humidifiers work with Home Assistant's official VeSync integration; their listings here don't name Alexa or Google.",
 "spec_fields": HF, "table_columns": HT,
 "awards": [
  {"asin": "B0CCVX6FSD", "label": "Best Overall", "kind": "overall", "why": "A quiet 4 L smart humidifier with Alexa and Google, rated 4.4 stars by 12,139 buyers."},
  {"asin": "B0BT93MJ4G", "label": "Best Budget", "kind": "budget", "why": "A top-fill 3 L smart humidifier with auto mode for $31.99, 6K+ bought last month."},
  {"asin": "B0DT48R3BR", "label": "Best for Large Rooms", "kind": "premium", "why": "8 L, warm or cool mist, 80-hour runtime, and voice control."},
  {"asin": "B0GR9DHR8W", "label": "Best Evaporative", "kind": "special", "why": "An evaporative model that can't over-humidify or leave white dust, at 19 dB."}],
 "products": [
  {"asin": "B0CCVX6FSD", "brand": "Dreo", "model": "Smart Humidifier 4L", "systems": ["alexa", "google-home"], "systems_label": "Dreo app",
   "specs": {"tank": "4 L", "coverage": "Bedroom", "mist": "Cool", "auto": NS},
   "features": {"auto": False, "voice": True, "warm": False, "big": False},
   "verdict": "The bedroom humidifier to get: quiet, simple, and works with Alexa and Google.",
   "pros": ["12,139 reviews", "Alexa and Google", "5K+ bought in the past month"],
   "cons": ["Cool mist only", "Auto mode isn't in the bullets", "4 L"]},
  {"asin": "B0BT93MJ4G", "brand": "GoveeLife", "model": "Smart Humidifier 3L", "systems": ["alexa", "google-home"], "systems_label": "Govee Home",
   "specs": {"tank": "3 L, top fill", "coverage": "Bedroom", "mist": "Cool", "auto": "Yes"},
   "features": {"auto": True, "voice": True, "warm": False, "big": False},
   "verdict": "A cheap top-fill humidifier with auto humidity and voice control.",
   "pros": ["$31.99", "Auto humidity", "6K+ bought in the past month"],
   "cons": ["4.2 stars", "3 L", "Cool mist only"]},
  {"asin": "B0C2GKJ9RT", "brand": "Levoit", "model": "Dual 200S (3L)", "systems": LV, "systems_label": "VeSync app",
   "specs": {"tank": "3 L, top fill", "coverage": "Bedroom", "mist": "Cool", "auto": "Yes"},
   "features": {"auto": True, "voice": False, "warm": False, "big": False},
   "verdict": "The most-reviewed smart humidifier, with an auto mode.",
   "pros": ["63,981 reviews", "Auto mode", "Quiet"],
   "cons": ["Voice assistants aren't named in the bullets", "3 L", "$49.99"]},
  {"asin": "B0GR99R7XD", "brand": "Levoit", "model": "Smart Humidifier 6.2L", "systems": LV, "systems_label": "VeSync app",
   "specs": {"tank": "6.2 L", "coverage": "Up to 536 sq. ft.", "mist": "Cool", "auto": "Yes"},
   "features": {"auto": True, "voice": False, "warm": False, "big": True},
   "verdict": "A big-tank Levoit for living rooms, at 26 dB.",
   "pros": ["6.2 L tank", "26 dB", "5K+ bought in the past month"],
   "cons": ["Cool mist only", "Voice assistants aren't named in the bullets", "$79.99"]},
  {"asin": "B0CB4CK3ZS", "brand": "Dreo", "model": "Smart Humidifier 6L (warm and cool)", "systems": [], "systems_label": "Dreo app",
   "specs": {"tank": "6 L", "coverage": "Up to 550 sq. ft.", "mist": "Warm and cool", "auto": "Yes"},
   "features": {"auto": True, "voice": False, "warm": True, "big": True},
   "verdict": "Warm or cool mist for a large room, with auto humidity.",
   "pros": ["Warm and cool mist", "Auto humidity", "5,679 reviews"],
   "cons": ["Voice control isn't in the bullets", "4.3 stars", "$79.93"]},
  {"asin": "B0DHRD584W", "brand": "GoveeLife", "model": "Smart Humidifier 6L", "systems": ["alexa", "google-home"], "systems_label": "Govee Home",
   "specs": {"tank": "6 L, top fill", "coverage": "Up to 500 sq. ft.", "mist": "Warm and cool", "auto": "Yes"},
   "features": {"auto": True, "voice": True, "warm": True, "big": True},
   "verdict": "Warm or cool mist, auto humidity, and voice control in one.",
   "pros": ["4.5 stars", "Warm and cool mist", "Alexa and Google"],
   "cons": ["Only 570 reviews", "$79.99", "Govee Home app"]},
  {"asin": "B095KGXPW5", "brand": "Levoit", "model": "LV600S (warm and cool)", "systems": LV, "systems_label": "VeSync app",
   "specs": {"tank": NS, "coverage": "Large room", "mist": "Warm and cool", "auto": "Yes"},
   "features": {"auto": True, "voice": False, "warm": True, "big": True},
   "verdict": "Levoit's warm-and-cool large-room model.",
   "pros": ["Warm and cool mist", "Auto humidity", "6,814 reviews"],
   "cons": ["$109", "4.3 stars", "Voice assistants aren't named in the bullets"]},
  {"asin": "B0DT48R3BR", "brand": "Dreo", "model": "HM717S Smart Humidifier 8L", "systems": ["alexa", "google-home"], "systems_label": "Dreo app",
   "specs": {"tank": "8 L, 80-hour runtime", "coverage": "Up to 600 sq. ft.", "mist": "Warm and cool", "auto": "Yes"},
   "features": {"auto": True, "voice": True, "warm": True, "big": True},
   "verdict": "The large-room pick: 8 liters, warm or cool, and voice control.",
   "pros": ["80-hour runtime", "Warm and cool mist", "Alexa and Google"],
   "cons": ["$99.94", "Only 950 reviews", "Large footprint"]},
  {"asin": "B0GR9DHR8W", "brand": "Levoit", "model": "Superior Studio Evaporative", "systems": LV, "systems_label": "VeSync app",
   "specs": {"tank": NS, "coverage": "Up to 600 sq. ft.", "mist": "Evaporative", "auto": "Yes"},
   "features": {"auto": True, "voice": False, "warm": False, "big": True},
   "verdict": "Evaporative humidifying with no white dust, at a whisper-quiet 19 dB.",
   "pros": ["Evaporative, no white dust", "19 dB", "1K+ bought in the past month"],
   "cons": ["$139.99", "Wick filters to replace", "Only 294 reviews"]},
  {"asin": "B0GZWKMDLF", "brand": "Dreo", "model": "747S Smart Humidifier 11L", "systems": [], "systems_label": "Dreo app",
   "specs": {"tank": "11 L, 100-hour runtime", "coverage": "Up to 700 sq. ft.", "mist": "Cool", "auto": "Yes"},
   "features": {"auto": True, "voice": False, "warm": False, "big": True},
   "verdict": "The biggest tank here, for open-plan spaces.",
   "pros": ["11 L, 100-hour runtime", "21 dB", "1K+ bought in the past month"],
   "cons": ["Only 92 reviews", "Voice control isn't in the bullets", "$99.98"]}],
 "avoid": []})

GF = [{"key": "type", "label": "Type"}, {"key": "radio", "label": "Connection"}, {"key": "extras", "label": "Extras"}]
W("matter-garage-openers", {"feature_weights": {"remote": 0.30, "no_wiring": 0.35, "rating": 0.35},
 "spec_fields": GF, "table_columns": GF,
 "awards": [
  {"asin": "B0FF4VHCJV", "label": "Best Overall", "kind": "overall", "why": "A Matter-certified garage controller with no hub or monthly fee, for $24.99."},
  {"asin": "B0FX4G3ML2", "label": "Best No-Wiring Install", "kind": "special", "why": "Retrofits with your existing remote instead of wiring to the opener."}],
 "products": [
  {"asin": "B0FF4VHCJV", "brand": "SwitchBot", "model": "Smart Garage Door Opener (Matter)", "systems": ALL,
   "specs": {"type": "Wired controller", "radio": "Wi-Fi (Matter)", "extras": "No hub, no monthly fee"},
   "features": {"remote": False, "no_wiring": False, "rating": True},
   "verdict": "The cheapest way to put a garage door into Apple Home, Google, or Alexa.",
   "pros": ["$24.99", "No hub or monthly fee", "Matter certified"],
   "cons": ["Only 78 reviews", "4.1 stars", "Wires to the opener"]},
  {"asin": "B0F38C31H2", "brand": "SwitchBot", "model": "Smart Garage Door Opener with Remote (Matter)", "systems": ALL,
   "specs": {"type": "Wired controller + remote", "radio": "Wi-Fi (Matter)", "extras": "Remote included, auto-close schedules"},
   "features": {"remote": True, "no_wiring": False, "rating": True},
   "verdict": "The same controller plus a handheld remote for family members.",
   "pros": ["Remote included", "Auto-close schedules", "Names Home Assistant"],
   "cons": ["$44.99", "4.1 stars", "Wires to the opener"]},
  {"asin": "B0FX4G3ML2", "brand": "THIRDREALITY", "model": "Smart Garage Door Opener (Matter)", "systems": ALL,
   "specs": {"type": "Retrofit using your existing remote", "radio": "Wi-Fi (Matter)", "extras": "Sectional doors only"},
   "features": {"remote": False, "no_wiring": True, "rating": False},
   "verdict": "Installs with your existing remote, so there's nothing to wire to the opener.",
   "pros": ["No opener wiring", "Matter certified", "Names Home Assistant and Homey"],
   "cons": ["Needs a Matter controller", "Sectional (flip-up) doors only", "4.0 stars"]}],
 "avoid": []})
print("ok")
