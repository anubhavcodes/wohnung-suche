import attr


@attr.ib
class Task:
    """A class to handle all the heavy lifting"""

    url: str = attr.ib()

    def work(self):
        pass
