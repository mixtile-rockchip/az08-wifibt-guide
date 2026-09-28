# Focalcrest RF Test Guide

WiFi / Bluetooth fixed-frequency RF test procedure for Focalcrest AZ products (AZ07, AZ08) with the AP6256 module. One shared procedure; the products differ only in the test image.

- Website: <https://mixtile-rockchip.github.io/focalcrest-rf-test-guide/> (English) · [中文](https://mixtile-rockchip.github.io/focalcrest-rf-test-guide/zh/)
- PDF: [English](https://mixtile-rockchip.github.io/focalcrest-rf-test-guide/pdf/Focalcrest-RF-Test-Guide-EN.pdf) · [中文](https://mixtile-rockchip.github.io/focalcrest-rf-test-guide/pdf/Focalcrest-RF-Test-Guide-ZH.pdf)

## Layout

| Path | Content |
|------|---------|
| `docs/products.md` | Product table: SoC, module, test image, download link |
| `docs/changelog.md` | Firmware changelog |
| `docs/flashing.md` | Flashing the test image (shared) |
| `docs/wifibt-test.md` | WiFi / Bluetooth RF test (shared) |
| `docs/*.zh.md` | Chinese version of each page |

To add a product, add a row to `docs/products.md` and `docs/products.zh.md`.

## Build

Pushing to `main` builds the site and both PDFs and deploys them to GitHub Pages (`.github/workflows/docs.yml`). Pull requests run the same build and checks without deploying; the PDFs are kept as a workflow artifact for 30 days.

Locally:

```
pip install -r requirements.txt
python -m playwright install chromium
mkdocs build --strict
python scripts/build_pdf.py
python scripts/check_pdf.py
```

Both PDFs end with `docs/assets/BT-RF-Test-Commands-for-Linux-v0.9.pdf` as an appendix; links to that manual jump to it.

The PDF build needs the Noto Sans CJK SC fonts (`fonts-noto-cjk` on Debian/Ubuntu) and poppler-utils; `check_pdf.py` fails if any other font ends up in a PDF.
