# Products

The flashing and RF-test steps are the same for every product. Only the test image differs.

| Product | SoC | WiFi / BT module | Test image | Download |
|---------|-----|------------------|------------|----------|
| AZ04B | RK3588S | AP6256 | `image-raw-format-AZ04B-Production-Test-<date>.img` | [Latest AZ04B image](https://mixtile-rockchip.github.io/focalcrest-rockchip-linux-ci/releases/#/AZ04B/latest) |
| AZ07 | RK3566 | AP6256 | `image-raw-format-AZ07-Production-Test-<date>.img` | [Latest AZ07 image](https://mixtile-rockchip.github.io/focalcrest-rockchip-linux-ci/releases/#/AZ07/latest) |
| AZ08 | RK3576S | AP6256 | `image-raw-format-AZ08-Production-Test-<date>.img` | [Latest AZ08 image](https://mixtile-rockchip.github.io/focalcrest-rockchip-linux-ci/releases/#/AZ08/latest) |

Opening a download link starts the download of the newest official test image for that product.

<!-- TODO(AZ04B): the RF-test steps have not been run on an AZ04B unit yet. Confirm on the Buildroot production image: wifi_ap6xxx_rftest.sh, wifibt-init.sh, and the "Successfully init BT for AP625X!" line. -->
<!-- TODO(all): per-product Maskrom / recovery button location and test fixture are not documented yet. -->
