import wifi
import socketpool
import board
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

from secrets import secrets
from adafruit_httpserver import Server, Request, Response

keyboard = Keyboard(usb_hid.devices)
TEXT_FILE = "/text.txt"

# Connect to Wi-Fi
print("Connecting to WiFi...")
wifi.radio.connect(secrets["ssid"], secrets["password"])
print("Connected to", secrets["ssid"])
print("IP address:", wifi.radio.ipv4_address)

# Set up HTTP server
pool = socketpool.SocketPool(wifi.radio)
server = Server(pool, "/static", debug=True)

CHAR_TO_KEYCODE = {
    'a': (Keycode.A, False), 'A': (Keycode.A, True),
    'b': (Keycode.B, False), 'B': (Keycode.B, True),
    'c': (Keycode.C, False), 'C': (Keycode.C, True),
    'd': (Keycode.D, False), 'D': (Keycode.D, True),
    'e': (Keycode.E, False), 'E': (Keycode.E, True),
    'f': (Keycode.F, False), 'F': (Keycode.F, True),
    'g': (Keycode.G, False), 'G': (Keycode.G, True),
    'h': (Keycode.H, False), 'H': (Keycode.H, True),
    'i': (Keycode.I, False), 'I': (Keycode.I, True),
    'j': (Keycode.J, False), 'J': (Keycode.J, True),
    'k': (Keycode.K, False), 'K': (Keycode.K, True),
    'l': (Keycode.L, False), 'L': (Keycode.L, True),
    'm': (Keycode.M, False), 'M': (Keycode.M, True),
    'n': (Keycode.N, False), 'N': (Keycode.N, True),
    'o': (Keycode.O, False), 'O': (Keycode.O, True),
    'p': (Keycode.P, False), 'P': (Keycode.P, True),
    'q': (Keycode.Q, False), 'Q': (Keycode.Q, True),
    'r': (Keycode.R, False), 'R': (Keycode.R, True),
    's': (Keycode.S, False), 'S': (Keycode.S, True),
    't': (Keycode.T, False), 'T': (Keycode.T, True),
    'u': (Keycode.U, False), 'U': (Keycode.U, True),
    'v': (Keycode.V, False), 'V': (Keycode.V, True),
    'w': (Keycode.W, False), 'W': (Keycode.W, True),
    'x': (Keycode.X, False), 'X': (Keycode.X, True),
    'y': (Keycode.Y, False), 'Y': (Keycode.Y, True),
    'z': (Keycode.Z, False), 'Z': (Keycode.Z, True),
    '0': (Keycode.ZERO, False), ')': (Keycode.ZERO, True),
    '1': (Keycode.ONE, False), '!': (Keycode.ONE, True),
    '2': (Keycode.TWO, False), '@': (Keycode.TWO, True),
    '3': (Keycode.THREE, False), '#': (Keycode.THREE, True),
    '4': (Keycode.FOUR, False), '$': (Keycode.FOUR, True),
    '5': (Keycode.FIVE, False), '%': (Keycode.FIVE, True),
    '6': (Keycode.SIX, False), '^': (Keycode.SIX, True),
    '7': (Keycode.SEVEN, False), '&': (Keycode.SEVEN, True),
    '8': (Keycode.EIGHT, False), '*': (Keycode.EIGHT, True),
    '9': (Keycode.NINE, False), '(': (Keycode.NINE, True),
    ' ': (Keycode.SPACE, False),
    '-': (Keycode.MINUS, False), '_': (Keycode.MINUS, True),
    '=': (Keycode.EQUALS, False), '+': (Keycode.EQUALS, True),
    '[': (Keycode.LEFT_BRACKET, False), '{': (Keycode.LEFT_BRACKET, True),
    ']': (Keycode.RIGHT_BRACKET, False), '}': (Keycode.RIGHT_BRACKET, True),
    '\\': (Keycode.BACKSLASH, False), '|': (Keycode.BACKSLASH, True),
    ';': (Keycode.SEMICOLON, False), ':': (Keycode.SEMICOLON, True),
    "'": (Keycode.QUOTE, False), '"': (Keycode.QUOTE, True),
    ',': (Keycode.COMMA, False), '<': (Keycode.COMMA, True),
    '.': (Keycode.PERIOD, False), '>': (Keycode.PERIOD, True),
    '/': (Keycode.FORWARD_SLASH, False), '?': (Keycode.FORWARD_SLASH, True),
    '`': (Keycode.GRAVE_ACCENT, False), '~': (Keycode.GRAVE_ACCENT, True),
    '\n': (Keycode.ENTER, False),
}

def save_text_to_file(text):
    with open(TEXT_FILE, "w") as f:
        f.write(text)

def load_stored_text():
    try:
        with open(TEXT_FILE, "r") as f:
            return f.read().strip()
    except OSError:
        return ""

@server.route("/set", methods=["POST"])
def set_text(request: Request):
    try:
        body = request.body.decode("utf-8").strip()
        save_text_to_file(body)  # Save the body to file
        print(f"Text saved successfully.")  # Do not print body to serial
        # Respond without printing the saved text
        return Response(request, content_type="text/plain", body="Text saved successfully.")
    except Exception as e:
        print("Set error:", e)
        return Response(
            request,
            status="500 Internal Server Error",
            content_type="text/plain",
            body=f"Error: {e}"
        )

@server.route("/print")
def print_text(request: Request):
    text = load_stored_text()
    if not text:
        return Response(
            request,
            status="404 Not Found",
            content_type="text/plain",
            body="No text to print"
        )

    print(f"Typing: {text}")
    for char in text:
        if char in CHAR_TO_KEYCODE:
            keycode, shift = CHAR_TO_KEYCODE[char]
            if shift:
                keyboard.press(Keycode.SHIFT, keycode)
            else:
                keyboard.press(keycode)
            keyboard.release_all()
        else:
            print(f"Unsupported char: {char}")
    return Response(request, content_type="text/plain", body="Text printed to keyboard.")

@server.route("/serial")
def print_to_serial(request: Request):
    text = load_stored_text()
    if not text:
        return Response(
            request,
            status="404 Not Found",
            content_type="text/plain",
            body="No text stored"
        )

    # Print the stored text to serial monitor
    print(f"[Serial Output] {text}")
    return Response(request, content_type="text/plain", body="Text sent to serial monitor.")

server.start(str(wifi.radio.ipv4_address), port=5000)
print("Server running at http://%s" % wifi.radio.ipv4_address)

while True:
    try:
        server.poll()
    except Exception as e:
        print("Server error:", e)
