import binascii
import math

def lcm(a, b):
    return (a * b) // math.gcd(a, b)


# do some math with the given equation
# 12p + 4q = x
# n = 4pq -> q = n/4p

# 12p + 4(n/4p) = x -> 12p + n/p = x -> 12p² + n = xp -> 12p² - xp + n = 0

# can run this code on sagecell.sagemath.org
p = var('p')
x = int('cdb05384a055aa4753034c7e2be958fa7a9113e42ba4df378ffce215692e8d8b3efb4ffdc7bd347427fbb6c2378a91b5b31f3484563ab157c9a3704024aa5af6aec8f3ca59356093fe765c3fe037e9689d0ee39d8c08da955f357fe9ca737fbcc042dfa6d956b354f8433d0d883247a05da1880c3ac127ba5d7421f953dfaeda0', 16)
n = int('23cf4c6b0afa3f6b7e48935edfe2ebf86fe256779c59aa41235d7bea7c52da7276051b07152e8b7917cfdb2769c0915642964c80725bfc657c42f62031646b552a641f455c7c95efecf0cbf7d9100b6385ca3207f97d8f9cb7f276d83922570601c964093cd95bd5b7b416d4c6c9898bd47f2e522ad08cc33a88443e48beed135d05d441128405cb80f98e91f0cf94491a2a3328cedec85087f6a5596a27e93b767afce152f0a4e5844a8675fdb8487862ca050551a370d369c021379fe87268e92ca2d1f02ca0170e2fff94d6dd35b2cd878ba1559a781c84bffb5f6e4124362dd5f7764fa4d022a0e4d4959d402a190de36e36da70acb96245d053175c6d8b4', 16)

# this gives two solution, pick the one that has no fraction
solve(12*p^2 - x*p + n, p)

