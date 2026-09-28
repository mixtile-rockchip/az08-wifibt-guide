# Device Image Flashing Guide (Windows)

Flash the test image for your product first. **Only after flashing succeeds** do the WiFi/Bluetooth test (separate guide).

Operated from a **Windows PC**.

---

## What you need

- A Windows PC with a USB port
- A USB cable from the PC to the device's flashing port
- Rockchip Flash Tool (Windows) — see step 1
- The test image for your product — see step 2

---

## 1. Get the flashing tool

1. Open the latest release: <https://github.com/mixtile-rockchip/rockchip-flash-tool/releases/latest>
2. Download **`Rockchip-Flash-Tool-windows-x64.zip`**.
3. Unzip it to a folder (e.g. `C:\Rockchip-Flash-Tool`).
4. Run the application (`Rockchip Flash Tool.exe`) from that folder.

## 2. Download the test image

1. In the [Products](products.md) table, open the download link for your product.
2. Save the `.img` file to your PC (remember the file location).

## 3. Put the device into flashing mode

Put the device into **Maskrom** or **Loader** mode, then connect it to the PC by USB:

- Typically: hold the **Maskrom / recovery** button while plugging the USB cable into the PC, then release.
- If the device already boots normally and ADB is set up (step 5), you can instead run `adb reboot loader`.

The Rockchip Flash Tool should now show the connected device.

> If the tool / Windows does not detect the device: install the **Rockchip USB driver** (DriverAssistant), then reconnect and retry step 3.

## 4. Flash the image

1. In Rockchip Flash Tool, **select firmware** → choose the image file downloaded in step 2.
2. Click **Start Flash**.
3. Wait until the tool reports **success**. Do not unplug during flashing.
4. The device reboots into the flashed system.

---

## 5. Set up ADB on the Windows PC (needed for the WiFi/BT test)

1. Download **Android SDK Platform Tools** for Windows: <https://developer.android.com/tools/releases/platform-tools>
   (direct: <https://dl.google.com/android/repository/platform-tools-latest-windows.zip>)
2. Unzip to a folder, e.g. `C:\platform-tools`.
3. Open **Command Prompt** (or PowerShell) in that folder — in File Explorer, type `cmd` in the address bar and press Enter.
4. Connect the (flashed, booted) device to the PC by USB, then run:

```
adb devices
```

Exactly one device must be listed as `device`. If it shows `unauthorized` or nothing, reconnect the cable and run it again.

---

## Next

The device is flashed and ADB works. Proceed to the **WiFi/Bluetooth RF Test Guide** ([wifibt-test.md](wifibt-test.md)).
