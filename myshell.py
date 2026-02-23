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
# Simulated files with permissions: format -> {filename: {"owner": role, "permissions": "rwx"}}
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
    if filename not in files:
        print(f"File {filename} does not exist.")
        return False
    perms = files[filename]["permissions"]
    role = user["role"]
    if role == "admin":
        return True  # admin has all access
    if action == "read" and perms[0] == "r":
        return True
    if action == "write" and perms[1] == "w":
        return True
    if action == "execute" and perms[2] == "x":
        return True
    print(f"Access denied: {role} cannot {action} {filename}")
    return False

# -------------------------
# Execute Commands with Piping
# -------------------------
def execute_command(command, user):
    # Split multiple commands by pipe
    commands = [cmd.strip() for cmd in command.split('|')]
    num_cmds = len(commands)
    processes = []

    for i, cmd in enumerate(commands):
        args = cmd.split()
        
        # File permission enforcement for certain commands
        if args[0] in ["cat", "nano", "rm"] and len(args) > 1:
            if not check_permission(user, args[1], "read" if args[0]=="cat" else "write"):
                return

        # Setup stdin/stdout for pipes
        if i == 0:
            # First command: stdin is default
            p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            # Middle or last command: stdin comes from previous process
            p = subprocess.Popen(args, stdin=processes[-1].stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        processes.append(p)

    # Close all previous pipes in parent
    for p in processes[:-1]:
        p.stdout.close()

    # Get output and errors from last process
    out, err = processes[-1].communicate()
    if out:
        print(out.decode())
    if err:
        print(err.decode())

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
