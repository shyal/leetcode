# REFERENCE: d203 Config Warning
class Solution:
    def warn(self, filename):
        buf = io.StringIO()
        handler = logging.StreamHandler(buf)
        handler.setFormatter(logging.Formatter("%(levelname)s:%(name)s:%(message)s"))
        log = logging.getLogger()
        log.addHandler(handler)
        try:
            log.warning("Warning:config file %s not found", filename)
        finally:
            log.removeHandler(handler)
        return buf.getvalue().rstrip("\n")
