# Wifi-Energy-Meter API for TP-Link HS110 Smartplug

Python library for the TP-Link HS110

**DISCLAIMER**
```
This is NOT an official Software by TP-Link.
We are not affiliated, associated, authorized, endorsed by, 
or in any way officially connected with TP-Link.
NO WARRANTY. Use on your own risk.
```

**Capabilities**
* Setup Device
* Read Measurements (power, voltage, current and the total consumption)
* Switch State

## Install

### Using pypi
```
pip install wifimeter
```

### Using source
```
python setup.py install
```

## Usage
```
Usage: wifimeter [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  info     Ask device for get_sysinfo.
  measure  Receives readings every second
  setup    Setup device (alias, WLAN)
  switch   Switch device ON/OFF
```

### Connect Smartplug to Wifi
**Before setup: Connect to the Smartplug's Wifi
(TP-LINK_Smart Plug_*)**
```
wifimeter setup -a <ALIAS> -n <WLAN-NAME> -p <PASSWORD> -t <WLAN-TYPE>
```
```
Usage: wifimeter setup [OPTIONS]

  Setup device (alias, WLAN)

Options:
  -a, --alias TEXT
  -n, --wlan-name TEXT
  -p, --password TEXT
  -t, --wlan-type [0|2|3]  0 = without any security, 2 = WEP, 3 = WPA
  -l, --log-level TEXT
  --help                     Show this message and exit.
```

### Read Measurements

Receives measurements every second and prints them on screen with a current
timestamp
```
wifimeter measure
```
Example Output:
```
alias, timestamp, current, total, power, voltage, err_code
testdevice, 2016-08-10 13:29:09.305675+02:00, 0.013050, 0.001, 0, 227.170061
testdevice, 2016-08-10 13:29:10.242483+02:00, 0.012753, 0.001, 0, 227.174989
testdevice, 2016-08-10 13:29:11.238036+02:00, 0.012842, 0.001, 0, 227.187237

```

### Switch
Switch plug ON/OFF
```
wifimeter switch --state 0
wifimeter switch --state 1
```


## License
This software is MIT licensed, as found in the [LICENSE](./LICENSE) file.
