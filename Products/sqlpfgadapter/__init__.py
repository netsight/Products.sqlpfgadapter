from Products.CMFCore.DirectoryView import registerDirectory
from Products.CMFCore import utils
from Products.Archetypes.public import process_types, listTypes
from Products.PloneFormGen.config import ADD_CONTENT_PERMISSION
from Products.sqlpfgadapter.config import SKINS_DIR, GLOBALS, PROJECTNAME

registerDirectory(SKINS_DIR, GLOBALS)

def initialize(context):
    """Initializer called when used as a Zope 2 product."""

    # add content type, taken from Products.PloneFormGen
    import content
    listOfTypes = listTypes(PROJECTNAME)
    content_types, constructors, ftis = process_types(
        listOfTypes,
        PROJECTNAME)
    allTypes = zip(content_types, constructors)
    for atype, constructor in allTypes:
        kind = "%s: %s" % (PROJECTNAME, atype.archetype_name)
        permission = ADD_CONTENT_PERMISSION
        utils.ContentInit(
            kind,
            content_types      = (atype,),
            permission         = permission,
            extra_constructors = (constructor,),
            fti                = ftis,
            ).initialize(context)

