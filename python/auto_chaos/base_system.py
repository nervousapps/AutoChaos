"""
🪐
Base system
🪐
"""
import asyncio


class BaseSystem:
    """
    Defines the base system class, all systems must inherit from this
    """

    def __init__(self) -> None:
        self.results = []
        self.errors = []

    def do_action(self, data: str) -> tuple[list[str], list[str]]:
        """
        Do the action defined in data.

        Args:
            data (str): ACTION_1 arg_1 arg_2, ACTION_2 arg_1
        """
        self.results = []
        self.errors = []
        all_tasks = []

        # Remove quotes
        if '"' in data:
            data = data.replace('"', "")
        if "'" in data:
            data = data.replace("'", "")
        # Parse the string and get the action
        if "," in data:
            datas = data.split(",")
        if "\n" in data:
            datas = data.split("\n")
        else:
            datas = [data]

        # Iterate over all actions and execute them in separate threads
        for data in datas:
            if not data:
                continue
            if data[0] == " ":
                data = data[1:]
            try:
                all_tasks.append(
                    asyncio.to_thread(
                        # Parse the action string to get the action name (corresponding to a
                        # method name in lower case in the given system) and arguments
                        getattr(self, data.split(" ")[0].lower()),
                        data.split(" ")[1:],
                    )
                )
            except AttributeError:
                pass
            except Exception as error:
                self.errors.append(error)
        asyncio.get_event_loop().run_until_complete(
            asyncio.gather(*all_tasks, return_exceptions=True)
        )
        return self.results, self.errors

    def default_action(self, args: list[str] = None):
        """
        Actions must be defined like that default action

        Args:
            args (list[str], optional): List of arguments to use. Defaults to None.
        """
        pass
