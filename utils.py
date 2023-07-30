class Logging:
    verboseMode = False

    @classmethod
    def log_info(cls, msg):
        if cls.verboseMode:
            print(f"INFO: {msg}", end="")

    @classmethod
    def log_warn(cls, msg):
        if cls.verboseMode:
            print(f"WARN: {msg}", end="")

    @staticmethod
    def log_crit(msg):
        print(f"CRITICAL: {msg}", end="")
        exit(3)


def setLogging(new_val):
    Logging.verboseMode = new_val


log = {0: Logging.log_info, 1: Logging.log_warn, 2: Logging.log_crit}
