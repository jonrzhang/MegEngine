# -*- coding: utf-8 -*-
# MegEngine is Licensed under the Apache License, Version 2.0 (the "License")
#
# Copyright (c) 2014-2020 Megvii Inc. All rights reserved.
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT ARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import collections
import functools
import math
import numbers
from typing import Optional, Sequence, Tuple, Union

from ..core.ops import builtin
from ..core.ops._internal import param_defs as P
from ..core.tensor import utils
from ..core.tensor.core import apply
from ..tensor import Tensor
from .elemwise import clamp, exp, log, log1p
from .tensor import remove_axis, reshape

__all__ = [
    "all",  # TODO
    "all_close",  # TODO
    "any",  # TODO
    "argmax",
    "argmin",
    "argsort",
    "isinf",
    "isnan",  # TODO
    "max",
    "mean",
    "median",  # TODO
    "min",
    "norm",
    "normalize",
    "prod",
    "sign",  # TODO
    "sort",
    "std",
    "sum",
    "topk",
    "unique",  # TODO
    "var",
]


def all(inp):
    raise NotImplementedError


def all_close(inp):
    raise NotImplementedError


def any(inp):
    raise NotImplementedError


def unique(inp):
    raise NotImplementedError


def isnan(inp: Tensor) -> Tensor:
    r"""Returns a new tensor representing if each element is NaN or not.

    :param: inp
    :return: a new tensor representing if each element in :attr:`inp` is NaN or not.

    Examples:

    .. testcode::

        from megengine import tensor
        import megengine.functional as F

        x = tensor([1, float("nan"), 0])

        print(F.isnan(x))

    .. testoutput::

        Tensor([0 1 0], dtype=uint8)

    """
    raise NotImplementedError
    # return (inp != inp).astype("uint8")


def isinf(inp: Tensor) -> Tensor:
    r"""Returns a new tensor representing if each element is Inf or not.

    :param: inp
    :return: a new tensor representing if each element in :attr:`inp` is Inf or not.

    Examples:

    .. testcode::

        from megengine import tensor
        import megengine.functional as F

        x = tensor([1, float("inf"), 0])

        print(F.isinf(x))

    .. testoutput::

        Tensor([0 1 0], dtype=uint8)

    """
    return (abs(inp).astype("float32") == float("inf")).astype("uint8")


def sign(inp: Tensor):
    raise NotImplementedError


def sum(
    inp: Tensor,
    axis: Optional[Union[int, Sequence[int]]] = None,
    keepdims: bool = False,
) -> Tensor:
    r"""Returns the sum of each row of the ``inp`` tensor in the given ``axis``.

    :param inp: The input tensor.
    :param axis: The dimension to reduce. If None, all the dimensions will be reduced.
        Default: None
    :param keepdims: Whether the output tensor has ``axis`` retained or not.
        Default: False
    :return: The output tensor

    Examples:

    .. testcode::

        import numpy as np
        from megengine import tensor
        import megengine.functional as F

        data = tensor(np.arange(1, 7, dtype=np.int32).reshape(2, 3))
        out = F.sum(data)
        print(out.numpy())

    .. testoutput::

        [21]

    """
    return inp.sum(axis=axis, keepdims=keepdims)


def prod(
    inp: Tensor, axis: Optional[Union[int, Sequence[int]]] = None, keepdims=False
) -> Tensor:
    r"""
    Returns the element product of input tensor along given *axis*.

    :param inp: The input tensor
    :param axis: The dimension to reduce. If None, all the dimensions will be reduced. Default: ``None``
    :param keepdims: Whether the output tensor has *axis* retained or not. Default: ``False``
    :return: The output tensor

    Examples:

    .. testcode::

        import numpy as np
        from megengine import tensor
        import megengine.functional as F

        data = tensor(np.arange(1, 7, dtype=np.int32).reshape(2, 3))
        out = F.prod(data)
        print(out.numpy())

    Outputs:

    .. testoutput::

        [720]

    """
    return inp.prod(axis=axis, keepdims=keepdims)


def mean(
    inp: Tensor,
    axis: Optional[Union[int, Sequence[int]]] = None,
    keepdims: bool = False,
) -> Tensor:
    """Returns the mean value of each row of the ``inp`` tensor in
    the given ``axis``. If axis is a list of dimensions,
    reduce over all of them.

    :param inp: The input tensor
    :param axis: The dimension to reduce. If None, all the dimensions will be reduced. Default: None
    :param keepdims: Whether the output tensor has ``axis`` retained or not. Default: False

    Examples:

    .. testcode::

        import numpy as np
        from megengine import tensor
        import megengine.functional as F

        data = tensor(np.arange(1, 7, dtype=np.int32).reshape(2, 3))
        out = F.mean(data)
        print(out.numpy())

    .. testoutput::

        [3.5]

    """
    return inp.astype("float32").mean(axis=axis, keepdims=keepdims)


def median(
    inp: Tensor,
    axis: Optional[Union[int, Sequence[int]]] = None,
    keepdims: bool = False,
) -> Tensor:
    raise NotImplementedError


def var(
    inp: Tensor,
    axis: Optional[Union[int, Sequence[int]]] = None,
    keepdims: bool = False,
) -> Tensor:
    """Returns the variance value of input tensor along
    given ``axis``. If axis is a list of dimensions,
    reduce over all of them.

    :param inp: The input tensor.
    :param axis: The dimension to reduce. If None, all the dimensions will be reduced. Default: ``None``.
    :param keepdims: Whether the output tensor has ``axis`` retained or not. Default: ``False``.
    :return: The output tensor.

    Examples:

    .. testcode::

        import numpy as np
        from megengine import tensor
        import megengine.functional as F

        data = tensor(np.arange(1, 7, dtype=np.float32).reshape(2, 3))
        out = F.var(data)
        print(out.numpy())

    .. testoutput::

        [2.9166667]
    """
    if axis is None:
        m = mean(inp, axis=axis, keepdims=False)
    else:
        m = mean(inp, axis=axis, keepdims=True)
    v = inp - m
    return mean(v ** 2, axis=axis, keepdims=keepdims)


def std(
    inp: Tensor,
    axis: Optional[Union[int, Sequence[int]]] = None,
    keepdims: bool = False,
) -> Tensor:
    """Returns the standard deviation of input tensor along
    given ``axis``. If axis is a list of dimensions,
    reduce over all of them.

    :param inp: The input tensor.
    :param axis: The dimension to reduce. If None, all the dimensions will be reduced. Default: ``None``.
    :param keepdims: Whether the output tensor has ``axis`` retained or not. Default: ``False``.
    :return: The output tensor.

    Examples:

    .. testcode::

        import numpy as np
        from megengine import tensor
        import megengine.functional as F

        data = tensor(np.arange(1, 7, dtype=np.float32).reshape(2, 3))
        out = F.std(data, axis=1)
        print(out.numpy())

    .. testoutput::

        [0.8164966 0.8164966]
    """
    return var(inp, axis=axis, keepdims=keepdims) ** 0.5


def min(
    inp: Tensor,
    axis: Optional[Union[int, Sequence[int]]] = None,
    keepdims: bool = False,
) -> Tensor:
    r"""
    Returns the min value of input tensor along given *axis*.

    :param inp: The input tensor
    :param axis: The dimension to reduce. If None, all the dimensions will be reduced. Default: None
    :param keepdims: Whether the output tensor has *axis* retained or not. Default: False
    :return: The output tensor

    Examples:

    .. testcode::

        import numpy as np
        from megengine import tensor
        import megengine.functional as F

        x = tensor(np.arange(1, 7, dtype=np.int32).reshape(2,3))
        y = F.min(x)
        print(y.numpy())

    Outputs:

    .. testoutput::

        [1]

    """
    return inp.min(axis=axis, keepdims=keepdims)


def max(
    inp: Tensor,
    axis: Optional[Union[int, Sequence[int]]] = None,
    keepdims: bool = False,
) -> Tensor:
    r"""Returns the max value of the input tensor along given *axis*.

    :param inp: The input tensor
    :param axis: The dimension to reduce. If None, all the dimensions will be reduced. Default: None
    :param keepdims: Whether the output tensor has *axis* retained or not. Default: False
    :return: The output tensor

    Examples:

    .. testcode::

        import numpy as np
        from megengine import tensor
        import megengine.functional as F

        x = tensor(np.arange(1, 7, dtype=np.int32).reshape(2,3))
        y = F.max(x)
        print(y.numpy())

    .. testoutput::

        [6]

    """
    return inp.max(axis=axis, keepdims=keepdims)


def norm(
    inp: Tensor,
    p: int = 2,
    axis: Optional[Union[int, Sequence[int]]] = None,
    keepdims=False,
):
    """Calculate ``p``-norm of input tensor along certain axis.

    :param inp: The input tensor
    :param p: power of value ``p`` applied to ``inp``. Default: 2
    :param axis: The dimension to reduce. If None, all the dimensions will be reduced. Default: None
    :param keepdims: Whether the output tensor has ``axis`` retained or not. Default: False
    :return: The output tensor

    Examples:

    .. testcode::

        import numpy as np
        from megengine import tensor
        import megengine.functional as F

        x = tensor(np.arange(-3, 3, dtype=np.float32).reshape(2,3))
        y = F.norm(x)
        print(y.numpy())

    .. testoutput::

        [4.358899]

    """
    if p == 0:
        return sum(inp != 0, axis=axis, keepdims=keepdims)
    if p == math.inf:
        return max(abs(inp))
    if p == -math.inf:
        return min(abs(inp))
    return sum(abs(inp) ** p, axis=axis, keepdims=keepdims) ** (1.0 / p)


def argmin(
    inp: Tensor,
    axis: Optional[Union[int, Sequence[int]]] = None,
    keepdims: bool = False,
) -> Tensor:
    r"""Returns the indices of the minimum values along an axis

    :param inp: The input tensor
    :param axis: The dimension to reduce. If None, all the dimensions will be reduced. Default: None
    :param keepdims: Whether the output tensor has *axis* retained or not. Default: False
    :return: The output tensor

    Examples:

    .. testcode::

        import numpy as np
        from megengine import tensor
        import megengine.functional as F

        x = tensor(np.arange(1, 7, dtype=np.int32).reshape(2,3))
        y = F.argmin(x)
        print(y.numpy())

    .. testoutput::

        [0]

    """
    if isinstance(axis, collections.Iterable):
        axis = list(axis)
        axis.sort(reverse=True)

        for ai in axis:
            op = builtin.Argmin(axis=ai)
            (inp,) = apply(op, inp)

            if not keepdims:
                inp = remove_axis(inp, ai)

        return inp

    if axis is None:
        assert not keepdims, "can not set axis=None and keepdims=True"
        inp = inp.flatten()
        axis = 0

    op = builtin.Argmin(axis=axis)
    (result,) = apply(op, inp)
    if not keepdims:
        result = remove_axis(result, axis)
    return result


def argmax(
    inp: Tensor,
    axis: Optional[Union[int, Sequence[int]]] = None,
    keepdims: bool = False,
) -> Tensor:
    r"""Returns the indices of the maximum values along an axis

    :param inp: The input tensor
    :param axis: The dimension to reduce. If None, all the dimensions will be reduced. Default: None
    :param keepdims: Whether the output tensor has *axis* retained or not. Default: False
    :return: The output tensor

    Examples:

    .. testcode::

        import numpy as np
        from megengine import tensor
        import megengine.functional as F

        x = tensor(np.arange(1, 7, dtype=np.int32).reshape(2,3))
        y = F.argmax(x)
        print(y.numpy())

    .. testoutput::

        [5]

    """
    if isinstance(axis, collections.Iterable):
        axis = list(axis)
        axis.sort(reverse=True)

        for ai in axis:
            op = builtin.Argmax(axis=ai)
            (inp,) = apply(op, inp)

            if not keepdims:
                inp = remove_axis(inp, ai)

        return inp

    if axis is None:
        assert not keepdims, "can not set axis=None and keepdims=True"
        inp = inp.flatten()
        axis = 0

    op = builtin.Argmax(axis=axis)
    (result,) = apply(op, inp)
    if not keepdims:
        result = remove_axis(result, axis)
    return result


def normalize(
    inp: Tensor,
    p: int = 2,
    axis: Optional[Union[int, Sequence[int]]] = None,
    eps: float = 1e-12,
) -> Tensor:
    r"""Perform :math:`L_p` normalization of input tensor along certain axis.

    For a tensor :attr:`inp` of shape :math:`(n_0, ..., n_{dim}, ..., n_k)`, each
    :math:`n_{dim}` -element vector :math:`v` along dimension :attr:`axis` is transformed as:

    .. math::
        v = \frac{v}{\max(\lVert v \rVert_p, \epsilon)}.

    :param inp: the input tensor
    :param p: power of value ``p`` applied to ``inp``. Default: 2
    :param axis: The dimension to reduce. If None, all the dimensions will be reduced
        to calculate the norm. Default: None
    :param eps: a small value to avoid division by zero. Default: 1e-12
    :return: the normalized output tensor

    """
    if axis is None:
        return inp / clamp(norm(inp, p, axis), lower=eps)
    else:
        return inp / clamp(norm(inp, p, axis, keepdims=True), lower=eps)


def argsort(inp: Tensor, descending: bool = False) -> Tensor:
    r"""
    Sort the target 2d matrix by row, return both the sorted tensor and indices.

    :param inp: The input tensor, if 2d, each row will be sorted
    :param descending: Sort in descending order, where the largest comes first. Default: ``False``
    :return: Tuple of two tensors (sorted_tensor, indices_of_int32)

    Examples:

    .. testcode::

        import numpy as np
        from megengine import tensor
        import megengine.functional as F
        data = tensor(np.array([1,2], dtype=np.float32))
        indices = F.argsort(data)
        print(indices.numpy())

    Outputs:

    .. testoutput::

        [0 1]

    """
    assert len(inp.shape) <= 2, "Input should be 1d or 2d"
    if descending:
        order = P.Argsort.Order.DESCENDING
    else:
        order = P.Argsort.Order.ASCENDING

    op = builtin.Argsort(order=order)
    if len(inp.shape) == 1:
        inp = inp.reshape(1, -1)
        _, result = apply(op, inp)
        return result[0]
    _, result = apply(op, inp)
    return result


def sort(inp: Tensor, descending: bool = False) -> Tuple[Tensor, Tensor]:
    assert len(inp.shape) <= 2, "Input should be 1d or 2d"
    if descending:
        order = P.Argsort.Order.DESCENDING
    else:
        order = P.Argsort.Order.ASCENDING

    op = builtin.Argsort(order=order)
    if len(inp.shape) == 1:
        inp = inp.reshape(1, -1)
        tns, ind = apply(op, inp)
        return tns[0], ind[0]
    tns, ind = apply(op, inp)
    return tns, ind


def topk(
    inp: Tensor,
    k: int,
    descending: bool = False,
    kth_only: bool = False,
    no_sort: bool = False,
) -> Tuple[Tensor, Tensor]:
    r"""
    Selected the Top-K (by default) smallest elements of 2d matrix by row.

    :param inp: The input tensor, if 2d, each row will be sorted
    :param k: The number of elements needed
    :param descending: If true, return the largest elements instead. Default: ``False``
    :param kth_only: If true, only the k-th element will be returned. Default: ``False``
    :param no_sort: If true, the returned elements can be unordered. Default: ``False``
    :return: Tuple of two tensors (topk_tensor, indices_of_int32)

    Examples:

    .. testcode::

        import numpy as np
        from megengine import tensor
        import  megengine.functional as F
        data = tensor(np.array([2, 4, 6, 8, 7, 5, 3, 1], dtype=np.float32))
        top, indices = F.topk(data, 5)
        print(top.numpy(), indices.numpy())

    Outputs:

    .. testoutput::

        [1. 2. 3. 4. 5.] [7 0 6 1 5]

    """
    if descending:
        inp = -inp

    Mode = P.TopK.Mode
    if kth_only:
        mode = Mode.KTH_ONLY
    elif no_sort:
        mode = Mode.VALUE_IDX_NOSORT
    else:
        mode = Mode.VALUE_IDX_SORTED
    op = builtin.TopK(mode=mode)

    if len(inp.shape) == 1:
        inp = inp.reshape(1, -1)
        res = apply(op, inp, Tensor(k, dtype="int32"))
        if kth_only:
            tns = res[0]
        else:
            tns, ind = res[0][0], res[1][0]
    else:
        res = apply(op, inp, Tensor(k, dtype="int32"))
        if kth_only:
            tns = res
        else:
            tns, ind = res[0], res[1]

    if descending:
        tns = -tns
    return tns, ind