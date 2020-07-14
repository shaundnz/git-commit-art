import os
import subprocess
import sys
import argparse
import datetime

def set_args():
    parser = argparse.ArgumentParser(
        description="Create a local git repo and make commits to create art in Github's activity graph")
    parser.add_argument("-N", "--name", type=str, required=True,
                        help="Name of remote repo, creates new directory with same in CWD name to hold local repo, default is 'dummy_repo'")
    parser.add_argument("-U", "--username", type=str, required=True, help="GitHub username")
    parser.add_argument("-D", "--startdate", type=datetime.datetime.fromisoformat, required=False, help="date to start commits, default is from Sunday 1 year ago")
    return parser.parse_args()



















def main():
    arguments = set_args()
    dir_name = arguments.name

    # Create directory for local repo and move into it
    try:
        os.makedirs(dir_name)
        os.chdir(dir_name)
    except FileExistsError:
        return

    # Init the git repo
    subprocess.run(["git", "init"])
    # Create and open README.md, the add it to be versioned
    file = open(os.path.join(os.getcwd(), "README.md"), "a+")
    subprocess.run(["git", "add", "README.md"])

    # Carry out commits
    file.write("commit1")
    subprocess.run(["git", "commit", "-m", "testing commit"])

    # Ask for username and password
    # subprocess.run(["git", "config", "--local credential.helper"])

    # Push the commits to remote repository
    remote_repo = "https://github.com/" + arguments.username + "/" + arguments.name + ".git"
    subprocess.run(["git", "remote", "add", "origin", "git@github.com:" + arguments.username + "/" + arguments.name + ".git"])
    subprocess.run(["git", "push", "-u", "origin", "master"])


if __name__ == "__main__":
    main()
