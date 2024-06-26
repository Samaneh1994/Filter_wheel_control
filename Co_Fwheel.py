import pyvisa
import time

def send_command(inst, command):
    try:
        print(f"Sending command: {command}")
        inst.write(command)
      
        time.sleep(0.1)  # Adjust delay as necessary, The delay time between consequitve commands
        response = inst.read()
        print(f"Response for '{command}': {response.strip()}")
        return response.strip()
    except pyvisa.errors.VisaIOError as e:
        print(f"VISA I/O error: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

try:
    # Initialize Resource Manager
    rm = pyvisa.ResourceManager()

    # Open serial resource (replace 'ASRL5::INSTR' the digit in ASRL refers to number of port, exp: ASRL5::COM5 )
    inst = rm.open_resource('ASRL5::INSTR')

    # Set communication parameters for the filter wheel, available on the User guide note
    inst.baud_rate = 9600  #  Baud rate 
    inst.data_bits = 8     # data bits
    inst.stop_bits = pyvisa.constants.StopBits.one # stop bit, one here
    inst.parity = pyvisa.constants.Parity.none  # parity
    inst.flow_control = pyvisa.constants.ControlFlow.none # control flow
    inst.timeout = 23   # it can be changed, I used  [1 100] the higher the more time to respnse! so, reduce timeout if the instrument responds quickly

    print("Connection established:)) Sending commands to the instrument...")

    # List of commands to send, here are filter wheel positions. Add more commands as needed!
    commands = [
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
    ]
    # Send each command and print the response
    start_time = time.time()
    for command in commands:
        response = send_command(inst, command)
    end_time = time.time()
    print(f"Total time to send commands: {end_time - start_time:.2f} seconds")

except pyvisa.errors.VisaIOError as e:
    print(f"VISA I/O error: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
finally:
    # Close the instrument connection
    if 'inst' in locals():
        inst.close()
    print("Session closed.")
