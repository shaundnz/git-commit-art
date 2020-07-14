import os
import subprocess
import sys
import argparse

def set_args():
    parser = argparse.ArgumentParser(
        description="Create a new git repo and make commits to create art in Github's activity graph")
    parser.add_argument("-N", "--name", type=str, required=False, default="dummy_repo",
                        help="Name of new repo, creates new directory with same in CWD name to hold local repo")
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

    # Create and open README.md, the add it
    file = open(os.path.join(os.getcwd(), "README.md"), "a+")
    subprocess.run(["git", "add", "README.md"])





if __name__ == "__main__":
    main()
