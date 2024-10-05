import hub75
import time
import network
import ubinascii
import urequests
import qrcode
import ujson
import gc
from get_proxmox_data import get_node_usage
from draw_number import *

HEIGHT = 32
WIDTH = 64

h75 = hub75.Hub75(WIDTH, HEIGHT, stb_invert=False)
h75.start()


def blink(n=1, c=(255, 0, 0), delay=1.0):
    global h75
    for _ in range(n):
        h75.set_pixel(0, 0, *c)
        time.sleep(0.1)
        h75.set_pixel(0, 0, 0, 0, 0)
        time.sleep(delay)


def error(n):
    global h75
    while True:
        for _ in range(n):
            h75.set_pixel(0, 0, 255, 0, 0)
            time.sleep(0.1)
            h75.set_pixel(0, 0, 0, 0, 0)
            time.sleep(0.25)
        time.sleep(1)


blink()

ssid = 'YOURSSID'
password = 'YOURPASSWORD'

wlan = network.WLAN(network.STA_IF)
mac = ubinascii.hexlify(network.WLAN().config('mac')).decode()
print(mac)
del mac
wlan.active(True)
wlan.connect(ssid, password)

# Wait for connect or fail
max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')
    time.sleep(1)

# Handle connection error
if wlan.status() != 3:
    error(3)
    exit()

blink(n=3, c=(0, 255, 0), delay=0.25)
print('connected')
status = wlan.ifconfig()
print('ip = ' + status[0])

# Set QR code to IP address of PI
qr = qrcode.QRCode()
qr.set_text(status[0])

for x in range(qr.get_size()[0]+2):
    for y in range(qr.get_size()[1]+2):
        if qr.get_module(x-1, y-1):
            h75.set_pixel(x, y, 0, 0, 0)
        else:
            h75.set_pixel(x, y, 255, int(255*(x/qr.get_size()[0]+1)), int(255*(y/qr.get_size()[1]+1)))
del qr


def draw_line(x0, y0, x1, y1, r, g, b):
    # Line drawing code, stolen from ChatGPT
    # Calculate differences
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)

    # Determine the direction of the line
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1

    err = dx - dy

    while True:
        # Set the pixel at the current coordinates
        h75.set_pixel(x0, y0, r, g, b)

        # If we've reached the end point, break the loop
        if x0 == x1 and y0 == y1:
            break

        # Calculate the error and adjust x or y accordingly
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy


gc.collect()
print(gc.mem_free())

queue_len = 16
buckets = {"cpu": queue_len * [-1], "memory": queue_len * [-1], "storage": queue_len * [-1]}

while True:
    data = get_node_usage('proxmox')
    h75.clear()
    for k, v in data.items():
        buckets[k].pop(0)
        buckets[k].append(v)
        try:
            min_value = min(v for v in buckets[k] if v != -1)
            max_value = max(v for v in buckets[k])
        except:
            continue
        for x, hist in enumerate(list(zip(buckets[k], buckets[k][1:]))):
            if hist[0] == -1 or hist[1] == -1:
                continue
            p1 = 0.5 if max_value == min_value else (hist[0] - min_value) / (max_value - min_value)
            p2 = 0.5 if max_value == min_value else (hist[1] - min_value) / (max_value - min_value)   
            if k == "storage":
                draw_line(x * 3, 9 - round(p1 * 9), x * 3 + 3, 9 - round(p2 * 9), 127, 127, 127)
                draw_number(h75, v * 100, 49, 3, 255, 255, 255)
            elif k == "memory":
                draw_line(x * 3, 20 - round(p1 * 9), x * 3 + 3, 20 - round(p2 * 9), 255, 0, 0)
                draw_number(h75, v * 100, 49, 14, 255, 0, 0)
            elif k == "cpu":
                draw_line(x * 3, 31 - round(p1 * 9), x * 3 + 3, 31 - round(p2 * 9), 0, 255, 255)
                draw_number(h75, v * 100, 49, 25, 0, 255, 255)
        #print(k, min_value, max_value)
        
    #print()
    gc.collect()
    time.sleep(0.1)
