#python

import lx, lxu, modo, traceback

NAME_CMD = 'neatFreak.alphabetizeChildren'

class CMD_neatFreak(lxu.command.BasicCommand):

    _first_run = True

    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

    def basic_Execute(self, msg, flags):
        try:
            items = list()

            for item in lxu.select.ItemSelection().current():
                items.append(item)
	
            for parent in items:
                children = list()
                for idx in xrange(parent.SubCount()):
                    children.append(parent.SubByIndex(idx))
                children.sort(key = lambda s : s.Name())
		
                for idx in xrange(len(children)):
                    lx.eval("item.parent %(name)s %(parent)s %(index)d" % {"name" : children[idx].Name(), "parent" : parent.Name(), "index" : idx})

        except:
            traceback.print_exc()

lx.bless(CMD_neatFreak, NAME_CMD)
