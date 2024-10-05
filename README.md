# pico-proxmox-monitor
A project I made for monitoring Proxmox system usage!

# Hardware
- Raspberry Pi Pico 2W (Pico W might be fine, haven't tested)
- [64x32 LED Matrix](https://www.adafruit.com/product/2279)
- [Power supply](https://www.adafruit.com/product/1466)
- [Hub75 Hat](https://www.digikey.com/en/products/detail/adafruit-industries-llc/3211/8535237?utm_adgroup=&utm_source=google&utm_medium=cpc&utm_campaign=PMax%20Shopping_Product_Low%20ROAS%20Categories&utm_term=&utm_content=&utm_id=go_cmp-20243063506_adg-_ad-__dev-c_ext-_prd-8535237_sig-CjwKCAjwx4O4BhAnEiwA42SbVJyumFphNeKcb4d-vKaA66kscJa-CfjE17rJQ32VC_XsbUS2cKx_gBoCTdoQAvD_BwE&gad_source=1&gclid=CjwKCAjwx4O4BhAnEiwA42SbVJyumFphNeKcb4d-vKaA66kscJa-CfjE17rJQ32VC_XsbUS2cKx_gBoCTdoQAvD_BwE) (This may not be strictly necessary. I had it on hand since I was previously using a Rpi 4 to drive the display. Obviously it's not compatible with the Pico so I am using some jumper cables to connect to the pinholes.)

# Usage
- Flash your Pico W (or 2W) with the [latest Pimoroni MicroPython fork](https://github.com/pimoroni/pimoroni-pico/releases/) (I am currently running pico-v1.23.0-1-pimoroni-micropython.uf2). This includes the hub75 module needed for driving the display.
- Then connect via USB and open your favorite editor, like Thonny, and send the 3 Python files over.
- Modify main.py to include your WIFI SSID and password.
- Modify get_proxmox_data.py to include your Proxmox instance's IP address and [API token](https://pve.proxmox.com/wiki/Proxmox_VE_API).
- All set!

# Issues?
[Open an issue here, and I will try to respond.](https://github.com/R2bEEaton/pico-proxmox-monitor/issues) I made this for fun, feel free to edit it.
