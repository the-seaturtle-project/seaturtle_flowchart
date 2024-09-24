import re
import pathlib
from collections.abc import Callable
from typing import Any, Optional

class STFCReader:
    """This is an object that parses Seaturtle Flowchart files, which have the ``.stfc`` extension.

    :param filename: The path to target the ``.stfc`` file.
    :type filename: str | pathlib.Path
    """

    METADATA_PATTERN = re.compile(r"^\s*--meta \"(.+?)\" \"(.+?)\"\n*")

    def __init__(self, filename: str | pathlib.Path) -> None:
        """Constructor method"""

        self.filename = filename

    def requires_file_inline(self) -> None:
        """Method similar to :py:meth:`STFCReader.requires_file`, except it is a function instead of a decorator. Checks if the specified :py:attr:`STFCReader.filename` is a valid file.

        :raises FileNotFoundError: If the specified filepath is not found.
        """
        if not pathlib.Path(self.filename).is_file():
            raise FileNotFoundError(f"The given file path {self.filename!r} does not lead to a valid file")

    def requires_file(func) -> Callable[["STFCReader", Optional[tuple[Any, ...]], Optional[dict[str, Any]]], Any]:
        """A decorator used to ensure errors aren't thrown in the middle of processing an operation in case the specified :py:attr:`.STFCReader.filename` does not exist or is not a file.

        :param func: The function before which file existance check is carried out.
        :type func: Callable[[:py:class:`.STFCReader`, Optional[tuple[Any, ...]], Optional[dict[str, Any]]], Any]

        :return: A wrapper function around the target function `func`.
        :rtype: Callable[[:py:class:`.STFCReader`, Optional[tuple[Any, ...]], Optional[dict[str, Any]]], Any]
        """

        def wrapper(self, *args, **kwargs) -> Any:
            STFCReader.requires_file_inline()

            return func(self, *args, **kwargs)

        return wrapper

    @property
    def metadata(self) -> dict:
        """
        :getter: Returns a dict of the metadata held in the file.
        :type: dict[str, str]
        """
        self.requires_file_inline()

        _metadata = {}

        with open(self.filename, 'r') as stfc:
            for line in stfc.readlines():
                if result := re.findall(STFCReader.METADATA_PATTERN, line):
                    label, value = result[0]
                    _metadata[label.lower()] = value

        return _metadata


