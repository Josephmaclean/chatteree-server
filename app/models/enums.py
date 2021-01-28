import enum


class MessageTypeEnum(str, enum.Enum):
    text = 1
    images = 3
    audio = 2
    video = 4
    document = 5
