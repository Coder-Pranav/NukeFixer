import fixer
import nuke
import sys

toolbar = nuke.menu('Nodes')
c = toolbar.addMenu('PP Tools', 'pptool.png')
c.addCommand('Fixer', lambda: fixer_run(),icon='pptool.png')


def fixer_run():
    try:
        del sys.modules['fixer']
    except:
        pass
    import fixer
    fixer.run()