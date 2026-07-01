# horizons_timeline

## what
This project is a countdown to my first every IRL hack club event, Horizons! It runs as an app on the Pimoroni Badger 2350 (an e-ink conference badge with battery power and WiFi).

It counts down days/hours until the event & shows the Hackatime projects you're working on (and how long you've spent on each), so you can see how many more hours you have to do!

## how
The project is written in MicroPython, throughout the development I learned a lot about things like tuples, classes and inherited classes! 

The biggest challenges were probably drawing the progress bars (i wrote custom classes for these!)

## why
i'm really excited for Horizons, and wanted a quick way to check out how much more coding I have to do and how much longer to go!

## installation guide
1. Download the repo & unzip
2. Put your badge in mass storage mode
3. Copy the `__init__.py`, `icon.png`, and `assets/` into a folder called `horizons_timeline` in `/system/apps` on the badge (don't copy the whole repo folder as it contains large git history)
4. Ensure your badge has wifi configured in `secrets.py`
5. Eject the badge and open the app!

## AI declaration
I used AI only for debugging and research / calculations, all of the code was written by hand!
