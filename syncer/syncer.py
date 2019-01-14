import argparse
import os
import logging
from github import Github
from pathlib import Path
from subprocess import call


logging.basicConfig(filename='sync.log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)
logger = logging.getLogger('sync_logger')


def sync_list(repos):
    logger.info("syncing %d forked repositories" % len(repos))
    for repo in repos:
        try:
            logger.info("cloning into: %s" % repo.name)
        finally:
            call(["rm", "-fr", repo.name])


def get_repo_list():
    g = Github(os.environ['SYNC_GITHUB_TOKEN'])
    repos = []
    user = g.get_user()
    for repo in user.get_repos():
        if repo.fork and repo.owner.name == user.name:
            repos.append(repo)
    return repos


if __name__ == "__main__":
    print(r'''
    (`-').->          <-. (`-')_           (`-')  _   (`-')
    ( OO)_      .->      \( OO) )_         ( OO).-/<-.(OO )
    (_)--\_) ,--.'  ,-.,--./ ,--/ \-,-----.(,------.,------,)
    /    _ /(`-')'.'  /|   \ |  |  |  .--./ |  .---'|   /`. '
    \_..`--.(OO \    / |  . '|  |)/_) (`-')(|  '--. |  |_.' |
    .-._)   \|  /   /) |  |\    | ||  |OO ) |  .--' |  .   .'
    \       /`-/   /`  |  | \   |(_'  '--'\ |  `---.|  |\  \
    `-----'   `--'    `--'  `--'   `-----' `------'`--' '--'

    Beginning syncing...
    ''')

    config_file = os.path.dirname(os.path.abspath(__file__))
    config = Path(os.path.join(config_file, '.config'))
    repos = []

    if config.is_file():
        logger.info('found configuration file at location... syncing repos from file')
        with open(config) as conf:
            for line in conf:
                repos.append(line.strip())
    else:
        logger.info('no config files found. syncing all remote repos')
        repos = get_repo_list()

    sync_list(repos)
