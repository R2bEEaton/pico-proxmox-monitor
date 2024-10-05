# pico-proxmox-monitor
A project I made for monitoring Proxmox system usage!

# Usage
- Flash your Pico W (or 2W) with the [latest Pimoroni MicroPython fork](https://github.com/pimoroni/pimoroni-pico/releases/) (I am currently running pico-v1.23.0-1-pimoroni-micropython.uf2).
- Then connect via USB and open your favorite editor, like Thonny, and send the 3 Python files over.
- Modify main.py to include your WIFI SSID and password.
- Modify get_proxmox_data.py to include your Proxmox instance's IP address and [API token](https://pve.proxmox.com/wiki/Proxmox_VE_API).
- All set!

# Issues?
[Open an issue here, and I will try to respond.](https://github.com/R2bEEaton/pico-proxmox-monitor/issues) I made this for fun, feel free to edit it.
