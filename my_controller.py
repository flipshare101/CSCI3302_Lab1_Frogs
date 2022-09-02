from controller import Robot, DistanceSensor, Motor

# time in [ms] of a simulation step
TIME_STEP = 64

MAX_SPEED = 6.28

# create the Robot instance.
robot = Robot()

# initialize devices
ps = []
psNames = [
    'ps0', 'ps1', 'ps2', 'ps3',
    'ps4', 'ps5', 'ps6', 'ps7'
]

for i in range(8):
    ps.append(robot.getDevice(psNames[i]))
    ps[i].enable(TIME_STEP)

leftMotor = robot.getDevice('left wheel motor')
rightMotor = robot.getDevice('right wheel motor')
leftMotor.setPosition(float('inf'))
rightMotor.setPosition(float('inf'))
leftMotor.setVelocity(0.0)
rightMotor.setVelocity(0.0)

state = move_straight()
while robot.step(TIME_STEP) != -1:
    psValues = []
    for i in range(8):
        psValues.append(ps[i].getValue())
    state = state.update()

class move_straight:

    def __init__(self, s_number): #default action of state
        self.step = s_number
        leftMotor.setVelocity(3)
        rightMotor.setVelocity(3)
    
    def update(self): #condition to change state
        if psValues[7] < 34 or psValues[0] < 34: # obstical in front
            if self.step == 0:
                return u_turn()
            else:
                return find_left_wall()
        else:
            return self
                
                
                
class u_turn:

     def __init__(self): #turn the robot 180
        leftMotor.setVelocity(-MAX_SPEED)
        rightMotor.setVelocity(MAX_SPEED)
        
     def update(self):
         if psValues[3] < 34 or psValues[4] < 34: #obstical behind
             return move_straight(1)
         else:
             return self
         
class find_left_wall:

    def __init__(self): #turn the robot
        leftMotor.setVelocity(-1)
        rightMotor.setVelocity(1)
        
    def update(self):
        if psValues[5] < 34:
            return move_along_left_wall()
        else:
            return self
            
class move_along_left_wall:
   def __init__(self):
       leftMotor.setVelocity(3)
       rightMotor.setVelocity(3)
    
   def update(self):
        if psValues[5] > 34:
            return rest()
        else:
            return self
                
class rest:
    def __init__(self):
        print('done')

    def update(self):
        stop_motors()
        return self
