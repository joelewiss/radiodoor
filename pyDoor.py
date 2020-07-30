import json
import time
import sys
from http import client as web
from threading import Timer

# WebHook configuration
HOST = "localhost"
PORT = "80"
ENDPT = "/action/doors/"

SENSORS = [
    {
        "name":     "front",
        "device":   "55555554985a8ef0b01001d20ac",
        "closed":   "a900",
        "opened":   "2900",
    },

    {
        "name":     "back",
        "device":   "55555554985a8ef0b01001d20b4",
        "closed":   "bc80",
        "opened":   "3c80",
    }
]

# These timing procedures are to prevent
# multiple calls to the API. In reality, with good radio
# conditions, the door sensors send three different open
# and close signals each.
lastMethod = ""
def send(sensor, action):
    global lastMethod

    print(f"Got call to {sensor} {action}")

    if lastMethod != sensor + action:
        url = "{}{}_{}/".format(ENDPT, sensor, action)
        print(f"Sending to {url}")
        
        client = web.HTTPConnection(HOST, port=PORT)
        client.request("GET", url)
        client.close()

    lastMethod = sensor + action


def analyse(obj):
    try:
        rows = obj["rows"]
        if (len(rows) == 1):
            data = rows[0]["data"]
            length = rows[0]["len"]
            device = data[:27]
            code = data[28:]
            special = code[1:5]

            #print(f"New data!\nLength: {length}")
            #print(f"Device ID: {device}")
            #print(f"Codes sent: {code}")
            #print(special)

            for s in SENSORS:
                if device == s["device"]:
                    print(f"Got device match for {s['name']}")
                    if special == s["closed"]:
                        send(s["name"], "close")
                    elif special == s["opened"]:
                        send(s["name"], "open")

            """
            sensor = ""

            if device == "55555554985a8ef0b01001d20ac":
                sensor = "front"
            elif device == "55555554985a8ef0b01001d20b4":
                sensor = "back"

            if sensor != "":

                if sensor == "front":
                    closed = "a900"
                    opened = "2900"
                elif sensor == "back":
                    closed = "3c80"
                    opened = "bc80"


                if special == closed:
                    send(sensor, "close") 
                elif special == opened:
                    send(sensor, "open")
            """

        else:
            print("Found json with more than one data row")

    except KeyError:
        # It was probably just noise or something...
        pass


if __name__ == "__main__":
    print("PYTHON RADIO ANALYSIS...\n\n")

    # Wait until RTL_443 is finished setting up...
    time.sleep(2)
    print("\n\n--------\nPython ready to decode\n--------\n\n")

    while True:
        line = sys.stdin.readline()
        try: 
            jsonObj = json.loads(line)
            #print(json.dumps(jsonObj, indent=True))
            analyse(jsonObj)
        except json.JSONDecodeError:
            pass
