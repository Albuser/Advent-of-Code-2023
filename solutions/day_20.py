with open("inputs/day_20.txt") as f:
    myInput = [line.strip() for line in f.readlines()]

# myInput = r"""broadcaster -> a, b, c
# %a -> b
# %b -> c
# %c -> inv
# &inv -> a""".split(
#     "\n"
# )

# myInput = r"""broadcaster -> a
# %a -> inv, con
# &inv -> b
# %b -> con
# &con -> output""".split(
#     "\n"
# )


class Module:
    def __init__(self, children, type, id):
        self.children = children
        self.type = type
        self.id = id

    def addChildren(self, children):
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
        return self.dest.handleSignal(self)

    def __repr__(self):
        return self.source.id + " -" + self.val + "-> " + self.dest.id


class Button(Module):
    def __init__(self, children, type, id):
        super().__init__(children, type, id)

    def pushButton(self):
        return super().sendSignal("LO")


class Broadcaster(Module):
    def __init__(self, children, type, id):
        super().__init__(children, type, id)
        self.children = children

    def handleSignal(self, signal):
        return super().sendSignal(signal.val)


class FlipFlop(Module):
    def __init__(self, children, type, id):
        super().__init__(children, type, id)
        self.state = False
        self.stateHash = hash(self.state)

    def handleSignal(self, signal):
        value = signal.val
        assert value in ["HI", "LO"]
        if value == "HI":
            return
        if self.state == False:
            signals = super().sendSignal("HI")
        else:
            signals = super().sendSignal("LO")
        self.state = not self.state
        self.stateHash = hash(self.state)
        return signals


class Output(Module):
    def __init__(self, type, id):
        super().__init__([], type, id)

    def handleSignal(self, signal):
        return


class Conjunction(Module):
    def __init__(self, children, type, id):
        super().__init__(children, type, id)
        self.state = {}
        self.updateStateHash()

    def allHigh(self):
        return all([val == "HI" for val in self.state.values()])

    def addChildren(self, children):
        super().addChildren(children)

    def updateStateHash(self):
        ids = [module for module in self.state.keys()]
        ids.sort(key=lambda x: x.id)
        self.stateHash = [hash(self.state[id]) for id in ids]

    def addParents(self, parents):
        for parent in parents:
            self.state[parent] = "LO"
        self.updateStateHash()

    def handleSignal(self, signal):
        self.state[signal.source] = signal.val
        self.updateStateHash()
        if self.allHigh():
            return super().sendSignal("LO")
        else:
            return super().sendSignal("HI")


def initializeModules(myInput):
    modules = {}
    for line in myInput:
        type = line[0]
        if type == "b":
            id = line.split(" ")[0]
        else:
            id = line.split(" ")[0][1:]
        if type == "%":
            modules[id] = FlipFlop([], type, id)
        elif type == "&":
            modules[id] = Conjunction([], type, id)
        else:
            modules[id] = Broadcaster([], type, id)
    modules["button"] = Button([modules["broadcaster"]], "button", "button")
    return modules


def addChildren(myInput, modules):
    for line in myInput:
        type = line[0]
        if type == "b":
            id = line.split(" ")[0]
        else:
            id = line.split(" ")[0][1:]
        childIds = line.split(" -> ")[1].split(",")
        for child in childIds:
            if child not in modules:
                modules[child] = Output("o", child)
        modules[id].addChildren([modules[child.strip()] for child in childIds])


def allModuleState(modules):
    myHash = ""
    ids = [key for key in modules.keys()]
    ids.sort()
    for id in ids:
        if modules[id].type in ["%", "&"]:
            myHash += str(modules[id].stateHash)
    return myHash


def addParents(modules):
    conjunctions = {}
    for id, module in modules.items():
        children = module.children
        for child in children:
            if child.type == "&":
                if child.id in conjunctions:
                    conjunctions[child.id].append(id)
                else:
                    conjunctions[child.id] = [id]
    for conjunction, children in conjunctions.items():
        modules[conjunction].addParents([modules[child] for child in children])


def pushButton(button):
    low = 0
    high = 0
    signals = button.pushButton()
    while len(signals) > 0:
        signal = signals.pop(0)
        # print(signal)
        if signal.val == "HI":
            high += 1
        else:
            low += 1
        newSignals = signal.process()
        if newSignals:
            signals += newSignals
    return low, high, allModuleState(modules)


# Part One
modules = initializeModules(myInput)
addChildren(myInput, modules)
addParents(modules)
button = modules["button"]

totalLow, totalHigh, state = pushButton(button)
for i in range(999):
    low, high, state = pushButton(button)
    totalLow += low
    totalHigh += high
print(totalLow * totalHigh)

# Part Two
modules = initializeModules(myInput)
addChildren(myInput, modules)
addParents(modules)
button = modules["button"]

# Find the first cycle:
# seenStates = [allModuleState(modules)]
# low, high, state = pushButton(button)
# while not state in seenStates:
#     seenStates.append(state)
#     low, high, state = pushButton(button)
# print(seenStates.index(state), len(seenStates))

# Find the first rx LOW message
indx = 1
signals = button.pushButton()
signal = signals.pop(0)
while not ((signal.dest.id == "rx") and (signal.val == "LO")):
    # print(signal.dest.id, signal.val)
    # rx is triggered by a conjunction module fed by four independent circuits
    # rx will receive 'low' after the LCM of all the cycles of those circuits
    if (signal.dest.id == "vg") and (signal.val == "LO"):
        print("VG is Low", indx)
    if (signal.dest.id == "kp") and (signal.val == "LO"):
        print("KP is Low", indx)
    if (signal.dest.id == "gc") and (signal.val == "LO"):
        print("GC is Low", indx)
    if (signal.dest.id == "tx") and (signal.val == "LO"):
        print("TX is Low", indx)
    newSignals = signal.process()
    if newSignals:
        signals += newSignals
    if len(signals) == 0:
        signals = button.pushButton()
        indx += 1
        if (indx % 50000) == 0:
            print(f"we pushed the button {indx} times...")
    signal = signals.pop(0)

print(indx)  # 238593356738827
