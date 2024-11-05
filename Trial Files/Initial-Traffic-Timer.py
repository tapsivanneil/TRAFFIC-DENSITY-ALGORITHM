import time
import threading

# Initial green and red times for the lanes
lane_1_green_time = 5
lane_2_green_time = 10
lane_3_green_time = 15
lane_4_green_time = 20

# Assuming red times are initially set based on the green times
lane_1_red_time = lane_2_green_time + lane_3_green_time + lane_4_green_time
lane_2_red_time = lane_1_green_time
lane_3_red_time = lane_1_green_time + lane_2_green_time 
lane_4_red_time = lane_1_green_time + lane_2_green_time + lane_3_green_time

def calculate_red_light_timer(lane):
    if lane == 1:
        return lane_2_green_time + lane_3_green_time + lane_4_green_time
    elif lane == 2:
        return lane_1_green_time + lane_3_green_time + lane_4_green_time
    elif lane == 3:
        return lane_1_green_time + lane_2_green_time + lane_4_green_time
    elif lane == 4:
        return lane_1_green_time + lane_2_green_time + lane_3_green_time

def lane_timer(focused_lane):
    global lane_1_green_time, lane_2_green_time, lane_3_green_time, lane_4_green_time
    global lane_1_red_time, lane_2_red_time, lane_3_red_time, lane_4_red_time

    while True:
        time.sleep(1)  # Simulate the passing of time

        if focused_lane == 1:
            if lane_1_green_time > 0:
                lane_1_green_time -= 1
                lane_2_red_time -= 1
                lane_3_red_time -= 1
                lane_4_red_time -= 1
            else:
                focused_lane = 2
                lane_1_green_time = 5
                lane_1_red_time = calculate_red_light_timer(1)

        elif focused_lane == 2:
            if lane_2_green_time > 0:
                lane_2_green_time -= 1
                lane_1_red_time -= 1
                lane_3_red_time -= 1
                lane_4_red_time -= 1
            else:
                focused_lane = 3
                lane_2_green_time = 10
                lane_2_red_time = calculate_red_light_timer(2)


        elif focused_lane == 3:
            if lane_3_green_time > 0:
                lane_3_green_time -= 1
                lane_2_red_time -= 1
                lane_1_red_time -= 1
                lane_4_red_time -= 1
            else:
                focused_lane = 4
                lane_3_green_time = 15
                lane_3_red_time = calculate_red_light_timer(3)

        elif focused_lane == 4:
            if lane_4_green_time > 0:
                lane_4_green_time -= 1
                lane_1_red_time -= 1
                lane_2_red_time -= 1
                lane_3_red_time -= 1
            else:
                focused_lane = 1
                lane_4_green_time = 20
                lane_4_red_time = calculate_red_light_timer(4)


        output = (f"LANE 1: {'GREEN' if focused_lane == 1 else 'RED'} {lane_1_green_time if focused_lane == 1 else lane_1_red_time} | "
                f"LANE 2: {'GREEN' if focused_lane == 2 else 'RED'} {lane_2_green_time if focused_lane == 2 else lane_2_red_time} | "
                f"LANE 3: {'GREEN' if focused_lane == 3 else 'RED'} {lane_3_green_time if focused_lane == 3 else lane_3_red_time} | "
                f"LANE 4: {'GREEN' if focused_lane == 4 else 'RED'} {lane_4_green_time if focused_lane == 4 else lane_4_red_time}")
        
        print(f"{output}")


# Example usage: Start a timer for lane 1\

thread1 = threading.Thread(target=lane_timer, args=(1,))
thread1.start()
