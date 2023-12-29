c1 = "YbfPGS";
c2 = "arkg_";
c2 += "gvzr_";
c2 += "hfr_";
c2 += "qbhoyr_ebg13";
c = c1;
c += "{";
c += c2;
c += "}";
p = c.replace(/[a-zA-Z]/g,function(c){return String.fromCharCode((c<="Z"?90:122)>=(c=c.charCodeAt(0)+13)?c:c-26);});
console.log(p)
