def FOREVER():
    global speed_forward
    speed_forward = last_command_speed_fwd
    if speed_forward > 30:
        filter_distance()
        if filtered_distance < 20:
            Kitronik_Move_Motor.stop()
            stop_blink(1500)
            normal_lights()
        else:
            Kitronik_Move_Motor.motor_on(Kitronik_Move_Motor.Motors.MOTOR_LEFT,
                Kitronik_Move_Motor.MotorDirection.FORWARD,
                speed_forward)
            Kitronik_Move_Motor.motor_on(Kitronik_Move_Motor.Motors.MOTOR_RIGHT,
                Kitronik_Move_Motor.MotorDirection.FORWARD,
                speed_forward)
    elif speed_forward < -30:
        Kitronik_Move_Motor.motor_on(Kitronik_Move_Motor.Motors.MOTOR_LEFT,
            Kitronik_Move_Motor.MotorDirection.REVERSE,
            49)
        Kitronik_Move_Motor.motor_on(Kitronik_Move_Motor.Motors.MOTOR_RIGHT,
            Kitronik_Move_Motor.MotorDirection.REVERSE,
            49)
    else:
        Kitronik_Move_Motor.stop()
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
def ORR(text: str, num: number):
    global last_command_speed_fwd, last_command_speed_right
    if text.compare("cmd_fwd") == 0:
        last_command_speed_fwd = num
    if text.compare("cmd_rgt") == 0:
        last_command_speed_right = num

def on_received_string(receivedString):
    if receivedString.compare("beep") == 0:
        Kitronik_Move_Motor.beep_horn()
    if receivedString.compare("beeeeeeeep") == 0:
        music.play_melody("C5 C5 C5 C5 C5 C5 C5 C5 ", 120)
radio.on_received_string(on_received_string)

def on_received_value(name, value):
    ORR(name, value)
radio.on_received_value(on_received_value)

def filter_distance():
    global filtered_distance
    Kitronik_Move_Motor.set_ultrasonic_units(Kitronik_Move_Motor.Units.CENTIMETERS)
    if Kitronik_Move_Motor.measure() != 0 and Kitronik_Move_Motor.measure() < 200:
        filtered_distance = Kitronik_Move_Motor.measure()
    radio.send_value("filterd distance", filtered_distance)
    radio.send_value("measured distance", Kitronik_Move_Motor.measure())
last_command_speed_right = 0
speed_forward = 0
last_command_speed_fwd = 0
blink_time = 0
filtered_distance = 0
moveMotorZIP: Kitronik_Move_Motor.MoveMotorZIP = None
moveMotorZIP = Kitronik_Move_Motor.create_move_motor_zipled(4)
normal_lights()
radio.set_group(111)
Kitronik_Move_Motor.motor_balance(Kitronik_Move_Motor.SpinDirections.RIGHT, 1)
filtered_distance = 100
blink_time = 250
last_command_speed_fwd = 0
speed_forward = 0

def on_forever():
    FOREVER()
basic.forever(on_forever)
