# Notes

## Setup

```sh
git clone https://chromium.googlesource.com/chromium/tools/depot_tools.git
export PATH=/path/to/depot_tools:$PATH
fetch v8
cd v8
./build/install-build-deps.sh
git checkout 970c2bf28dd
git apply v8.patch
gclient sync
./tools/dev/v8gen.py x64.debug
ninja -C ./out.gn/x64.debug
cd ./out.gn/x64.debug
./d8 --allow-natives-syntax  # %DebugPrint, %SystemBreak
./d8 --shell ./script.js  # go into interactive mode after executing script.js
```

## Type Confusion Bug Analysis

- do `%DebugPrint(float_rel)` to get started and look around and notice elements of `a`
- `0x338c005c4334` is elements of `a` after its type changes from `PACKED_DOUBLE_ELEMENTS` to `PACKED_ELEMENTS`
- `0x000006e9` is `the_hole_value`
- when `0x1337133700010000` is pushed to `a` as 26th elements, this `push` operation still sees `a` as `PACKED_DOUBLE_ELEMENTS`
- hence, `0x1337133700010000` is inserted @ `0x338c005c4404`
- notice that `0x338c005c43f8` is the address of `float_rel` and `0x338c005c4404` is the `length` field
- therefore, 

```text
0x338c005c4334|+0x0000|+000: 0x0000003400000565
0x338c005c433c|+0x0008|+001: 0x000006e9005c4319
0x338c005c4344|+0x0010|+002: 0x000006e9000006e9
0x338c005c434c|+0x0018|+003: 0x000006e9000006e9
0x338c005c4354|+0x0020|+004: 0x000006e9000006e9
0x338c005c435c|+0x0028|+005: 0x000006e9000006e9
0x338c005c4364|+0x0030|+006: 0x000006e9000006e9
0x338c005c436c|+0x0038|+007: 0x000006e9000006e9
0x338c005c4374|+0x0040|+008: 0x000006e9000006e9
0x338c005c437c|+0x0048|+009: 0x000006e9000006e9
0x338c005c4384|+0x0050|+010: 0x000006e9000006e9
0x338c005c438c|+0x0058|+011: 0x000006e9000006e9
0x338c005c4394|+0x0060|+012: 0x005c43b1000006e9  # 0x5c43b1 is HeapNumber 0x4018666666666666 (6.1)
0x338c005c439c|+0x0068|+013: 0x000006e9005c43bd  # 0x5c43bd is HeapNumber 0x401c666666666666 (7.1)
0x338c005c43a4|+0x0070|+014: 0x9999999a000007b1
0x338c005c43ac|+0x0078|+015: 0x000007b13fb99999
0x338c005c43b4|+0x0080|+016: 0x4018666666666666
0x338c005c43bc|+0x0088|+017: 0x66666666000007b1
0x338c005c43c4|+0x0090|+018: 0x00000851401c6666
0x338c005c43cc|+0x0098|+019: 0x9999999a0000000a
0x338c005c43d4|+0x00a0|+020: 0x9999999a3fb99999
0x338c005c43dc|+0x00a8|+021: 0xcccccccd3ff19999
0x338c005c43e4|+0x00b0|+022: 0xcccccccd4000cccc
0x338c005c43ec|+0x00b8|+023: 0x666666664008cccc
0x338c005c43f4|+0x00c0|+024: 0x0018efb140106666
0x338c005c43fc|+0x00c8|+025: 0x005c4411000006cd
0x338c005c4404|+0x00d0|+026: 0x000010850000000a
0x338c005c440c|+0x00d8|+027: 0x0000085100ce797d
0x338c005c4414|+0x00e0|+028: 0x9999999a0000000a
0x338c005c441c|+0x00e8|+029: 0x9999999a3fb99999
```

`float_rel`

```text
0x338c005c43f8|+0x0000|+000: 0x000006cd0018efb1
0x338c005c4400|+0x0008|+001: 0x0000000a005c4411
0x338c005c4408|+0x0010|+002: 0x00ce797d00001085
0x338c005c4410|+0x0018|+003: 0x0000000a00000851
0x338c005c4418|+0x0020|+004: 0x3fb999999999999a  # 0.1
0x338c005c4420|+0x0028|+005: 0x3ff199999999999a  # 1.1
0x338c005c4428|+0x0030|+006: 0x4000cccccccccccd  # 2.1
0x338c005c4430|+0x0038|+007: 0x4008cccccccccccd  # 3.1
0x338c005c4438|+0x0040|+008: 0x4010666666666666  # 4.1
0x338c005c4440|+0x0048|+009: 0x0000000200000851
```

## References

- https://github.com/rapid7/metasploit-framework/blob/master//modules/exploits/multi/browser/chrome_jscreate_sideeffect.rb
- https://starlabs.sg/blog/2022/12-deconstructing-and-exploiting-cve-2020-6418
- https://www.numencyber.com/use-wasm-to-bypass-latest-chrome-v8sbx-again/

- https://v8.github.io/api/head/
- https://v8.dev/blog/pointer-compression
- https://mem2019.github.io/jekyll/update/2022/02/06/DiceCTF-Memory-Hole.html
- https://docs.google.com/document/d/1HSap8-J3HcrZvT7-5NsbYWcjfc0BVoops5TDHZNsnko/edit#heading=h.suker1x4zgzz
- https://jhalon.github.io/chrome-browser-exploitation-1/
- https://blog.theori.io/a-deep-dive-into-v8-sandbox-escape-technique-used-in-in-the-wild-exploit-d5dcf30681d4
- https://anvbis.au/posts/exploring-historical-v8-heap-sandbox-escapes-i/
- https://blog.kylebot.net/2022/02/06/DiceCTF-2022-memory-hole/
- https://mgp25.com/blog/2021/browser-exploitation/
- https://faraz.faith/2019-12-13-starctf-oob-v8-indepth/
- https://v8.dev/blog/elements-kinds

## Appendix

### JSArray

```console
d8> %DebugPrint(arr)
DebugPrint: 0x19b5001cb6c9: [JSArray]
 - map: 0x19b5000ce6b1 <Map[16](PACKED_SMI_ELEMENTS)> [FastProperties]
 - prototype: 0x19b5000ce925 <JSArray[0]>
 - elements: 0x19b5000dac01 <FixedArray[5]> [PACKED_SMI_ELEMENTS (COW)]
 - length: 5
 - properties: 0x19b5000006cd <FixedArray[0]>
 - All own properties (excluding elements): {
    0x19b500000d41: [String] in ReadOnlySpace: #length: 0x19b50030f6f9 <AccessorInfo name= 0x19b500000d41 <String[6]: #length>, data= 0x19b500000061 <undefined>> (const accessor descriptor), location: descriptor
 }
 - elements: 0x19b5000dac01 <FixedArray[5]> {
           0: 0
           1: 1
           2: 2
           3: 3
           4: 4
 }
0x19b5000ce6b1: [Map] in OldSpace
 - map: 0x19b5000c3c29 <MetaMap (0x19b5000c3c79 <NativeContext[285]>)>
 - type: JS_ARRAY_TYPE
 - instance size: 16
 - inobject properties: 0
 - unused property fields: 0
 - elements kind: PACKED_SMI_ELEMENTS
 - enum length: invalid
 - back pointer: 0x19b500000061 <undefined>
 - prototype_validity cell: 0x19b500000a31 <Cell value= 1>
 - instance descriptors #1: 0x19b5000cef3d <DescriptorArray[1]>
 - transitions #1: 0x19b5000cef59 <TransitionArray[4]>Transition array #1:
     0x19b500000e05 <Symbol: (elements_transition_symbol)>: (transition to HOLEY_SMI_ELEMENTS) -> 0x19b5000cef71 <Map[16](HOLEY_SMI_ELEMENTS)>

 - prototype: 0x19b5000ce925 <JSArray[0]>
 - constructor: 0x19b5000ce61d <JSFunction Array (sfi = 0x19b500335da5)>
 - dependent code: 0x19b5000006dd <Other heap object (WEAK_ARRAY_LIST_TYPE)>
 - construction counter: 0

[0, 1, 2, 3, 4, ]
```

```text
map
prototype
elements
length
```

```text
0x19b5001cb6c8|+0x0000|+000: 0x000006cd000ce6b1
0x19b5001cb6d0|+0x0008|+001: 0x0000000a000dac01
0x19b5001cb6d8|+0x0010|+002: 0x000006cd000cf031
0x19b5001cb6e0|+0x0018|+003: 0x0000000c001cb705
```

- map_ptr = (DWORD)0x19b5001cb6c8
- prototype_ptr = (DWORD)0x19b5001cb6cc
- elements_ptr = (DWORD)0x19b5001cb6d0
- length = (*0x19b5001cb6d4) >> 1

### JSTypedArray

- 0x1c: byte_length // type size (dword)
- 0x28: length (dword) (formula = 5 + x * 8, for example if 0x13 is at offset 0x28, then length = 5 + 0x13 * 8 )
- 0x2f: external_pointer (byte)
- 0x34: base_pointer (dword)

### WasmInstanceObject

- 0x48: jump_table_start
