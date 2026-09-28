# 产品

所有产品的烧录和射频测试步骤都相同，只是测试镜像不同。

| 产品 | SoC | WiFi / 蓝牙模块 | 测试镜像 | 下载 |
|------|-----|-----------------|----------|------|
| AZ04B | RK3588S | AP6256 | `image-raw-format-AZ04B-Production-Test-<日期>.img` | [最新 AZ04B 镜像](https://mixtile-rockchip.github.io/focalcrest-rockchip-linux-ci/releases/#/AZ04B/latest) |
| AZ07 | RK3566 | AP6256 | `image-raw-format-AZ07-Production-Test-<日期>.img` | [最新 AZ07 镜像](https://mixtile-rockchip.github.io/focalcrest-rockchip-linux-ci/releases/#/AZ07/latest) |
| AZ08 | RK3576S | AP6256 | `image-raw-format-AZ08-Production-Test-<日期>.img` | [最新 AZ08 镜像](https://mixtile-rockchip.github.io/focalcrest-rockchip-linux-ci/releases/#/AZ08/latest) |

打开下载链接后，会自动开始下载该产品最新的正式测试镜像。

<!-- TODO(AZ04B): 射频测试步骤尚未在 AZ04B 实机上跑过。需在 Buildroot 量产测试镜像上确认：wifi_ap6xxx_rftest.sh、wifibt-init.sh，以及 "Successfully init BT for AP625X!" 这一行输出。 -->
<!-- TODO(all): 各产品的 Maskrom / recovery 按键位置和测试治具尚未整理。 -->
