from .utils import typename


class VariadicSignatureType(type):
    # checking if subclass is a subclass of self
    def __subclasscheck__(self, subclass):
        other_type = subclass.variadic_type if isvariadic(subclass) else (subclass,)
        return subclass is self or all(
            issubclass(other, self.variadic_type) for other in other_type
        )

    def __eq__(self, other):
        """
        Return True if other has the same variadic type

        Parameters
        ----------
        other : object (type)
            The object (type) to check

        Returns
        -------
        bool
            Whether or not `other` is equal to `self`
        """
        return isvariadic(other) and set(self.variadic_type) == set(other.variadic_type)

    def __hash__(self):
        return hash((type(self), frozenset(self.variadic_type)))


def isvariadic(obj):
    """Check whether the type `obj` is variadic.

    Parameters
    ----------
    obj : type
        The type to check

    Returns
    -------
    bool
        Whether or not `obj` is variadic

    Examples
    --------
    >>> isvariadic(int)
    False
    >>> isvariadic(Variadic[int])
    True
    """
    return isinstance(obj, VariadicSignatureType)


class VariadicSignatureMeta(type):
    """A metaclass that overrides ``__getitem__`` on the class. This is used to
    generate a new type for Variadic signatures. See the Variadic class for
    examples of how this behaves.
    """

    def __getitem__(self, variadic_type):
        if not (isinstance(variadic_type, (type, tuple)) or type(variadic_type)):
            raise ValueError(
                "Variadic types must be type or tuple of types"
                " (Variadic[int] or Variadic[(int, float)]"
            )

        if not isinstance(variadic_type, tuple):
            variadic_type = (variadic_type,)
        return VariadicSignatureType(
            "Variadic[%s]" % typename(variadic_type),
            (),
            dict(variadic_type=variadic_type, __slots__=()),
        )


class Variadic(metaclass=VariadicSignatureMeta):
    """A class whose getitem method can be used to generate a new type
    representing a specific variadic signature.

    Examples
    --------
    >>> Variadic[int]  # any number of int arguments
    <class 'multipledispatch.variadic.Variadic[int]'>
    >>> Variadic[(int, str)]  # any number of one of int or str arguments
    <class 'multipledispatch.variadic.Variadic[(int, str)]'>
    >>> issubclass(int, Variadic[int])
    True
    >>> issubclass(int, Variadic[(int, str)])
    True
    >>> issubclass(str, Variadic[(int, str)])
    True
    >>> issubclass(float, Variadic[(int, str)])
    False
    """
