#!/usr/bin/env python3

# type: ignore

import angr
import claripy

proj = angr.Project("./sim")

sym_arg = claripy.BVS('sym_arg', 8 * 4)

argv = [proj.filename]
argv.append(sym_arg)
initial_state = proj.factory.entry_state(args=argv)

for byte in sym_arg.chop(8):
    initial_state.solver.add(byte >= ord(' '))
    initial_state.solver.add(byte <= ord('~'))
#     initial_state.solver.add(byte >= ord('A'))
#     initial_state.solver.add(byte <= ord('Z'))
#     initial_state.solver.add(byte >= ord('a'))
#     initial_state.solver.add(byte <= ord('z'))

sim = proj.factory.simgr(initial_state)
sim.explore(find=0x000000000040113f, avoid=0x000000000040112a)

if sim.found:
    sol_state = sim.found[0]
    print(sol_state.solver.eval(sym_arg))
else:
    print("Unluck")
