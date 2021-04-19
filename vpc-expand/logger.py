import emoji


class LogColors:
    BLUE1 = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    ERROR = '\033[91m'
    NOCOLOR = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    START_ERROR = '|·| ' + '\033[91m'
    LOADING = BLUE1 + 'ººº' + NOCOLOR

class Logger:
    def __init__(self, debug_flag: bool):
        self.debug_flag = debug_flag

    def error(self, msg: str, exception: Exception):
        print(LogColors.START_ERROR+ msg + LogColors.NOCOLOR)
        if self.debug_flag:
            print('Exception: {}', exception)
