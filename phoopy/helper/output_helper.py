
class OutputHelper:
    colors = {
        'default_foreground': 39,
        'black': 30,
        'red': 31,
        'green': 32,
        'yellow': 33,
        'blue': 34,
        'magenta': 35,
        'cyan': 36,
        'light_gray': 37,
        'dark_gray': 90,
        'light_red': 91,
        'light_green': 92,
        'light_yellow': 93,
        'light_blue': 94,
        'light_magenta': 95,
        'light_cyan': 96,
        'white': 97,
    }

    @staticmethod
    def colorize(text, color):
        if color in OutputHelper.colors:
            return "\033[" + str(OutputHelper.colors[color]) + "m" + text + "\033[0m"

        return text
