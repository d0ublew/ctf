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

## JSArray

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

## JSTypedArray

- 0x1c: byte_length // type size (dword)
- 0x28: length (dword) (formula = 5 + x * 8, for example if 0x13 is at offset 0x28, then length = 5 + 0x13 * 8 )
- 0x2f: external_pointer (byte)
- 0x34: base_pointer (dword)

## WasmInstanceObject

- 0x48: jump_table_start

## References

- https://github.com/rapid7/metasploit-framework/blob/master//modules/exploits/multi/browser/chrome_jscreate_sideeffect.rb
- https://starlabs.sg/blog/2022/12-deconstructing-and-exploiting-cve-2020-6418
- https://www.numencyber.com/use-wasm-to-bypass-latest-chrome-v8sbx-again/

- https://jhalon.github.io/chrome-browser-exploitation-1/
- https://blog.theori.io/a-deep-dive-into-v8-sandbox-escape-technique-used-in-in-the-wild-exploit-d5dcf30681d4
- https://anvbis.au/posts/exploring-historical-v8-heap-sandbox-escapes-i/
- https://blog.kylebot.net/2022/02/06/DiceCTF-2022-memory-hole/
- https://mgp25.com/blog/2021/browser-exploitation/
