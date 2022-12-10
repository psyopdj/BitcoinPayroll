# BitcoinPayroll
Project for Blockchains &amp; Smart Contracts taught at the University of Texas at Austin

Bitcoin Payroll is a system where employees are paid in satoshis immediately upon finishing their shift of work.

## Details

- Each employee has an RFID badge that they use to badge in/out of work. Both RFID transactions are logged to a database. 
- The hours worked is calculated upon clocking out. 
- The satoshis paid are then sent to the address on file for the employee.

## Hardware Setup

You will need the following hardware below:

- Arduino: MEGA2560 R3
- RFID-RC522 Sensor 
- RFID card and RFID tag

1. Connect RFID sensor onto the arduino with the schematic in the top right corner 
1. The arduino is connected to a laptop using USB cable. 

```Note: The MEGA2560 doesn’t have WIFI capabilities and needed to be hooked up via a USB to connect to the server```

## Code Setup

### Creating a Virtual Environment

Make sure that you have a virtual python environment setup with the required packages installed.

Use your IDE or follow the steps below.

```bash
$ python3 -m venv env
$ source env/bin/activate
$ pip install -r requirements.txt
```

### Running the app

```bash
# run
$ python main.py
```

The app runs locally on your machine with this URL.

`` http://127.0.0.1:5000/``

Go to the URL on your browser to take a look at the app or use ``curl`` to make any API requests.

### Setting up ngrok

You need to expose the local url running on your machine so the arudino can hit it.

Follow steps [here](https://ngrok.com/docs/getting-started) to set it up.
