from __future__ import annotations

__all__ = ["SphinxSectorFactory"]

from dataclasses import dataclass
from typing import Any, Generic, Type, TypeVar

from multibar.interfaces.product import AbstractSectorMixin

_AbcSectorT_co = TypeVar("_AbcSectorT_co", bound=AbstractSectorMixin, covariant=True)


@dataclass
class SphinxSectorFactory(Generic[_AbcSectorT_co]):
    """Class that represents Sector factory.

    Parameters:
    -----------
    bind: :class:`Type[_AbcSectorT_co]`
        Sector cls implementation (or subclass of Sector...).
    """

    bind: Type[_AbcSectorT_co]

    @classmethod
    def from_bind(
        cls: Type[SphinxSectorFactory[_AbcSectorT_co]],
        *,
        sector_type: Type[_AbcSectorT_co],
    ) -> SphinxSectorFactory[_AbcSectorT_co]:
        """``classmethod``
        Returns instance with new "template" (Sector implementation).

        Parameters:
        -----------
        sector_type: :class:`Type[_AbcSectorT_co]`
            Sector cls implementation.
        """
        return cls(
            bind=sector_type,
        )

    def rebind(
        self,
        *,
        sector_type: Type[_AbcSectorT_co],
    ) -> None:
        """``sync method``
        Sets new "template" (Sector implementation) for factory.

        Raises:
        -------
        :class:`TypeError`:
            If Sector is not subclass of :class:`AbstractSectorMixin`

        Parameters:
        -----------
        sector_type: :class:`Type[_AbcSectorT_co]`
            Sector cls implementation.
        """
        if not issubclass(sector_type, AbstractSectorMixin):
            raise TypeError("Sector must be subclass of :class:`AbstractSectorMixin`")

        self.bind = sector_type

    def create_product(
        self,
        *args: Any,
        name: str = "",
        position: int = 0,
        empty: bool = False,
        **kwargs: Any,
    ) -> _AbcSectorT_co:
        """``sync method``
        Creates Sector object.

        *args: :class:`Any`
            Args that will be passed in custom Sector implementation.

            For more information and examples see:
                https://animatea.github.io/python-multibar/abc/?h=abstractsectormixin

        name: :class:`str`
            Sector name parameter.

        position: :class:`int`
            Sector position parameter.

        empty: :class:`bool`
            For empty sectors used :line: emoji (and unfilled_start, unfilled_end if passed).

        **kwargs: :class:`Any`
            Kwargs that will be passed in custom Container implementation.

            For more information and examples see:
                https://animatea.github.io/python-multibar/abc/?h=abstractseqbasedcontainermixin
        """
        return self.bind(
            *args,
            name=name,
            position=position,
            empty=empty,
            **kwargs,
        )
