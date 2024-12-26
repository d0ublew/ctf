let correct_ans = null;
let eqs = null;
const count = 0;
let home_instance = null;
const Intent = Java.use("android.content.Intent");
const jstring_arr = Java.use("[Ljava.lang.String;");
setTimeout(() => {
	Java.perform(() => {
		const e = Java.use("d2.e");
		e.$init.implementation = (h) => {
			console.log("[+] e init");
		};
		const HomeActivity = Java.use("com.intigriti.quiz.HomeActivity");
		Java.choose("com.intigriti.quiz.MainActivity", {
			onMatch: (instance) => {
				console.log("[+] Found MainActivity");
				const intent = Intent.$new(instance, HomeActivity.class);
				instance.startActivity(intent);
				setTimeout(() => {
					solve();
				}, 500);
			},
			onComplete: (instance) => {},
		});
	});
}, 1000);

function debug() {
	console.log(correct_ans.value);

	console.log(eqs.value.length);
	console.log(count);
}

function solve() {
	console.log("[+] home");
	Java.choose("com.intigriti.quiz.HomeActivity", {
		onMatch: (instance) => {
			console.log("[+] Found HomeActivity");
			home_instance = instance;
			correct_ans = instance.D;
			eqs = instance.E;
			setTimeout(() => {
				solve2();
			}, 3000);
		},
		onComplete: (instance) => {},
	});
}

function solve2() {
	//if (eqs.value === null) {
	//	console.log("Eqs not found");
	//	return;
	//}
	//count = eqs.value.length;
	console.log("[+] Solve part 2");
	home_instance["t"].implementation = function (i3) {
		console.log(`HomeActivity.t is called: i3=${correct_ans.value}`);
		this["t"](correct_ans.value);
	};
	for (let i = 0; i < eqs.value.length; i++) {
		console.log(i);
		setTimeout(() => {
			try {
				home_instance.t(correct_ans.value);
			} catch {}
		}, 50);
	}
}

function solve3() {
	home_instance.t(correct_ans.value);
}
