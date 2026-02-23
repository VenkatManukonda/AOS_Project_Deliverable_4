import os
import sys
import getpass
import subprocess

# -------------------------
# Users & Roles
# -------------------------
users = {
    "admin": {"password": "admin123", "role": "admin"},
    "user": {"password": "user123", "role": "standard"}
}

# -------------------------
# Files & Permissions
# -------------------------
files = {
    "system_file.txt": {"owner": "admin", "permissions": "r--"},
    "user_data.txt": {"owner": "user", "permissions": "rw-"}
}

# -------------------------
# Authenticate User
# -------------------------
def authenticate():
    print("=== Welcome to Integrated Shell ===")
    for attempt in range(3):
        username = input("Username: ")
        password = getpass.getpass("Password: ")
        if username in users and users[username]["password"] == password:
            print(f"Login successful. Role: {users[username]['role']}\n")
            # Return both username and role
            return {"username": username, "role": users[username]["role"]}
        else:
            print("Invalid credentials. Try again.\n")
    print("Too many failed attempts. Exiting...")
    sys.exit()

# -------------------------
# Permission Check
# -------------------------
def check_permission(user, filename, action):
    filename = os.path.basename(filename)

    if filename not in files:
        print(f"File {filename} does not exist.")
        return False

    file_info = files[filename]

    # Admin can do anything
    if user["role"] == "admin":
        return True

    # Standard user: check ownership by username
    if file_info["owner"] != user["username"]:
        print(f"Access denied: {user['role']} cannot {action} {filename}")
        return False

    # Check permissions string
    perms = file_info["permissions"]  # e.g., "r--", "rw-"
    if action == "read" and perms[0] == "r":
        return True
    if action == "write" and perms[1] == "w":
        return True
    if action == "execute" and perms[2] == "x":
        return True

    print(f"Access denied: {user['role']} cannot {action} {filename}")
    return False

# -------------------------
# Execute Commands with Piping
# -------------------------
def execute_command(command, user):
    commands = [cmd.strip() for cmd in command.split('|')]
    processes = []

    for i, cmd in enumerate(commands):
        parts = cmd.split()

        # Enforce read permissions for file commands
        if len(parts) > 1 and parts[0].lower() in ["type"]:
            filename = parts[1]
            if not check_permission(user, filename, "read"):
                return

        # Run command via cmd /c to support Windows/Powershell
        p = subprocess.Popen(
            ["cmd", "/c", cmd],
            stdin=processes[-1].stdout if i > 0 else None,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        processes.append(p)

    for p in processes[:-1]:
        p.stdout.close()

    output, error = processes[-1].communicate()

    if output:
        print(output.decode())
    if error:
        print(error.decode())

# -------------------------
# Main Shell Loop
# -------------------------
def shell():
    user = authenticate()

    while True:
        try:
            command = input(f"{user['role']}@shell> ")

            if command.lower() in ["exit", "quit"]:
                print("Exiting shell. Goodbye!")
                break

            execute_command(command, user)

        except KeyboardInterrupt:
            print("\nSession interrupted. Use 'exit' to quit.")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    shell()
