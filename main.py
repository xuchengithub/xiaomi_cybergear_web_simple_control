from flask import Flask, render_template
from flask_socketio import SocketIO
import can
import logging
from pcan_cybergear import CANMotorController  # 假设代码1保存为 your_motor_controller_module.py

app = Flask(__name__)
socketio = SocketIO(app)

# 设置 CAN 接口
can_interface = 'can1'
try:
    bus = can.interface.Bus(can_interface, interface='socketcan')
except Exception as e:
    logging.error(f"Failed to initialize CAN interface {can_interface}: {e}")

# 初始化电机控制器
motor_controller = CANMotorController(bus, motor_id=127, main_can_id=254)
# 设置运行模式
motor_controller.set_run_mode(CANMotorController.RunModes.CONTROL_MODE)


@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('forward')
def handle_forward():
    """
    处理前进命令。通过电机控制器发送前进指令。
    """
    torque = 1.0  # 设置合适的扭矩
    target_angle = 1.0  # 设置目标角度
    target_velocity = 1.0  # 设置目标速度
    Kp = 0.03  # 设置比例增益
    Kd = 0.01  # 设置微分增益

    # 使用电机控制器发送前进命令
    motor_controller.send_motor_control_command(
        torque=torque, 
        target_angle=target_angle, 
        target_velocity=target_velocity, 
        Kp=Kp, 
        Kd=Kd
    )
@socketio.on('enable')
def handle_enable():
    motor_controller.enable()

@socketio.on('backward')
def handle_backward():
    """
    处理后退命令。通过电机控制器发送后退指令。
    """
    torque = -5.0  # 设置合适的负扭矩
    target_angle = -1.0  # 设置目标角度
    target_velocity = -2.0  # 设置目标速度
    Kp =0.03  # 设置比例增益
    Kd = 0.03  # 设置微分增益

    # 使用电机控制器发送后退命令
    motor_controller.send_motor_control_command(
        torque=torque, 
        target_angle=target_angle, 
        target_velocity=target_velocity, 
        Kp=Kp, 
        Kd=Kd
    )

@socketio.on('stop')
def handle_stop():
    """
    处理停止命令。通过电机控制器发送停止指令。
    """
    motor_controller.disable()  # 直接调用电机控制器的disable方法停止电机

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    socketio.run(app, debug=False, host='0.0.0.0', port=5000)

