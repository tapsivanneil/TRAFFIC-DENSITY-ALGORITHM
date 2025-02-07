import time
import serial

def change_light_pattern():

    port = 'COM3'  # Replace with your port if different
    baudrate = 9600  # Standard baud rate for HC-06
    timeout = 1


    ser = serial.Serial(port, baudrate, timeout=timeout)

    try:
       for light_pattern in range(1, 13):  # Loop from 1 to 12
        time.sleep(2)  # 1-second interval between sending patterns
        ser.write(str(light_pattern).encode())  # Send the light pattern to the Arduino
        print(f"Sent light pattern: {light_pattern}")  # Optional: Print to confirm it's sent

    except KeyboardInterrupt:
        print("\nInterrupted by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # ser.close()  # Close the serial connection
        print("Serial connection closed.")


change_light_pattern()