import sys
import random

from workflow import Workflow, web


def open_issues():
    return web.get('https://api.github.com/search/issues?q=is:open%20is:issue%20user:kfdm').json()


def main(wf):
    # Save data from `get_web_data` for 30 seconds under
    # the key ``example``
    data = wf.cached_data('github_issues', open_issues, max_age=30)
    for datum in random.sample(data['items'], 4):
        parts = datum['html_url'].split('/')
        title = '{0}/{1} {2}'.format(parts[3], parts[4], datum['title'])
        wf.add_item(title, datum['body'], arg=datum['html_url'], valid=True)
    wf.send_feedback()

if __name__ == '__main__':
    wf = Workflow()
    sys.exit(wf.run(main))
