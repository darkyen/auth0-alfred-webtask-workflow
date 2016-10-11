import sys
sys.path.append('./libs')

from workflow import Workflow, ICON_WEB, web

def main(wf):
    wf.delete_password('twitter-alfred')
    return

if __name__ == u"__main__":
     wf = Workflow()
     sys.exit(wf.run(main))
