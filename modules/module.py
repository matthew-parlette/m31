class ModuleMount(type):
    def __init__(cls, name, bases, attrs):
        if not hasattr(cls, 'modules'):
            # This branch only executes when processing the mount point itself.
            # So, since this is a new module type, not an implementation, this
            # class shouldn't be registered as a module. Instead, it sets up a
            # list where modules can be registered later.
            cls.modules = []
        else:
            # This must be a module implementation, which should be registered.
            # Simply appending it to the list is all that's needed to keep
            # track of it later.
            cls.modules.append(cls)


class Module:
    """
    To define a module for the system, simply subclass this object.
    """
    __metaclass__ = ModuleMount

    def __init__(self, log):
        log.info("Registering module {}".format(str(self.__class__.__name__)))
        self.log = log

        # Links
        self.parents = []
        self.siblings = []
        self.children = []

        # Adjectives
        self.user = False  # Can this be assumed by a user?
        self.container = False  # Can this hold cargo?
        self.accessible = False  # Can this be entered?
