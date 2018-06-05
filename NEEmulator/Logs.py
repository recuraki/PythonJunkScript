

class Log(object):
    seq: int = 0
    limitCount: int = 255
    buffer: list = []

    def dp(self, log):
        if self.isdebug:
            pprint(log)

    def __init__(self, debug: bool=False):
        self.isdebug = debug
        self.resetlog()

    def setseq(self, seq: int):
        """
        ログシーケンスの初期化(reset時に使う)
        :param seq:
        :return:
        """
        self.seq = seq

    def resetlog(self):
        """
        ログバッファの初期化
        :return:
        """
        self.buffer = []
        self.setseq(0)

    def writeLog(self, msg: str, category: str = "default"):
        """
        VR内のログ記録
        :param msg: ログ本文の完全なる文字列
        :param category:
        :return:
        """
        if self.seq < self.limitCount:
            self.buffer.append({"seq": self.seq, "category": category, "msg": msg})
            self.seq = self.seq + 1
        else:
            self.dp("log limit")

    def dumpLog(self):
        """
        ログをテキストでdumpする
        :return:
        """
        out = []
        for d in self.buffer:
            out = "[{0}:{1}] {2}".format(d["seq"], d["category"], d["msg"])
        return "\n".join(out)