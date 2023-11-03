function chall01_solver() {
    const challenge_01 = Java.use("uk.rossmarks.fridalab.challenge_01");
    challenge_01.chall01.value = 1;
    // send('set challenge_01.chall01 = 1', [0xde, 0xad, 0xbe, 0xef])
    send('set challenge_01.chall01 = 1');
}

function chall02_solver() {
    Java.choose("uk.rossmarks.fridalab.MainActivity", {
        onMatch: function (instance) {
            instance.chall02();
            send("invoked MainActivity.chall02");
        },
        onComplete: function () {},
    });
}

function chall03_solver() {
    const MainActivity = Java.use("uk.rossmarks.fridalab.MainActivity");
    const chall03 = MainActivity.chall03;
    chall03.implementation = function () {
        send('hooked chall03');
        return true;
    }
}

function chall04_solver() {
    Java.choose("uk.rossmarks.fridalab.MainActivity", {
        onMatch: function (instance) {
            instance.chall04("frida");
            send("invoked MainActivity.chall04('frida')");
        },
        onComplete: function () {},
    });
}

function chall05_solver() {
    const MainActivity = Java.use("uk.rossmarks.fridalab.MainActivity");
    const chall05 = MainActivity.chall05;
    chall05.implementation = function (str) {
        send('chall05("' + str + '") is called');
        // chall05.call(this, 'frida'); // this also works
        this.chall05('frida'); // this also works
    }
}

function chall06_solver() {
    const challenge_06 = Java.use("uk.rossmarks.fridalab.challenge_06");
    const addChall06 = challenge_06.addChall06;
    addChall06.implementation = function (i) {
        send('addChall06(' + i + ') is called', [i]);
        this.addChall06(i);
    }
    recv('chall06_solver', function onMessage(data) {
        // const i = data.arg
        const i = challenge_06.chall06.value
        Java.choose("uk.rossmarks.fridalab.MainActivity", {
            onMatch: function (instance) {
                instance.chall06(i);
                send(`invoked MainActivity.chall06(${i})`);
            },
            onComplete: function () {},
        });

    })
}

function chall07_solver() {
    const challenge_07 = Java.use("uk.rossmarks.fridalab.challenge_07");
    // send('Target PIN: ' + challenge_07.chall07.value);
    let pin = 0;
    for (let i = 1000; i <= 10000; i++) {
        if (challenge_07.check07Pin(i.toString())) {
            send('Found PIN: ' + i);
            pin = i;
            break;
        }
    }
    Java.choose("uk.rossmarks.fridalab.MainActivity", {
        onMatch: function (instance) {
            instance.chall07(pin.toString());
        },
        onComplete: function () {},
    });
}

function chall08_solver() {
    const button = Java.use('android.widget.Button');
    let checkHandle;
    Java.choose("uk.rossmarks.fridalab.MainActivity", {
        onMatch: function (instance) {
            checkHandle = instance.findViewById(2131165231);
        },
        onComplete: function () {},
    });
    const checkButton = Java.cast(checkHandle, button);
    Java.scheduleOnMainThread(function () {
        const string = Java.use("java.lang.String")
        checkButton.setText(string.$new('Confirm'))
    })
}

Java.perform(function () {
    chall01_solver();
    chall02_solver();
    chall03_solver();
    chall04_solver();
    chall05_solver();
    chall06_solver();
    chall07_solver();
    chall08_solver();
})
