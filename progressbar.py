#
# Creator - DenyS#1469
# Progressbar for discord
# This is my first module, don't judge strictly)
#

import discord

from . import progressbar_errors as errors


class DSprogressbar:

    """
    __init__ function

    [] - Required, <> - Optional

    Params:
     - [type] (get / post)
     ↳ get : Only returns a string with progressbar
     ↳ post : This parameter requires an embed,
     adds a field to the embed with progressbar

     - [now] : Progress now, used when calculating
     the progress, should not be more than [needed]

     - [needed] : The progress that is generally required
     is used to calculate the progress. Should be more than [now]

     - [embed] : (Optional if the type is "get")
     Required parameter for the "post" type, must be discord.Embed()

     - <is_left> : Shows what progress is now from the needed progress,
     set to the right of the progressbar in the format [100/1000]

     - <to_dict> : This parameter requires discord.Embed,
     returns you an embed with a progress bar in the dictionary

     - <percents> : Shows the percentage of progress made,
     set to the right of the progressbar before <is_left>, if specified

     - <field_name> : Default - "Progress", changes the name of the
     added field with a progressbar

     - <field_inline> : Default - False, changes the inline of the
     added field with a progressbar

     - <field_position> : Default - sets it as the last field in embed,
     sets the position of the field in the embed, the counting starts from 0

     - <clear_fields> : Default - False, removes all fields from
     the embed before adding a field with a progressbar
    """

    __slots__ = [
        'now',
        'type',
        'embed',
        'needed',
        'is_left',
        'to_dict',
        'percents',
        'field_name',
        'clear_fields',
        'field_inline',
        'field_position'
    ]

    def __init__(
            self,
            now: int=None,
            type: str=None,
            needed: int=None,
            to_dict: bool=False,
            is_left: bool=False,
            percents: bool=False,
            field_name: str=None,
            field_inline: bool=False,
            clear_fields: bool=False,
            field_position: int=None,
            embed: discord.Embed=None
    ):
            self.now = now
            self.type = type
            self.embed = embed
            self.needed = needed
            self.is_left = is_left
            self.to_dict = to_dict
            self.percents = percents
            self.field_name = field_name
            self.field_inline = field_inline
            self.clear_fields = clear_fields
            self.field_position = field_position

            if now is None:
                raise errors.MissingArgument('The [now] argument was expected')

            if now is not None:
                if not isinstance(self.now, int):
                    raise TypeError('The [now] argument must be integer')

            if needed is None:
                raise errors.MissingArgument('The [needed] argument was expected')

            if needed is not None:
                if not isinstance(self.needed, int):
                    raise TypeError('The [needed] argument must be integer')

            if type is None:
                raise errors.MissingArgument('The [type] argument was expected (post / get)')

            if type is not None and type not in ['post', 'get']:
                raise errors.BadType('Expected [post] or [get]')

            if embed is None and type == 'post':
                raise errors.MissingArgument('Specify the embed to which you want to add a field with progress')

            if embed is not None and type == 'post':
                if not isinstance(self.embed, discord.Embed): # checks if embed is valid
                    raise errors.BadEmbed('The specified is incorrect embed, must be discord.Embed()')

            if isinstance(self.embed, discord.Embed) and len(self.embed.fields) + 1 > 24:
                raise errors.TooManyFields('The number of fields in your embed cannot exceed 24')

            if field_position is not None:
                if not isinstance(self.field_position, int):
                    raise TypeError('the argument <field_position> must be integer')

            if field_position is not None and field_position > 25:
                raise errors.TooLargeArgument('The value specified is too high')

            if now > needed:
                raise errors.ProgressError('[now] cannot be greater than what is [needed]')


    async def progress(self, line=None, fill=None) -> str:
        """
        Function for simpler calls

        If you do not specify characters for filling, then
        ↳ line default is ":black_large_square:"
        ↳ fill default is ":red_square:"

        Params:
        - line : the character or string that will be a line
        that we will fill in as progress increases

        - fill : the character or string that will fill the
        line as progress increases
        """
        return await self._write_progress(to_line=line, to_fill=fill)


    async def _write_progress(self, to_line=None, to_fill=None) -> str:
        """
        Protected method that checks the return type
        of the progressbar and characters for None

        Params:
        - to_line : the character that will be the string to fill
        - to_fill : the character with which we will fill the string
        """

        to_line = ':black_large_square:' if to_line is None else to_line
        to_fill = ':red_square:' if to_fill is None else to_fill

        progressline = await self.__calculate_progress(to_line=to_line, to_fill=to_fill)
        if self.type == 'get':
            return progressline
        else:
            return await self._embed_checker(progressline=progressline)


    async def __calculate_progress(self, to_line, to_fill) -> str:
        """
        Private method for calculating the progress bar

        Params:
        - to_line : the character that will be the string to fill
        - to_fill : the character with which we will fill the string
        """

        procent_bar = round(self.now/self.needed * 100)
        progressbar = ""

        for i in range(round(procent_bar / 5)):
            progressbar += to_fill

        for i in range(20 - round(procent_bar / 5)):
            progressbar += to_line

        return progressbar


    async def _embed_checker(self, progressline):
        """
        Protected method that adds embed to us by checking for parameters

        Params:
        - progressline : The progressbar that we transfer in order
        to fold the embed and return the final version
        """
        name = self.field_name if self.field_name is not None else 'Progress'

        if self.clear_fields:
            self.embed.clear_fields()

        if await self.__check_params():
            value = progressline

        if self.percents and self.percents is not None:
            _percents = round((self.now/self.needed) * 100)
            value = f"{progressline} {_percents}%"

            if self.is_left and self.is_left is not None:
                _is_left = f"{self.now}/{self.needed}"
                value = f"{progressline} {_percents}% [{_is_left}]"

        elif (self.is_left and self.is_left is not None
            and not self.percents is None and self.percents is None):

            _is_left = f"{self.now}/{self.needed}"
            value = f"{progressline} [{_is_left}]"

        if self.field_position is not None:
            self.embed.insert_field_at(
                index=self.field_position,
                name=name,
                value=value,
                inline = self.field_inline
            )
        else:
            self.embed.add_field(
                name=name,
                value=value,
                inline = self.field_inline
            )

        if self.to_dict:
            return self.embed.to_dict()

        return self.embed


    async def __check_params(self):
        """
        A private method that checks for 2 params - is_left,
        percents and if one of them is specified, returns True
        """
        if self.is_left is None and self.percents is None:
            return False
        return True
