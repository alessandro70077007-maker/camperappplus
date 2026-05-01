CAMPERappPLUS v1.0
====================

Thanks for trying CAMPERappPLUS. This app does not need installation:
just extract and launch. The in-app UI is available in 5 languages
(Italian, English, German, French, Spanish) — change it in Settings.


HOW TO LAUNCH
-------------

1. Extract this folder (CamperAppPlus) anywhere on your PC.
   Example: Documents\CamperAppPlus

2. Open the extracted folder.

3. Double-click  CamperAppPlus.exe

4. A Microsoft Edge window will open with the app inside.


SMARTSCREEN WARNING ON FIRST LAUNCH
------------------------------------

Windows will likely show a blue warning saying "Windows protected
your PC". This is normal: the app is not digitally signed (signing
costs hundreds of euros per year) but it is safe and fully local.

To proceed:
- Click "More info"
- Click "Run anyway" (button at the bottom)

You only need to do this once.


REQUIREMENTS
------------

- Windows 10 or 11 (64-bit)
- Microsoft Edge already installed (it's bundled with Windows)
- Internet connection for: parking site map, weather, geolocation
  (everything else works offline)


WHERE IS MY DATA?
-----------------

Your data and documents are stored in:
   %APPDATA%\CamperAppPlus\data

(typically: C:\Users\YOURNAME\AppData\Roaming\CamperAppPlus\data)

This folder survives app updates. If you delete the extracted folder,
your data stays.

For a complete backup (DB + documents): Settings -> Backup -> Export.
This generates a ZIP you can import on another PC.


HOW TO QUIT
-----------

Close the Edge window. The app will stop automatically.
If the Edge window won't close, right-click the taskbar icon and
choose "Close window".


COMMON ISSUES
-------------

* "App won't open" / "Edge opens but the page is blank":
  Try again. The first launch can take 10-20 seconds for Streamlit
  to start. If it persists, make sure Edge is installed.

* "Parking sites won't load":
  Internet is required. Also make sure you've granted geolocation
  permission, or use the "Search by city or place name" field.

* "GPS shows me in another city":
  On a desktop PC without GPS hardware, Edge uses your IP to estimate
  the location, which can be inaccurate. Use the "Search by city or
  place name" field on the Map page.


FEEDBACK
--------

Bugs, ideas, requests: alessandro7007@live.it


Have a great trip!
