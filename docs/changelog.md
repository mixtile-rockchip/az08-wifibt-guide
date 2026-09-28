# Firmware changelog

## 2026-09-23 · AZ07 / AZ08 Production-Test

WiFi nvram (`nvram_ap6256.txt`): 5 GHz adaptivity (energy-detect) threshold changed.

| Parameter | Old | New |
|-----------|-----|-----|
| `ed_thresh5g` | -54 | -74 |
| `eu_edthresh5g` | -54 | -74 |

2.4 GHz (`ed_thresh2g`, `eu_edthresh2g`) unchanged at -54. Affects the [A6 adaptivity test](wifibt-test.md#a6-adaptivity-interference-avoidance).
