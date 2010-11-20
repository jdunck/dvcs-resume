import datetime, logging

import git
from github2.client import Github

def _get_client(client):
    if client is None:
        client = Github(requests_per_second=1,debug=True)
    return client
def _get_date(date):
    if date is None:
        date = datetime.datetime.min
    return date 

def find_repos(username, since=None, github=None):
    github = _get_client(github)
    since = _get_date(since)
        
    seen = set()
    def _unseen(repos, since):
        result = []
        for repo in repos:
            if not repo.url in seen:
                if repo.created_at > since: #FIXME: verify created_at is for the watched-at/fork-at time, not original repo creation.
                    repo.new = True
                result.append(repo)
                seen.add(repo.url)
        return result

    owns = _unseen(github.repos.list(username), since)
    forks = []
    for i,repo in enumerate(owns):
        if repo.new and repo.fork:
            if not hasattr(repo, 'parent'):
                repo = github.repos.show(repo.project)
                #FIXME: some forks really don't have a parent marked.  Why is this?!
                if not hasattr(repo, 'parent'):
                    logging.warning("crawl skipping fork w/o parent %s" % (repo.project))
                
                repo.new = True
                owns[i] = repo
            fork = github.repos.show(repo.parent)
            fork.new = True
            forks.append(fork)
    watches = _unseen(github.repos.watching(username), since)
    
    result = {
        'owns':dict((repo.project,repo) for repo in owns),
        'watches':dict((repo.project,repo) for repo in watches),
        'forked_from':dict((repo.project,repo) for repo in forks)
    }
    return result
    