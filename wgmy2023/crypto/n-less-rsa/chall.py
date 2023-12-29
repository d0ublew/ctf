from Crypto.Util.number import getStrongPrime,bytes_to_long
from gmpy2 import next_prime
from secret import flag

def generate_secure_primes():
	p = getStrongPrime(1024)
	q = int(next_prime(p*13-37*0xcafebabe))
	return p,q

# Generate two large and secure prime numbers
p,q = generate_secure_primes()
n = p*q
e = 0x10001
phi = (p-1)*(q-1)
c = pow(bytes_to_long(flag),e,n)

print(f"{phi=}")
print(f"{e=}")
print(f"{c=}")

# Output
# phi=340577739943302989719266782993735388309601832841016828686908999285012058530245805484748627329704139660173847425945160209180457321640204169512394827638011632306948785371994403007162635069343890640834477848338513291328321869076466503121338131643337897699133626182018407919166459719722436289514139437666592605970785141028842985108396221727683676279586155612945405799488550847950427003696307451671161762595060053112199628695991211895821814191763549926078643283870094478487353620765318396817109504580775042655552744298269080426470735712833027091210437312338074255871034468366218998780550658136080613292844182216509397934480
# e=65537
# c=42363396533514892337794168740335890147978814270714150292304680028514711494019233652215720372759517148247019429253856607405178460072049996513931921948067945946086278782910016494966199807084840772350780861440737097778578207929043800432279437709296060384506082883401105820800844187947410153745248466533960754243807208804084908637481187348394987532434982032302570226378255458486161579167482667571132674473067323283939026297508548130085016660893371076973067425309491443342096329853486075971866389182944671697660246503465740169215121081002338163263904954365965203570590704089906222868145676419033148652705335290006075758484