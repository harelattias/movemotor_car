def set_motor_speed(speed: number, motor: bool):
    if motor:
        if speed > 0:
            Kitronik_Move_Motor.motor_on(Kitronik_Move_Motor.Motors.MOTOR_RIGHT,
                Kitronik_Move_Motor.MotorDirection.FORWARD,
                speed)
        elif speed < 0:
            Kitronik_Move_Motor.motor_on(Kitronik_Move_Motor.Motors.MOTOR_RIGHT,
                Kitronik_Move_Motor.MotorDirection.REVERSE,
                abs(speed))
        else:
            Kitronik_Move_Motor.motor_off(Kitronik_Move_Motor.Motors.MOTOR_RIGHT)
    else:
        if speed > 0:
            Kitronik_Move_Motor.motor_on(Kitronik_Move_Motor.Motors.MOTOR_LEFT,
                Kitronik_Move_Motor.MotorDirection.FORWARD,
                speed)
        elif speed < 0:
            Kitronik_Move_Motor.motor_on(Kitronik_Move_Motor.Motors.MOTOR_LEFT,
                Kitronik_Move_Motor.MotorDirection.REVERSE,
                abs(speed))
        else:
            Kitronik_Move_Motor.motor_off(Kitronik_Move_Motor.Motors.MOTOR_LEFT)
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
        music.play_tone(659, music.beat(BeatFraction.WHOLE))
        basic.pause(blink_time)
        moveMotorZIP.show()

def on_received_string(receivedString):
    if receivedString.compare("off_lig") == 0:
        moveMotorZIP.set_color(Kitronik_Move_Motor.colors(Kitronik_Move_Motor.ZipLedColors.BLACK))
        moveMotorZIP.show()
    if receivedString.compare("off_off") == 0:
        normal_lights()
    if receivedString.compare("beep") == 0:
        Kitronik_Move_Motor.beep_horn()
radio.on_received_string(on_received_string)

def on_received_value(name, value):
    global last_command_right_motor_speed, last_command_left_motor_speed
    if name.compare("rgt_spd") == 0:
        last_command_right_motor_speed = value
    if name.compare("left_spd") == 0:
        last_command_left_motor_speed = value
radio.on_received_value(on_received_value)

speed_left_motor = 0
speed_right_motor = 0
last_command_left_motor_speed = 0
last_command_right_motor_speed = 0
blink_time = 0
moveMotorZIP: Kitronik_Move_Motor.MoveMotorZIP = None
moveMotorZIP = Kitronik_Move_Motor.create_move_motor_zipled(4)
normal_lights()
radio.set_group(111)
Kitronik_Move_Motor.motor_balance(Kitronik_Move_Motor.SpinDirections.RIGHT, 1)
filtered_distance = 100
blink_time = 250
last_command_right_motor_speed = 0

def on_forever():
    global speed_right_motor, speed_left_motor, filtered_distance
    speed_right_motor = last_command_right_motor_speed
    speed_left_motor = last_command_left_motor_speed
    Kitronik_Move_Motor.set_ultrasonic_units(Kitronik_Move_Motor.Units.CENTIMETERS)
    if Kitronik_Move_Motor.measure() != 0 and Kitronik_Move_Motor.measure() < 200:
        filtered_distance = Kitronik_Move_Motor.measure()
    radio.send_value("filterd distance", filtered_distance)
    if filtered_distance < 20 and speed_left_motor + speed_right_motor > 0:
        Kitronik_Move_Motor.stop()
        stop_blink(500)
        normal_lights()
    else:
        set_motor_speed(speed_right_motor, True)
        set_motor_speed(speed_left_motor, False)
basic.forever(on_forever)
