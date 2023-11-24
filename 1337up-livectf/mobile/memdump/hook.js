Java.perform(function () {
    const MainActivity = Java.use("com.example.mynative.MainActivity");
    // const oncreate_lambda = MainActivity.onCreate$lambda$0;
    // oncreate_lambda.implementation = function (a, b) {
    //     send('oncreate_lambda ' + a + ' ' + b);
    // }
    const getBuffer = MainActivity.getBuffer;
    getBuffer.implementation = function() {
        let buf = this.getBuffer();
        send('get ' + buf);
        return buf;
    }
})
