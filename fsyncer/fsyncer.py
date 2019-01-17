import os
import logging
from github import Github, Repository
from pathlib import Path
from subprocess import run, CalledProcessError
from typing import List


logging.basicConfig(filename='fsync.log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)
logger = logging.getLogger('fsync_logger')


def sync_list(repos: List[Repository.Repository]):
    logger.info("syncing %d forked repositories" % len(repos))
    for repo in repos:  # type: Repository.Repository
        try:
            logger.info("cloning into: %s" % repo.name)
            run(["git", "clone", repo.ssh_url, repo.name])
            # setup upstream for updating
            logger.info("setup upstream to {repo.parent.ssh_url}")
            run(["cd {repo.name} && git remote add upstream {repo.parent.ssh_url}"])
            # do the update
            logger.info("doing the update with push")
            run(["cd {repo.name} && git fetch upstream && git rebase upstream/master && git push origin"])
            logger.info("successfully updated {repo.name}")
        except CalledProcessError:
            logger.info("failed updating {repo.name}")
        finally:
            run(["rm", "-fr", repo])


def get_repo_list():
    g = Github(os.environ['SYNC_GITHUB_TOKEN'])
    repos = []
    user = g.get_user()
    for repo in user.get_repos():
        if repo.fork and repo.owner.name == user.name:
            repos.append(repo)
    return repos


def main():
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
    only = []
    if config.is_file():
        logger.info('found configuration file... syncing repos from file')
        with open(config) as conf:
            for line in conf:
                only.append(line.strip())

    logger.info('retrieving forks for user')
    repos = get_repo_list()
    if len(only) > 0:
        repos = list(filter(lambda r: r.name in only, repos))

    sync_list(repos)
