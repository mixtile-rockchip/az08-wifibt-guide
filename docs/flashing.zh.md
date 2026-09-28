# 设备镜像烧录指南（Windows）

请先烧录对应产品的测试镜像。**只有烧录成功后**，才开始 WiFi/蓝牙测试（另见测试指南）。

在 **Windows PC** 上操作。

---

## 准备

- 一台带 USB 口的 Windows PC
- 一根从 PC 连到设备烧录口的 USB 线
- Rockchip Flash Tool（Windows 版）—— 见步骤 1
- 对应产品的测试镜像 —— 见步骤 2

---

## 1. 获取烧录工具

1. 打开最新 Release：<https://github.com/mixtile-rockchip/rockchip-flash-tool/releases/latest>
2. 下载 **`Rockchip-Flash-Tool-windows-x64.zip`**。
3. 解压到一个文件夹（例如 `C:\Rockchip-Flash-Tool`）。
4. 从该文件夹运行程序（`Rockchip Flash Tool.exe`）。

## 2. 下载测试镜像

1. 在 [产品](products.md) 表格中，打开对应产品的下载链接。
2. 把 `.img` 文件保存到 PC（记住保存位置）。

## 3. 让设备进入烧录模式

让设备进入 **Maskrom** 或 **Loader** 模式，再用 USB 连接到 PC：

- 通常做法：按住 **Maskrom / recovery** 按键的同时插入 USB 线，然后松开。
- 如果设备已能正常启动且已配好 ADB（步骤 5），也可以直接执行 `adb reboot loader`。

此时 Rockchip Flash Tool 应能显示已连接的设备。

> 若工具 / Windows 识别不到设备：安装 **Rockchip USB 驱动**（DriverAssistant），然后重新连接并重试步骤 3。

## 4. 烧录镜像

1. 在 Rockchip Flash Tool 中，**选择固件**（select firmware）→ 选中步骤 2 下载的镜像文件。
2. 点击 **Start Flash**（开始烧录）。
3. 等待工具提示 **success**（成功）。烧录过程中不要拔线。
4. 设备会重启进入已烧录的系统。

---

## 5. 在 Windows PC 上配置 ADB（WiFi/蓝牙测试需要）

1. 下载 **Android SDK Platform Tools**（Windows 版）：<https://developer.android.com/tools/releases/platform-tools>
   （直链：<https://dl.google.com/android/repository/platform-tools-latest-windows.zip>）
2. 解压到一个文件夹，例如 `C:\platform-tools`。
3. 在该文件夹打开 **命令提示符**（或 PowerShell）—— 在文件资源管理器地址栏输入 `cmd` 回车即可。
4. 用 USB 连接（已烧录并启动的）设备，然后执行：

```
adb devices
```

必须恰好列出一台设备且状态为 `device`。若显示 `unauthorized` 或没有设备，重新插拔 USB 线再执行一次。

---

## 下一步

设备已烧录、ADB 可用。进入 **WiFi/蓝牙射频测试指南**（[wifibt-test.md](wifibt-test.md)）。
