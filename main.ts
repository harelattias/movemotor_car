radio.onReceivedValue(function (name, value) {
    if (name.compare("drive") == 0) {
        if (value == 0) {
            Kitronik_Move_Motor.stop()
        }
        if (value == 1) {
            Kitronik_Move_Motor.move(Kitronik_Move_Motor.DriveDirections.Forward, 0)
        }
        if (value == -1) {
            Kitronik_Move_Motor.move(Kitronik_Move_Motor.DriveDirections.Reverse, 0)
        }
    }
})
radio.setGroup(111)
basic.forever(function () {
	
})
