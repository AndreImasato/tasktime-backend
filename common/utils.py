# pylint: disable=C0209
"""
Contains utilitaries functions
"""


class Utils:
    @classmethod
    def get_client_ip(cls, request) -> str:
        """
        Method to obtain client IP from a given
        incoming request

        Returns:
            str: IP address
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(', ')[-1].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    @classmethod
    def get_request_info(cls, request) -> tuple:
        """
        Method to obtain information from client
        incoming request

        Returns:
            tuple: tuple containing user_agent
                platform and ip_address, respectively,
                information
        """
        user_agent = request.headers.get('User-Agent')
        platform = request.headers.get('Sec-Ch-Ua-Platform')
        ip_address = cls.get_client_ip(request)
        return (user_agent, platform, ip_address)

    @classmethod
    def parse_interval(cls, interval: float) -> str:
        """
        Helper method to parse a interval to
        string format 00:00:00
        """
        hours = interval // 3600
        hours_remainder = interval % 3600
        minutes = hours_remainder // 60
        minutes_remainder = hours_remainder % 60
        parsed_interval = "{hour}:{minute}:{sec}".format(
            hour=str(hours).zfill(2),
            minute=str(minutes).zfill(2),
            sec=str(minutes_remainder).zfill(2)
        )
        return parsed_interval
