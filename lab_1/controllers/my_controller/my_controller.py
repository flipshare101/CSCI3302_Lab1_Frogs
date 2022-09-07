from controller import Robot, DistanceSensor, Motor

# time in [ms] of a simulation step
TIME_STEP = 10

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

class move_straight:

    def __init__(self, s_number): #default action of state
        self.step = s_number
        leftMotor.setVelocity(3)
        rightMotor.setVelocity(3)
        print("move_straight")
    
    def update(self): #condition to change state
        if psValues[7] > 450 or psValues[0] > 450: # obstical in front
            if self.step == 0:
                return u_turn()
            else:
                return find_left_wall()
        else:
            return self
                
                
                
class u_turn:

     def __init__(self): #turn the robot 180
        leftMotor.setVelocity(-0.5)
        rightMotor.setVelocity(0.5)
        print("u_turn")
        
     def update(self):
         print("PS3: ", psValues[3], "PS4", psValues[4])
         if psValues[3] > 350 and psValues[4] > 350  and (abs(psValues[3] - psValues[4]) < 50): #obstical behind
             return move_straight(1)
         else:
             return self
         
class find_left_wall:

    def __init__(self): #turn the robot
        leftMotor.setVelocity(-1)
        rightMotor.setVelocity(1)
        print("find_left_wall")
        
    def update(self):
        if psValues[5] > 100:
            return move_along_left_wall()
        else:
            return self
            
class move_along_left_wall:
   def __init__(self):
       leftMotor.setVelocity(3)
       rightMotor.setVelocity(3)
       print("move_along_left_wall")
    
   def update(self):
        if psValues[5] < 100:
            return rest()
        else:
            return self
                
class rest:
    def __init__(self):
        print('rest')

    def update(self):
        stop_motors()
        return self
        
state = move_straight(0)
while robot.step(TIME_STEP) != -1:
    psValues = []
    for i in range(8):
        psValues.append(ps[i].getValue())
    state = state.update()
