function set_motor_speed(speed: number, motor: boolean) {
    if (motor) {
        if (speed > 0) {
            Kitronik_Move_Motor.motorOn(Kitronik_Move_Motor.Motors.MotorRight, Kitronik_Move_Motor.MotorDirection.Forward, speed)
        } else if (speed < 0) {
            Kitronik_Move_Motor.motorOn(Kitronik_Move_Motor.Motors.MotorRight, Kitronik_Move_Motor.MotorDirection.Reverse, Math.abs(speed))
        } else {
            Kitronik_Move_Motor.motorOff(Kitronik_Move_Motor.Motors.MotorRight)
        }
        
    } else if (speed > 0) {
        Kitronik_Move_Motor.motorOn(Kitronik_Move_Motor.Motors.MotorLeft, Kitronik_Move_Motor.MotorDirection.Forward, speed)
    } else if (speed < 0) {
        Kitronik_Move_Motor.motorOn(Kitronik_Move_Motor.Motors.MotorLeft, Kitronik_Move_Motor.MotorDirection.Reverse, Math.abs(speed))
    } else {
        Kitronik_Move_Motor.motorOff(Kitronik_Move_Motor.Motors.MotorLeft)
    }
    
}

function normal_lights() {
    
    moveMotorZIP.clear()
    moveMotorZIP = Kitronik_Move_Motor.createMoveMotorZIPLED(4)
    moveMotorZIP.setZipLedColor(0, Kitronik_Move_Motor.colors(Kitronik_Move_Motor.ZipLedColors.White))
    moveMotorZIP.setZipLedColor(1, Kitronik_Move_Motor.colors(Kitronik_Move_Motor.ZipLedColors.White))
    moveMotorZIP.setZipLedColor(2, Kitronik_Move_Motor.colors(Kitronik_Move_Motor.ZipLedColors.Orange))
    moveMotorZIP.setZipLedColor(3, Kitronik_Move_Motor.colors(Kitronik_Move_Motor.ZipLedColors.Orange))
    moveMotorZIP.show()
}

function stop_blink(time_in_ms: number) {
    moveMotorZIP.clear()
    moveMotorZIP.setZipLedColor(0, Kitronik_Move_Motor.colors(Kitronik_Move_Motor.ZipLedColors.White))
    moveMotorZIP.setZipLedColor(1, Kitronik_Move_Motor.colors(Kitronik_Move_Motor.ZipLedColors.White))
    moveMotorZIP.setZipLedColor(2, Kitronik_Move_Motor.colors(Kitronik_Move_Motor.ZipLedColors.Red))
    moveMotorZIP.setZipLedColor(3, Kitronik_Move_Motor.colors(Kitronik_Move_Motor.ZipLedColors.Red))
    for (let index = 0; index < time_in_ms / blink_time; index++) {
        moveMotorZIP.rotate(2)
        music.playTone(659, music.beat(BeatFraction.Whole))
        basic.pause(blink_time)
        moveMotorZIP.show()
    }
}

radio.onReceivedString(function on_received_string(receivedString: string) {
    if (receivedString.compare("off_lig") == 0) {
        moveMotorZIP.setColor(Kitronik_Move_Motor.colors(Kitronik_Move_Motor.ZipLedColors.Black))
        moveMotorZIP.show()
    }
    
    if (receivedString.compare("off_off") == 0) {
        normal_lights()
    }
    
    if (receivedString.compare("beep") == 0) {
        Kitronik_Move_Motor.beepHorn()
    }
    
})
radio.onReceivedValue(function on_received_value(name: string, value: number) {
    
    if (name.compare("rgt_spd") == 0) {
        last_command_right_motor_speed = value
    }
    
    if (name.compare("left_spd") == 0) {
        last_command_left_motor_speed = value
    }
    
})
let speed_left_motor = 0
let speed_right_motor = 0
let last_command_left_motor_speed = 0
let last_command_right_motor_speed = 0
let blink_time = 0
let moveMotorZIP : Kitronik_Move_Motor.MoveMotorZIP = null
moveMotorZIP = Kitronik_Move_Motor.createMoveMotorZIPLED(4)
normal_lights()
radio.setGroup(111)
Kitronik_Move_Motor.motorBalance(Kitronik_Move_Motor.SpinDirections.Right, 1)
let filtered_distance = 100
blink_time = 250
last_command_right_motor_speed = 0
basic.forever(function on_forever() {
    
    speed_right_motor = last_command_right_motor_speed
    speed_left_motor = last_command_left_motor_speed
    Kitronik_Move_Motor.setUltrasonicUnits(Kitronik_Move_Motor.Units.Centimeters)
    if (Kitronik_Move_Motor.measure() != 0 && Kitronik_Move_Motor.measure() < 200) {
        filtered_distance = Kitronik_Move_Motor.measure()
    }
    
    radio.sendValue("filterd distance", filtered_distance)
    if (filtered_distance < 20 && speed_left_motor + speed_right_motor > 0) {
        Kitronik_Move_Motor.stop()
        stop_blink(500)
        normal_lights()
    } else {
        set_motor_speed(speed_right_motor, true)
        set_motor_speed(speed_left_motor, false)
    }
    
})
