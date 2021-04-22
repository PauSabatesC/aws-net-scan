import traceback


class LogColors:
    BLUE1 = '\033[95m'
    BLUE2 = '\033[96m'
    SUCCESS = '\033[92m'
    WARNING = '\033[93m'
    ERROR = '\033[91m'
    NOCOLOR = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    START_ERROR = ERROR + '|X| '
    START_WARNING = WARNING + '|·| '
    START_INFO = BLUE2 + '|·| '
    START_TITLE = WARNING + '  |·'
    START_SUBTITLE = BLUE1 + '  |·'
    START_SUBTITLE_2 = BLUE2 + '  |·'
    START_DEBUG = BLUE2 + '|DEBUG| '
    START_SUCCESS = SUCCESS + '|·| '
    LOADING = BLUE1 + 'ººº' + NOCOLOR
    INTERSECTION = ERROR + ' · '


class Logger:
    def __init__(self, debug_flag: bool):
        self.debug_flag = debug_flag

    def error(self, msg: str, exception: Exception = None):
        print(LogColors.START_ERROR + msg + LogColors.NOCOLOR)
        if self.debug_flag and exception:
            print('Exception: ', exception)
            print('Trace: ')
            traceback.print_exc()

    def error_and_exit(self, msg: str, exception: Exception = None):
        print(LogColors.START_ERROR + msg + LogColors.NOCOLOR)
        if self.debug_flag and exception:
            print('Exception: ', exception)
            print('Trace: ')
            traceback.print_exc()
        exit(1)

    def warn(self, msg: str, exception: Exception = None):
        print(LogColors.START_WARNING + msg + LogColors.NOCOLOR)
        if self.debug_flag and exception:
            print('Exception: ', exception)

    def info(self, msg: str, exception: Exception = None):
        print(LogColors.START_INFO + msg + LogColors.NOCOLOR)
        if self.debug_flag and exception:
            print('Exception: ', exception)

    def success(self, msg: str, exception: Exception = None):
        print(LogColors.START_SUCCESS + msg + LogColors.NOCOLOR)
        if self.debug_flag and exception:
            print('Exception: ', exception)

    def debug(self, msg: str, exception: Exception = None):
        if self.debug_flag:
            print(LogColors.START_DEBUG + msg + LogColors.NOCOLOR)
            if self.debug_flag and exception:
                print('Exception: ', exception)

    def loading(self, msg: str):
        print(LogColors.LOADING + msg + LogColors.NOCOLOR, end='', flush=True)

