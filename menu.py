import nuke
import sys
menu = nuke.menu('Nuke')
menu.addCommand('Tools/Fixer', lambda: fixer_run())


def fixer_run():
    try:
        del sys.modules['fixer']
    except:
        pass
    import fixer
    fixer.run()