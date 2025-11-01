import abc

class RichRenderable(metaclass=abc.ABCMeta):
    """A virtual base class for objects renderable by rich."""

    @classmethod
    def __subclasshook__(cls, subclass):
        # Duck-type check: must have a __rich_console__ or __rich__ method
        if any(hasattr(subclass, m) for m in ("__rich_console__", "__rich__")):
            return True
        return NotImplemented
