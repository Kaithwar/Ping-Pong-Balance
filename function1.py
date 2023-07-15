from cmath import exp

# Limits of servo

# 1 -> height servo
servo2_min = 130
servo2_stable = 160
servo2_max = 180

# 2 -> width servo
servo1_min = 125
servo1_stable = 155
servo1_max = 175

# Parameters of the control function
A = 10
b = 0.1
m = 50

# Value at which function changes to linear
thresh = 0.10

# Input a value between -1 to 1
# Outputs an integer between -90 and 90 according to parameters
# def control_function(x):
#     Y = A * (exp(pow(thresh/b,2))-1)
#     out = complex(0)
#     if(x <= thresh and x >= 0):
#         out = (A * (exp(pow(x/b,2))-1))
#     elif(x>thresh and x>=0):
#         out = ((m * (x - thresh)) + Y)
#     elif(abs(x)<=thresh and x<0):
#         out = (-1 * A * (exp(pow(x/b,2))-1))
#     elif(abs(x)>thresh and x<0):
#         out = ((-1 * m * (abs(x)-thresh)) - Y)
#     return int(out.real)


# Input a value between -1 to 1
# Returns scaled value according to servo
def scaled_output(servo_num, x):
    # y=control_function(x)
    y=x*90
    if servo_num==1:
        if y>=0:
            angle = 155 + (2*y/9)
        else:
            angle = 155 + (y/3)
    elif servo_num==2:
        if y>=0:
            angle = 160 - (y/3)
        else:
            angle = 160 - (2*y/9)
    return int(angle)


# while True:
#     inp = float(input())
#     print(control_function(inp))
