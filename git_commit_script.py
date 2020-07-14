import os
import subprocess
import sys
import argparse
from datetime import datetime
from datetime import timedelta

commit_one_week = [1,2,3,4,5,6,7]

def set_args():
    parser = argparse.ArgumentParser(
        description="Create a local git repo and make commits to create art in Github's activity graph")
    parser.add_argument("-N", "--name", type=str, required=True,
                        help="Name of remote repo, creates new directory with same in CWD name to hold local repo, default is 'dummy_repo'")
    parser.add_argument("-U", "--username", type=str, required=True, help="GitHub username")
    parser.add_argument("-D", "--startdate", type=datetime.fromisoformat, required=False,
                        default=datetime.today() - timedelta(366),
                        help="first Sunday from date to start commits, default is from first Sunday 1 year ago - format YYYY-MM-DD")
    return parser.parse_args()

def get_first_sunday(date):
    first_sunday = date
    day_index = datetime.weekday(first_sunday)
    while (day_index < 6):
        first_sunday = first_sunday + timedelta(1)
        day_index = datetime.weekday(first_sunday)
    return first_sunday

def main():
    arguments = set_args()
    dir_name = arguments.name

    # Create directory for local repo and move into it
    try:
        os.makedirs(dir_name)
        os.chdir(dir_name)
    except FileExistsError:
        print("File already exists")
        return


    commit_date = get_first_sunday(arguments.startdate)


    # Init the git repo
    subprocess.run(["git", "init"])
    # Create and open README.md, the add it to be versioned
    file = open(os.path.join(os.getcwd(), "README.md"), "a+")
    subprocess.run(["git", "add", "README.md"])


    # Carry out commits
    for commit in commit_one_week:
        for i in range(commit):
            file = open(os.path.join(os.getcwd(), "README.md"), "a+")
            file.write("test + \n")
            subprocess.run(["git", "add", "."])
            subprocess.run(["git", "commit", "-m", "testing commit", '--date', commit_date.strftime('"%Y-%m-%d %H:%M:%S"')])
        commit_date = commit_date + timedelta(1)


    # Push the commits to remote repository
    remote_repo = "https://github.com/" + arguments.username + "/" + arguments.name + ".git"
    subprocess.run(
        ["git", "remote", "add", "origin", "https://github.com/" + arguments.username + "/" + arguments.name + ".git"])
    subprocess.run(["git", "push", "-u", "origin", "master"])


if __name__ == "__main__":
    main()
