local dbg = require("debugger")
dbg.auto_where = 1
local table_dump = require("table_dump")
local a = string.byte
local h = string.char
local t = string.sub
local D = table.concat
local E = table.insert
local s = function(x, exp)
	return x * (2 ^ exp)
end
local C = getfenv or function()
	return _ENV
end
local G = setmetatable
local r = select
local f = unpack or table.unpack
local d = tonumber

-- LZW compression
local function F(a)
	local l, n, f = "", "", {}
	local c = 256
	local o = {}
	for e = 0, c - 1 do
		o[e] = h(e)
	end
	local e = 1

	local function i()
		local l = d(t(a, e, e), 36)
		e = e + 1
		local n = d(t(a, e, e + l - 1), 36)
		e = e + l
		return n
	end

	l = h(i())
	f[1] = l
	while e < #a do
		local e = i()
		if o[e] then
			n = o[e]
		else
			n = l .. t(l, 1, 1)
		end
		o[c] = l .. t(n, 1, 1)
		f[#f + 1], l, c = n, n, c + 1
	end
	return table.concat(f)
end

local i = F(
	"25924D27524E2752781T25R26527727827525L27C27E24D22L25K27H27E26525Q27M27E27P27D27E25N27Q2751T25P27W24D1T27G27T27522L25F28022L25G28024D25Z28825M28026525H28825J28G28A28427J27S27I1T25W28G25C28825D28G27V28N24D28S28N1T25Y28B25T2801T29628N26525E26524C24F27826S26Q24C24827826I26N26S26H26W24C23X27826026R29P26N25926H26T26W25926Z26P27026Y24N25924C24927826N26W27026X29J27826L29N29V24C24Y27826626Q26R26Y26N27026H26G2A426H29H26R26M25825925G26Q26G25626J2A126Z2B426R26X29Y2A025927226Q26N2AC27226H2A22A426Y24Z24C25327825Q2BH26N26C24X2BD2B82BN25926S26M25926R26Q2BL2BG2BI26W2BK24Z25925L2BV2592A527026S26R24Z27T24527824C24B27826M26H2AJ26Y2A927827326C29P29A27Z29228Y27I24D24N28G28I2922872CW27527226T27026N27E24F23K27823Z25P24D29F24C2782742DO2DT29F27828Z27529F2DZ24D24327624D24A24D2DQ29F24924Z2782E52DQ2E92782E22DQ25724T2DT2EG24D2AA2EE2752EL2592CN27729F27D25Z24D2772772DQ2592642EX2F329K2592542DT2EY2EM2EA27523U2E62E123Z24D2CQ23W2FE2E82FB24D2FJ2ED2FM2FD2EH2EJ29F2FR2E42FA2782FV2ER2F329F2CQ28C2F32EZ24D2F12G524D2F52F72EU2FH24D23Z2BR2G627525923N2G92CN2782AA2DV27E2772AA27I2DX2CO2782GQ2CP2CR2CT2CJ2CV2GT24D2DE2DG2DI23T27E25M2DT27E2FG2F32DQ2GJ2E32ET27E2H42GU2DU2HK2FE27I2E82DT2HE2GI2G72HI2HC2752AA2HG2HO2HZ2GR2HN2G329F2FO2F32EO2FN2HP23V2HF27E24G2G12GO2FM23Y2IB2F327I2IF2HJ2782FJ2752I02462DW2D523124I2AG27526H27027326P29Q2G324D2CJ26M26W26N26H2GZ2752CS2CU2DC24D2CY29P24C27T26M26G2732IY24D2AI2CJ2JB23O27825W26R26L26G2BL2J32AQ29Z2C426W26W26X2C326H26Q2592732A124C2412DR2H62AS2BK2J92B02GV2JC2J626L2CI26N26M27E24C26027E23Q2HP2DL2DY2KY2IU2HD2HY2KY2GT2I62FE2GG2GE2GQ2592632GE2CQ2842EC2KZ24D2CN2H42DS2CN2CN2F52752442782J524D2IT29K27I2KF2LW27E2LR2KF27I2GN2D52J52ED24O2DT29K2HG2E52DP27E2522IL27E2E52F927524B27429F23M2FE2GS2FM2MO2DQ2L929F2E527523Z24N2F32M42GO2D52L42H42HE29K2LR2HM2772LZ2HN2I02HX2HQ2NE25N2NE2GF25A2ID2EB2EM2KY23Z2NK2MA2GO25D2F324W2L82BR2MC2DR2612FW2MI27E2CN2GQ2782LR2ND2752472FE2LT2IT2LT2LQ2LU2D52MW2FE2492M82772552L82NK2772OA2MX2BR2AA2IT2782OA29K2O525O2NN2G22FX2752MZ2DQ24B24I2LJ24D2M82DQ2FP2782PB2P324D24L2OO24D2O72LS2P82LR24K2FE2PD2752PP2MT2NK2LR2OR2752EW2F92LR24B2402NN24V2FK2PG2Q52HG2MF2HL2752E52EN2LS25T2F32F22ED2PG2QI2PG2672HP25U2NN27I2IC2I22782IF2GP27E2IQ2L12O02782Q527523R2LI2PC2LI2E02MX2HW2R92NN2N527529K2LZ2HE2CQ2J52HE2NY2RB2CN2OI2HE2LR2M423Z2AM2OA2N82GF2752IT27T2HE2KF2PX2HE2Q32OV2RW2E124D2M22S624224D2Q32RB29S2E22RB2FJ2S52HE2FG2S92HE2IJ2SB2MX2AM2H929S2RB23S2OG2RB2IC2SM2FC24D2ST2S623P2IA2RB2JU2HE2S62R42SZ24D2KX2IJ2RB23L24D2S22752DK2H92SQ24D2GL2TB2MO2SV2RB2742IC2RB2582SW2S625B24D2FD2RB2NK2T42RB2ON2TR2S62F72TU2S62572T52S625624D2JU2782512782UF2E72QT2LS25L2DT2R62DV25I2GW2782UT2M52UP2HJ2E72752UW2D52V22GQ23Z2T42AA2R42HH2RC2TC2S629K2TG27I2QW2MT2L42V92HV2VB2DK2N22V027829K28Z2CQ2QB2GA2I429F29K2652L52FM2VZ2MT2BR29K2GL2MX2NK2CQ2MO2782TZ2OY2OJ2FM2662NW2VV2W62NJ2GE2DS2752WC2UQ2752QY2I0"
)

-- xor
local o = bit and bit.bxor
	or function(e, l)
		local n, o = 1, 0
		while 0 < e and 0 < l do
			local t, c = e % 2, l % 2
			if t ~= c then
				o = o + n
			end
			e, l, n = (e - t) / 2, (l - c) / 2, n * 2
		end
		if e < l then
			e = l
		end
		while 0 < e do
			local l = e % 2
			if 0 < l then
				o = o + n
			end
			e, n = (e - l) / 2, n * 2
		end
		return o
	end

local n = function(l, e, n)
	if n then
		local e = l / 2 ^ (e - 1) % 2 ^ (n - 1 - (e - 1) + 1)
		return e - e % 1
	else
		local e = 2 ^ (e - 1)
		return e <= l % (e + e) and 1 or 0
	end
end
local e = 1

local function l()
	local t, n, l, c = a(i, e, e + 3) -- i[1:4]
	t = o(t, 157)
	n = o(n, 157)
	l = o(l, 157)
	c = o(c, 157)
	e = e + 4 -- 5
	return c * 16777216 + l * 65536 + n * 256 + t
end

local function d()
	local l = o(a(i, e, e), 157) -- i[5]
	e = e + 1 -- 6
	return l
end

local function c()
	local n, l = a(i, e, e + 2) -- i[6:8]
	n = o(n, 157)
	l = o(l, 157)
	e = e + 2 -- 8
	return l * 256 + n
end

local function H()
	local o = l() -- 32
	local e = l() -- 32
	local t = 1
	local o = n(e, 1, 20) * 4294967296 + o -- 0xd9dbd9d9d9dbd
	local l = n(e, 21, 31) -- 473
	local e = (-1) ^ n(e, 32) -- -1
	if l == 0 then
		if o == 0 then
			return e * 0
		else
			l = 1
			t = 0
		end
	elseif l == 2047 then
		return o == 0 and e * (1 / 0) or e * (0 / 0)
	end
	return s(e, l - 1023) * (t + o / 4503599627370496)
end

local s = l

local function N(l)
	local n
	if not l then
		l = s() -- 32
		if l == 0 then
			return ""
		end
	end
	n = t(i, e, e + l - 1)
	e = e + l
	local l = {}
	for e = 1, #n do
		l[e] = h(o(a(t(n, e, e)), 157))
	end
	return D(l)
end

local e = l

local function s(...)
	return {
		...,
	}, r("#", ...)
end

local function F()
	local i = {}
	local t = {}
	local e = {}
	local a = {
		i,
		t,
		nil,
		e,
	}
	local e = l()
	local o = {}
	for n = 1, e do
		local l = d()
		local e
		if l == 0 then
			e = d() ~= 0
		elseif l == 3 then
			e = H()
		elseif l == 1 then
			e = N()
		end
		o[n] = e
	end
	for e = 1, l() do
		t[e - 1] = F()
	end
	a[3] = d()
	for a = 1, l() do
		local e = d()
		if n(e, 1, 1) == 0 then
			local t = n(e, 2, 3)
			local f = n(e, 4, 6)
			local e = {
				c(),
				c(),
				nil,
				nil,
			}
			if t == 0 then
				e[3] = c()
				e[4] = c()
			elseif t == 1 then
				e[3] = l()
			elseif t == 2 then
				e[3] = l() - 65536
			elseif t == 3 then
				e[3] = l() - 65536
				e[4] = c()
			end
			if n(f, 1, 1) == 1 then
				e[2] = o[e[2]]
			end
			if n(f, 2, 2) == 1 then
				e[3] = o[e[3]]
			end
			if n(f, 3, 3) == 1 then
				e[4] = o[e[4]]
			end
			i[a] = e
		end
	end
	return a
end

local function h(e, d, a)
	local n = e[1]
	local l = e[2]
	local e = e[3] -- 0
	return function(...)
		local t = n
		local D = l
		local o = e -- 0
		local i = s
		local l = 1
		local c = -1
		local C = {}
		local s = {
			...,
		}
		local F = r("#", ...) - 1 -- argc - 1
		local r = {}
		local n = {}
		for e = 0, F do
			if o <= e then
				C[e - o] = s[e + 1] -- C = argv
			else
				n[e] = s[e + 1]
			end
		end
		local e = F - o + 1
		local e, o
		while true do
			e = t[l] -- [50, 0, 26, 0]
			o = e[1] -- 50
			-- dbg()
			if o <= 46 then
				if o <= 22 then
					if o <= 10 then
						if o <= 4 then
							if o <= 1 then
								if o == 0 then
									local o = e[2]
									local t = n[o]
									local c = n[o + 2]
									if 0 < c then
										if t > n[o + 1] then
											l = e[3]
										else
											n[o + 3] = t
										end
									elseif t < n[o + 1] then
										l = e[3]
									else
										n[o + 3] = t
									end
								else
									local e = e[2]
									-- dbg()
									n[e](f(n, e + 1, c))
								end
							elseif o <= 2 then
								if n[e[2]] then
									l = l + 1
								else
									l = e[3]
								end
							elseif o == 3 then
								local l = e[2]
								-- dbg()
								return n[l](f(n, l + 1, e[3]))
							else -- o == 4
								n[e[2]] = h(D[e[3]], nil, a) -- n[1] = function with [2][0] table
							end
						elseif o <= 7 then
							if o <= 5 then
								n[e[2]] = n[e[3]][e[4]]
							elseif 6 < o then -- o == 7
								-- dbg()
								n[e[2]] = #n[e[3]]
							else
								n[e[2]] = n[e[3]][e[4]]
							end
						elseif o <= 8 then -- o == 8
							n[e[2]] = n[e[3]] - e[4] -- subtract with 65
						elseif o == 9 then
							local e = e[2]
							-- dbg()
							n[e](n[e + 1])
						else
							n[e[2]] = n[e[3]]
						end
					elseif o <= 16 then
						if o <= 13 then
							if o <= 11 then
								n[e[2]] = n[e[3]][n[e[4]]]
							elseif o == 12 then
								if n[e[2]] <= e[4] then
									l = l + 1
								else
									l = e[3]
								end
							else
								local t = e[2]
								local c = e[4]
								local o = t + 2
								-- dbg()
								local t = {
									n[t](n[t + 1], n[o]),
								}
								for e = 1, c do
									n[o + e] = t[e]
								end
								local t = t[1]
								if t then
									n[o] = t
									l = e[3]
								else
									l = l + 1
								end
							end
						elseif o <= 14 then
							local e = e[2]
							-- dbg()
							n[e] = n[e](n[e + 1])
						elseif o == 15 then
							n[e[2]] = n[e[3]] % e[4]
						else
							return
						end
					elseif o <= 19 then
						if o <= 17 then
							return
						elseif 18 < o then
							local e = e[2]
							-- dbg()
							n[e] = n[e](n[e + 1])
						elseif e[2] <= n[e[4]] then -- more than 97
							l = e[3]
						else
							l = l + 1
						end
					elseif o <= 20 then
						n[e[2]] = n[e[3]] + e[4]
					elseif o == 21 then
						local o = e[3]
						local l = n[o]
						for e = o + 1, e[4] do
							l = l .. n[e]
						end
						n[e[2]] = l
					else -- o == 22
						n[e[2]] = e[3] ~= 0
					end
				elseif o <= 34 then
					if o <= 28 then
						if o <= 25 then
							if o <= 23 then
								local e = e[2]
								return f(n, e, c)
							elseif o == 24 then
								local o
								n[e[2]] = a[e[3]] -- io
								l = l + 1
								e = t[l]
								n[e[2]] = n[e[3]][e[4]] -- io.write
								l = l + 1
								e = t[l]
								n[e[2]] = e[3]
								l = l + 1 -- 52
								e = t[l]
								o = e[2]
								-- dbg()
								n[o](n[o + 1])
								l = l + 1 -- 53
								e = t[l]
								n[e[2]] = a[e[3]]
								l = l + 1 -- 54
								e = t[l]
								n[e[2]] = n[e[3]][e[4]]
								l = l + 1 -- 55
								e = t[l]
								o = e[2]
								-- dbg()
								n[o] = n[o]()
								l = l + 1 -- 56
								e = t[l]
								n[e[2]] = n[e[3]]
								l = l + 1 -- 57
								e = t[l]
								n[e[2]] = n[e[3]]
								l = l + 1 -- 58
								e = t[l]
								o = e[2]
								-- dbg()
								n[o] = n[o](n[o + 1]) -- h([2][2])
							else
								n[e[2]] = d[e[3]]
							end
						elseif o <= 26 then
							local t = e[2]
							local c = e[4]
							local o = t + 2
							-- dbg()
							local t = {
								n[t](n[t + 1], n[o]),
							}
							for e = 1, c do
								n[o + e] = t[e]
							end
							local t = t[1]
							if t then
								n[o] = t
								l = e[3]
							else
								l = l + 1
							end
						elseif 27 < o then
							local e = e[2]
							-- dbg()
							n[e](f(n, e + 1, c))
						else -- o == 27
							local f, c, o
							n[e[2]] = {}
							l = l + 1 -- [2][2][2]
							e = t[l]
							n[e[2]] = e[3]
							l = l + 1 -- [2][2][3] => length of our input
							e = t[l]
							n[e[2]] = #n[e[3]]
							l = l + 1 -- [2][2][4]
							e = t[l]
							n[e[2]] = e[3]
							l = l + 1 -- [2][2][5]
							e = t[l]
							o = e[2]
							c = n[o]
							f = n[o + 2]
							if 0 < f then
								if c > n[o + 1] then
									l = e[3]
								else
									n[o + 3] = c
								end
							elseif c < n[o + 1] then
								l = e[3]
							else
								n[o + 3] = c
							end
						end
					elseif o <= 31 then
						if o <= 29 then
							local e = e[2]
							return f(n, e, c)
						elseif 30 < o then
							n[e[2]] = #n[e[3]]
						else -- o == 30
							local o
							n[e[2]] = n[e[3]][e[4]]
							l = l + 1 -- [2][0][26]
							e = t[l]
							n[e[2]] = n[e[3]]
							l = l + 1 -- [2][0][27]
							e = t[l]
							o = e[2]
							do
								-- dbg()
								return n[o](f(n, o + 1, e[3])) -- char
							end
							l = l + 1
							e = t[l]
							o = e[2]
							do
								return f(n, o, c)
							end
							l = l + 1
							e = t[l]
							return
						end
					elseif o <= 32 then -- o == 32
						if n[e[2]] ~= n[e[4]] then
							l = l + 1
						else
							l = e[3]
						end
					elseif 33 < o then
						local e = e[2]
						-- dbg()
						n[e](n[e + 1])
					else
						local o = e[3]
						local l = n[o]
						for e = o + 1, e[4] do
							l = l .. n[e]
						end
						n[e[2]] = l
					end
				elseif o <= 40 then
					if o <= 37 then
						if o <= 35 then -- o == 35
							n[e[2]] = e[3]
						elseif 36 < o then -- o == 37
							n[e[2]] = n[e[3]] + e[4]
							-- dbg()
						else
							return n[e[2]]
						end
					elseif o <= 38 then
						n[e[2]] = n[e[3]] - e[4]
					elseif 39 < o then -- o == 40 (0, 39, 1) => copies the 39 bytes to index 0
						local l = e[2]
						local o = n[l]
						for e = l + 1, e[3] do
							E(o, n[e])
						end
					else
						local l = e[2]
						-- dbg()
						local o, e = i(n[l](f(n, l + 1, e[3])))
						c = e + l - 1
						local e = 0
						for l = l, c do
							e = e + 1
							n[l] = o[e]
						end
					end
				elseif o <= 43 then
					if o <= 41 then -- o == 41
						n[e[2]] = h(D[e[3]], nil, a)
					elseif o == 42 then
						n[e[2]] = a[e[3]] -- table (string for [2][0])
					else -- o == 43
						n[e[2]] = d[e[3]] -- the 39 bytes stuff
					end
				elseif o <= 44 then -- o == 44
					local l = e[2]
					-- dbg()
					n[l] = n[l](f(n, l + 1, e[3]))
				elseif o == 45 then
					n[e[2]] = {}
				else -- o == 46
					l = e[3]
				end
			elseif o <= 69 then
				if o <= 57 then
					if o <= 51 then
						if o <= 48 then
							if 47 < o then -- o == 48
								if n[e[2]] <= e[4] then
									-- dbg()
									l = l + 1
								else
									-- dbg()
									l = e[3]
								end
							else -- o == 47 => (start_idx, val) // assign table[i] = [1][i][3] where i starts from start_idx until start_idx+9 (inclusive)
								n[e[2]] = e[3]
								l = l + 1
								e = t[l]
								n[e[2]] = e[3]
								l = l + 1
								e = t[l]
								n[e[2]] = e[3]
								l = l + 1
								e = t[l]
								n[e[2]] = e[3]
								l = l + 1
								e = t[l]
								n[e[2]] = e[3]
								l = l + 1
								e = t[l]
								n[e[2]] = e[3]
								l = l + 1
								e = t[l]
								n[e[2]] = e[3]
								l = l + 1
								e = t[l]
								n[e[2]] = e[3]
								l = l + 1
								e = t[l]
								n[e[2]] = e[3]
								l = l + 1
								e = t[l]
								n[e[2]] = e[3] -- l += 9
							end
						elseif o <= 49 then -- o == 49
							local l = e[2]
							-- dbg()
							return n[l](f(n, l + 1, e[3]))
						elseif 50 < o then -- o == 51
							l = e[3]
						else -- o == 50
							n[e[2]] = {} -- initializes index 0
							l = l + 1
							e = t[l] -- [0, 1, 74]
							n[e[2]] = e[3] -- n[1] == 74
							l = l + 1
							e = t[l] -- [0, 2, 80]
							n[e[2]] = e[3]
							l = l + 1
							e = t[l]
							n[e[2]] = e[3]
							l = l + 1
							e = t[l]
							n[e[2]] = e[3]
							l = l + 1
							e = t[l]
							n[e[2]] = e[3]
							l = l + 1
							e = t[l]
							n[e[2]] = e[3]
							l = l + 1
							e = t[l]
							n[e[2]] = e[3]
							l = l + 1
							e = t[l]
							n[e[2]] = e[3]
							l = l + 1
							e = t[l]
							n[e[2]] = e[3] -- l += 9
						end
					elseif o <= 54 then
						if o <= 52 then -- o == 52
							local e = e[2]
							-- dbg()
							local o, l = i(n[e](f(n, e + 1, c)))
							c = l + e - 1
							local l = 0
							for e = e, c do
								l = l + 1
								n[e] = o[l]
							end
						elseif o == 53 then
							local o = e[2]
							local c = n[o + 2]
							local t = n[o] + c
							n[o] = t
							if 0 < c then
								if t <= n[o + 1] then
									l = e[3]
									n[o + 3] = t
								end
							elseif t >= n[o + 1] then
								l = e[3]
								n[o + 3] = t
							end
						elseif n[e[2]] == n[e[4]] then
							l = l + 1
						else
							l = e[3]
						end
					elseif o <= 55 then
						local e = e[2]
						-- dbg()
						n[e] = n[e]()
					elseif o == 56 then
						if not n[e[2]] then
							l = l + 1
						else
							l = e[3]
						end
					else
						local c, o
						n[e[2]] = e[3]
						l = l + 1
						e = t[l]
						n[e[2]] = e[3]
						l = l + 1
						e = t[l]
						n[e[2]] = e[3]
						l = l + 1
						e = t[l]
						n[e[2]] = e[3]
						l = l + 1
						e = t[l]
						n[e[2]] = e[3]
						l = l + 1
						e = t[l]
						n[e[2]] = e[3]
						l = l + 1
						e = t[l]
						n[e[2]] = e[3]
						l = l + 1
						e = t[l]
						o = e[2]
						c = n[o]
						for e = o + 1, e[3] do
							E(c, n[e])
						end
					end
				elseif o <= 63 then
					if o <= 60 then
						if o <= 58 then
							local f, o, c
							n[e[2]] = e[3]
							l = l + 1
							e = t[l]
							n[e[2]] = d[e[3]]
							l = l + 1
							e = t[l]
							n[e[2]] = #n[e[3]]
							l = l + 1
							e = t[l]
							n[e[2]] = e[3]
							l = l + 1
							e = t[l]
							c = e[3]
							o = n[c]
							for e = c + 1, e[4] do
								o = o .. n[e]
							end
							n[e[2]] = o
							l = l + 1
							e = t[l]
							f = e[2]
							-- dbg()
							n[f](n[f + 1])
							l = l + 1
							e = t[l]
							n[e[2]] = e[3] ~= 0
							l = l + 1
							e = t[l]
							return n[e[2]]
						elseif o == 59 then
							n[e[2]] = e[3] ~= 0
							l = l + 1
						else
							local l = e[2]
							-- dbg()
							n[l] = n[l](f(n, l + 1, e[3]))
						end
					elseif o <= 61 then -- o == 61
						return n[e[2]]
					elseif o == 62 then
						if n[e[2]] then
							l = l + 1
						else
							l = e[3]
						end
					elseif not n[e[2]] then
						l = l + 1
					else
						l = e[3]
					end
				elseif o <= 66 then
					if o <= 64 then
						n[e[2]] = n[e[3]][n[e[4]]]
					elseif o == 65 then
						n[e[2]] = n[e[3]] % e[4] -- mod 26
					else
						n[e[2]] = e[3]
						l = l + 1
						e = t[l]
						n[e[2]] = e[3]
						l = l + 1
						e = t[l]
						n[e[2]] = e[3]
						l = l + 1
						e = t[l]
						n[e[2]] = e[3]
						l = l + 1
						e = t[l]
						n[e[2]] = e[3]
						l = l + 1
						e = t[l]
						n[e[2]] = e[3]
						l = l + 1
						e = t[l]
						n[e[2]] = e[3]
						l = l + 1
						e = t[l]
						n[e[2]] = e[3]
						l = l + 1
						e = t[l]
						n[e[2]] = e[3]
						l = l + 1
						e = t[l]
						n[e[2]] = e[3]
					end
				elseif o <= 67 then
					n[e[2]] = a[e[3]]
				elseif o == 68 then
					local a, s, h, o
					-- dbg()
					n[e[2]] = n[e[3]][e[4]] -- table.insert
					l = l + 1 -- [2][2][39]
					e = t[l]
					n[e[2]] = n[e[3]]
					l = l + 1 -- [2][2][40]
					e = t[l]
					n[e[2]] = d[e[3]]
					l = l + 1 -- [2][2][41]
					e = t[l]
					n[e[2]] = n[e[3]][n[e[4]]]
					l = l + 1 -- [2][2][42]
					e = t[l]
					n[e[2]] = n[e[3]]
					l = l + 1 -- [2][2][43]
					e = t[l]
					o = e[2]
					-- dbg()
					s, h = i(n[o](f(n, o + 1, e[3]))) -- h([2][1])
					c = h + o - 1
					a = 0
					for e = o, c do
						a = a + 1
						n[e] = s[a]
					end
					l = l + 1
					e = t[l]
					o = e[2]
					-- dbg()
					n[o](f(n, o + 1, c)) -- insert
				else
					local o = e[2]
					local c = n[o + 2]
					local t = n[o] + c
					n[o] = t
					if 0 < c then
						if t <= n[o + 1] then
							l = e[3]
							n[o + 3] = t
						end
					elseif t >= n[o + 1] then
						l = e[3]
						n[o + 3] = t
					end
				end
			elseif o <= 81 then
				if o <= 75 then
					if o <= 72 then
						if o <= 70 then -- o == 70
							-- convert input to bytes
							local d, s, h, r, o
							n[e[2]] = n[e[3]][e[4]] -- table.insert
							l = l + 1 -- [2][2][8]
							e = t[l]
							n[e[2]] = n[e[3]]
							l = l + 1 -- [2][2][9]
							e = t[l]
							n[e[2]] = a[e[3]] -- string
							l = l + 1 -- [2][2][10]
							e = t[l]
							n[e[2]] = n[e[3]][e[4]] -- string.byte
							l = l + 1 -- [2][2][11]
							e = t[l]
							o = e[2]
							r = n[e[3]]
							n[o + 1] = r
							n[o] = r[e[4]]
							l = l + 1 -- [2][2][12]
							e = t[l]
							n[e[2]] = n[e[3]]
							l = l + 1 -- [2][2][13]
							e = t[l]
							n[e[2]] = n[e[3]]
							l = l + 1 -- [2][2][14]
							e = t[l]
							o = e[2]
							-- dbg()
							s, h = i(n[o](f(n, o + 1, e[3]))) -- substring
							c = h + o - 1
							d = 0
							for e = o, c do
								d = d + 1
								n[e] = s[d]
							end
							l = l + 1 -- [2][2][15]
							e = t[l]
							o = e[2]
							-- dbg()
							s, h = i(n[o](f(n, o + 1, c))) -- string.byte
							c = h + o - 1
							d = 0
							for e = o, c do
								d = d + 1
								n[e] = s[d]
							end
							l = l + 1 -- [2][2][16]
							e = t[l]
							o = e[2]
							-- dbg()
							n[o](f(n, o + 1, c)) -- table.insert
							-- dbg()
						elseif 71 < o then
							local l = e[2]
							-- dbg()
							local t = {
								n[l](n[l + 1]),
							}
							local o = 0
							for e = l, e[4] do
								o = o + 1
								n[e] = t[o]
							end
						else
							do
								local f = D[e[3]]
								local c
								local o = {}
								c = G({}, {
									__index = function(l, e)
										local e = o[e]
										return e[1][e[2]]
									end,
									__newindex = function(n, e, l)
										local e = o[e]
										e[1][e[2]] = l
									end,
								})
								for c = 1, e[4] do
									l = l + 1
									local e = t[l]
									if e[1] == 91 then
										o[c - 1] = {
											n,
											e[3],
										}
									else
										o[c - 1] = {
											d,
											e[3],
										}
									end
									r[#r + 1] = o
								end
								n[e[2]] = h(f, c, a)
							end
						end
					elseif o <= 73 then
						n[e[2]] = e[3] ~= 0
					elseif 74 < o then
						local l = e[2]
						local o = n[l]
						for e = l + 1, e[3] do
							E(o, n[e])
						end
					else -- o == 74
						-- dbg()
						n[e[2]] = n[e[3]] + n[e[4]]
					end
				elseif o <= 78 then
					if o <= 76 then
						if n[e[2]] == n[e[4]] then
							l = l + 1
						else
							l = e[3]
						end
					elseif 77 < o then
						if e[2] <= n[e[4]] then
							l = e[3]
						else
							l = l + 1
						end
					else
						local e = e[2]
						-- dbg()
						n[e] = n[e]()
					end
				elseif o <= 79 then
					n[e[2]] = e[3] ~= 0
					l = l + 1
				elseif 80 < o then
					local o = e[2]
					-- dbg()
					local t = {
						n[o](n[o + 1]),
					}
					local l = 0
					for e = o, e[4] do
						l = l + 1
						n[e] = t[l]
					end
				else -- o == 80
					local o
					n[e[2]] = a[e[3]] -- string
					l = l + 1 -- [2][0][2]
					e = t[l]
					n[e[2]] = n[e[3]][e[4]] -- string.byte
					l = l + 1 -- [2][0][3]
					e = t[l]
					n[e[2]] = n[e[3]]
					l = l + 1 -- [2][0][4]
					e = t[l]
					o = e[2]
					-- dbg()
					n[o] = n[o](n[o + 1]) -- byte
					l = l + 1 -- [2][0][5]
					e = t[l]
					if e[2] <= n[e[4]] then
						l = e[3]
					else
						l = l + 1
					end
				end
			elseif o <= 87 then
				if o <= 84 then
					if o <= 82 then
						local e = e[2]
						-- dbg()
						local o, l = i(n[e](f(n, e + 1, c)))
						c = l + e - 1
						local l = 0
						for e = e, c do
							l = l + 1
							n[e] = o[l]
						end
					elseif 83 < o then -- o == 84
						local f = D[e[3]] -- [2][1]
						local c
						local o = {}
						c = G({}, {
							__index = function(l, e)
								local e = o[e]
								return e[1][e[2]]
							end,
							__newindex = function(n, e, l)
								local e = o[e]
								e[1][e[2]] = l
							end,
						})
						for c = 1, e[4] do
							l = l + 1
							local e = t[l]
							if e[1] == 91 then
								o[c - 1] = {
									n,
									e[3],
								}
							else
								o[c - 1] = {
									d,
									e[3],
								}
							end
							r[#r + 1] = o
						end
						n[e[2]] = h(f, c, a) -- n[2] = function with [2][1] table
					else
						n[e[2]] = n[e[3]] + n[e[4]]
					end
				elseif o <= 85 then
					local o = e[2]
					local l = n[e[3]]
					n[o + 1] = l
					n[o] = l[e[4]]
				elseif 86 < o then -- o == 87
					local o
					n[e[2]] = d[e[3]] -- lambda
					l = l + 1 -- [2][1][2]
					e = t[l]
					n[e[2]] = a[e[3]] -- string
					l = l + 1 -- [2][1][3]
					e = t[l]
					n[e[2]] = n[e[3]][e[4]] -- string.char
					l = l + 1 -- [2][1][4]
					e = t[l]
					n[e[2]] = n[e[3]]
					l = l + 1 -- [2][1][5]
					e = t[l]
					o = e[2]
					-- dbg()
					n[o] = n[o](n[o + 1]) -- char
					l = l + 1 -- [2][1][6]
					e = t[l]
					n[e[2]] = n[e[3]]
					l = l + 1 -- [2][1][7]
					e = t[l]
					o = e[2]
					-- dbg()
					n[o] = n[o](f(n, o + 1, e[3])) -- h([2][0])
					l = l + 1 -- [2][1][8]
					e = t[l]
					n[e[2]] = a[e[3]] -- string
					l = l + 1 -- [2][1][9]
					e = t[l]
					n[e[2]] = n[e[3]][e[4]] -- string.char
					l = l + 1 -- [2][1][10]
					e = t[l]
					n[e[2]] = d[e[3]]
					-- dbg()
					l = l + 1 -- [2][1][11]
					e = t[l]
					n[e[2]] = n[e[3]][n[e[4]]]
					l = l + 1 -- [2][1][12]
					e = t[l]
					o = e[2]
					-- dbg()
					n[o] = n[o](n[o + 1])
					l = l + 1 -- [2][1][13]
					e = t[l]
					-- dbg()
					if n[e[2]] == n[e[4]] then
						l = l + 1
					else
						l = e[3]
					end
				else -- o == 86
					n[e[2]] = {}
				end
			elseif o <= 90 then
				if o <= 88 then
					local l = e[2]
					-- dbg()
					local o, e = i(n[l](f(n, l + 1, e[3])))
					c = e + l - 1
					local e = 0
					for l = l, c do
						e = e + 1
						n[l] = o[e]
					end
				elseif o == 89 then
					n[e[2]] = e[3]
				elseif n[e[2]] ~= n[e[4]] then
					l = l + 1
				else
					l = e[3]
				end
			elseif o <= 91 then
				n[e[2]] = n[e[3]]
			elseif 92 < o then
				local l = e[2]
				local o = n[e[3]]
				n[l + 1] = o
				n[l] = o[e[4]]
			else -- o == 92
				local o = e[2]
				local t = n[o]
				local c = n[o + 2]
				if 0 < c then
					if t > n[o + 1] then
						l = e[3]
					else
						n[o + 3] = t
					end
				elseif t < n[o + 1] then
					l = e[3]
				else
					n[o + 3] = t
				end
			end
			l = l + 1
		end
	end
end

return h(F(), {}, C())()
