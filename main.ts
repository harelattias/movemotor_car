input.onButtonPressed(Button.A, function () {
    Kitronik_Move_Motor.motorBalance(Kitronik_Move_Motor.SpinDirections.Right, left_bias)
    left_bias += 1
    basic.showNumber(left_bias)
})
input.onButtonPressed(Button.B, function () {
    Kitronik_Move_Motor.motorBalance(Kitronik_Move_Motor.SpinDirections.Right, left_bias)
    left_bias += -1
    basic.showNumber(left_bias)
})
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
})
let left_bias = 0
radio.setGroup(111)
basic.forever(function () {
	
})
