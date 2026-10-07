# REFERENCE: d289 Order Status From Events
class Solution:
    def __init__(self):
        self.last_seq = {}
        self.open = {}
        self.state = {}
        self.owner = {}
        self.total = defaultdict(int)

    def apply(self, seq, order_id, user, kind, qty):
        if seq <= self.last_seq.get(order_id, 0):
            return False
        self.last_seq[order_id] = seq
        self.owner.setdefault(order_id, user)
        before = self.open.get(order_id, 0)
        if kind == "NEW":
            after = qty
            self.state[order_id] = "open"
        elif kind == "PARTIAL":
            after = max(before - qty, 0)
            self.state[order_id] = "open"
        elif kind == "FILLED":
            after = 0
            self.state[order_id] = "filled"
        else:
            after = 0
            self.state[order_id] = "cancelled"
        self.open[order_id] = after
        self.total[self.owner[order_id]] += after - before
        return True

    def status(self, order_id):
        return self.state.get(order_id)

    def exposure(self, user):
        return self.total.get(user, 0)
