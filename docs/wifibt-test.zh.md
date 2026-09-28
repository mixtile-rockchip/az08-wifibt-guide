# 射频定频测试指南

---

## 0. 开始

前置条件：设备必须已烧录镜像 —— 见 [烧录指南](flashing.md)。

在 PC 上：
```
adb devices
```
必须列出一台设备且状态为 `device`。然后进入设备 shell（以下所有命令都在该 shell 内执行）：
```
adb shell
```

先测 WiFi，再测蓝牙。

---

## A 部分 —— WiFi

### A1. 进入测试模式（每次上电执行一次）

```
wifi_ap6xxx_rftest.sh

```
脚本末尾会打印 `wl ver` —— 其中必须包含 **`WLTEST`**。若没有，重新执行 `wifi_ap6xxx_rftest.sh`。

### A2. TX —— 整块复制对应制式的命令

参数修改：
- 速率：改 `-r` / `-m` / `-v` 后面的数字。
- 固定功率：把 `wl txpwr1 -1` 换成 `wl txpwr1 -o -d <数值>`。
- HT40 / VHT40：信道 = 测试信道 − 2；VHT80：信道 = 测试信道 − 6。

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

### A3. 停止 TX（切换到下一制式前执行）

```
wl pkteng_stop tx
wl down

```

### A4. RX

**11a/b/g/n RX HT20（单天线）**
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

**5.8G RX HT40（单天线）**
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

**802.11ac RX HT20（单天线）**
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

**802.11ac RX HT40（单天线）**
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

**802.11ac RX HT80（单天线）**
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

### A5. 单载波（未调制载波）

一次一个信道，不发包。载波落在信道中心频点上。

```
wl down
wl mpc 0
wl country ALL
wl up
wl scansuppress 1
wl phy_watchdog 0
wl band b
wl phy_forcecal 1
wl phy_txpwrctrl 0
wl phy_txpwrindex 90
wl out
wl fqacurcy 11

```

确认信道已生效 —— `current mac channel` 必须等于传给 `wl fqacurcy` 的信道号：
```
wl channel

```

参数修改：
- 频段：`wl band b` = 2.4G，`wl band a` = 5G。频段必须在 `wl out` **之前**设置。
- 信道：即 `wl fqacurcy` 的参数，从下表中选取。`wl fqacurcy` **不校验**该参数：`14`、`200` 这类超范围的值同样会被接受且不报错，但产生不出有效载波。
- 功率：`wl phy_txpwrindex <0–127>` —— 这是 PHY 增益表索引，**不是** dBm 值。超过 127 的值会翻转为负数且不报错。
- `wl phy_txpwrindex` 及其之前的所有命令都必须在 `wl out` **之前**执行。进入 `out` 状态后，`wl phy_txpwrindex` 和 `wl phy_forcecal` 都会返回 `wl: Not up`。

| 频段 | 信道 |
|------|------|
| 2.4G (2400–2483) | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13 |
| 5G band 1 (5150–5250) | 36, 40, 44, 48 |
| 5G band 2 (5250–5350) | 52, 56, 60, 64 |
| 5G band 3 (5475–5725) | 100, 104, 108, 112, 116, 120, 124, 128, 132, 136, 140, 144 |
| 5G band 4 (5725–5850) | 149, 153, 157, 161, 165 |

同频段内换信道，重复执行 `wl fqacurcy <信道>` 即可，无需退出 `out` 状态。换频段则需要整段重新执行。

停止：
```
wl fqacurcy 0
wl up
wl phy_txpwrctrl 1
wl down

```

---

## B 部分 —— 蓝牙

> 更详细 / 完整的命令（完整参数表和全部示例），参见 [BT RF Test Commands for Linux 手册（v0.9）](assets/BT-RF-Test-Commands-for-Linux-v0.9.pdf)。该手册中请**跳过第 1、2 节**（Prerequisites / Enable BT），从 **2-1 节**看起 —— 本板由下面的 B1 替代这两节。

### B1. 准备（每次都要执行 —— A1 的 WiFi 测试会关闭蓝牙）

第 1 步 —— 重新初始化蓝牙控制器：
```
killall bluetoothd
wifibt-init.sh stop
wifibt-init.sh start_bt

```
等到输出出现这一行（约 10 秒）：`Successfully init BT for AP625X!`

第 2 步 —— 拉起并确认有响应：
```
hciconfig hci0 up
hcitool cmd 0x04 0x0001

```
输出中必须出现以 `> HCI Event` 开头的行。蓝牙即就绪。
（**不要**以 `hciconfig` 显示 `UP RUNNING` 为准 —— 控制器已死时它仍可能显示 `UP RUNNING`。）

> 下面每组测试都以 `hcitool cmd 0x03 0x0003`（HCI reset）开头。执行下一组的 reset 会停止上一组测试。随时想停止任意蓝牙测试，执行 `hcitool cmd 0x03 0x0003`。

---

## 经典蓝牙（BR/EDR）

### B2. 进入 DUT（待测）模式 —— B3 之前必做

依次执行（每条返回 `> HCI Event: 0x0e ... 00`）：
```
hcitool cmd 0x03 0x0003
hcitool cmd 0x03 0x1a 0x03
hcitool cmd 0x03 0x05 0x02 0x00 0x02
hcitool cmd 0x06 0x03

```

### B3. 连续包发射（Tx_Test）

示例（PDF §2-2 模板）—— DH1，BD_ADDR 00:11:22:33:44:55，跳频开（79 信道），PRBS9，长度 10000，最大功率：
```
hcitool cmd 0x03 0x0003
hcitool cmd 0x3f 0x0051 55 44 33 22 11 00 00 00 04 01 04 10 27 09 00 00

```
必须返回 `> HCI Event: 0x0e ... 01 51 FC 00`。

若要在**单一信道**上做定频测试，把第 7 字节设为 `01`（单频、关跳频），第 8 字节设为目标信道。

修改参数时，编辑以下字节（`0x0051` 之后的位置）：

| 位置 | 参数 | 取值 |
|------|------|------|
| 第 1–6 字节 | BD_ADDR（倒序）| `55 44 33 22 11 00`（= 00:11:22:33:44:55；填你设备的地址）|
| 第 7 字节 | 跳频模式 | 79 信道（跳频开）=`00`，单频（跳频关）=`01`，固定图案=`02` |
| 第 8 字节 | 频点/信道 | CH0=`00`，CH39=`27`，CH78=`4E`（范围 `00`–`4E`）|
| 第 9 字节 | 调制 | PRBS9=`04`（`00000000`=`01`，`11111111`=`02`，`01010101`=`03`，`11110000`=`09`）|
| 第 10 字节 | 逻辑信道 | ACL Basic=`01`；2-/3-（EDR）包类型用 `00` |
| 第 11 字节 | 包类型 | DH1=`04`，3-DH1=`08`，DH3=`0B`，DH5=`0F` |
| 第 12–13 字节 | 长度（低字节在前）| 10000 = `10 27` |
| 第 14–16 字节 | 固定 | `09 00 00` |

（完整的 36 条示例 / 包类型列表见 `BT RF Test Commands for Linux-v09.pdf`。）

### B4. 单音 / 载波发射（Set_Tx_Carrier_Frequency）

示例 —— 信道 0，PRBS9，GFSK：
```
hcitool cmd 0x03 0x0003
hcitool cmd 0x3f 0x0014 00 02 01 00 09 00 00

```
第二条必须返回 `> HCI Event: 0x0e ... 01 14 FC 00`。

`0x0014` 之后是 `00 <freq> <mode> <mod> 09 00 00`：

| 字段 | 含义 | 取值 |
|------|------|------|
| freq | 信道 + 2 | CH0=`02`，CH39=`29`，CH78=`50` |
| mode | 图案 | 未调制（单载波）=`00`，PRBS9=`01`，PRBS15=`02`，全0=`03`，全1=`04`，递增=`05` |
| mod | 调制 | GFSK(1M)=`00`，QPSK(2M/EDR)=`01`，8PSK(3M/EDR)=`02` |

### B5. 仅接收、固定信道（Write_Receive_Only）

示例 —— 信道 0：
```
hcitool cmd 0x03 0x0003
hcitool cmd 0x3f 0x002b 02

```
第二条必须返回 `> HCI Event: 0x0e ... 01 2B FC 00`。
最后一个字节是 `信道 + 2`（CH0=`02`，CH39=`29`，CH78=`50`）。

### B6. 带 BER 的接收（Rx_Test）

1. 在射频综测仪上：选择 **Continuous Tx** 并开始发射。
2. 在设备上：
```
hcitool cmd 0x03 0x0003
hcitool cmd 0x3f 0x0052 EE FF C0 88 00 00 E8 03 26 04 00 04 FF FF

```
第二条必须返回 `> HCI Event: 0x0e ... 01 52 FC 00`。

3. 读取周期性接收报告：
```
hcidump -x

```
每隔 Report_Period 会出现一条 Vendor 事件（`HCI Event: Vendor (0xff)`）。取相邻两条，读出两个 32 位值 X（总比特）和 Y（错误比特），计算 `BER = ((X2−X1) − (Y2−Y1)) / (X2−X1)`。判据：BDR < 0.001，EDR < 0.0001。
4. **先**在综测仪上停止 **Continuous Tx**，再执行 reset（`hcitool cmd 0x03 0x0003`）。

`0x0052` 之后：`<BD_ADDR 倒序 ×6> <Report_Period 2字节> <Freq 1字节> <Mod 1字节> <LogCh 1字节> <PktType 1字节> <Length 2字节>`
Report_Period：250=`FA 00`，1000=`E8 03`，2000=`D0 07`。Freq：0–78 = `00`–`4E`。

---

## 低功耗蓝牙（BLE）

### B7. LE 发射（LE_Transmitter_Test）

示例 —— 信道 10，数据长度 37，PRBS9：
```
hcitool cmd 0x03 0x0003
hcitool cmd 0x08 0x001e 0A 25 00

```
第二条必须返回 `> HCI Event: 0x0e ... 01 1E 20 00`。
停止测试：
```
hcitool cmd 0x08 0x001f

```
`0x001e` 之后是 `<信道> <长度> <payload>`：

| 字段 | 含义 | 取值 |
|------|------|------|
| 信道 | 0–39 | `00`–`27` |
| 长度 | 测试数据长度 0–255 | `00`–`FF` |
| payload | 图案 | PRBS9=`00`，11110000=`01`，10101010=`02`，PRBS15=`03`，11111111=`04`，00000000=`05` |

### B8. 带 PER 的 LE 接收（LE_Receiver_Test）

示例 —— 信道 1：
```
hcitool cmd 0x03 0x0003
hcitool cmd 0x08 0x001d 01

```
第二条必须返回 `> HCI Event: 0x0e ... 01 1D 20 00`。
（信道 = 0–39 = `00`–`27`。）

从综测仪发送 1000 个包，然后结束并读出接收计数：
```
hcitool cmd 0x08 0x001f

```
返回 `> HCI Event: 0x0e ... 01 1F 20 00 <计数低字节> <计数高字节>`。最后两字节是接收到的包数（小端）。`PER = (1000 − 计数) / 1000`。

### B9. LE 增强发射（LE_Enhanced_Transmitter_Test）

示例 —— 信道 10，长度 37，PRBS9，LE 1M PHY：
```
hcitool cmd 0x03 0x0003
hcitool cmd 0x08 0x0034 0A 25 00 01

```
第二条必须返回 `> HCI Event: 0x0e ... 01 34 20 00`。
停止测试：
```
hcitool cmd 0x08 0x001f

```
`0x0034` 之后是 `<信道> <长度> <payload> <phy>`（信道/长度/payload 同 B7）：

| PHY | 取值 |
|-----|------|
| LE 1M | `01` |
| LE 2M | `02` |
| LE Coded S=8 | `03` |
| LE Coded S=2 | `04` |

### B10. 带 PER 的 LE 增强接收（LE_Enhanced_Receiver_Test）

示例 —— 信道 1，LE 2M PHY，标准调制：
```
hcitool cmd 0x03 0x0003
hcitool cmd 0x08 0x0033 01 02 00

```
第二条必须返回 `> HCI Event: 0x0e ... 01 33 20 00`。
`0x0033` 之后是 `<信道> <phy> <调制>`：phy 1M=`01`/2M=`02`/Coded=`03`；调制 标准=`00`/稳定=`01`。

从综测仪发送 1000 个包，然后结束并读出计数：
```
hcitool cmd 0x08 0x001f

```
最后两字节返回接收到的包数（小端）。`PER = (1000 − 计数) / 1000`。

---

## 速查表

| 任务 | 命令 |
|------|------|
| 进入 WiFi 测试模式 | `wifi_ap6xxx_rftest.sh` → `wl ver` 显示 `WLTEST` |
| 停止 WiFi TX | `wl pkteng_stop tx` 然后 `wl down` |
| WiFi 单载波 | `wl band b` → `wl out` → `wl fqacurcy <信道>`；用 `wl fqacurcy 0` 停止（A5）|
| 准备蓝牙 | `killall bluetoothd` → `wifibt-init.sh stop` → `wifibt-init.sh start_bt` → `hciconfig hci0 up` → 检查 `hcitool cmd 0x04 0x0001` 返回 `> HCI Event` |
| 经典蓝牙连续 TX | `hcitool cmd 0x3f 0x0051 …`（需先做 B2 DUT 模式）|
| 经典蓝牙单音 TX | `hcitool cmd 0x3f 0x0014 …` |
| BLE TX | `hcitool cmd 0x08 0x001e …` |
| BLE RX / 结束 | `hcitool cmd 0x08 0x001d …` / `hcitool cmd 0x08 0x001f` |
| 停止任意蓝牙测试 | `hcitool cmd 0x03 0x0003` |

## 规则

1. 执行任何 `hcitool cmd` 前先 `killall bluetoothd`。
2. 先做 WiFi 测试；WiFi 测试模式会关闭蓝牙，因此测蓝牙前要重新执行 B1。
