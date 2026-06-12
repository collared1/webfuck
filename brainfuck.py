import requests
import ast
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


def brainfuck(code):
    memory = memoryRegister()
    pointer = 0
    loopBeginnings = []
    index = 0
    output = []
    urlToSend = ""
    payloadToSend = ""
    token = ""
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
            memory[pointer] = output[0] if output[0] else memory[pointer]
            output.pop(0) if output[0] else None
        elif char == "?":
            urlToSend += chr(memory[pointer])
        elif char == "$":
            payloadToSend += chr(memory[pointer])
        elif char == "@":
            token += chr(memory[pointer])
        elif char == "^":
            print(f"DEBUG url={urlToSend!r} payload={payloadToSend!r} token={token!r}")
            response = requests.post(urlToSend, json=ast.literal_eval(payloadToSend), headers={"Authorization": f"Bot {token}", "Content-Type": "application/json"})
            for responseChar in response.text:
                output.append(ord(responseChar))
                print(responseChar, end="")
            payloadToSend = ""
            urlToSend = ""
        elif char == "[":
            loopBeginnings.append([index, pointer])
        elif char == "]":
            if memory[pointer]:
                index = loopBeginnings[-1][0]
            else:
                loopBeginnings.pop(-1)
        index += 1
