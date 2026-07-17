# RF Fixed-Frequency Test Guide


---

## 0. Start

Prerequisite: the device must already be flashed — see [flashing guide](flashing.md).

On the PC:
```
adb devices
```
One device must be listed as `device`. Then open the shell (run all following commands inside it):
```
adb shell
```

Test WiFi first, then Bluetooth.

---

## Part A — WiFi

### A1. Enter test mode (run once per power-up)

```
wifi_ap6xxx_rftest.sh

```
The script prints `wl ver` at the end — it must contain **`WLTEST`**. If it does not, run `wifi_ap6xxx_rftest.sh` again.

### A2. TX — copy the whole block for the mode under test

Parameter changes:
- Rate: change the number after `-r` / `-m` / `-v`.
- Fixed power: replace `wl txpwr1 -1` with `wl txpwr1 -o -d <value>`.
- HT40 / VHT40: set channel = test_channel − 2.  VHT80: set channel = test_channel − 6.

**2.4G 11b**
```
wl down
wl mpc 0
wl country ALL
wl band b
wl mimo_txbw -1
wl up
wl nrate -r 11
wl channel 13
wl phy_watchdog 0
wl scansuppress 1
wl phy_forcecal 1
wl txpwr1 -1
wl pkteng_start 00:90:4c:14:43:19 tx 100 1000 0

```

**2.4G 11g**
```
wl down
wl band b
wl mpc 0
wl nrate -r 54
wl rateset 54b
wl country ALL
wl up
wl channel 1
wl scansuppress 1
wl txpwr1 -1
wl phy_forcecal 1
wl pkteng_start 00:11:22:33:44:55 tx 100 1000 0

```

**2.4G 11n HT20**
```
wl down
wl band b
wl mpc 0
wl nrate -m 7
wl rateset 54b
wl country ALL
wl up
wl channel 13
wl scansuppress 1
wl txpwr1 -1
wl phy_forcecal 1
wl pkteng_start 00:11:22:33:44:55 tx 100 1000 0

```

**5G 11a**
```
wl down
wl band a
wl mpc 0
wl nrate -r 54
wl rateset 54b
wl country ALL
wl up
wl channel 161
wl scansuppress 1
wl phy_forcecal 1
wl txpwr1 -1
wl phy_forcecal 1
wl pkteng_start 00:11:22:33:44:55 tx 100 1000 0

```

**5G 11n HT20**
```
wl down
wl mpc 0
wl country ALL
wl band a
wl mimo_txbw -1
wl up
wl nrate -m 7
wl channel 165
wl phy_watchdog 0
wl scansuppress 1
wl phy_forcecal 1
wl txpwr1 -1
wl phy_forcecal 1
wl pkteng_start 00:11:22:33:44:55 tx 100 1000 0

```

**5G 11n HT40**
```
wl down
wl mpc 0
wl country ALL
wl band a
wl mimo_txbw 4
wl up
wl nrate -m 7
wl chanspec 157/40
wl phy_watchdog 0
wl scansuppress 1
wl phy_forcecal 1
wl txpwr1 -1
wl phy_forcecal 1
wl pkteng_start 00:90:4c:14:43:19 tx 40 1500 0

```

**5G 11ac VHT20**
```
wl down
wl mpc 0
wl country ALL
wl band a
wl up
wl 5g_rate -v 7 -s 1 -b 20
wl chanspec 36/20
wl phy_watchdog 0
wl scansuppress 1
wl phy_forcecal 1
wl txpwr1 -1
wl phy_forcecal 1
wl pkteng_start 00:90:4c:14:43:19 tx 40 1500 0

```

**5G 11ac VHT40**
```
wl down
wl mpc 0
wl country ALL
wl band a
wl up
wl 5g_rate -v 7 -s 1 -b 40
wl chanspec 36/40
wl phy_watchdog 0
wl scansuppress 1
wl phy_forcecal 1
wl txpwr1 -1
wl phy_forcecal 1
wl pkteng_start 00:90:4c:14:43:19 tx 20 1500 0

```

**5G 11ac VHT80**
```
wl down
wl mpc 0
wl country ALL
wl band a
wl mimo_bw_cap 1
wl mimo_txbw -1
wl up
wl 5g_rate -v 9 -s 1 -b 80
wl chanspec 149/80
wl phy_watchdog 0
wl scansuppress 1
wl phy_forcecal 1
wl phy_txpwrctrl 1
wl txpwr1 -1
wl phy_forcecal 1
wl pkteng_start 00:90:4c:14:43:19 tx 20 2000 0

```

### A3. Stop TX (before switching to another mode)

```
wl pkteng_stop tx
wl down

```

### A4. RX

**11a/b/g/n RX HT20 (single antenna)**
```
wl down
wl band auto
wl mpc 0
wl country ALL
wl channel 36
wl bi 65535
wl up
wl phy_watchdog 0
wl scansuppress 1
wl phy_forcecal 1
wl counters
wl reset_cnts

```

**5.8G RX HT40 (single antenna)**
```
wl down
wl band auto
wl mpc 0
wl country ALL
wl mimo_bw_cap 1
wl mimo_txbw 4
wl chanspec 36/40
wl bi 65535
wl up
wl phy_watchdog 0
wl scansuppress 1
wl phy_forcecal 1
wl counters
wl reset_cnts

```

**802.11ac RX HT20 (single antenna)**
```
wl down
wl band auto
wl mpc 0
wl country ALL
wl mimo_txbw 4
wl chanspec 36/20
wl bi 65535
wl up
wl phy_watchdog 0
wl scansuppress 1
wl phy_forcecal 1
wl reset_cnts
wl counters

```

**802.11ac RX HT40 (single antenna)**
```
wl down
wl band auto
wl mpc 0
wl country ALL
wl mimo_txbw 4
wl chanspec 157/40
wl bi 65535
wl up
wl phy_watchdog 0
wl scansuppress 1
wl phy_forcecal 1
wl reset_cnts
wl counters

```

**802.11ac RX HT80 (single antenna)**
```
wl down
wl band auto
wl mpc 0
wl country ALL
wl mimo_txbw 4
wl chanspec 149/80
wl bi 65535
wl up
wl phy_watchdog 0
wl scansuppress 1
wl phy_forcecal 1
wl counters
wl reset_cnts

```

---

## Part B — Bluetooth

> For more detailed / complete commands (full parameter tables and the entire example list), refer to the [BT RF Test Commands for Linux manual (v0.9)](assets/BT-RF-Test-Commands-for-Linux-v0.9.pdf). In that manual, **skip sections 1 and 2** (Prerequisites / Enable BT) and start from **section 2-1** — B1 below replaces them for this board.

### B1. Prepare (always run — the A1 WiFi test powered Bluetooth off)

Step 1 — re-initialize the Bluetooth controller:
```
killall bluetoothd
wifibt-init.sh stop
wifibt-init.sh start_bt

```
Wait until the output shows this line (about 10 seconds): `Successfully init BT for AP625X!`

Step 2 — bring it up and confirm it responds:
```
hciconfig hci0 up
hcitool cmd 0x04 0x0001

```
The output must contain a line starting with `> HCI Event`. Bluetooth is now ready.
(Do **not** rely on `hciconfig` showing `UP RUNNING` — it can show `UP RUNNING` even when the controller is dead.)

> Every test group below starts with `hcitool cmd 0x03 0x0003` (HCI reset). Running the next group's reset stops the previous test. To stop any Bluetooth test at any time, run `hcitool cmd 0x03 0x0003`.

---

## Classic Bluetooth (BR/EDR)

### B2. Enable Device Under Test Mode — required before B3

Run in order (each returns `> HCI Event: 0x0e ... 00`):
```
hcitool cmd 0x03 0x0003
hcitool cmd 0x03 0x1a 0x03
hcitool cmd 0x03 0x05 0x02 0x00 0x02
hcitool cmd 0x06 0x03

```

### B3. Continuous packet TX (Tx_Test)

Example (PDF §2-2 template) — DH1, BD_ADDR 00:11:22:33:44:55, Hopping ON (79-channel), PRBS9, length 10000, max power:
```
hcitool cmd 0x03 0x0003
hcitool cmd 0x3f 0x0051 55 44 33 22 11 00 00 00 04 01 04 10 27 09 00 00

```
Must return `> HCI Event: 0x0e ... 01 51 FC 00`.

For fixed-frequency testing on a **single channel**, set byte 7 = `01` (single frequency, hopping off) and byte 8 = the channel.

To change parameters, edit these bytes (positions after `0x0051`):

| Position | Parameter | Values |
|----------|-----------|--------|
| bytes 1–6 | BD_ADDR (reversed) | `55 44 33 22 11 00` (= 00:11:22:33:44:55; use your device's address) |
| byte 7 | Hopping mode | 79-channel (hop ON)=`00`, single frequency (hop OFF)=`01`, fixed pattern=`02` |
| byte 8 | Frequency/channel | CH0=`00`, CH39=`27`, CH78=`4E` (range `00`–`4E`) |
| byte 9 | Modulation | PRBS9=`04` (`00000000`=`01`, `11111111`=`02`, `01010101`=`03`, `11110000`=`09`) |
| byte 10 | Logical channel | ACL Basic=`01`; use `00` for 2-/3- (EDR) packet types |
| byte 11 | Packet type | DH1=`04`, 3-DH1=`08`, DH3=`0B`, DH5=`0F` |
| bytes 12–13 | Length (LSB first) | 10000 = `10 27` |
| bytes 14–16 | fixed | `09 00 00` |

(Full 36-example / packet-type list: `BT RF Test Commands for Linux-v09.pdf`.)

### B4. Single-tone / carrier TX (Set_Tx_Carrier_Frequency)

Example — channel 0, PRBS9, GFSK:
```
hcitool cmd 0x03 0x0003
hcitool cmd 0x3f 0x0014 00 02 01 00 09 00 00

```
Second command must return `> HCI Event: 0x0e ... 01 14 FC 00`.

Bytes after `0x0014` are `00 <freq> <mode> <mod> 09 00 00`:

| Field | Meaning | Values |
|-------|---------|--------|
| freq | channel + 2 | CH0=`02`, CH39=`29`, CH78=`50` |
| mode | pattern | Unmodulated(single carrier)=`00`, PRBS9=`01`, PRBS15=`02`, AllZero=`03`, AllOne=`04`, Increment=`05` |
| mod | modulation | GFSK(1M)=`00`, QPSK(2M/EDR)=`01`, 8PSK(3M/EDR)=`02` |

### B5. Receive-only, fixed channel (Write_Receive_Only)

Example — channel 0:
```
hcitool cmd 0x03 0x0003
hcitool cmd 0x3f 0x002b 02

```
Second command must return `> HCI Event: 0x0e ... 01 2B FC 00`.
The last byte is `channel + 2` (CH0=`02`, CH39=`29`, CH78=`50`).

### B6. RX with BER (Rx_Test)

1. On your RF tester: select **Continuous Tx** and start transmitting.
2. On the device:
```
hcitool cmd 0x03 0x0003
hcitool cmd 0x3f 0x0052 EE FF C0 88 00 00 E8 03 26 04 00 04 FF FF

```
Second command must return `> HCI Event: 0x0e ... 01 52 FC 00`.

3. Read the periodic RX reports:
```
hcidump -x

```
Vendor events (`HCI Event: Vendor (0xff)`) appear every Report_Period. Take two consecutive events, read the two 32-bit values X (total bits) and Y (error bits), and compute `BER = ((X2−X1) − (Y2−Y1)) / (X2−X1)`. Pass: BDR < 0.001, EDR < 0.0001.
4. Stop **Continuous Tx** on the tester **first**, then reset (`hcitool cmd 0x03 0x0003`).

Bytes after `0x0052`: `<BD_ADDR reversed ×6> <Report_Period 2B> <Freq 1B> <Mod 1B> <LogCh 1B> <PktType 1B> <Length 2B>`
Report_Period: 250=`FA 00`, 1000=`E8 03`, 2000=`D0 07`.  Freq: 0–78 = `00`–`4E`.

---

## Bluetooth Low Energy (BLE)

### B7. LE TX (LE_Transmitter_Test)

Example — channel 10, data length 37, PRBS9:
```
hcitool cmd 0x03 0x0003
hcitool cmd 0x08 0x001e 0A 25 00

```
Second command must return `> HCI Event: 0x0e ... 01 1E 20 00`.
Stop the test:
```
hcitool cmd 0x08 0x001f

```
Bytes after `0x001e` are `<channel> <length> <payload>`:

| Field | Meaning | Values |
|-------|---------|--------|
| channel | 0–39 | `00`–`27` |
| length | test data length 0–255 | `00`–`FF` |
| payload | pattern | PRBS9=`00`, 11110000=`01`, 10101010=`02`, PRBS15=`03`, 11111111=`04`, 00000000=`05` |

### B8. LE RX with PER (LE_Receiver_Test)

Example — channel 1:
```
hcitool cmd 0x03 0x0003
hcitool cmd 0x08 0x001d 01

```
Second command must return `> HCI Event: 0x0e ... 01 1D 20 00`.
(channel = 0–39 = `00`–`27`.)

Transmit 1000 packets from the tester, then end and read the received count:
```
hcitool cmd 0x08 0x001f

```
Returns `> HCI Event: 0x0e ... 01 1F 20 00 <count_LSB> <count_MSB>`. The last two bytes are the received-packet count (little-endian). `PER = (1000 − count) / 1000`.

### B9. LE Enhanced TX (LE_Enhanced_Transmitter_Test)

Example — channel 10, length 37, PRBS9, LE 1M PHY:
```
hcitool cmd 0x03 0x0003
hcitool cmd 0x08 0x0034 0A 25 00 01

```
Second command must return `> HCI Event: 0x0e ... 01 34 20 00`.
Stop the test:
```
hcitool cmd 0x08 0x001f

```
Bytes after `0x0034` are `<channel> <length> <payload> <phy>` (channel/length/payload as in B7):

| PHY | Value |
|-----|-------|
| LE 1M | `01` |
| LE 2M | `02` |
| LE Coded S=8 | `03` |
| LE Coded S=2 | `04` |

### B10. LE Enhanced RX with PER (LE_Enhanced_Receiver_Test)

Example — channel 1, LE 2M PHY, standard modulation:
```
hcitool cmd 0x03 0x0003
hcitool cmd 0x08 0x0033 01 02 00

```
Second command must return `> HCI Event: 0x0e ... 01 33 20 00`.
Bytes after `0x0033` are `<channel> <phy> <modulation>`: phy 1M=`01`/2M=`02`/Coded=`03`; modulation standard=`00`/stable=`01`.

Transmit 1000 packets from the tester, then end and read the count:
```
hcitool cmd 0x08 0x001f

```
Returns the received-packet count in the last two bytes (little-endian). `PER = (1000 − count) / 1000`.

---

## Quick Reference

| Task | Command |
|------|---------|
| Enter WiFi test mode | `wifi_ap6xxx_rftest.sh` → `wl ver` shows `WLTEST` |
| Stop WiFi TX | `wl pkteng_stop tx` then `wl down` |
| Prepare BT | `killall bluetoothd` → `wifibt-init.sh stop` → `wifibt-init.sh start_bt` → `hciconfig hci0 up` → check `hcitool cmd 0x04 0x0001` returns `> HCI Event` |
| Classic BT continuous TX | `hcitool cmd 0x3f 0x0051 …` (after B2 DUT mode) |
| Classic BT single-tone TX | `hcitool cmd 0x3f 0x0014 …` |
| BLE TX | `hcitool cmd 0x08 0x001e …` |
| BLE RX / end | `hcitool cmd 0x08 0x001d …` / `hcitool cmd 0x08 0x001f` |
| Stop any BT test | `hcitool cmd 0x03 0x0003` |

## Rules

1. `killall bluetoothd` before any `hcitool cmd`.
2. Do WiFi tests first; WiFi test mode turns Bluetooth off, so re-run B1 before Bluetooth tests.
