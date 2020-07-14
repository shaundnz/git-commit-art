import os
import subprocess
import argparse
from datetime import datetime
from datetime import timedelta

commit_one_week = [1,2,3,4,5,6,7]
COMMIT_MULTIPLIER = 4

SPACE_INVADER = [ [0, 0, 0, 1, 1, 1, 0],  # 0
                  [0, 0, 1, 1, 0, 0, 0],  # 1
                  [0, 1, 1, 1, 1, 1, 0],  # 2
                  [1, 1, 0, 1, 1, 0, 1],  # 3
                  [0, 1, 1, 1, 1, 0, 1],  # 4
                  [0, 1, 1, 1, 1, 0, 0],  # 5
                  [0, 1, 1, 1, 1, 0, 1],  # 6
                  [1, 1, 0, 1, 1, 0, 1],  # 7
                  [0, 1, 1, 1, 1, 1, 0],  # 8
                  [0, 0, 1, 1, 0, 0, 0],  # 9
                  [0, 0, 0, 1, 1, 1, 0] ] # 10


def set_args():
    parser = argparse.ArgumentParser(
        description="Create a local git repo and make commits to create art in Github's activity graph")
    # Repo name
    parser.add_argument("-N", "--name", type=str, required=True,
                        help="Name of remote repo, creates new directory with same in CWD name to hold local repo, default is 'dummy_repo'")
    # GitHub username
    parser.add_argument("-U", "--username", type=str, required=True, help="GitHub username")
    # Start date for image
    parser.add_argument("-D", "--startdate", type=datetime.fromisoformat, required=False,
                        default=datetime.today() - timedelta(366),
                        help="first Sunday from date to start commits, default is from first Sunday 1 year ago - format YYYY-MM-DD")
    return parser.parse_args()

# Top left corner of any image created
def get_first_sunday(date):
    first_sunday = date
    day_index = datetime.weekday(first_sunday)
    while (day_index < 6):
        first_sunday = first_sunday + timedelta(1)
        day_index = datetime.weekday(first_sunday)
    return first_sunday

# Edit the README then commit the changes
def change_and_commit(commit_date):
    file = open(os.path.join(os.getcwd(), "README.md"), "a+")
    file.write("making art + \n\n")
    subprocess.run(["git", "add", "."], stdout=subprocess.DEVNULL)
    subprocess.run(["git", "commit", "-m", "testing commit", '--date', commit_date.strftime('"%Y-%m-%d %H:%M:%S"')], stdout=subprocess.DEVNULL)

def main():
    arguments = set_args()

    # Create directory for local repo and move into it
    dir_name = arguments.name
    try:
        os.makedirs(dir_name)
        os.chdir(dir_name)
    except FileExistsError:
        print("File already exists")
        return

    # Starting date for all commits
    commit_date = get_first_sunday(arguments.startdate)

    # Init the git repo
    subprocess.run(["git", "init"])

    # Carry out specified number of commits per day
    image = SPACE_INVADER
    for week in image:
        for day in week:
            for i in range(day * COMMIT_MULTIPLIER):
                change_and_commit(commit_date)
            commit_date = commit_date + timedelta(1)

    # Push the commits to remote repository
    subprocess.run(
        ["git", "remote", "add", "origin", "https://github.com/" + arguments.username + "/" + arguments.name + ".git"])
    subprocess.run(["git", "push", "-u", "origin", "master"])


if __name__ == "__main__":
    main()
