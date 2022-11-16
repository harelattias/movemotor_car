radio.onReceivedValue(function (name, value) {
    if (name.compare("drive") == 0) {
        if (value == 0) {
            Kitronik_Move_Motor.stop()
        }
        if (value == 1) {
            Kitronik_Move_Motor.move(Kitronik_Move_Motor.DriveDirections.Forward, 50)
        }
        if (value == -1) {
            Kitronik_Move_Motor.move(Kitronik_Move_Motor.DriveDirections.Reverse, 50)
        }
    }
    if (name.compare("acc_y") == 0) {
        if (value < -200) {
            Kitronik_Move_Motor.move(Kitronik_Move_Motor.DriveDirections.Forward, 50)
        } else if (value > 200) {
            Kitronik_Move_Motor.move(Kitronik_Move_Motor.DriveDirections.Reverse, 50)
        } else {
            Kitronik_Move_Motor.stop()
        }
    }
})
radio.setGroup(111)
Kitronik_Move_Motor.motorBalance(Kitronik_Move_Motor.SpinDirections.Right, 1)
basic.forever(function () {
	
})
