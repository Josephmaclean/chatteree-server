import abc


class EmailServiceInterface(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, "send_mail")
            and callable(subclass.send_mail)
            or NotImplemented
        )

    @abc.abstractmethod
    def send_mail(self, email: str, subject: str, message: str):
        """
        Send email
        """
        raise NotImplementedError
