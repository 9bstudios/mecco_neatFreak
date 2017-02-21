#python

import lx, lxu, modo, traceback

NAME_CMD = "neatFreak.cleanupShaderTree"

# Returns a list of all mesh layers containing any of the provided pTag(s)
# of type i_POLYTAG, e.g. lx.symbol.i_POLYTAG_MATERIAL.
# pTag can be a tag or list of tags.
def get_layers_by_pTag(pTags,i_POLYTAG=lx.symbol.i_POLYTAG_MATERIAL):
    """Returns a list of all mesh layers containing any of the provided pTag(s)
    of type i_POLYTAG, e.g. lx.symbol.i_POLYTAG_MATERIAL.
    """
    
    # If signle value is passed put into list
    if not isinstance(pTags,list):
        pTags = [pTags]

    scene = modo.Scene()

    mm = set()
    # Collect result meshes in mm
    for m in scene.meshes:
        # For each polygon tag
        for i in range(m.geometry.internalMesh.PTagCount(i_POLYTAG)):
            tag = m.geometry.internalMesh.PTagByIndex(i_POLYTAG,i)
            # If need to be found in i_POLYTAG_PIC (polygon belongs to each selection set in tag)
            if i_POLYTAG == lx.symbol.i_POLYTAG_PICK:
                # Add mesh if one of selection sets present in pTags
                if [i for i in tag.split(";") if i in pTags]:
                    mm.add(m)
            else:
                # Add mesh if tag exists in pTags
                if tag in pTags:
                    mm.add(m)

    return list(mm)

# Returns an lx.symbol.i_POLYTAG_* symbol based on a mask
# item's lx.symbol.sICHAN_MASK_PTYP channel string.
def get_i_POLYTAG(sICHAN_MASK_PTYP):
    """Returns an lx.symbol.i_POLYTAG_* symbol based on a mask
    item's lx.symbol.sICHAN_MASK_PTYP channel string."""

    # Return polygon tag type corresponding to channel string
    return {
        '':lx.symbol.i_POLYTAG_MATERIAL,
        'Material':lx.symbol.i_POLYTAG_MATERIAL,
        'Selection Set':lx.symbol.i_POLYTAG_PICK,
        'Part':lx.symbol.i_POLYTAG_PART
    }[sICHAN_MASK_PTYP]


# Returns all items in the scene of type itype.
def get_items_by_type(itype):
    """Returns all items in the scene of type itype."""

    scene_service = lx.service.Scene()
    current_scene = lxu.select.SceneSelection().current()

    items = []
    # lookup the item type
    item_type = scene_service.ItemTypeLookup(itype)
    # get a count of itype items in the scene
    numitems = current_scene.ItemCount(item_type)
    for x in range(numitems):
        items.append(current_scene.ItemByIndex(item_type, x))
    return items


# Standard command implementation
class CMD_neatFreak(lxu.command.BasicCommand):

    _first_run = True

    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

        self.dyna_Add("emptyGroups", lx.symbol.sTYPE_BOOLEAN)
        self.dyna_Add("unusedGroups", lx.symbol.sTYPE_BOOLEAN)
        self.dyna_Add("unusedIClips", lx.symbol.sTYPE_BOOLEAN)
        self.dyna_Add("unusedTLocs", lx.symbol.sTYPE_BOOLEAN)

    def cmd_Flags(self):
        return lx.symbol.fCMD_POSTCMD | lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def arg_UIHints(self, index, hints):
        if index == 0:
            hints.Label("Delete empty groups")
        if index == 1:
            hints.Label("Delete unused groups")
        if index == 2:
            hints.Label("Delete unused image clips")
        if index == 3:
            hints.Label("Delete unused texture locators")

    def cmd_DialogInit(self):
        if self._first_run:
            # At first run check all checkboxes
            self.attr_SetInt(0, 1)
            self.attr_SetInt(1, 1)
            self.attr_SetInt(2, 1)
            self.attr_SetInt(3, 1)
            self.after_first_run()

    @classmethod
    def after_first_run(cls):
        cls._first_run = False

    def basic_Execute(self, msg, flags):
        try:
            scene = modo.scene.current()

            hitlist = set()
            for m in scene.iterItems(lx.symbol.sITYPE_MASK):
                del_empty = self.dyna_Bool(0)
                del_unused = self.dyna_Bool(1)

                # delete empty groups
                if not m.children() and del_empty:
                    hitlist.add(m)

                if del_unused:
                    # type of poly tag (material, selection set, etc)
                    i_POLYTAG = get_i_POLYTAG(m.channel(lx.symbol.sICHAN_MASK_PTYP).get())

                    # poly tag ("myGreatMaterialTag")
                    sICHAN_MASK_PTAG = m.channel(lx.symbol.sICHAN_MASK_PTAG).get()

                    # delete obsolete (unused) polytag groups
                    if (sICHAN_MASK_PTAG and not get_layers_by_pTag(sICHAN_MASK_PTAG,i_POLYTAG)):
                        hitlist.add(m)

            # Loop through all image clips
            for imageClip in scene.items( itype=lx.symbol.sITYPE_VIDEOSTILL ):
                del_unused_image_clips = self.dyna_Bool(2)
            
                # delete unused image clips
                if del_unused_image_clips:
            
                   # We will get the 'shadeLoc' graph and check if there are any connections.
                   graph = imageClip.itemGraph('shadeLoc')
            
                   # If no connections are found for this graph, we delete the clip item from the scene.
                   if len(graph.forward()) is 0 and len(graph.reverse()) is 0:
            
                      lx.out("Deleting clip: %s" % imageClip.name)
                      hitlist.add(imageClip)
            
            # delete unused texture locators
            del_unused_texture_locators = self.dyna_Bool(3)
            if del_unused_texture_locators:
            
                shadeloc_graph = lx.object.ItemGraph(scene.GraphLookup(lx.symbol.sGRAPH_SHADELOC))
            
                texlocs = get_items_by_type(lx.symbol.sITYPE_TEXTURELOC)
                if texlocs:
                    for texloc in texlocs:
                        if (shadeloc_graph.FwdCount(texloc) == 0) and (shadeloc_graph.RevCount(texloc) == 0):
 		   
                            lx.out("Deleting texture locator: %s" % texloc.Ident().name)
                            hitlist.add(texloc.Ident())

            for hit in hitlist:
                # TD SDK removeItems() method crashes on some groups. This is more robust.
                lx.eval("item.delete item:{%s}" % hit.id)

        except:
            traceback.print_exc()

lx.bless(CMD_neatFreak, NAME_CMD)
