from displaytools import *

f = Font('ledFont')
d = Display('10.23.5.143')

Flicker(d, 3).show(True)
StaticRow(d, f, '--Fien en Jesse--').show(1)
effect = ScrollText(d, f, 'De kat krabt de krollen van de trap', sleeptime = 0.05)
effect.show(visual = True)

