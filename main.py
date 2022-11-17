def normal_lights():
    global moveMotorZIP
    moveMotorZIP.clear()
    moveMotorZIP = Kitronik_Move_Motor.create_move_motor_zipled(4)
    moveMotorZIP.set_zip_led_color(0,
        Kitronik_Move_Motor.colors(Kitronik_Move_Motor.ZipLedColors.WHITE))
    moveMotorZIP.set_zip_led_color(1,
        Kitronik_Move_Motor.colors(Kitronik_Move_Motor.ZipLedColors.WHITE))
    moveMotorZIP.set_zip_led_color(2,
        Kitronik_Move_Motor.colors(Kitronik_Move_Motor.ZipLedColors.ORANGE))
    moveMotorZIP.set_zip_led_color(3,
        Kitronik_Move_Motor.colors(Kitronik_Move_Motor.ZipLedColors.ORANGE))
    moveMotorZIP.show()
def stop_blink(time_in_ms: number):
    moveMotorZIP.clear()
    moveMotorZIP.set_zip_led_color(0,
        Kitronik_Move_Motor.colors(Kitronik_Move_Motor.ZipLedColors.WHITE))
    moveMotorZIP.set_zip_led_color(1,
        Kitronik_Move_Motor.colors(Kitronik_Move_Motor.ZipLedColors.WHITE))
    moveMotorZIP.set_zip_led_color(2,
        Kitronik_Move_Motor.colors(Kitronik_Move_Motor.ZipLedColors.RED))
    moveMotorZIP.set_zip_led_color(3,
        Kitronik_Move_Motor.colors(Kitronik_Move_Motor.ZipLedColors.RED))
    for index in range(time_in_ms / blink_time):
        moveMotorZIP.rotate(2)
        moveMotorZIP.show()
        basic.pause(blink_time)

def on_received_value(name, value):
    if name.compare("acc_y") == 0:
        if value < -300:
            filter_distance()
            if filtered_distance < 20:
                Kitronik_Move_Motor.stop()
                music.play_melody("C5 - C5 - C5 - C5 - ", 150)
                stop_blink(1500)
                normal_lights()
            else:
                Kitronik_Move_Motor.motor_on(Kitronik_Move_Motor.Motors.MOTOR_LEFT,
                    Kitronik_Move_Motor.MotorDirection.FORWARD,
                    50)
                Kitronik_Move_Motor.motor_on(Kitronik_Move_Motor.Motors.MOTOR_RIGHT,
                    Kitronik_Move_Motor.MotorDirection.FORWARD,
                    50)
        elif value > 200:
            Kitronik_Move_Motor.move(Kitronik_Move_Motor.DriveDirections.REVERSE, 50)
        else:
            Kitronik_Move_Motor.stop()
radio.on_received_value(on_received_value)

def filter_distance():
    global filtered_distance
    Kitronik_Move_Motor.set_ultrasonic_units(Kitronik_Move_Motor.Units.CENTIMETERS)
    if Kitronik_Move_Motor.measure() != 0 and Kitronik_Move_Motor.measure() != 1019:
        filtered_distance = Kitronik_Move_Motor.measure()
    radio.send_value("distance", filtered_distance)
blink_time = 0
filtered_distance = 0
moveMotorZIP: Kitronik_Move_Motor.MoveMotorZIP = None
moveMotorZIP = Kitronik_Move_Motor.create_move_motor_zipled(4)
normal_lights()
radio.set_group(111)
Kitronik_Move_Motor.motor_balance(Kitronik_Move_Motor.SpinDirections.RIGHT, 1)
filtered_distance = 100
blink_time = 250

def on_forever():
    pass
basic.forever(on_forever)
