#!/bin/bash

# 加载必要的内核模块
sudo modprobe can
sudo modprobe can_raw
sudo modprobe slcan

# 将 CANable 设备附加到 slcan0 接口，并设置波特率
# 请根据需要修改波特率，-s6 对应 500Kbps
BAUD_RATE_SETTING="8"  # 1 Mbps
DEVICE="/dev/ttyACM6"
INTERFACE="can1"

echo "Configuring CANable device on $DEVICE with baud rate setting $BAUD_RATE_SETTING"

# 设置设备并启用
sudo slcand -o -c -s$BAUD_RATE_SETTING $DEVICE $INTERFACE


# 延迟一小段时间，确保设备准备就绪
sleep 2

# 激活 CAN 网络接口
sudo ip link set up $INTERFACE

# 显示接口状态
echo "Interface $INTERFACE configuration:"
ip link show $INTERFACE

# 提示信息
echo "To send a CAN message: cansend $INTERFACE <can_id>#<data>"
echo "To dump CAN messages: candump $INTERFACE"
echo "To stop the interface: sudo ip link set down $INTERFACE && sudo slcand -k"

