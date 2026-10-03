
class State:
    def get(self, k, d=None): return getattr(self, k, d)
ss = State()
