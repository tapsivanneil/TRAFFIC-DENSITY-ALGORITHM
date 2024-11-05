import serial
import time

# Configure the serial connection
port = 'COM6'  # Replace with your port if different
baudrate = 9600  # Standard baud rate for HC-06
timeout = 1

# Initialize the serial connection
try:
    ser = serial.Serial(port, baudrate, timeout=timeout)
    time.sleep(2)  # Wait for the connection to be established
    print("Connected to HC-06")
except serial.SerialException as e:
    print(f"Error connecting to Bluetooth module: {e}")
    exit()

try:
    while True:
        # Accept user input
        user_input = input("Enter 0 or 1 (or 'exit' to quit): ").strip()
        
        if user_input.lower() == 'exit':
            print("Exiting...")
            break
        
        if user_input in ['0', '1']:
            ser.write(user_input.encode())  # Send the input to the HC-06
            print(f"Sent: {user_input}")
        else:
            ser.write(user_input.encode())  # Send the input to the HC-06
            print(f"Sent: {user_input}")

except KeyboardInterrupt:
    print("\nInterrupted by user.")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    ser.close()  # Close the serial connection
    print("Serial connection closed.")