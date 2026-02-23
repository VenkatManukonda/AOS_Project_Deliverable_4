import os
import sys
import getpass
import subprocess

# -------------------------
# User Authentication Setup
# -------------------------
users = {
    "admin": {"password": "admin123", "role": "admin"},
    "user": {"password": "user123", "role": "standard"}
}

# -------------------------
# File Permissions Setup
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
            return users[username]
        else:
            print("Invalid credentials. Try again.\n")
    print("Too many failed attempts. Exiting...")
    sys.exit()


# -------------------------
# Permission Check
# -------------------------
def check_permission(user, filename, action):
    import os
    # Only get the file name itself
    filename = os.path.basename(filename)

    # Check if file exists in our simulated file system
    if filename not in files:
        print(f"File {filename} does not exist.")
        return False

    # Admin can do anything
    if user["role"] == "admin":
        return True

    # Standard user permissions
    perms = files[filename]["permissions"]  # e.g., "r--", "rw-"

    # Map action to index in permissions string
    action_index = {"read": 0, "write": 1, "execute": 2}

    if action in action_index:
        if perms[action_index[action]] == action[0]:  # "r" for read, etc.
            return True
        else:
            print(f"Access denied: {user['role']} cannot {action} {filename}")
            return False

    # Default deny
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
        if len(parts) > 1 and parts[0].lower() in ["type"]:
            filename = parts[1]
            if not check_permission(user, filename, "read"):
                return

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
