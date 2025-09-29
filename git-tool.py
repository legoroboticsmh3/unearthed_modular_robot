#!/usr/bin/env python3
import subprocess
import datetime
import os

def show_menu():
    print("\n==============================")
    print("      Git Helper Script")
    print("==============================")
    print("1) Commit changes")
    print("2) Pull latest changes from remote")
    print("3) Show last 25 commits (one line)")
    print("4) Exit")
    print("==============================")

def get_git_changes():
    result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
    return [line for line in result.stdout.splitlines() if line.strip()]

def commit_changes():
    changes = get_git_changes()
    if not changes:
        print("No changes to commit.")
        input("Press Enter to continue...")
        return

    print("\nModified/added files:")
    for line in changes:
        print(line)
    
    name = input("\nEnter your name: ").strip()
    msg = input("Enter a short message: ").strip()
    
    files_to_add = []
    for line in changes:
        parts = line.split(maxsplit=1)
        if len(parts) < 2:
            continue
        file = parts[1]
        include = input(f"Include {file} in commit? (Y/N): ").strip().lower()
        if include == 'y':
            files_to_add.append(file)
    
    if not files_to_add:
        print("No files selected. Nothing to commit.")
        input("Press Enter to continue...")
        return
    
    for file in files_to_add:
        subprocess.run(["git", "add", file])

    datetime_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    commit_msg = f"[{datetime_str}] {name} - {msg}"
    print(f"\nCommitting with message: {commit_msg}")
    subprocess.run(["git", "commit", "-m", commit_msg])
    print("Pushing changes...")
    subprocess.run(["git", "push"])
    print("Commit complete!")
    input("Press Enter to continue...")

def git_pull():
    print("\nPulling latest changes from remote...")
    subprocess.run(["git", "rebase"])
    subprocess.run(["git", "pull"])
    print("Pull complete!")
    input("Press Enter to continue...")

def show_log():
    print("\nLast 25 commits:")
    subprocess.run(["git", "log", "-25", "--oneline"])
    input("Press Enter to continue...")

# Main loop
while True:
    show_menu()
    choice = input("Choose an option: ").strip()
    if choice == '1':
        commit_changes()
    elif choice == '2':
        git_pull()
    elif choice == '3':
        show_log()
    elif choice == '4':
        print("Exiting...")
        break
    else:
        print("Invalid choice. Try again.")
        input("Press Enter to continue...")

