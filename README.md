# Flight Tracker ("Overhead")

A kitchen display that shows the planes flying near home: a radar view centred on your location, the featured flight (with route, altitude, speed, aircraft type and a photo), and a list of everything in range.

## Files

| File | What it is |
|---|---|
| `index.html` | The tracker screen itself |
| `server.py` | Small helper program that serves the screen and fetches the flight data. The flight-data sites don't allow web pages to call them directly, so the helper does it for the page. Needs only Python 3. |
| `start-windows.bat` | Double-click launcher for Windows |

## Run it on a Windows computer

1. Install **Python 3** from the Microsoft Store (free, one time).
2. On this GitHub page click **Code → Download ZIP**, then unzip it somewhere (e.g. Documents).
3. Double-click **start-windows.bat**. Your browser opens **http://localhost:8000** with the tracker.
4. In **Settings**, enter your home latitude/longitude (right-click your home in Google Maps to copy them) and radius.

Keep the black window open while you use it; close it to stop.

## Run it on a Raspberry Pi (kitchen display)

```bash
git clone https://github.com/rgarabedian16/flight-tracker.git
cd flight-tracker
python3 server.py
```

Then open http://localhost:8000 in Chromium. (Auto-start on boot in full-screen kiosk mode: steps to come once the Pi is set up.)

## Settings (saved on each device)

Location and name, radius, minimum/maximum altitude, hide planes on the ground, refresh rate, and the **Featured plane** mode:
- **Mix it up** (default): rotates through planes, favouring international flights, wide-body jets, military and unusual aircraft, never the same airline twice in a row
- **Most interesting**: stays on the most unusual plane in range
- **Always closest**: the nearest plane

## Data sources

Flight positions: adsb.lol (backups: airplanes.live, adsb.fi) · Routes: adsb.lol · Photos: Planespotters.net (photographer credited on screen) · Place names: OpenStreetMap Nominatim.

The GitHub Pages copy of the page can't show live planes on its own, because it has no helper behind it. Use one of the two options above.
