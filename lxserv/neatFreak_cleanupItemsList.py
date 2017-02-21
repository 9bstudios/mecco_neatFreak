#python

import lx, lxu, modo, traceback

NAME_CMD = 'neatFreak.cleanupItemsList'

# Standard command implementation
class CMD_neatFreak(lxu.command.BasicCommand):

    _first_run = True

    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

        self.dyna_Add("emptyMeshes", lx.symbol.sTYPE_BOOLEAN)
        self.dyna_Add("emptyGroups", lx.symbol.sTYPE_BOOLEAN)
        self.dyna_Add("unusedTLocs", lx.symbol.sTYPE_BOOLEAN)

    def cmd_Flags(self):
        return lx.symbol.fCMD_POSTCMD | lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_DialogInit(self):
        if self._first_run:
            # At first run check all checkboxes
            self.attr_SetInt(0, 1)
            self.attr_SetInt(1, 1)
            self.attr_SetInt(2, 1)
            self.after_first_run()

    @classmethod
    def after_first_run(cls):
        cls._first_run = False

    def basic_Execute(self, msg, flags):
        try:
            del_empty_meshes = self.dyna_Bool(0)
            del_empty_groups = self.dyna_Bool(1)
            del_unused_tlocs = self.dyna_Bool(2)

            hitlist = set()

            # Collect empty meshes if selected
            if del_empty_meshes:
                for i in modo.Scene().locators:
                        # Append locator if type is 'mesh' and it doesn't contain any polygons
                	if i.type == 'mesh' and not i.geometry.numPolygons:
                		hitlist.add(i)

            # Collect empty groups if selected
            if del_empty_groups:
                for i in modo.Scene().locators:
                        # Append locator if type is 'groupLocator' and it doesn't contain any child
                	if i.type == 'groupLocator' and not i.children():
                		hitlist.add(i)

            # Collect unused texture locators if selected
            if del_unused_tlocs:
                for i in modo.Scene().locators:
                    # Append texture locator if sharedLoc graph is empty
                    if i.type == 'txtrLocator' and len(i.itemGraph('shadeLoc').reverse()) == 0:
                        hitlist.add(i)

            # Delete collected locators
            for hit in hitlist:
                # TD SDK removeItems() method crashes on some groups. This is more robust.
                lx.eval("item.delete item:{%s}" % hit.id)

        except:
            traceback.print_exc()


lx.bless(CMD_neatFreak, NAME_CMD)
