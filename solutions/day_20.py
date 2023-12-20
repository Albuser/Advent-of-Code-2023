with open("inputs/day_19.txt") as f:
    myInput = [line.strip() for line in f.readlines()]


class Module:
    def __init__(self, children):
        self.children = children

    def sendSignal(self, value):
        return [Signal(self, child, value) for child in self.children]


class Signal:
    def __init__(self, source, dest, val):
        assert val in ["HI", "LO"]
        self.source = source
        self.dest = dest
        self.val = val

    def process(self):
        self.dest.handleSignal(self.dest, self)


class Button(Module):
    def __init__(self, children):
        self.children = children

    def pushButton(self):
        return self.sendSignal("LO")


class Broadcaster(Module):
    def __init__(self, children):
        self.children = children

    def handleSignal(self, signal):
        return self.sendSignal(signal.val)


class FlipFlop(Module):
    def __init__(self, children):
        self.state = False
        self.children = children
        self.stateHash = hash(self.state)

    def handleSignal(self, signal):
        value = signal.val
        assert value in ["HI", "LO"]
        if value == "HI":
            return
        if self.state == False:
            signals = self.sendSignal("HI")
        else:
            signals = self.sendSignal("LO")
        self.state = not self.state
        self.stateHash = hash(self.state)
        return signals


class Conjunction(Module):
    def __init__(self, children):
        self.children = children
        self.state = {}
        for child in children:
            self.state[child] = "LO"
        self.stateHash = hash(self.state)

    def allHigh(self):
        return all([val == "HI" for val in self.state.values()])

    def handleSignal(self, signal):
        self.state[signal.source] = signal.val
        self.stateHash = hash(self.state)
        if self.allHigh():
            return self.sendSignal("LO")
        else:
            return self.sendSignal("HI")
