def exrypz(computer):
	# new format
	if '-' in computer and len(computer) >= 8:
		floor = computer.split('r')[0]
		row = computer.split('r')[1].split('s')[0]
		seat = computer.split('s')[1]
		res = {"building": computer.split('-')[0], "p_sep": "s", "etage": floor, "range": row,
		       "place": seat}
		return res
	# old format
	if len(computer) >= 6:
		res = {"building": "main", "p_sep": "p", "etage": computer.split('r')[0],
		       "range": computer.split('r')[1].split('p')[0],
		       "place": computer.split('p')[1]}
		return res
	return False


# @formatter:off
map = {
	"bess-f1": [
		['R1', 'R2', 'R3', 'R4', 'R5', 'R6'],
		['bess-f1r1s1', 'bess-f1r1s2', 'bess-f1r1s3', 'bess-f1r1s4', 'bess-f1r1s5', 'bess-f1r1s6', 'bess-f1r1s7', 'bess-f1r1s8', '', 'bess-f1r1s9', 'bess-f1r1s10', 'bess-f1r1s11', 'bess-f1r1s12', 'bess-f1r1s13', 'bess-f1r1s14', ''],
		['', 'bess-f1r2s1', 'bess-f1r2s2', 'bess-f1r2s3', 'bess-f1r2s4', 'bess-f1r2s5', 'bess-f1r2s6', '', '', 'bess-f1r2s7', 'bess-f1r2s8', 'bess-f1r2s9', 'bess-f1r2s10', 'bess-f1r2s11', 'bess-f1r2s12', ''],
		['bess-f1r3s1', 'bess-f1r3s2', 'bess-f1r3s3', 'bess-f1r3s4', 'bess-f1r3s5', 'bess-f1r3s6', 'bess-f1r3s7', 'bess-f1r3s8', '', 'bess-f1r3s9', 'bess-f1r3s10', 'bess-f1r3s11', 'bess-f1r3s12', 'bess-f1r3s13', 'bess-f1r3s14', ''],
		['bess-f1r4s1', 'bess-f1r4s2', 'bess-f1r4s3', 'bess-f1r4s4', 'bess-f1r4s5', 'bess-f1r4s6', 'bess-f1r4s7', '', '', 'bess-f1r4s8', 'bess-f1r4s9', 'bess-f1r4s10', 'bess-f1r4s11', 'bess-f1r4s12', 'bess-f1r4s13', 'bess-f1r4s14'],
		['', 'bess-f1r5s1', 'bess-f1r5s2', 'bess-f1r5s3', 'bess-f1r5s4', 'bess-f1r5s5', 'bess-f1r5s6', 'bess-f1r5s7', '', 'bess-f1r5s8', 'bess-f1r5s9', 'bess-f1r5s10', 'bess-f1r5s11', 'bess-f1r5s12', 'bess-f1r5s13', ''],
		['', '', '', '', '', '', '', '', '', 'bess-f1r6s1', 'bess-f1r6s2', 'bess-f1r6s3', 'bess-f1r6s4', 'bess-f1r6s5', 'bess-f1r6s6', '']
	],
	"bess-f2": [
		['R1', 'R2', 'R3', 'R4', 'R5', 'R6'],
		['bess-f2r1s1', 'bess-f2r1s2', 'bess-f2r1s3', 'bess-f2r1s4', 'bess-f2r1s5', 'bess-f2r1s6', '', 'bess-f2r1s7', 'bess-f2r1s8', 'bess-f2r1s9', 'bess-f2r1s10', 'bess-f2r1s11', 'bess-f2r1s12', 'bess-f2r1s13', 'bess-f2r1s14', '', 'bess-f2r1s15', 'bess-f2r1s16', 'bess-f2r1s17', 'bess-f2r1s18', 'bess-f2r1s19', 'bess-f2r1s20', 'bess-f2r1s21'],
		['bess-f2r2s1', 'bess-f2r2s2', 'bess-f2r2s3', 'bess-f2r2s4', 'bess-f2r2s5', 'bess-f2r2s6', '', '', 'bess-f2r2s7', 'bess-f2r2s8', 'bess-f2r2s9', 'bess-f2r2s10', 'bess-f2r2s11', 'bess-f2r2s12', '', '', 'bess-f2r2s13', 'bess-f2r2s14', 'bess-f2r2s15', 'bess-f2r2s16', 'bess-f2r2s17', 'bess-f2r2s18', ''],
		['bess-f2r3s1', 'bess-f2r3s2', 'bess-f2r3s3', 'bess-f2r3s4', 'bess-f2r3s5', 'bess-f2r3s6', '', 'bess-f2r3s7', 'bess-f2r3s8', 'bess-f2r3s9', 'bess-f2r3s10', 'bess-f2r3s11', 'bess-f2r3s12', 'bess-f2r3s13', 'bess-f2r3s14', '', 'bess-f2r3s15', 'bess-f2r3s16', 'bess-f2r3s17', 'bess-f2r3s18', 'bess-f2r3s19', 'bess-f2r3s20', ''],
		['bess-f2r4s1', 'bess-f2r4s2', 'bess-f2r4s3', 'bess-f2r4s4', 'bess-f2r4s5', 'bess-f2r4s6', '', 'bess-f2r4s7', 'bess-f2r4s8', 'bess-f2r4s9', 'bess-f2r4s10', 'bess-f2r4s11', 'bess-f2r4s12', 'bess-f2r4s13', '', '', 'bess-f2r4s14', 'bess-f2r4s15', 'bess-f2r4s16', 'bess-f2r4s17', 'bess-f2r4s18', 'bess-f2r4s19', ''],
		['', '', '', 'bess-f2r5s1', 'bess-f2r5s2', 'bess-f2r5s3', '', '', 'bess-f2r5s4', 'bess-f2r5s5', 'bess-f2r5s6', 'bess-f2r5s7', 'bess-f2r5s8', 'bess-f2r5s9', 'bess-f2r5s10', '', 'bess-f2r5s11', 'bess-f2r5s12', 'bess-f2r5s13', 'bess-f2r5s14', 'bess-f2r5s15', 'bess-f2r5s16', ''],
		['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'bess-f2r6s1', 'bess-f2r6s2', 'bess-f2r6s3', 'bess-f2r6s4', 'bess-f2r6s5', 'bess-f2r6s6', '']
	],
	"bess-f3": [
		['R1', 'R2', 'R3', 'R4', 'R5', 'R6'],
		['bess-f3r1s1', 'bess-f3r1s2', 'bess-f3r1s3', 'bess-f3r1s4', 'bess-f3r1s5', 'bess-f3r1s6', 'bess-f3r1s7', 'bess-f3r1s8', '', 'bess-f3r1s9', 'bess-f3r1s10', 'bess-f3r1s11', 'bess-f3r1s12', 'bess-f3r1s13', 'bess-f3r1s14', 'bess-f3r1s15'],
		['', 'bess-f3r2s1', 'bess-f3r2s2', 'bess-f3r2s3', 'bess-f3r2s4', 'bess-f3r2s5', 'bess-f3r2s6', '', '', 'bess-f3r2s7', 'bess-f3r2s8', 'bess-f3r2s9', 'bess-f3r2s10', 'bess-f3r2s11', 'bess-f3r2s12', ''],
		['bess-f3r3s1', 'bess-f3r3s2', 'bess-f3r3s3', 'bess-f3r3s4', 'bess-f3r3s5', 'bess-f3r3s6', 'bess-f3r3s7', 'bess-f3r3s8', '', 'bess-f3r3s9', 'bess-f3r3s10', 'bess-f3r3s11', 'bess-f3r3s12', 'bess-f3r3s13', 'bess-f3r3s14', ''],
		['bess-f3r4s1', 'bess-f3r4s2', 'bess-f3r4s3', 'bess-f3r4s4', 'bess-f3r4s5', 'bess-f3r4s6', 'bess-f3r4s7', '', '', 'bess-f3r4s8', 'bess-f3r4s9', 'bess-f3r4s10', 'bess-f3r4s11', 'bess-f3r4s12', 'bess-f3r4s13', ''],
		['', 'bess-f3r5s1', 'bess-f3r5s2', 'bess-f3r5s3', 'bess-f3r5s4', 'bess-f3r5s5', 'bess-f3r5s6', 'bess-f3r5s7', '', 'bess-f3r5s8', 'bess-f3r5s9', 'bess-f3r5s10', 'bess-f3r5s11', 'bess-f3r5s12', 'bess-f3r5s13', ''],
		['', '', '', '', '', '', '', '', '', 'bess-f3r6s1', 'bess-f3r6s2', 'bess-f3r6s3', 'bess-f3r6s4', 'bess-f3r6s5', 'bess-f3r6s6', 'bess-f3r6s7']
	],
	"bess-f4": [
		['R1', 'R2', 'R3', 'R4', 'R5', 'R6'],
		['bess-f4r1s1', 'bess-f4r1s2', 'bess-f4r1s3', 'bess-f4r1s4', 'bess-f4r1s5', 'bess-f4r1s6', 'bess-f4r1s7', 'bess-f4r1s8', '', 'bess-f4r1s9', 'bess-f4r1s10', 'bess-f4r1s11', 'bess-f4r1s12', 'bess-f4r1s13', 'bess-f4r1s14'],
		['bess-f4r2s1', 'bess-f4r2s2', 'bess-f4r2s3', 'bess-f4r2s4', 'bess-f4r2s5', 'bess-f4r2s6', 'bess-f4r2s7', '', '', 'bess-f4r2s8', 'bess-f4r2s9', 'bess-f4r2s10', 'bess-f4r2s11', 'bess-f4r2s12', 'bess-f4r2s13'],
		['bess-f4r3s1', 'bess-f4r3s2', 'bess-f4r3s3', 'bess-f4r3s4', 'bess-f4r3s5', 'bess-f4r3s6', 'bess-f4r3s7', 'bess-f4r3s8', '', 'bess-f4r3s9', 'bess-f4r3s10', 'bess-f4r3s11', 'bess-f4r3s12', 'bess-f4r3s13', 'bess-f4r3s14'],
		['bess-f4r4s1', 'bess-f4r4s2', 'bess-f4r4s3', 'bess-f4r4s4', 'bess-f4r4s5', 'bess-f4r4s6', 'bess-f4r4s7', '', '', 'bess-f4r4s8', 'bess-f4r4s9', 'bess-f4r4s10', 'bess-f4r4s11', 'bess-f4r4s12', 'bess-f4r4s13'],
		['', '', '', 'bess-f4r5s1', 'bess-f4r5s2', 'bess-f4r5s3', 'bess-f4r5s4', 'bess-f4r5s5', '', 'bess-f4r5s6', 'bess-f4r5s7', 'bess-f4r5s8', 'bess-f4r5s9', 'bess-f4r5s10', 'bess-f4r5s11'],
		['', '', '', '', '', '', '', '', '', 'bess-f4r6s1', 'bess-f4r6s2', 'bess-f4r6s3', 'bess-f4r6s4', 'bess-f4r6s5', '']
	],
	"paul-f3": [
		['R10', 'R9', 'R8', 'R7', 'R6', 'R5', 'R4', 'R3', 'R2', 'R1'],
		['', '', '', '', '', '', '', '', '', '', '', '', 'x', '', 'paul-f3Br10s1', 'paul-f3Br10s2', '', '', '', '', '', ''],
		['', '', '', '', '', '', '', '', '', '', '', 'paul-f3Ar9s1', 'x', 'paul-f3Br9s1', 'paul-f3Br9s2', 'paul-f3Br9s3', '', '', '', '', '', ''],
		['', '', '', '', '', '', '', '', '', 'paul-f3Ar8s1', 'paul-f3Ar8s2', 'paul-f3Ar8s3', 'x', 'paul-f3Br8s1', 'paul-f3Br8s2', 'paul-f3Br8s3', '', '', '', '', '', ''],
		['', '', '', '', '', '', 'paul-f3Ar7s1', 'paul-f3Ar7s2', '', 'paul-f3Ar7s3', 'paul-f3Ar7s4', 'paul-f3Ar7s5', 'x', 'paul-f3Br7s1', 'paul-f3Br7s2', 'paul-f3Br7s3', '', 'paul-f3Br7s4', 'paul-f3Br7s5', 'x', 'paul-f3Br7s6', 'paul-f3Br7s7'],
		['', 'paul-f3Ar6s1', 'paul-f3Ar6s2', 'paul-f3Ar6s3', 'paul-f3Ar6s4', 'paul-f3Ar6s5', 'paul-f3Ar6s6', 'paul-f3Ar6s7', '', 'paul-f3Ar6s8', 'paul-f3Ar6s9', 'paul-f3Ar6s10', 'x', 'paul-f3Br6s1', 'paul-f3Br6s2', 'paul-f3Br6s3', '', 'paul-f3Br6s4', 'paul-f3Br6s5', 'paul-f3Br6s6', 'paul-f3Br6s7', 'paul-f3Br6s8'],
		['paul-f3Ar5s1', 'paul-f3Ar5s2', 'paul-f3Ar5s3', 'paul-f3Ar5s4', 'paul-f3Ar5s5', 'paul-f3Ar5s6', 'paul-f3Ar5s7', 'paul-f3Ar5s8', '', 'paul-f3Ar5s9', 'paul-f3Ar5s10', 'paul-f3Ar5s11', 'x', 'paul-f3Br5s1', 'paul-f3Br5s2', 'paul-f3Br5s3', '', 'paul-f3Br5s4', 'paul-f3Br5s5', 'paul-f3Br5s6', 'paul-f3Br5s7', 'paul-f3Br5s8'],
		['paul-f3Ar4s1', 'paul-f3Ar4s2', 'paul-f3Ar4s3', 'paul-f3Ar4s4', 'paul-f3Ar4s5', 'x', 'paul-f3Ar4s6', 'paul-f3Ar4s7', '', 'paul-f3Ar4s8', 'paul-f3Ar4s9', 'paul-f3Ar4s10', 'x', 'paul-f3Br4s1', 'paul-f3Br4s2', 'paul-f3Br4s3', '', 'paul-f3Br4s4', 'paul-f3Br4s5', 'paul-f3Br4s6', 'paul-f3Br4s7', 'paul-f3Br4s8'],
		['paul-f3Ar3s1', 'paul-f3Ar3s2', 'paul-f3Ar3s3', 'paul-f3Ar3s4', 'paul-f3Ar3s5', 'paul-f3Ar3s6', 'paul-f3Ar3s7', 'paul-f3Ar3s8', '', 'paul-f3Ar3s9', 'paul-f3Ar3s10', 'paul-f3Ar3s11', 'x', 'paul-f3Br3s1', 'paul-f3Br3s2', 'paul-f3Br3s3', '', 'paul-f3Br3s4', 'paul-f3Br3s5', 'x', 'paul-f3Br3s6', 'paul-f3Br3s7'],
		['paul-f3Ar2s1', 'paul-f3Ar2s2', 'paul-f3Ar2s3', 'paul-f3Ar2s4', 'paul-f3Ar2s5', '', '', '', '', '', '', '', 'x', '', '', '', '', '', '', '', 'paul-f3Br2s1', 'paul-f3Br2s2'],
		['paul-f3Ar1s1', 'paul-f3Ar1s2', '', '', '', '', '', '', '', '', '', '', 'x', '', '', '', '', '', '', '', 'paul-f3Br1s1', 'paul-f3Br1s2']
	],
	"paul-f4": [
		['R9', 'R8', 'R7', 'R6', 'R5', 'R4', 'R3', 'R2', 'R1'],
		['', '', '', '', '', '', '', '', '', '', '', '', 'x', 'paul-f4Br9s1', 'paul-f4Br9s2', 'paul-f4Br9s3', '', '', '', '', '', ''],
		['', '', '', 'paul-f4Ar8s1', 'paul-f4Ar8s2', 'paul-f4Ar8s3', 'paul-f4Ar8s4', 'paul-f4Ar8s5', '', 'paul-f4Ar8s6', 'paul-f4Ar8s7', 'paul-f4Ar8s8', 'x', 'paul-f4Br8s1', 'paul-f4Br8s2', 'paul-f4Br8s3', '', '', '', '', '', ''],
		['paul-f4Ar7s1', 'paul-f4Ar7s2', 'paul-f4Ar7s3', 'paul-f4Ar7s4', 'paul-f4Ar7s5', 'paul-f4Ar7s6', 'paul-f4Ar7s7', 'paul-f4Ar7s8', '', 'paul-f4Ar7s9', 'paul-f4Ar7s10', 'paul-f4Ar7s11', 'x', 'paul-f4Br7s1', 'paul-f4Br7s2', 'paul-f4Br7s3', '', 'paul-f4Br7s4', 'paul-f4Br7s5', 'x', 'paul-f4Br7s6', 'paul-f4Br7s7'],
		['paul-f4Ar6s1', 'paul-f4Ar6s2', 'paul-f4Ar6s3', 'paul-f4Ar6s4', 'paul-f4Ar6s5', 'x', 'paul-f4Ar6s6', 'paul-f4Ar6s7', '', 'paul-f4Ar6s8', 'paul-f4Ar6s9', 'paul-f4Ar6s10', 'x', 'paul-f4Br6s1', 'paul-f4Br6s2', 'paul-f4Br6s3', '', 'paul-f4Br6s4', 'paul-f4Br6s5', 'paul-f4Br6s6', 'paul-f4Br6s7', 'paul-f4Br6s8'],
		['paul-f4Ar5s1', 'paul-f4Ar5s2', 'paul-f4Ar5s3', 'paul-f4Ar5s4', 'paul-f4Ar5s5', 'paul-f4Ar5s6', 'paul-f4Ar5s7', 'paul-f4Ar5s8', '', 'paul-f4Ar5s9', 'paul-f4Ar5s10', 'paul-f4Ar5s11', 'x', 'paul-f4Br5s1', 'paul-f4Br5s2', 'paul-f4Br5s3', '', 'paul-f4Br5s4', 'paul-f4Br5s5', 'paul-f4Br5s6', 'paul-f4Br5s7', 'paul-f4Br5s8'],
		['paul-f4Ar4s1', 'paul-f4Ar4s2', 'paul-f4Ar4s3', 'paul-f4Ar4s4', 'paul-f4Ar4s5', '', '', '', '', '', '', '', 'x', 'paul-f4Br4s1', 'paul-f4Br4s2', 'paul-f4Br4s3', '', 'paul-f4Br4s4', 'paul-f4Br4s5', 'paul-f4Br4s6', 'paul-f4Br4s7', 'paul-f4Br4s8'],
		['paul-f4Ar3s1', 'paul-f4Ar3s2', '', '', '', '', '', '', '', '', '', '', 'x', 'paul-f4Br3s1', 'paul-f4Br3s2', 'paul-f4Br3s3', '', 'paul-f4Br3s4', 'paul-f4Br3s5', 'x', 'paul-f4Br3s6', 'paul-f4Br3s7'],
		['paul-f4Ar2s1', 'paul-f4Ar2s2', 'paul-f4Ar2s3', 'paul-f4Ar2s4', 'paul-f4Ar2s5', '', '', '', '', '', '', '', 'x', '', '', '', '', '', '', '', 'paul-f4Br2s1', 'paul-f4Br2s2'],
		['paul-f4Ar1s1', 'paul-f4Ar1s2', 'paul-f4Ar1s3', 'paul-f4Ar1s4', 'paul-f4Ar1s5', '', '', '', '', '', '', '', 'x', '', '', '', '', '', '', '', 'paul-f4Br1s1', 'paul-f4Br1s2']
	],
	"paul-f5": [
		['R6', 'R5', 'R4', 'R3', 'R2', 'R1'],
		['', '', '', '', '', '', '', '', '', '', 'paul-f5Ar6s1', 'paul-f5Ar6s2', 'x', 'paul-f5Br6s1', 'paul-f5Br6s2', 'paul-f5Br6s3', '', 'paul-f5Br6s4', 'paul-f5Br6s5', 'paul-f5Br6s6', 'paul-f5Br6s7'],
		['', '', '', '', '', '', '', '', '', 'paul-f5Ar5s1', 'paul-f5Ar5s2', 'paul-f5Ar5s3', 'x', 'paul-f5Br5s1', 'paul-f5Br5s2', 'paul-f5Br5s3', '', 'paul-f5Br5s4', 'paul-f5Br5s5', 'paul-f5Br5s6', 'paul-f5Br5s7'],
		['', '', '', '', '', '', 'paul-f5Ar4s1', 'paul-f5Ar4s2', '', 'paul-f5Ar4s3', 'paul-f5Ar4s4', 'paul-f5Ar4s5', 'x', 'paul-f5Br4s1', 'paul-f5Br4s2', 'paul-f5Br4s3', '', 'paul-f5Br4s4', 'paul-f5Br4s5', 'paul-f5Br4s6', 'paul-f5Br4s7'],
		['', 'paul-f5Ar3s1', 'paul-f5Ar3s2', 'paul-f5Ar3s3', 'paul-f5Ar3s4', 'paul-f5Ar3s5', 'paul-f5Ar3s6', 'paul-f5Ar3s7', '', 'paul-f5Ar3s8', 'paul-f5Ar3s9', 'paul-f5Ar3s10', 'x', 'paul-f5Br3s1', 'paul-f5Br3s2', 'paul-f5Br3s3', '', 'paul-f5Br3s4', 'paul-f5Br3s5', 'x', 'paul-f5Br3s6'],
		['paul-f5Ar2s1', 'paul-f5Ar2s2', 'paul-f5Ar2s3', 'paul-f5Ar2s4', 'paul-f5Ar2s5', '', '', '', '', '', '', '', 'x', '', '', '', '', '', 'paul-f5Br2s1', 'x', 'paul-f5Br2s2'],
		['paul-f5Ar1s1', 'paul-f5Ar1s2', 'paul-f5Ar1s3', 'paul-f5Ar1s4', 'paul-f5Ar1s5', '', '', '', '', '', '', '', 'x', '', '', '', '', '', 'paul-f5Br1s1', 'paul-f5Br1s2', 'paul-f5Br1s3']
	],
	"allowed": ['bess-f1', 'bess-f2', 'bess-f3', 'bess-f4', 'paul-f3', 'paul-f4', 'paul-f5'],
	"piscine": ['bess-f1', 'bess-f2', 'bess-f3', 'bess-f4', 'paul-f3', 'paul-f4'],
	"default": 'bess-f1',
	"exrypz": exrypz
}

# @formatter:on
