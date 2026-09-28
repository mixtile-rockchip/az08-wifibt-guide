# 固件变更记录

## 2026-09-23 · AZ07 / AZ08 Production-Test

WiFi nvram（`nvram_ap6256.txt`）：5G 自适应（能量检测）门限调整。

| 参数 | 原值 | 新值 |
|------|------|------|
| `ed_thresh5g` | -54 | -74 |
| `eu_edthresh5g` | -54 | -74 |

2.4G（`ed_thresh2g`、`eu_edthresh2g`）保持 -54 不变。影响 [A6 自适应测试](wifibt-test.md#a6-自适应干扰规避)。
