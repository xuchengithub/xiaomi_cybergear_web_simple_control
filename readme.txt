物理 CAN 设备与串口绑定：
CAN0 绑定到 /dev/ttyACM0：

通过 slcand 工具，将 CAN0（与物理 CAN 总线相连的设备）绑定到 /dev/ttyACM0，使其成为 Linux 系统中的 can0 网络接口。

bash
复制代码
sudo slcand -o -c -s8 /dev/ttyACM0 can0
sudo ip link set can0 up
CAN1 绑定到 /dev/ttyACM1：

同样，通过 slcand 将 CAN1 绑定到 /dev/ttyACM1，并将其设置为 can1 网络接口。

bash
复制代码
sudo slcand -o -c -s8 /dev/ttyACM1 can1
sudo ip link set can1 up
2. 数据发送与接收
发送数据：

当您在 can1 接口上发送数据时，例如通过 cansend 命令：

bash
复制代码
cansend can1 123#1122334455667788
这个数据帧首先通过 Linux 内核的 SocketCAN 子系统传递到 can1 接口。

can1 接口将数据帧通过 slcan 协议转换为串行数据，然后通过 USB 端口 /dev/ttyACM1 发送到 CAN 控制器。
