import sys
import random

from workflow import Workflow, web


def open_issues():
    return web.get('https://api.github.com/search/issues?q=is:open%20is:issue%20user:kfdm&per_page=100').json()


def main(wf):
    # Cache our list of issues since it's unlikely to change much during the
    # time when we're calling this script
    data = wf.cached_data('github_issues', open_issues, max_age=600)
    for datum in random.sample(data['items'], 4):
        parts = datum['html_url'].split('/')
        title = '{0}/{1} {2}'.format(parts[3], parts[4], datum['title'])
        wf.add_item(title, datum['body'], arg=datum['html_url'], valid=True)
    wf.send_feedback()

if __name__ == '__main__':
    wf = Workflow()
    sys.exit(wf.run(main))
