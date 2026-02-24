## Repository Contents

- myshell.py – Main Python shell program
- files/user_data.txt – Sample file accessible by standard users
- files/system_file.txt – Admin-only protected file

## How to Run

1. Ensure Python 3.x is installed
2. Open a terminal or PowerShell and navigate to the repository folder:
   cd path\to\Deliverable_4_Shell
3. Launch the shell:
   python myshell.py
4. Log in using one of the available users:
   Username: admin
   Password: [password]

   Username: user
   Password: [password]

## Example Commands

Read a file:
admin@shell> type files\user_data.txt

Pipe commands:
admin@shell> type files\user_data.txt | sort
admin@shell> type files\user_data.txt | sort | findstr Error

Attempt access as a standard user:
standard@shell> type files\system_file.txt
Access denied: standard cannot read system_file.txt

