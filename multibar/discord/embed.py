"""
Copyright [2021] [DenyS]

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from __future__ import annotations

import attr
import types
import typing
import datetime
import contextlib
import collections

from multibar import ProgressObject
from multibar.discord import errors, inspections
from multibar.discord.abstract import EmbedABC
from multibar.discord.ext.manipulator import Manipulator

if typing.TYPE_CHECKING:
    from multibar.discord.ext.manipulator import _Bar, _Percents, _IsLeft

    _AnyValueT = typing.TypeVar("_AnyValueT")
    MaybeNone = typing.Union[_AnyValueT, None]

    _EmbedType = typing.Literal["rich", "image", "video", "gifv", "article", "link"]


__all__: typing.Sequence[str] = (
    "ProgressEmbed",
    "EmbedVideo",
    "EmbedProvider",
    "EmbedField",
    "EmbedImage",
    "EmbedAuthor",
)


T = typing.TypeVar("T")
KT = typing.TypeVar("KT")  # Key type
VT = typing.TypeVar("VT")  # Value type
PT_invariant = typing.TypeVar("PT_invariant")  # Proxy type


class ParamProxy(typing.Generic[PT_invariant]):
    def __init__(self, *parameters: typing.Any) -> None:
        self.__parameters = parameters

    def __repr__(self) -> str:
        return f"<Param.Proxy{self.__parameters}>"

    def __iter__(self) -> typing.Iterator[typing.Any]:
        return iter(self.__parameters)

    def __contains__(self, item: str) -> bool:
        return getattr(self, item, None) is not None

    def __len__(self) -> int:
        return len(self.__parameters)

    def __getitem__(self, index: int) -> typing.Any:
        return self.__parameters[index]

    def __new__(cls, *args: typing.Any) -> typing.Any:
        if cls is not ParamProxy:
            raise TypeError("Proxy cannot be inherited.")
        return super().__new__(cls, *args)


""" ``|const|``
All attributes available to the embed.
"""
ALLOWED_ATTRS: typing.Final[typing.List[str]] = [
    "_" + i
    for i in (
        "title",
        "type",
        "url",
        "description",
        "timestamp",
        "color",
        "video",
        "provider",
        "fields",
        "author",
        "footer",
        "image",
        "thumbnail",
    )
]


def field_converter(_: typing.Any, fields: typing.Iterable[typing.Any]) -> typing.List[typing.Any]:
    """``|attr converter|``

    Field converter by annotation.

    Parameters:
    -----------
    _: :class:`typing.Any`
        Required argument for field_converter signature.

    fields: :class:`typing.Iterable`
        Fields by which the conversion will take place during iteration.

    Returns:
    --------
    results: :class:`typing.List[T]`
        Converted fields.
    """
    results: typing.List[typing.Any] = []
    converter: typing.Optional[typing.Callable[..., typing.Any]]
    for field in fields:
        if field.converter is not None:
            # Converter is already set.
            results.append(field)
            continue

        elif field.type in {str, "str"}:
            converter = lambda v: str(v) if v else v

        elif field.type in {int, "int"}:
            converter = lambda v: int(v) if v else v

        elif field.type in {datetime.datetime, "datetime.datetime"}:
            # From datetime.datetime to isoformat convert.
            converter = lambda d: datetime.datetime.isoformat(d) if isinstance(d, datetime.datetime) else d
        else:
            converter = None
        results.append(field.evolve(converter=converter))
    return results


@attr.define(kw_only=True, slots=True, repr=False, field_transformer=field_converter)
class EmbedVideo(EmbedABC):
    """``|Embed video attribute|``

    Parameters:
    -----------
    url: :class:`typing.Optional[str]` = None
        Source url of video.

    proxy_url: :class:`typing.Optional[str]` = None
        A proxied url of the video.

    height: :class:`typing.Optional[int]` = None
        Height of video.

    width: :class:`typing.Optional[int]` = None
        Width of video.
    """

    url: str = attr.field(default=None)
    """ !!! will be converted to :class:`str` """

    proxy_url: str = attr.field(default=None)
    """ !!! will be converted to :class:`str` """

    height: int = attr.field(default=None)
    """ !!! will be converted to :class:`int` """

    width: int = attr.field(default=None)
    """ !!! will be converted to :class:`int` """

    def _source_(self) -> typing.Dict[str, VT]:
        """``|abc method|``

        !!! note:
            Since there were problems with inheritance and extensibility was needed,
            it was decided to make this method abstract. A method that returns the
            source code for the API requesting any embed or embed parameter in the dictionary.
        """
        return {i: getattr(self, i) for i in dir(self) if not i.startswith("_")}


@attr.define(kw_only=True, slots=True, repr=False, field_transformer=field_converter)
class EmbedProvider(EmbedABC):
    """``|Embed provider attribute|``

    Parameters:
    -----------
    name: :class:`typing.Optional[str]` = None
        Name of provider.

    url: :class:`typing.Optional[str]` = None
        Url of provider.
    """

    name: str = attr.field(default=None)
    """ !!! will be converted to :class:`str` """

    url: str = attr.field(default=None)
    """ !!! will be converted to :class:`str` """

    def _source_(self) -> typing.Dict[str, typing.Any]:
        """``|abc method|``

        !!! note:
            Since there were problems with inheritance and extensibility was needed,
            it was decided to make this method abstract. A method that returns the
            source code for the API requesting any embed or embed parameter in the dictionary.
        """
        return {i: getattr(self, i) for i in dir(self) if not i.startswith("_")}


@attr.define(kw_only=True, slots=True, repr=False, field_transformer=field_converter)
class EmbedFooter(EmbedABC):
    """``|Embed footer attribute|``

    Parameters:
    -----------
    text: :class:`typing.Optional[str]` = None
        Footer text.

    icon_url: :class:`typing.Optional[str]` = None
        Url of footer icon (only supports http(s) and attachments).

    proxy_icon_url: :class:`typing.Optional[str]` = None
        A proxied url of footer icon.
    """

    text: str = attr.field(default=None)
    """ !!! will be converted to :class:`str` """

    icon_url: str = attr.field(default=None)
    """ !!! will be converted to :class:`str` """

    proxy_icon_url: str = attr.field(default=None)
    """ !!! will be converted to :class:`str` """

    def _source_(self) -> typing.Dict[str, typing.Any]:
        """``|abc method|``

        !!! note:
            Since there were problems with inheritance and extensibility was needed,
            it was decided to make this method abstract. A method that returns the
            source code for the API requesting any embed or embed parameter in the dictionary.
        """
        return {i: getattr(self, i) for i in dir(self) if not i.startswith("_")}


@attr.define(kw_only=True, slots=True, repr=False, field_transformer=field_converter)
class EmbedThumbnail(EmbedABC):
    """``|Embed thumbnail attribute|``

    Parameters:
    -----------
    url: :class:`typing.Optional[str]` = None
        Source url of thumbnail (only supports http(s) and attachments).

    proxy_url: :class:`typing.Optional[str]` = None
        A proxied url of the thumbnail.

    height: :class:`typing.Optional[int]` = None
        Height of thumbnail.

    width: :class:`typing.Optional[int]` = None
        Width of thumbnail.
    """

    url: str = attr.field(default=None)
    """ !!! will be converted to :class:`str` """

    proxy_url: str = attr.field(default=None)
    """ !!! will be converted to :class:`str` """

    height: int = attr.field(default=None)
    """ !!! will be converted to :class:`int` """

    width: int = attr.field(default=None)
    """ !!! will be converted to :class:`int` """

    def _source_(self) -> typing.Dict[str, typing.Any]:
        """``|abc method|``

        !!! note:
            Since there were problems with inheritance and extensibility was needed,
            it was decided to make this method abstract. A method that returns the
            source code for the API requesting any embed or embed parameter in the dictionary.
        """
        return {i: getattr(self, i) for i in dir(self) if not i.startswith("_")}


@attr.define(kw_only=True, slots=True, repr=False, field_transformer=field_converter)
class EmbedImage(EmbedABC):
    """``|Embed image attribute|``

    Parameters:
    -----------
    url: :class:`typing.Optional[str]` = None
        Source url of image (only supports http(s) and attachments).

    proxy_url: :class:`typing.Optional[str]` = None
        A proxied url of the image.

    height: :class:`typing.Optional[int]` = None
        Height of image.

    width: :class:`typing.Optional[int]` = None
        Width of image.
    """

    url: str = attr.field(default=None)
    """ !!! will be converted to :class:`str` """

    proxy_url: str = attr.field(default=None)
    """ !!! will be converted to :class:`str` """

    height: int = attr.field(default=None)
    """ !!! will be converted to :class:`int` """

    width: int = attr.field(default=None)
    """ !!! will be converted to :class:`int` """

    def _source_(self) -> typing.Dict[str, typing.Any]:
        """``|abc method|``

        !!! note:
            Since there were problems with inheritance and extensibility was needed,
            it was decided to make this method abstract. A method that returns the
            source code for the API requesting any embed or embed parameter in the dictionary.
        """
        return {i: getattr(self, i) for i in dir(self) if not i.startswith("_")}


@attr.define(kw_only=True, slots=True, repr=False, field_transformer=field_converter)
class EmbedAuthor(EmbedABC):
    """``|Embed author attribute|``

    Parameters:
    -----------
    name: :class:`typing.Optional[str]` = None
        Name of author.

    url: :class:`typing.Optional[str]` = None
        Url of author.

    icon_url: :class:`typing.Optional[str]` = None
        Url of author icon (only supports http(s) and attachments).

    proxy_icon_url: :class:`typing.Optional[str]` = None
        A proxied url of author icon.
    """

    name: str = attr.field(default=None)
    """ !!! will be converted to :class:`str` """

    url: str = attr.field(default=None)
    """ !!! will be converted to :class:`str` """

    icon_url: str = attr.field(default=None)
    """ !!! will be converted to :class:`str` """

    proxy_icon_url: str = attr.field(default=None)
    """ !!! will be converted to :class:`str` """

    def _source_(self) -> typing.Dict[str, typing.Any]:
        """``|abc method|``

        !!! note:
            Since there were problems with inheritance and extensibility was needed,
            it was decided to make this method abstract. A method that returns the
            source code for the API requesting any embed or embed parameter in the dictionary.
        """
        return {i: getattr(self, i) for i in dir(self) if not i.startswith("_")}


@attr.define(kw_only=True, slots=True, repr=False, field_transformer=field_converter)
class EmbedField(EmbedABC):
    """``|Embed author attribute|``

    !!! note:
        <name> and <value> are required attributes,
        by default - None for more customization of checks.
        If one of these attributes is None, it will throw an error.

    Parameters:
    -----------
    name: :class:`typing.Optional[str]` = None
        Name of the field.

    value: :class:`typing.Optional[str]` = None
        Value of the field.

    inline: :class:`bool` = True
        Whether or not this field should display inline.

    progress: :class:`typing.Optional[ProgressObject]` = None
        Progress bar object, if specified, will set the progress
        bar to the <value> of this field. You can change its output
        with :class:`Manipulator`.

    Raises:
    -------
    :class:`ValueError`:
        If <name> or <value> of the field is empty.
    """

    def _footer_validator(self, attribute: attr.Attribute[typing.Any], value: typing.Any) -> None:
        """``|footer validator|``

        Validator that checks the value of certain attributes.

        Parameters:
        -----------
        attribute: :class:`attr.Attribute`
            Attribute to be checked.

        value: :class:`typing.Any`
            The value that is passed to the given attribute.
        """
        if inspections.is_empty_field(value):
            raise ValueError(
                f"Attribute <{attribute.name}> cannot be None or <{attribute.name}> length must be > 0"
            )

    name: str = attr.field(default=None, validator=_footer_validator)
    """ !!! will be converted to :class:`str` """

    value: str = attr.field(default=None, validator=_footer_validator)
    """ !!! will be converted to :class:`str` """

    inline: bool = attr.field(default=True)
    """ !!! without converter """

    progress: typing.Optional[ProgressObject] = attr.field(default=None)
    """ !!! without converter """

    @staticmethod
    def __format_value(attrib: str, value: typing.Any) -> typing.Any:
        """``|staticmethod|``

        A method that, depending on the context, changes a specific value.

        Parameters:
        -----------
        attrib: :class:`str`
            The current attribute that defines the context.

        value: :class:`typing.Any`
            A specific value that defines the context and will be changed later.

        Returns:
        --------
        value: :class:`typing.Any`
            Modified value.
        """

        if isinstance(value, (list, collections.deque)):
            return "".join(i.emoji_name for i in value)
        if attrib == "_percents":
            return f"{value}%"
        return value

    def _set_progress(self, manipulator: Manipulator = None, sep: str = " ") -> typing.Optional[Manipulator]:
        """``|method|``

        A method that sets progress and changes its output depending on the `embed manipulator`.

        Parameters:
        -----------
        manipulator: :class:`Manipulator`
            A manipulator that will subsequently change the output of progress.

        sep: :class:`str`
            Separator through which such parts of the progress will be located as:
            "is_left", "percents" and "bar"

        Returns:
        --------
        manipulator: :class:`typing.Optional[Manipulator]`
            The current state of the manipulator.
        """
        if self.progress is not None:
            if manipulator is None:
                self.value = (
                    f"[{self.progress.now}/{self.progress.needed}] "
                    f"{self.progress} "
                    f"{self.progress.percents}%"
                )
            else:
                setattr(
                    self.progress,
                    "isleft",
                    f"{self.progress.now}/{self.progress.needed}",
                )
                _value: typing.List[str] = ["", "", ""]
                for attrib in ("_percents", "_bar", "_isleft"):
                    if hasattr(manipulator, attrib):
                        temp = getattr(manipulator, attrib)
                        _value.insert(
                            temp.position,
                            f"{temp.prefix}"
                            f"{self.__format_value(attrib, getattr(self.progress, attrib[1:]))}"
                            f"{temp.suffix}",
                        )
                self.value = f"{sep}".join(_value)
                if hasattr(getattr(manipulator, "_bar", None), "_reverse"):
                    self.name, self.value = self.value, self.name

                return manipulator

    def _source_(self) -> typing.Dict[str, typing.Any]:
        """``|abc method|``

        !!! note:
            Since there were problems with inheritance and extensibility was needed,
            it was decided to make this method abstract. A method that returns the
            source code for the API requesting any embed or embed parameter in the dictionary.
        """
        return {i: getattr(self, i) for i in dir(self) if not i.startswith("_") and i not in ("progress",)}


@attr.define(kw_only=True, slots=True, repr=False, field_transformer=field_converter)
class ProgressEmbed(EmbedABC):
    """``|Main Embed class|``

    The main class that represents an `embed`.

    Parameters:
    -----------
    title: :class:`typing.Optional[str]` = None
        Title of embed.

    type: :class:`_EmbedType` = 'rich'
        Type of embed (always "rich" for webhook embeds)

    description: :class:`typing.Optional[str]` = None
        Description of embed.

    url: :class:`typing.Optional[str]` = None
        Url of embed.

    timestamp: :class:`datetime.datetime` = datetime.datetime.utcnow()
        Timestamp of embed content.

    color: :class:`typing.Optional[int]` = None
        Color code of the embed.

    video: :class:`typing.Optional[EmbedVideo]` = None
        Video information.

    provider: :class:`typing.Optional[EmbedProvider]` = None
        Provider information.

    fields: :class:`typing.List[EmbedField]` = []
        Fields information.
    """

    _title: str = attr.field(default=None)
    """ !!! will be converted to :class:`str` """

    _type: _EmbedType = attr.field(default="rich")
    """ !!! without converter """

    _description: str = attr.field(default=None)
    """ !!! will be converted to :class:`str` """

    _url: str = attr.field(default=None)
    """ !!! will be converted to :class:`str` """

    _timestamp: datetime.datetime = attr.field(default=datetime.datetime.utcnow())
    """ !!! will be converted to `isoformat` from :class:`datetime.datetime` """

    _color: int = attr.field(default=None)
    """ !!! will be converted to :class:`int` """

    _video: EmbedVideo = attr.field(default=None)
    """ !!! without converter """

    _provider: EmbedProvider = attr.field(default=None)
    """ !!! without converter """

    _fields: typing.List[EmbedField] = attr.field(default=[])
    """ !!! without converter """

    async def _source_(self) -> typing.Any:
        """``|abc method|``

        !!! note:
            Since there were problems with inheritance and extensibility was needed,
            it was decided to make this method abstract. A method that returns the
            source code for the API requesting any embed or embed parameter in the dictionary.
        """
        _source = {}
        for attribute in dir(self):
            if attribute in ALLOWED_ATTRS and not repr(value := getattr(self, attribute)).startswith(
                "(_CountingAttr"
            ):
                if hasattr(value, "_source_"):
                    _source.update({attribute[1:]: value._source_()})
                elif isinstance(value, list):
                    fields: typing.Dict[str, typing.List[EmbedField]] = {"fields": []}
                    for idx, field in enumerate(value):
                        fields["fields"].append(field._source_())
                    _source.update(fields)
                else:
                    _source.update({attribute[1:]: value})
        return _source

    @property
    def fields(self) -> ParamProxy[typing.List[MaybeNone[EmbedField]]]:
        """``|property|``

        Returns information about `fields` in the given embed.

        Returns:
        --------
        Fields information: :class:`types.MappingProxyType`
            Fields attribute value.
        """
        return ParamProxy(getattr(self, "_fields", []))

    @property
    def footer(self) -> types.MappingProxyType[KT, VT]:
        """``|property|``

        Returns information about `footer` in the given embed.

        Returns:
        --------
        footer information: :class:`types.MappingProxyType`
            Footer attribute value.
        """
        return types.MappingProxyType(getattr(self, "_footer", {}))

    @property
    def title(self) -> ParamProxy[MaybeNone[str]]:
        """``|property|``

        Returns information about `title` in the given embed.

        Returns:
        --------
        title information: :class:`types.MappingProxyType`
            Title attribute value.
        """
        return ParamProxy(getattr(self, "_title", None))

    @title.setter
    def title(self, new: str) -> None:
        """``|property setter|``

        A setter that changes the value of the `title` attribute.
        """
        self._title = new

    @property
    def type(self) -> ParamProxy[MaybeNone[str]]:
        """``|property|``

        Returns information about `type` in the given embed.

        Returns:
        --------
        type information: :class:`types.MappingProxyType`
            Type attribute value.
        """
        return ParamProxy(getattr(self, "_type", None))

    @type.setter
    def type(self, new: _EmbedType) -> None:
        """``|property setter|``

        A setter that changes the value of the `type` attribute.
        """
        self._type = new

    @property
    def description(self) -> ParamProxy[MaybeNone[str]]:
        """``|property|``

        Returns information about `description` in the given embed.

        Returns:
        --------
        description information: :class:`types.MappingProxyType`
            Description attribute value.
        """
        return ParamProxy(getattr(self, "_description", None))

    @description.setter
    def description(self, new: str) -> None:
        """``|property setter|``

        A setter that changes the value of the `description` attribute.
        """
        self._description = new

    @property
    def url(self) -> ParamProxy[MaybeNone[str]]:
        """``|property|``

        Returns information about `url` in the given embed.

        Returns:
        --------
        url information: :class:`types.MappingProxyType`
            Url attribute value.
        """
        return ParamProxy(getattr(self, "_url", None))

    @url.setter
    def url(self, new: str) -> None:
        """``|property setter|``

        A setter that changes the value of the `url` attribute.
        """
        self._url = new

    @property
    def timestamp(self) -> ParamProxy[MaybeNone[datetime.datetime]]:
        """``|property|``

        Returns information about `timestamp` in the given embed.

        Returns:
        --------
        timestamp information: :class:`types.MappingProxyType`
            Timestamp attribute value.
        """
        return ParamProxy(getattr(self, "_timestamp", None))

    @timestamp.setter
    def timestamp(self, new: datetime.datetime) -> None:
        """``|property setter|``

        A setter that changes the value of the `timestamp` attribute.
        """
        self._timestamp = new

    @property
    def color(self) -> ParamProxy[MaybeNone[int]]:
        """``|property|``

        Returns information about `color` in the given embed.

        Returns:
        --------
        color information: :class:`types.MappingProxyType`
            Color attribute value.
        """
        return ParamProxy(getattr(self, "_color", None))

    @color.setter
    def color(self, new: int) -> None:
        """``|property setter|``

        A setter that changes the value of the `color` attribute.
        """
        self._color = new

    @property
    def video(self) -> ParamProxy[MaybeNone[EmbedVideo]]:
        """``|property|``

        Returns information about `video` in the given embed.

        Returns:
        --------
        video information: :class:`types.MappingProxyType`
            Video attribute value.
        """
        return ParamProxy(getattr(self, "_video", None))

    @property
    def provider(self) -> ParamProxy[MaybeNone[EmbedProvider]]:
        """``|property|``

        Returns information about `provider` in the given embed.

        Returns:
        --------
        provider information: :class:`types.MappingProxyType`
            Provider attribute value.
        """
        return ParamProxy(getattr(self, "_provider", None))

    @property
    def image(self) -> ParamProxy[MaybeNone[EmbedImage]]:
        """``|property|``

        Returns information about `image` in the given embed.

        Returns:
        --------
        image information: :class:`types.MappingProxyType`
            Image attribute value.
        """
        return ParamProxy(getattr(self, "_image", None))

    def set_footer(
        self,
        *,
        text: typing.Optional[str] = None,
        icon_url: typing.Optional[str] = None,
        proxy_icon_url: typing.Optional[str] = None,
    ) -> ProgressEmbed:
        """``|method|``

        The method by which you can set the footer to the embed.

        Parameters:
        -----------
        text: :class:`typing.Optional[str]` = None [Keyword only]
            Footer text.

        icon_url: :class:`typing.Optional[str]` = None [Keyword only]
            Footer icon url.

        proxy_icon_url: :class:`typing.Optional[str]` = None [Keyword only]
            Proxied footer icon url.

        Returns:
        --------
        self: :class:`ProgressEmbed`
            Class instance to allow for fluent-style chaining.
        """
        setattr(
            self,
            "_footer",
            EmbedFooter(text=text, icon_url=icon_url, proxy_icon_url=proxy_icon_url),
        )
        return self

    def set_image(
        self,
        *,
        url: typing.Optional[str] = None,
        proxy_url: typing.Optional[str] = None,
        width: typing.Optional[int] = None,
        height: typing.Optional[int] = None,
    ) -> ProgressEmbed:
        """``|method|``

        The method by which you can set the image to the embed.

        Parameters:
        -----------
        url: :class:`typing.Optional[str]` = None [Keyword only]
            Url of image.

        proxy_url: :class:`typing.Optional[str]` = None [Keyword only]
            Proxied url of image.

        width: :class:`typing.Optional[int]` = None [Keyword only]
            Width of image.

        height: :class:`typing.Optional[int]` = None [Keyword only]
            Height of image.

        Returns:
        --------
        self: :class:`ProgressEmbed`
            Class instance to allow for fluent-style chaining.
        """
        setattr(
            self,
            "_image",
            EmbedImage(url=url, proxy_url=proxy_url, width=width, height=height),
        )
        return self

    def set_thumbnail(
        self,
        *,
        url: typing.Optional[str] = None,
        proxy_url: typing.Optional[str] = None,
        width: typing.Optional[int] = None,
        height: typing.Optional[int] = None,
    ) -> ProgressEmbed:
        """``|method|``

        The method by which you can set the thumbnail to the embed.

        Parameters:
        -----------
        url: :class:`typing.Optional[str]` = None [Keyword only]
            Url of thumbnail.

        proxy_url: :class:`typing.Optional[str]` = None [Keyword only]
            Proxied url of thumbnail.

        width: :class:`typing.Optional[int]` = None [Keyword only]
            Width of thumbnail.

        height: :class:`typing.Optional[int]` = None [Keyword only]
            Height of thumbnail.

        Returns:
        --------
        self: :class:`ProgressEmbed`
            Class instance to allow for fluent-style chaining.
        """
        setattr(
            self,
            "_thumbnail",
            EmbedThumbnail(url=url, proxy_url=proxy_url, width=width, height=height),
        )
        return self

    def set_author(
        self,
        *,
        name: typing.Optional[str] = None,
        url: typing.Optional[str] = None,
        icon_url: typing.Optional[str] = None,
        proxy_icon_url: typing.Optional[str] = None,
    ) -> ProgressEmbed:
        """``|method|``

        The method by which you can set the author to the embed.

        Parameters:
        -----------
        name: :class:`typing.Optional[str]` = None [Keyword only]
            Name of the embed author.

        url: :class:`typing.Optional[str]` = None [Keyword only]
            Url of embed author.

        icon_url: :class:`typing.Optional[str]` = None [Keyword only]
            Icon url of the embed author.

        proxy_icon_url: :class:`typing.Optional[str]` = None [Keyword only]
            Proxied icon url of the embed author.

        Returns:
        --------
        self: :class:`ProgressEmbed`
            Class instance to allow for fluent-style chaining.
        """
        setattr(
            self,
            "_author",
            EmbedAuthor(name=name, url=url, icon_url=icon_url, proxy_icon_url=proxy_icon_url),
        )
        return self

    def set_video(
        self,
        *,
        url: typing.Optional[str] = None,
        proxy_url: typing.Optional[str] = None,
        height: typing.Optional[int] = None,
        width: typing.Optional[int] = None,
    ) -> ProgressEmbed:
        """``|method|``

        The method by which you can set the video to the embed.

        Parameters:
        -----------
        url: :class:`typing.Optional[str]` = None
            Source url of video.

        proxy_url: :class:`typing.Optional[str]` = None
            A proxied url of the video.

        height: :class:`typing.Optional[int]` = None
            Height of video.

        width: :class:`typing.Optional[int]` = None
            Width of video.

        Returns:
        --------
        self: :class:`ProgressEmbed`
            Class instance to allow for fluent-style chaining.
        """
        setattr(self, "_video", EmbedVideo(url=url, proxy_url=proxy_url, height=height, width=width))
        return self

    def set_provider(
        self,
        *,
        name: typing.Optional[str] = None,
        url: typing.Optional[str] = None,
    ) -> ProgressEmbed:
        """``|method|``

        The method by which you can set the provider to the embed.

        Parameters:
        -----------
        name: :class:`typing.Optional[str]` = None
            Name of provider.

        url: :class:`typing.Optional[str]` = None
            Url of provider.

        Returns:
        --------
        self: :class:`ProgressEmbed`
            Class instance to allow for fluent-style chaining.
        """
        setattr(self, "_provider", EmbedProvider(name=name, url=url))
        return self

    def __replace_value(
        self,
        current_field: EmbedField,
        /,
        *,
        set_to: typing.Optional[typing.Literal["description", "title", "field"]],
    ) -> None:
        """``|private method|``

        A method with which it becomes possible to set progress on
        other embed positions besides fields.

        Parameters:
        -----------
        current_field: :class:`EmbedField` [Positional only]
            The current field whose value will be moved to a different position.

        set_to: :class:`typing.Literal['description', 'title', 'field']` [Keyword only]
            The position to which progress will be set.

        Raises:
        -------
        :class:`errors.UnexpectedArgumentError`
            If a wrong position is specified.
        """
        if set_to is not None:
            if set_to in ("title", "description"):
                setattr(self, f"_{set_to}", current_field.value)
            elif set_to == "field":
                ...
            else:
                raise errors.UnexpectedArgumentError(
                    set_to, expected='Literal["description", "title", "field"]'
                )

    def add_field(
        self,
        *,
        name: str,
        value: str,
        inline: bool = False,
        progress: typing.Optional[ProgressObject] = None,
        progress_sep: str = " ",
    ) -> ProgressEmbed:
        """``|method|``

        !!! note:
            <name> and <value> are required attributes,
            by default - None for more customization of checks.
            If one of these attributes is None, it will throw an error.

        A method by which you can add a field to your embed.

        name: :class:`typing.Optional[str]` = None [Keyword only]
            Name of the field.

        value: :class:`typing.Optional[str]` = None [Keyword only]
            Value of the field.

        inline: :class:`bool` = False [Keyword only]
            Inline of field.

        progress: :class`typing.Optional[ProgressObject]` = None [Keyword only]
            Progress bar object, if specified, will set the progress
            bar to the <value> of this field. You can change its output
            with :class:`Manipulator`.

        progress_sep: :class:`str` = ' ' [Keyword only]
            Separator through which attributes such as: "bar", "is left" and
            "percents" will be located.

        Returns:
        --------
        self: :class:`ProgressEmbed`
            Class instance to allow for fluent-style chaining.
        """
        field = EmbedField(name=name, value=value, inline=inline, progress=progress)
        edited = field._set_progress(getattr(self, "_has_manipulator", None), sep=progress_sep)
        if edited is not None:
            self.__replace_value(field, set_to=(place := getattr(self, "_progress_place", None)))
            if place != "field":
                # After fixing one error, another appears...
                field: typing.Optional[EmbedField] = None  # type: ignore[no-redef]

        if field is not None:
            self._fields.append(field)

        return self

    def remove_footer(self) -> ProgressEmbed:
        """``|method|``

        A method by which you can remove a footer from your embed.

        Returns:
        --------
        self: :class:`ProgressEmbed`
            Class instance to allow for fluent-style chaining.
        """
        if hasattr(self, "_footer"):
            del self._footer  # type: ignore[attr-defined]

        return self

    def remove_image(self) -> ProgressEmbed:
        """``|method|``

        A method by which you can remove a image from your embed.

        Returns:
        --------
        self: :class:`ProgressEmbed`
            Class instance to allow for fluent-style chaining.
        """
        if hasattr(self, "_image"):
            del self._image  # type: ignore[attr-defined]

        return self

    def remove_thumbnail(self) -> ProgressEmbed:
        """``|method|``

        A method by which you can remove a thumbnail from your embed.

        Returns:
        --------
        self: :class:`ProgressEmbed`
            Class instance to allow for fluent-style chaining.
        """
        if hasattr(self, "_thumbnail"):
            del self._thumbnail  # type: ignore[attr-defined]

        return self

    def remove_field(self, index: int) -> ProgressEmbed:
        """``|method|``

        A method by which you can remove a field by index from your embed.

        Parameters:
        -----------
        index: :class:`int`
            Index (counting from zero) at which the field will be removed.

        Returns:
        --------
        self: :class:`ProgressEmbed`
            Class instance to allow for fluent-style chaining.
        """
        with contextlib.suppress(IndexError, AttributeError):
            del self._fields[index]

        return self

    def remove_field_by(
        self, predicate: typing.Callable[..., typing.Any], /, *, stop_at: int = 1
    ) -> ProgressEmbed:
        """``|method|``

        !!! note:
            May not see the first field.

        A method by which you can remove a field by predicate from your embed.

        Parameters:
        -----------
        predicate: :class:`typing.Callable[..., typing.Any]` [Positional only]
            The check with which the fields will be removed.

        stop_at: :class:`int` = 1 [Keyword only]
            The parameter defining after what match the cycle will be stopped.

        Returns:
        --------
        self: :class:`ProgressEmbed`
            Class instance to allow for fluent-style chaining.
        """
        for idx, field in enumerate(self._fields):
            if predicate(field):
                del self._fields[self._fields.index(field)]
                if idx + 1 >= stop_at:
                    break
        return self

    def remove_author(self) -> ProgressEmbed:
        """``|method|``

        A method by which you can remove an author from your embed.

        Returns:
        --------
        self: :class:`ProgressEmbed`
            Class instance to allow for fluent-style chaining.
        """
        if hasattr(self, "_author"):
            del self._author  # type: ignore[attr-defined]

        return self

    def insert_field_at(self, index: int, *, name: str, value: str, inline: bool = True) -> ProgressEmbed:
        """``|method|``

        A method by which you can place a field at a specific position by index.

        Parameters:
        -----------
        index: :class:`int`
            The index of the position to which the field will be entered.

        name: :class:`str` [Keyword only]
            Name of field.

        value: :class:`str` [Keyword only]
            Value of field.

        inline: :class:`bool` = True [Keyword only]
            Inline of field.

        Returns:
        --------
        self: :class:`ProgressEmbed`
            Class instance to allow for fluent-style chaining.
        """
        self._fields.insert(index, EmbedField(name=name, value=value, inline=inline))
        return self

    def add_manipulator(
        self,
        bar: typing.Optional[_Bar] = None,
        percents: typing.Optional[_Percents] = None,
        is_left: typing.Optional[_IsLeft] = None,
        set_to: typing.Literal["description", "title", "field"] = "field",
    ) -> ProgressEmbed:
        """``|method|``

        A method by which you can add a `manipulator` to your embed,
        which will change the progress output according to your chosen settings.

        Parameters:
        -----------
        bar: :class:`typing.Optional[_Bar]` = None
            discord.ext.manipulator.BAR parameter.

        percents: :class:`typing.Optional[_Percents]` = None
            discord.ext.manipulator.PERCENTS parameter.

        is_left: :class:`typing.Optional[_IsLeft]` = None
            discord.ext.manipulator.IS_LEFT parameter.

        set_to: :class:`typing.Literal['description', 'title', 'field']` = 'field'
            The position to which progress will be set.

        Returns:
        --------
        self: :class:`ProgressEmbed`
            Class instance to allow for fluent-style chaining.

        Raises:
        -------
        :class:`errors.ManipulatorIsAlreadyExistsError`
            If the manipulator has already been installed.
        """
        if hasattr(self, "_has_manipulator"):
            raise errors.ManipulatorIsAlreadyExistsError

        setattr(self, "_progress_place", set_to)
        setattr(self, "_has_manipulator", Manipulator((bar, percents, is_left)))
        return self
