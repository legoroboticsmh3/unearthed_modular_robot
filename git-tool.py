#!/usr/bin/env python3
import subprocess
import datetime
import sys

# ANSI escape codes for color
RED = "\033[91m"
RESET = "\033[0m"

def run_git(args, capture=False, quiet=False):
    """Run a git command safely with error handling."""
    try:
        if capture:
            result = subprocess.run(["git"] + args, capture_output=True, text=True, check=True)
            return result.stdout.strip()
        else:
            subprocess.run(["git"] + args, check=True)
            return True
    except subprocess.CalledProcessError as e:
        if not quiet:
            print(f"{RED}⚠️  Git command failed: {' '.join(args)}{RESET}")
            if e.stderr:
                print(f"{RED}{e.stderr.strip()}{RESET}")
        return None

def check_git_repo():
    """Ensure we are inside a git repository."""
    if run_git(["rev-parse", "--is-inside-work-tree"], capture=True) != "true":
        print(f"{RED}Error: Not a git repository. Please run inside a git repo.{RESET}")
        input("Press Enter to exit...")
        sys.exit(1)

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
    result = run_git(["status", "--porcelain"], capture=True)
    if not result:
        return []
    return [line for line in result.splitlines() if line.strip()]

def safe_stash_and_pull():
    """Safely stash local changes, pull, then reapply stash."""
    print("\n🔒 Stashing local changes...")
    stash_result = run_git(["stash", "push", "-m", "auto-precommit-stash"], quiet=True)
    if stash_result is None:
        print(f"{RED}Failed to stash local changes.{RESET}")
        input("Press Enter to continue...")
        return False

    print("⬇️  Pulling latest from remote...")
    pull_result = run_git(["pull"])
    if pull_result is None:
        print(f"{RED}Failed to pull from remote. Please resolve network or merge issues.{RESET}")
        input("Press Enter to continue...")
        return False

    print("🔄 Reapplying stashed changes...")
    stash_list = run_git(["stash", "list"], capture=True, quiet=True)
    if stash_list and "auto-precommit-stash" in stash_list:
        pop_result = run_git(["stash", "pop"])
        if pop_result is None:
            print(f"{RED}Warning: Conflicts may have occurred when applying stashed changes.{RESET}")
    return True

def commit_changes():
    # Step 0: ensure we are inside a git repo
    check_git_repo()

    # Step 1: stash and pull first
    if not safe_stash_and_pull():
        return

    # Step 2: check for new/changed files after stash pop
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
        if run_git(["add", file]) is None:
            print(f"{RED}Failed to add {file}. Skipping.{RESET}")

    datetime_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    commit_msg = f"[{datetime_str}] {name} - {msg}"

    print(f"\n📝 Committing with message: {commit_msg}")
    if run_git(["commit", "-m", commit_msg]) is None:
        print(f"{RED}Commit failed. Possibly nothing to commit or conflict.{RESET}")
        input("Press Enter to continue...")
        return

    print("\n🚀 Pushing changes...")
    if run_git(["push"]) is None:
        print(f"{RED}Push failed. Please check remote or network issues.{RESET}")
    else:
        print("✅ Commit and push complete!")
    input("Press Enter to continue...")

def git_pull():
    check_git_repo()
    print("\n⬇️  Pulling latest changes from remote...")
    if run_git(["pull"]) is None:
        print(f"{RED}Pull failed. Please check remote or network issues.{RESET}")
    else:
        print("✅ Pull complete!")
    input("Press Enter to continue...")

def show_log():
    check_git_repo()
    print("\nLast 25 commits:")
    if run_git(["log", "-25", "--oneline"]) is None:
        print(f"{RED}Failed to fetch commit log.{RESET}")
    input("Press Enter to continue...")

# --- Main loop ---
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
        sys.exit(0)
    else:
        print(f"{RED}Invalid choice. Try again.{RESET}")
        input("Press Enter to continue...")