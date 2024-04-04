#!/usr/bin/env python3

# type: ignore

import sys

import angr

project = angr.Project("./crackme100")
initial_state = project.factory.entry_state()
sim = project.factory.simgr(initial_state)
sim.explore(find=0x401382, avoid=0x40138e)

if sim.found:
    sol_state = sim.found[0]
    sol = sol_state.posix.dumps(sys.stdin.fileno())
    with open("sol", "wb") as f:
        f.write(sol)
    print(sol.hex())
else:
    print("Unluck")
