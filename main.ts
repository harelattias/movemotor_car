function FOREVER () {
    speed_forward = last_command_speed_fwd
    if (speed_forward > 30) {
        filter_distance()
        if (filtered_distance < 20) {
            Kitronik_Move_Motor.stop()
            stop_blink(1500)
            normal_lights()
        } else {
            Kitronik_Move_Motor.motorOn(Kitronik_Move_Motor.Motors.MotorLeft, Kitronik_Move_Motor.MotorDirection.Forward, speed_forward)
            Kitronik_Move_Motor.motorOn(Kitronik_Move_Motor.Motors.MotorRight, Kitronik_Move_Motor.MotorDirection.Forward, speed_forward)
        }
    } else if (speed_forward < -30) {
        Kitronik_Move_Motor.motorOn(Kitronik_Move_Motor.Motors.MotorLeft, Kitronik_Move_Motor.MotorDirection.Reverse, 49)
        Kitronik_Move_Motor.motorOn(Kitronik_Move_Motor.Motors.MotorRight, Kitronik_Move_Motor.MotorDirection.Reverse, 49)
    } else {
        Kitronik_Move_Motor.stop()
    }
}
function normal_lights () {
    moveMotorZIP.clear()
    moveMotorZIP = Kitronik_Move_Motor.createMoveMotorZIPLED(4)
    moveMotorZIP.setZipLedColor(0, Kitronik_Move_Motor.colors(Kitronik_Move_Motor.ZipLedColors.White))
    moveMotorZIP.setZipLedColor(1, Kitronik_Move_Motor.colors(Kitronik_Move_Motor.ZipLedColors.White))
    moveMotorZIP.setZipLedColor(2, Kitronik_Move_Motor.colors(Kitronik_Move_Motor.ZipLedColors.Orange))
    moveMotorZIP.setZipLedColor(3, Kitronik_Move_Motor.colors(Kitronik_Move_Motor.ZipLedColors.Orange))
    moveMotorZIP.show()
}
function stop_blink (time_in_ms: number) {
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
function ORR (text: string, num: number) {
    if (text.compare("cmd_fwd") == 0) {
        last_command_speed_fwd = num
    }
    if (text.compare("cmd_rgt") == 0) {
        last_command_speed_right = num
    }
}
radio.onReceivedString(function (receivedString) {
    if (receivedString.compare("beep") == 0) {
        Kitronik_Move_Motor.beepHorn()
    }
    if (receivedString.compare("beeeeeeeep") == 0) {
        music.playMelody("C5 C5 C5 C5 C5 C5 C5 C5 ", 120)
    }
})
radio.onReceivedValue(function (name, value) {
    ORR(name, value)
})
function filter_distance () {
    Kitronik_Move_Motor.setUltrasonicUnits(Kitronik_Move_Motor.Units.Centimeters)
    if (Kitronik_Move_Motor.measure() != 0 && Kitronik_Move_Motor.measure() < 200) {
        filtered_distance = Kitronik_Move_Motor.measure()
    }
    radio.sendValue("filterd distance", filtered_distance)
    radio.sendValue("measured distance", Kitronik_Move_Motor.measure())
}
let last_command_speed_right = 0
let speed_forward = 0
let last_command_speed_fwd = 0
let blink_time = 0
let filtered_distance = 0
let moveMotorZIP: Kitronik_Move_Motor.MoveMotorZIP = null
moveMotorZIP = Kitronik_Move_Motor.createMoveMotorZIPLED(4)
normal_lights()
radio.setGroup(111)
Kitronik_Move_Motor.motorBalance(Kitronik_Move_Motor.SpinDirections.Right, 1)
filtered_distance = 100
blink_time = 250
last_command_speed_fwd = 0
speed_forward = 0
basic.forever(function () {
    FOREVER()
})
