import requests
import json
class WebfuckError(Exception):
    pass
class memoryRegister:
    def __init__(self):
        self._pos = []
        self._neg = []

    def __getitem__(self, index: int):
        if index >= 0:
            if index >= len(self._pos):
                self._pos.extend([0] * (index - len(self._pos) + 1))
            return self._pos[index]
        else:
            neg_i = -index - 1
            if neg_i >= len(self._neg):
                self._neg.extend([0] * (neg_i - len(self._neg) + 1))
            return self._neg[neg_i]

    def __setitem__(self, index: int, value):
        if index >= 0:
            if index >= len(self._pos):
                self._pos.extend([0] * (index - len(self._pos) + 1))
            self._pos[index] = value
        else:
            neg_i = -index - 1
            if neg_i >= len(self._neg):
                self._neg.extend([0] * (neg_i - len(self._neg) + 1))
            self._neg[neg_i] = value

    def __repr__(self):
        neg_part = list(reversed(self._neg))
        return f"memoryRegister(... {neg_part} | {self._pos} ...)"


def webfuck(code):
    memory = memoryRegister()
    pointer = 0
    loopBeginnings = []
    index = 0
    output = []
    urlToSend = ""
    payloadToSend = ""
    token = ""
    functions = []
    recentIndices = []
    while index < len(code):
        char = code[index]
        if char == ">" or char == "<":
            pointer += 1 if char == ">" else -1
        elif char == "+" or char == "-":
            memory[pointer] += 1 if char == "+" else -1
            if memory[pointer] < 0:
                memory[pointer] = 255
            memory[pointer] = memory[pointer] % 256
        elif char == ".":
            print(chr(memory[pointer]), end="")
        elif char == ",":
            if output:
                memory[pointer] = output[0]
                output.pop(0)
        elif char == "?":
            urlToSend += chr(memory[pointer])
        elif char == "$":
            payloadToSend += chr(memory[pointer])
        elif char == "@":
            token += chr(memory[pointer])
        elif char == "^":
            print(f"DEBUG url={urlToSend!r} payload={payloadToSend!r} token={token!r}")
            response = requests.post(urlToSend, json=json.loads(payloadToSend), headers={"Authorization": f"Bot {token}", "Content-Type": "application/json"})
            for responseChar in response.text:
                output.append(ord(responseChar))
                print(responseChar, end="")
            payloadToSend = ""
            urlToSend = ""
            token = ""
        elif char == "[":
            if not index in loopBeginnings:
                loopBeginnings.append(index)
        elif char == "]":
            if memory[pointer]:
                index = loopBeginnings[-1]
            else:
                loopBeginnings.pop(-1)
        elif char == "{":
            if not any(index in sublist for sublist in functions):
                functions.append([index])
        elif char == "}":
            if not any(index in sublist for sublist in functions):
                functions[-1].append(index)
            else:
                index = recentIndices[-1]
                recentIndices.pop(-1)
        elif char == "!":
            recentIndices.append(index)
            if memory[pointer] >= len(functions):
                raise WebfuckError("You cannot call a function without said function being defined.")
            else:
                index = functions[memory[pointer]][0]
        index += 1

def generateTestWebfuck(url, payload):
    webfuck = ""
    for char in url:
        webfuck += "[-] "
        for i in range(ord(char)):
            webfuck += "+"
        webfuck += " ?\n"
    for char in payload:
        webfuck += "[-] "
        for i in range(ord(char)):
            webfuck += "+"
        webfuck += " $\n"

    webfuck += "^"
    print(webfuck)
