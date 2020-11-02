import starter_shield
from common import num_range_scale, mbuild_color_table,color_table
import math

##############################################################################################################
#########################   car motion API API   ###################################################################
##############################################################################################################
__MAX_SPEED      = 200             # car speed, unit: rpm,  300 rmp = 1800°/s
__MAX_RUN_TIME   = 3600000         # run time, unit: ms,   3600000 ms = 1hour
__MAX_ACCEL_TIME = 10000           # accelerate time, unit: ms,   10000 ms = 10s
__MAX_DECEL_TIME = 10000           # decelerate time, unit: ms,   10000 ms = 10s
__MAX_DISTANCE   = 500            # straight distance, unit: cm,   1000 cm = 10m
__MAX_ANGLE      = 10000           # wheel turns clockwise angle, unit: mm,   10000 mm = 10m
__DEFAULT_SPEED  = 50              # car default speed, unit: rpm,  50 rmp = 300°/s
__DEFAULT_RUN_TIMS  = "null"             # car default run_time, unit: s, "null" means continue
__SECOND_TO_MS_FACTOR = 1000             # second convert to millisecond
# __CM_TO_MM_FACTOR = 10                   # centimeter convert to millimeter
__ANGLE_CAR_TO_WHEEL_FACTOR = 115/64.5   # car angle convert to wheel angle, __ANGLE_CAR_TO_WHEEL_FACTOR = WHEEL_TRACK / WHEEL_DIAMETER = 115/64.5
__SPEED_RPM_TO_DPS_FACTOR = 6            # RPM(revolutions per minute) convert to DPS(degrees per second), __SPEED_RPM_TO_DPS_FACTOR = 360/60 = 6 (°/s)
__DEFAULT_ACCELERATION  = 1000            # acceleration of speed
__DISTANCE_TO_ANGLE_FOCTOR = 17.76613    # the distance(unit:cm) of car going convert to the angle(unit:degree) of wheel turning, __DISTANCE_TO_ANGLE_FOCTOR = 360 / (WHEEL_DIAMETER * pi)

def forward(speed = __DEFAULT_SPEED, run_time = __DEFAULT_RUN_TIMS, accel_time = 1, decel_time = 1):
    if run_time == 0:
        run_time = 0.001 
    if run_time == __DEFAULT_RUN_TIMS:
        run_time = 0    
    if not isinstance(run_time, (int, float)):
        return     
    run_time = int(run_time * __SECOND_TO_MS_FACTOR)
    starter_shield.car_spd_mode_forward(speed, run_time, accel_time, decel_time)


def backward(speed = __DEFAULT_SPEED, run_time = __DEFAULT_RUN_TIMS, accel_time = 1, decel_time = 1):
    if run_time == 0:
        run_time = 0.001 
    if run_time == __DEFAULT_RUN_TIMS:
        run_time = 0  
    if not isinstance(run_time, (int, float)):
        return     
    run_time = int(run_time * __SECOND_TO_MS_FACTOR)    
    starter_shield.car_spd_mode_backward(speed, run_time, accel_time, decel_time)


def turn_left(speed = __DEFAULT_SPEED, run_time = __DEFAULT_RUN_TIMS, accel_time = 1, decel_time = 1):
    if run_time == 0:
        run_time = 0.001 
    if run_time == __DEFAULT_RUN_TIMS:
        run_time = 0  
    if not isinstance(run_time, (int, float)):
        return     
    run_time = int(run_time * __SECOND_TO_MS_FACTOR)
    starter_shield.car_spd_mode_turn_left(speed, run_time, accel_time, decel_time)


def turn_right(speed = __DEFAULT_SPEED, run_time = __DEFAULT_RUN_TIMS, accel_time = 1, decel_time = 1):
    if run_time == 0:
        run_time = 0.001 
    if run_time == __DEFAULT_RUN_TIMS:
        run_time = 0  
    if not isinstance(run_time, (int, float)):
        return     
    run_time = int(run_time * __SECOND_TO_MS_FACTOR)
    starter_shield.car_spd_mode_turn_right(speed, run_time, accel_time, decel_time)

     
def straight(distance = 50, speed = __DEFAULT_SPEED):
    if not isinstance(distance, (int, float)):
        return
    if not isinstance(speed, (int, float)):
        return
    distance = num_range_scale(distance, -__MAX_DISTANCE, __MAX_DISTANCE)
    wheel_angle = distance * __DISTANCE_TO_ANGLE_FOCTOR
    # distance = int(distance * __CM_TO_MM_FACTOR)
    speed = num_range_scale(speed, -__MAX_SPEED, __MAX_SPEED)
    speed = math.fabs(speed)     
    speed = speed * __SPEED_RPM_TO_DPS_FACTOR
    if math.fabs(wheel_angle) <= (speed * speed / __DEFAULT_ACCELERATION):
        accel_time = math.sqrt(math.fabs(wheel_angle / __DEFAULT_ACCELERATION))
        run_time = 2 * accel_time
    else:
        accel_time = speed / __DEFAULT_ACCELERATION
        run_time = math.fabs(wheel_angle) / speed + accel_time
    wheel_angle = int(wheel_angle)
    # run_time = int(run_time * __SECOND_TO_MS_FACTOR)
    # accel_time = int(accel_time * __SECOND_TO_MS_FACTOR)
    run_time   = int(round(run_time   * __SECOND_TO_MS_FACTOR/100)*100)
    accel_time = int(round(accel_time * __SECOND_TO_MS_FACTOR/100)*100)
    if accel_time <= 100:
        accel_time = 100
    if run_time   <= 2 * accel_time:
        run_time = 2 * accel_time + 100    
    # cyberpi.console.println("angle=%s"%(wheel_angle))    
    # cyberpi.console.println("speed=%s"%(speed))    
    # cyberpi.console.println("r_t=%s"%(run_time))
    # cyberpi.console.println("a_t=%s"%(accel_time))
    starter_shield.car_pos_mode_straight(wheel_angle, run_time, accel_time)


def turn(angle = 360, speed = __DEFAULT_SPEED):
    if not isinstance(angle, (int, float)):
        return
    if not isinstance(speed, (int, float)):
        return             
    wheel_angle = angle * __ANGLE_CAR_TO_WHEEL_FACTOR
    speed = num_range_scale(speed, -__MAX_SPEED, __MAX_SPEED)
    speed = math.fabs(speed)     
    speed = speed * __SPEED_RPM_TO_DPS_FACTOR
    if math.fabs(wheel_angle) <= (speed * speed / __DEFAULT_ACCELERATION):
        accel_time = math.sqrt(math.fabs(wheel_angle / __DEFAULT_ACCELERATION))
        run_time = 2 * accel_time
    else:
        accel_time = speed / __DEFAULT_ACCELERATION
        run_time = math.fabs(wheel_angle) / speed + accel_time
    wheel_angle = int(wheel_angle)
    # run_time = int(run_time * __SECOND_TO_MS_FACTOR)
    # accel_time = int(accel_time * __SECOND_TO_MS_FACTOR)
    run_time   = int(round(run_time   * __SECOND_TO_MS_FACTOR/100)*100)
    accel_time = int(round(accel_time * __SECOND_TO_MS_FACTOR/100)*100)
    if accel_time <= 100:
        accel_time = 100
    if run_time   <= 2 * accel_time:
        run_time = 2 * accel_time + 100    
    # cyberpi.console.println("angle=%s"%(wheel_angle))    
    # cyberpi.console.println("speed=%s"%(speed))    
    # cyberpi.console.println("r_t=%s"%(run_time))
    # cyberpi.console.println("a_t=%s"%(accel_time))       
    starter_shield.car_pos_mode_wheel_clockwise(wheel_angle, run_time, accel_time)


def drive_speed(EM1_speed = __DEFAULT_SPEED, EM2_speed = __DEFAULT_SPEED, run_time = __DEFAULT_RUN_TIMS, accel_time = 1, decel_time = 1):
    if run_time == 0:
        run_time = 0.001 
    if run_time == __DEFAULT_RUN_TIMS:
        run_time = 0
    if not isinstance(run_time, (int, float)):
        return     
    run_time = int(run_time * __SECOND_TO_MS_FACTOR)
    EM2_speed = -EM2_speed
    starter_shield.car_spd_mode_apiece(EM1_speed, EM2_speed, run_time, accel_time, decel_time)


def drive_power(EM1_power = 50, EM2_power = 50, run_time = 0, accel_time = 1, decel_time = 1):
    if not isinstance(run_time, (int, float)):
        return     
    run_time = int(run_time * __SECOND_TO_MS_FACTOR)
    starter_shield.encoder_motor_set_power_both(EM1_power, EM2_power)



# def cw(angle = 360, run_time = 0, accel_time = 1, decel_time = 1):
#     if not isinstance(run_time, (int, float)):
#         return     
#     run_time = int(run_time * __SECOND_TO_MS_FACTOR)
#     starter_shield.car_pos_mode_wheel_clockwise(angle, run_time, accel_time, decel_time)


# def ccw(angle = 360, run_time = 0, accel_time = 1, decel_time = 1):
#     if not isinstance(run_time, (int, float)):
#         return     
#     run_time = int(run_time * __SECOND_TO_MS_FACTOR)
#     starter_shield.car_pos_mode_wheel_anticlockwise(angle, run_time, accel_time, decel_time)


# def stop(decel_time = 1):
#     starter_shield.car_stop(decel_time = 1)

def EM_stop(port = "all"):
    if port not in [0, 1, 2, "all", "ALL", "em1", "em2", "EM1", "EM2"]:
        return
    if port == "all" or port == "ALL":
        port = 0
    if port == "em1" or port == "EM1":
        port = 1
    if port == "em2" or port == "EM2":
        port = 2    
    starter_shield.encoder_motor_stop(port)       
##############################################################################################################
#########################  car motion API   ##################################################################
##############################################################################################################

##############################################################################################################
#########################   encoder motor API   ##############################################################
##############################################################################################################
def EM_set_power(power = 50, port = "all"):
    if port not in [0, 1, 2, "all", "ALL", "em1", "em2", "EM1", "EM2"]:
        return
    if port == "all" or port == "ALL":
        port = 0
    if port == "em1" or port == "EM1":
        port = 1
    if port == "em2" or port == "EM2":
        port = 2
    starter_shield.encoder_motor_set_power(port, power)


def EM_set_speed(speed = __DEFAULT_SPEED, port = "all"):
    if port not in [0, 1, 2, "all", "ALL", "em1", "em2", "EM1", "EM2"]:
        return
    if port == "all" or port == "ALL":
        port = 0
    if port == "em1" or port == "EM1":
        port = 1
    if port == "em2" or port == "EM2":
        port = 2
    starter_shield.encoder_motor_set_speed(port, speed)


def EM_turn(angle = 360, speed = __DEFAULT_SPEED, port = "all"):
    if not isinstance(angle, (int, float)):
        return
    if not isinstance(speed, (int, float)):
        return
    if port not in [0, 1, 2, "all", "ALL", "em1", "em2", "EM1", "EM2"]:
        return
    if port == "all" or port == "ALL":
        port = 0
    if port == "em1" or port == "EM1":
        port = 1
    if port == "em2" or port == "EM2":
        port = 2             
    wheel_angle = angle
    speed = num_range_scale(speed, -__MAX_SPEED, __MAX_SPEED)
    speed = math.fabs(speed)     
    speed = speed * __SPEED_RPM_TO_DPS_FACTOR
    if math.fabs(wheel_angle) <= (speed * speed / __DEFAULT_ACCELERATION):
        accel_time = math.sqrt(math.fabs(wheel_angle / __DEFAULT_ACCELERATION))
        run_time = 2 * accel_time
    else:
        accel_time = speed / __DEFAULT_ACCELERATION
        run_time = math.fabs(wheel_angle) / speed + accel_time
    wheel_angle = int(wheel_angle)
    # run_time = int(run_time * __SECOND_TO_MS_FACTOR)
    # accel_time = int(accel_time * __SECOND_TO_MS_FACTOR)
    run_time   = int(round(run_time   * __SECOND_TO_MS_FACTOR/100)*100)
    accel_time = int(round(accel_time * __SECOND_TO_MS_FACTOR/100)*100)
    if accel_time <= 100:
        accel_time = 100
    if run_time   <= 2 * accel_time:
        run_time = 2 * accel_time + 100
    # cyberpi.console.println("angle=%s"%(wheel_angle))
    # cyberpi.console.println("speed=%s"%(speed))
    # cyberpi.console.println("r_t=%s"%(run_time))
    # cyberpi.console.println("a_t=%s"%(accel_time))
    starter_shield.encoder_motor_set_angle(port, wheel_angle, run_time, accel_time)
    

def EM_get_angle(port = "EM1"):
    if port not in [1, 2, "em1", "em2", "EM1", "EM2"]:
        return 0
    if port == "em1" or port == "EM1":
        port = 1
    if port == "em2" or port == "EM2":
        port = 2    
    ret = starter_shield.encoder_motor_get_positon(port)
    return ret


def EM_get_speed(port = "EM1"):
    if port not in [1, 2, "em1", "em2", "EM1", "EM2"]:
        return 0
    if port == "em1" or port == "EM1":
        port = 1
    if port == "em2" or port == "EM2":
        port = 2     
    ret = starter_shield.encoder_motor_get_speed(port)
    return ret


def EM_get_power(port = "EM1"):
    if port not in [1, 2, "em1", "em2", "EM1", "EM2"]:
        return 0
    if port == "em1" or port == "EM1":
        port = 1
    if port == "em2" or port == "EM2":
        port = 2
    ret = starter_shield.encoder_motor_get_power(port)
    return ret


def EM_reset_angle(port = "all"):
    if port not in [0, 1, 2, "all", "ALL", "em1", "em2", "EM1", "EM2"]:
        return
    if port == "all" or port == "ALL":
        port = 0
    if port == "em1" or port == "EM1":
        port = 1
    if port == "em2" or port == "EM2":
        port = 2       
    starter_shield.encoder_motor_reset_position(port)


def EM_lock(is_lock = False, port = "all"):
    if is_lock not in [0, 1, False, True]:
        # cyberpi.console.println("err_l=%s"%(is_lock))
        return
    if is_lock == False :
        is_lock = 0
    if is_lock == True :
        is_lock = 1
    if port not in [0, 1, 2, "all", "ALL", "em1", "em2", "EM1", "EM2"]:
        # cyberpi.console.println("err_p=%s"%(port))
        return
    if port == "all" or port == "ALL":
        port = 0
    if port == "em1" or port == "EM1":
        port = 1
    if port == "em2" or port == "EM2":
        port = 2  
    starter_shield.encoder_motor_lock(port, is_lock)
    # cyberpi.console.println("p=%s"%(port))
    # cyberpi.console.println("l=%s"%(is_lock))
##############################################################################################################
#########################   encoder motor API   ##############################################################
##############################################################################################################


##############################################################################################################
#########################   DC motor API   ###################################################################
##############################################################################################################
def motor_set(power, port):
    if port not in [1, 2, "all", "m1", "m2", "M1", "M2"]:
        return
    if port == "all":
        port = 0
    if port == "m1" or port == "M1":
        port = 1
    if port == "m2" or port == "M2":
        port = 2        
    starter_shield.dc_motor_set_power(port, power)


def motor_get(port):
    if port not in [1, 2, "m1", "m2", "M1", "M2"]:
        return -1
    if port == "m1" or port == "M1":
        port = 1
    if port == "m2" or port == "M2":
        port = 2 
    ret = starter_shield.dc_motor_get_power(port)
    return ret

def motor_add(power, port):
    if port not in [1, 2, "all", "m1", "m2", "M1", "M2"]:
        return
    if port == "all":
        port = 0
    if port == "m1" or port == "M1":
        port = 1
    if port == "m2" or port == "M2":
        port = 2 
    starter_shield.dc_motor_change_power(port, power)


def motor_drive(power1, power2):
    starter_shield.dc_motor_set_power_both(power1, power2)


def motor_stop(port):
    if port not in [1, 2, "all", "m1", "m2", "M1", "M2"]:
        return
    if port == "all":
        port = 0
    if port == "m1" or port == "M1":
        port = 1
    if port == "m2" or port == "M2":
        port = 2
    starter_shield.dc_motor_stop(port)

#备注：port 的有效值为 "all"/"m1"/"m2"/"M1"/"M2"/1/2   
##############################################################################################################
#########################   DC motor API   ###################################################################
##############################################################################################################



##############################################################################################################
#########################   AC servo API   ###################################################################
##############################################################################################################
def servo_set(angle, port):
    if port not in ["all", "s1", "s2", "s3", "s4", "S1", "S2", "S3", "S4", 1, 2, 3, 4]:
        return
    if port == "all":
        port = 0
    if port == "s1" or port == "S1":
        port = 1
    if port == "s2" or port == "S2":
        port = 2
    if port == "s3" or port == "S3":
        port = 3
    if port == "s4" or port == "S4":
        port = 4         
    starter_shield.servo_set_angle(port, angle)


def servo_get(port):
    if port not in ["s1", "s2", "s3", "s4", "S1", "S2", "S3", "S4", 1, 2, 3, 4]:
        return
    if port == "s1" or port == "S1":
        port = 1
    if port == "s2" or port == "S2":
        port = 2
    if port == "s3" or port == "S3":
        port = 3
    if port == "s4" or port == "S4":
        port = 4   
    ret = starter_shield.servo_get_angle(port)
    return ret

def servo_add(angle, port):
    if port not in ["all", "s1", "s2", "s3", "s4", "S1", "S2", "S3", "S4", 1, 2, 3, 4]:
        return
    if port == "all":
        port = 0
    if port == "s1" or port == "S1":
        port = 1
    if port == "s2" or port == "S2":
        port = 2
    if port == "s3" or port == "S3":
        port = 3
    if port == "s4" or port == "S4":
        port = 4    
    starter_shield.servo_change_angle(port, angle)


def servo_drive(angle1, angle2, angle3, angle4):
    starter_shield.servo_set_angle_all(angle1, angle2, angle3, angle4)


def servo_release(port):
    if port not in ["all", "s1", "s2", "s3", "s4", "S1", "S2", "S3", "S4", 1, 2, 3, 4]:
        return
    if port == "all":
        port = 0
    if port == "s1" or port == "S1":
        port = 1
    if port == "s2" or port == "S2":
        port = 2
    if port == "s3" or port == "S3":
        port = 3
    if port == "s4" or port == "S4":
        port = 4    
    starter_shield.servo_release(port)

#备注：port 的有效值为 "all"/"s1"/"s2"/"S1"/"S2"/1/2
##############################################################################################################
#########################   AC servo API   ###################################################################
##############################################################################################################



##############################################################################################################
#########################   LED strip API  ###################################################################
##############################################################################################################
def led_on(r, g = 0, b = 0, id = "all", port = "all"):
    if id == "all":
        id = 0
    if port not in [1, 2, "all", "s1", "s2", "S1", "S2"]:
        return
    if port == "all":
        port = 0
    if port == "s1" or port == "S1":
        port = 1
    if port == "s2" or port == "S2":
        port = 2

    if isinstance(r, str) and (r in color_table):
        v_r = color_table[r][0] 
        v_g = color_table[r][1] 
        v_b = color_table[r][2]
        starter_shield.led_strip_set_single(port, id, v_r, v_g, v_b)         
    elif isinstance(r, (int, float)) and isinstance(g, (int, float)) and isinstance(b, (int, float)):
        starter_shield.led_strip_set_single(port, id, r, g, b)


def led_show(color, port):
    if port not in [1, 2, "all", "s1", "s2", "S1", "S2"]:
        return
    if port == "all":
        port = 0
    if port == "s1" or port == "S1":
        port = 1
    if port == "s2" or port == "S2":
        port = 2 
    # led_num = len(color)

    MAX_LED_LEN = 36
    if (not isinstance(color, str)):
            return
    color = color.split(' ')
    led_num = len(color)
    if led_num <= 0:
        return
    if led_num > MAX_LED_LEN:
        led_num = MAX_LED_LEN
        color = color[0 : MAX_LED_LEN]

    list_data = [0] * led_num
    for i in range(led_num):
        if color[i] in mbuild_color_table: 
            list_data[i] = mbuild_color_table[color[i]]
        else:
            list_data[i] = 0   # black
    starter_shield.led_strip_set_block(port, led_num, list_data)


def led_move(step, cycle, port):
    if port not in [1, 2, "all", "s1", "s2", "S1", "S2"]:
        return
    if port == "all":
        port = 0
    if port == "s1" or port == "S1":
        port = 1
    if port == "s2" or port == "S2":
        port = 2 
    starter_shield.led_strip_set_move(port, step, cycle)


def led_off(id, port):
    if id == "all":
        id = 0
    if port not in [1, 2, "all", "s1", "s2", "S1", "S2"]:
        return
    if port == "all":
        port = 0
    if port == "s1" or port == "S1":
        port = 1
    if port == "s2" or port == "S2":
        port = 2 
    starter_shield.led_strip_set_single(port, id, 0, 0, 0)


def led_set_bri(brightness, port):
    if port not in [1, 2, "all", "s1", "s2", "S1", "S2"]:
        return
    if port == "all":
        port = 0
    if port == "s1" or port == "S1":
        port = 1
    if port == "s2" or port == "S2":
        port = 2 
    starter_shield.led_strip_set_brightness(port, brightness)


def led_get_bri(port):
    if port not in [1, 2, "s1", "s2", "S1", "S2"]:
        return
    if port == "s1" or port == "S1":
        port = 1
    if port == "s2" or port == "S2":
        port = 2 
    ret = starter_shield.led_strip_get_brightness(port)
    return ret


def led_add_bri(brightness, port):
    if port not in [1, 2, "all", "s1", "s2", "S1", "S2"]:
        return
    if port == "all":
        port = 0
    if port == "s1" or port == "S1":
        port = 1
    if port == "s2" or port == "S2":
        port = 2 
    starter_shield.led_strip_change_brightness(port, brightness)


#备注：port 的有效值为 "all"/"s1"/"s2"/"S1"/"S2"/1/2
##############################################################################################################
#########################   LED strip API  ###################################################################
##############################################################################################################




##############################################################################################################
#########################   power management API  ############################################################
##############################################################################################################
# def digital_write(val, port ):
def write_digital(val, port ):    
    if port not in [1, 2, "all", "s1", "s2", "S1", "S2"]:
        return
    if port == "all":
        port = 0
    if port == "s1" or port == "S1":
        port = 1
    if port == "s2" or port == "S2":
        port = 2 
    starter_shield.multifunction_digital_write(port, val)


# def digital_read(port):
def read_digital(port):
    if port not in [1, 2, "s1", "s2", "S1", "S2"]:
        return
    if port == "s1" or port == "S1":
        port = 1
    if port == "s2" or port == "S2":
        port = 2 
    ret = starter_shield.multifunction_digital_read(port)
    return ret


# def pwm_set(duty, frq, port):
def set_pwm(duty, frq, port):    
    if port not in [1, 2, "all", "s1", "s2", "S1", "S2"]:
        return
    if port == "all":
        port = 0
    if port == "s1" or port == "S1":
        port = 1
    if port == "s2" or port == "S2":
        port = 2 
    starter_shield.multifunction_pwm_set(port, duty, frq)


# def analog_read(port):
def read_analog(port):    
    if port not in [1, 2, "s1", "s2", "S1", "S2"]:
        return
    if port == "s1" or port == "S1":
        port = 1
    if port == "s2" or port == "S2":
        port = 2 
    ret = starter_shield.multifunction_analog_read(port)
    return ret

#备注：port 的有效值为 "all"/"s1"/"s2"/"S1"/"S2"/1/2
##############################################################################################################
#########################   power management API  ############################################################
##############################################################################################################