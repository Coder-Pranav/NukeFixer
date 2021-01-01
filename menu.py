import fixer
import nuke

toolbar = nuke.menu('Nodes')
c = toolbar.addMenu('PP Tools', 'pptool.png')
c.addCommand('Fixer', lambda: fixer.run(),icon='pptool.png')
