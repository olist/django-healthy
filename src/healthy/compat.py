try:
    from typing import Self
except ImportError:
    from typing_extensions import Self

try:
    from typing import override
except ImportError:
    from typing_extensions import override

try:
    from enum import StrEnum
except ImportError:
    from enum import Enum

    class StrEnum(str, Enum):
        pass


__all__ = [
    "Self",
    "override",
    "StrEnum",
]
