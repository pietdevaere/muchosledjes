from displaytools import *
from sockettools import *

social = PriorityReceiver()
f = Font('ledFont')
d = Display('10.23.5.143')

changed = True

while True:
    social.update()
    if changed and not social:
        StaticRow(d, f, 'wensen@devae.re').load(0)
        StaticRow(d, f, '#EmiEnEpi').show(1)
        changed = False
    if social:
        changed = True
        message, priority = social.pop()
        print(message)
        ScrollText(d, f, message, sleeptime = 0.05).show()  

Flicker(d, 3).show(True)
StaticRow(d, f, '--Fien en Jesse--').show(1)
effect = ScrollText(d, f, 'De kat krabt de krollen van de trap', sleeptime = 0.05)
effect.show(visual = True)
