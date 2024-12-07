from newspeedmode import TMotorManager_servo_can

with TMotorManager_servo_can() as motor:
    motor.debug = True
    motor.enter_velocity_control()

    for i in range(100):
        motor.velocity = 2.0
        motor.update()
        print("\r" + str(motor),end='')
