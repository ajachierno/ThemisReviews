import json


def W(s, o):
    open(f'editorial/{s}.json', 'w', encoding='utf-8').write(json.dumps(o, indent=2, ensure_ascii=False))


NS = "Not stated in bullets"
ZW = ["home-assistant", "smartthings", "hubitat", "homey"]

W("z-wave-range-extenders", {"feature_weights": {"dedicated": 0.30, "s800": 0.30, "any_hub": 0.25, "bonus": 0.15},
 "systems_note": "Every plug-in Z-Wave device repeats the mesh; the plugs here are sold partly as range extenders. The Ring extender only works inside a Ring Alarm system.",
 "spec_fields": [{"key": "type", "label": "Type"}, {"key": "series", "label": "Z-Wave"}, {"key": "extra", "label": "Also does"}],
 "table_columns": [{"key": "type", "label": "Type"}, {"key": "series", "label": "Z-Wave"}],
 "awards": [
  {"asin": "B081G97TLB", "label": "Best Overall", "kind": "overall", "why": "A dedicated repeater for any Z-Wave hub, rated 4.2 stars by 845 buyers."},
  {"asin": "B0BHL9MBRZ", "label": "Best Long Range Plug", "kind": "special", "why": "An 800 Series Long Range plug with power monitoring that also repeats your mesh."},
  {"asin": "B07ZB2VP4K", "label": "Best for Ring Alarm", "kind": "budget", "why": "A $14.99 extender for Ring Alarm systems, 4,194 reviews."}],
 "products": [
  {"asin": "B081G97TLB", "brand": "Aeotec", "model": "Range Extender 7", "systems": ZW,
   "specs": {"type": "Dedicated repeater", "series": "700 Series (Gen7), S2", "extra": "Repeats secure S2 devices such as locks"},
   "features": {"dedicated": True, "s800": False, "any_hub": True, "bonus": False},
   "verdict": "The standard fix for a weak spot in a Z-Wave mesh.",
   "pros": ["Works with any Z-Wave hub", "Repeats S2 security devices", "400+ bought in the past month"],
   "cons": ["700 Series", "Does nothing else", "4.2 stars"]},
  {"asin": "B0BHL9MBRZ", "brand": "Zooz", "model": "ZEN04 800LR Smart Plug", "systems": ["home-assistant", "smartthings", "hubitat", "homey"],
   "specs": {"type": "Smart plug that repeats", "series": "800 Series, Long Range", "extra": "Power monitoring, 15 A"},
   "features": {"dedicated": False, "s800": True, "any_hub": True, "bonus": True},
   "verdict": "A Long Range smart plug that strengthens the mesh while it switches a lamp.",
   "pros": ["4.8 stars", "Power monitoring", "800 Series Long Range"],
   "cons": ["Only 70 reviews", "$35.95", "Not a dimmer"]},
  {"asin": "B0CQX4JFV2", "brand": "Minoston", "model": "Mini Z-Wave 800 plug (repeater)", "systems": ["home-assistant", "smartthings", "hubitat", "homey"],
   "specs": {"type": "Smart plug that repeats", "series": "800 Series", "extra": "15 A, schedules"},
   "features": {"dedicated": False, "s800": True, "any_hub": True, "bonus": True},
   "verdict": "A cheap 800 Series plug sold as a repeater and range extender.",
   "pros": ["$26.09", "4.5 stars from 507 reviews", "Compact"],
   "cons": ["No power monitoring", "Sold by a third party", "Voice control needs your hub's integration"]},
  {"asin": "B0CQS4SS9F", "brand": "New One", "model": "Z-Wave 800 smart plug (repeater)", "systems": ["home-assistant", "smartthings", "hubitat", "homey"],
   "specs": {"type": "Smart plug that repeats", "series": "800 Series", "extra": "Up to 1,300 ft open-air range"},
   "features": {"dedicated": False, "s800": True, "any_hub": True, "bonus": True},
   "verdict": "An 800 Series plug that relays signals up to four hops deep.",
   "pros": ["4.7 stars", "800 Series", "$26.99"],
   "cons": ["Only 32 reviews", "Doesn't work with Echo hubs", "Lesser-known brand"]},
  {"asin": "B07ZB2VP4K", "brand": "Ring", "model": "Alarm Range Extender (2nd Gen)", "systems": ["alexa"], "systems_label": "Ring Alarm only",
   "specs": {"type": "Dedicated repeater", "series": "Z-Wave (Ring Alarm network)", "extra": "Up to 250 ft"},
   "features": {"dedicated": True, "s800": False, "any_hub": False, "bonus": False},
   "verdict": "Only for Ring Alarm: it boosts the Ring Base Station's network and nothing else.",
   "pros": ["$14.99", "4,194 reviews", "Sold by Amazon"],
   "cons": ["Requires a Ring Alarm Base Station", "Won't help other Z-Wave hubs", "Stock status wasn't shown"]}],
 "avoid": []})

W("z-wave-garage-openers", {"feature_weights": {"tilt": 0.30, "warning": 0.25, "lr": 0.20, "multi_door": 0.25},
 "systems_note": "Zooz relays need a separate tilt or contact sensor to report whether the door is open.",
 "spec_fields": [{"key": "type", "label": "Type"}, {"key": "doors", "label": "Doors"}, {"key": "sensor", "label": "Door sensor"}, {"key": "series", "label": "Z-Wave"}],
 "table_columns": [{"key": "type", "label": "Type"}, {"key": "doors", "label": "Doors"}, {"key": "sensor", "label": "Sensor"}],
 "awards": [
  {"asin": "B0846DZJD8", "label": "Best Overall", "kind": "overall", "why": "Three dry-contact relays run up to three garage doors from one Long Range module, 4.6 stars."},
  {"asin": "B0FXYWJ47K", "label": "Best All-in-One", "kind": "special", "why": "A dedicated garage controller with the tilt sensor in the box."}],
 "products": [
  {"asin": "B0846DZJD8", "brand": "Zooz", "model": "ZEN16 MultiRelay 800LR", "systems": ZW,
   "specs": {"type": "3-relay module", "doors": "Up to 3", "sensor": "Add a tilt or contact sensor", "series": "800 Series, Long Range"},
   "features": {"tilt": False, "warning": False, "lr": True, "multi_door": True},
   "verdict": "The favorite DIY garage controller: one module for up to three doors.",
   "pros": ["Up to 3 doors", "4.6 stars from 507 reviews", "Long Range"],
   "cons": ["Needs a separate door sensor", "Power supply not included", "No built-in warning light or beeper"]},
  {"asin": "B096LLL1C6", "brand": "Zooz", "model": "ZEN17 Relay 800LR", "systems": ZW,
   "specs": {"type": "2-relay module with 2 inputs", "doors": "Up to 2", "sensor": "Wire a sensor to its inputs", "series": "800 Series, Long Range"},
   "features": {"tilt": False, "warning": False, "lr": True, "multi_door": True},
   "verdict": "Two relays plus two sensor inputs, so it can report the door state too.",
   "pros": ["Built-in sensor inputs", "Up to 2 doors", "USB-C cable included"],
   "cons": ["Needs a wired sensor", "No warning beeper", "$45.75"]},
  {"asin": "B0FXYWJ47K", "brand": "GoControl", "model": "GD00Z-7 Smart Garage Door Controller", "systems": ZW,
   "specs": {"type": "Dedicated garage controller", "doors": "1", "sensor": "Tilt sensor included", "series": "Z-Wave Plus"},
   "features": {"tilt": True, "warning": True, "lr": False, "multi_door": False},
   "verdict": "Everything for one door in the box, including the tilt sensor.",
   "pros": ["Tilt sensor included", "Purpose-built for garage doors", "Installation hardware included"],
   "cons": ["Only 1 review on this listing", "Z-Wave Plus, not 800 Series", "$74.99"]}],
 "avoid": [
  {"asin": "B085LKPHK6", "brand": "GoControl", "model": "GD00Z-8-GC (reseller listing)", "systems": ZW,
   "flag": "Listing copy is for a door lock",
   "verdict": "The title names a Z-Wave garage controller, but the only product detail tells you to measure your door's backset and cross bore, which is how you size a door lock. Buy the GD00Z-7 listing above instead.",
   "reasons": ["Title: \"GD00Z-8-GC: Z-Wave Plus S2 Security, Black, Small.\"", "Bullet: \"Measure your door's backset, cross bore and thickness to ensure you find the right fit.\"", "Sold by a reseller, with 16 left at capture time."]}]})

W("z-wave-water-valves", {"feature_weights": {"no_plumber": 0.35, "leak_sensor": 0.30, "strong": 0.20, "outdoor": 0.15},
 "spec_fields": [{"key": "install", "label": "Install"}, {"key": "pipes", "label": "Valve sizes"}, {"key": "sensor", "label": "Leak sensor"}, {"key": "series", "label": "Z-Wave"}],
 "table_columns": [{"key": "install", "label": "Install"}, {"key": "pipes", "label": "Valves"}, {"key": "sensor", "label": "Sensor"}],
 "awards": [
  {"asin": "B09G82YM3B", "label": "Best Overall", "kind": "overall", "why": "A strong valve actuator with a leak sensor in the box and no tools needed."},
  {"asin": "B07DJZCFBH", "label": "Best Rated", "kind": "special", "why": "The Bulldog Valve Robot, rated 4.7 stars by 280 buyers."}],
 "products": [
  {"asin": "B09G82YM3B", "brand": "Zooz", "model": "ZAC36 Titan Water Valve Actuator", "systems": ZW,
   "specs": {"install": "Clamps over your ball valve, no tools", "pipes": "0.5 to 1.25 in. ball valves", "sensor": "Plug-in leak sensor included", "series": "700 Series"},
   "features": {"no_plumber": True, "leak_sensor": True, "strong": True, "outdoor": True},
   "verdict": "Shuts your main water off automatically when a leak is found, and installs in minutes.",
   "pros": ["Leak sensor included", "Powerful motor for stiff valves", "Usable outdoors", "Works with Ring Alarm"],
   "cons": ["Needs 3 in. of clearance on each side", "$199.95", "Only 19 left at capture time"]},
  {"asin": "B07DJZCFBH", "brand": "EcoNet Controls", "model": "Bulldog Valve Robot (EVC200-HCSML)", "systems": ["smartthings", "hubitat", "home-assistant", "homey"],
   "specs": {"install": "Mounts over existing valve, no plumbing", "pipes": "Quarter-turn ball valves", "sensor": "Not included", "series": "Z-Wave Plus"},
   "features": {"no_plumber": True, "leak_sensor": False, "strong": True, "outdoor": False},
   "verdict": "A well-rated, long-running valve robot for Z-Wave hubs.",
   "pros": ["4.7 stars", "No plumbing", "Wide hub compatibility"],
   "cons": ["No leak sensor in the box", "$215", "Z-Wave Plus, not 800 Series"]}],
 "avoid": []})
print("ok")
