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
	if len(computer) >= 6 and 'r' in computer and 'p' in computer:
		res = {"building": "main", "p_sep": "p", "etage": computer.split('r')[0],
		       "range": computer.split('r')[1].split('p')[0],
		       "place": computer.split('p')[1]}
		return res
	return False


# @formatter:off
map = {
	"exrypz": exrypz,
	"c1": [
		['R2', 'R1'],
		["c1r2p1", "c1r2p2", "c1r2p3", "c1r2p4", "c1r2p5", "c1r2p6", '', "c1r2p7", "c1r2p8", "c1r2p9", "c1r2p10"],
		["c1r1p1", "c1r1p2", "c1r1p3", "c1r1p4", "c1r1p5", "c1r1p6", '', "c1r1p7", "c1r1p8", "c1r1p9", "c1r1p10"]
	],
	"c2": [
		['R7', 'R6', '', 'R5', 'R4', 'R3', 'R2', 'R1'],
		['c2r7p1', 'c2r7p2', 'c2r7p3', 'c2r7p4', 'c2r7p5', 'c2r7p6', '', '', '', '', '', '', '', '', ''],
		['c2r6p1', 'c2r6p2', 'c2r6p3', 'c2r6p4', 'c2r6p5', 'c2r6p6', '', '', '', '', '', '', '', '', ''],
		['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
		['c2r5p1', 'c2r5p2', 'c2r5p3', 'c2r5p4', 'c2r5p5', 'c2r5p6', 'c2r5p7', 'c2r5p8', 'c2r5p9', 'c2r5p10', '', 'c2r5p11', 'c2r5p12', 'c2r5p13', 'c2r5p14'],
		['', '', '', '', 'c2r4p1', 'c2r4p2', 'c2r4p3', 'c2r4p4', 'c2r4p5', 'c2r4p6', '', '', '', 'c2r4p7', 'c2r4p8'],
		['c2r3p1', 'c2r3p2', 'c2r3p3', 'c2r3p4', 'c2r3p5', 'c2r3p6', 'c2r3p7', 'c2r3p8', 'c2r3p9', 'c2r3p10', '', 'c2r3p11', 'c2r3p12', 'c2r3p13', 'c2r3p14'],
		['', '', '', '', 'c2r2p1', 'c2r2p2', 'c2r2p3', 'c2r2p4', 'c2r2p5', 'c2r2p6', '', '', '', 'c2r2p7', 'c2r2p8'],
		['c2r1p1', 'c2r1p2', 'c2r1p3', 'c2r1p4', 'c2r1p5', 'c2r1p6', 'c2r1p7', 'c2r1p8', 'c2r1p9', 'c2r1p10', '', 'c2r1p11', 'c2r1p12', 'c2r1p13', 'c2r1p14'],
	],
	"c3": [
		['R10', 'R9', '', 'R8', 'R7', 'R6', 'R5', 'R4', 'R3', 'R2', 'R1'],
		['c3r10p1', 'c3r10p2', 'c3r10p3', 'c3r10p4', 'c3r10p5', 'c3r10p6', 'c3r10p7', 'c3r10p8', '', '', '', '', ''],
		['c3r9p1', 'c3r9p2', 'c3r9p3', 'c3r9p4', 'c3r9p5', 'c3r9p6', 'c3r9p7', 'c3r9p8', '', '', '', '', ''],
		['', '', '', '', '', '', '', '', '', '', '', '', ''],
		['c3r5p1', 'c3r5p2', 'c3r5p3', 'c3r5p4', 'c3r5p5', 'c3r5p6', '', 'c3r8p1', 'c3r8p2', 'c3r8p3', 'c3r8p4', 'c3r8p5', 'c3r8p6'],
		['c3r4p1', 'c3r4p2', 'c3r4p3', 'c3r4p4', 'c3r4p5', 'c3r4p6', '', 'c3r7p1', 'c3r7p2', 'c3r7p3', 'c3r7p4', 'c3r7p5', 'c3r7p6'],
		['c3r3p1', 'c3r3p2', 'c3r3p3', 'c3r3p4', 'c3r3p5', 'c3r3p6', '', 'c3r8p1', 'c3r8p2', 'c3r8p3', 'c3r8p4', 'c3r8p5', 'c3r8p6'],
		['c3r2p1', 'c3r2p2', 'c3r2p3', 'c3r2p4', 'c3r2p5', 'c3r2p6', '', '', '', '', '', '', ''],
		['c3r1p1', 'c3r1p2', 'c3r1p3', 'c3r1p4', 'c3r1p5', 'c3r1p6', '', '', '', '', '', '', '']
	],
	"c4": [
		['', '', '', '', ''],
		['c4r6p1', 'c4r6p2', 'c4r6p3', 'c4r6p4', '', 'c4r6p5', 'c4r6p6', 'c4r6p7', 'c4r6p8', 'c4r6p9', 'c4r6p10', '', 'c4r1p1', 'c4r1p2', 'c4r1p3', 'c4r1p4', 'c4r1p5', 'c4r1p6', '', 'c4r1p7', 'c4r1p8', 'c4r1p9', 'c4r1p10'],
		['c4r7p1', 'c4r7p2', 'c4r7p3', 'c4r7p4', '', 'c4r7p5', 'c4r7p6', 'c4r7p7', 'c4r7p8', 'c4r7p9', 'c4r7p10', '', 'c4r2p1', 'c4r2p2', 'c4r2p3', 'c4r2p4', 'c4r2p5', 'c4r2p6', '', 'c4r2p7', 'c4r2p8', 'c4r2p9', 'c4r2p10'],
		['', '', '', '', '', '', '', '', '', '', '', '', 'c4r3p1', 'c4r3p2', 'c4r3p3', 'c4r3p4', 'c4r3p5', 'c4r3p6', '', 'c4r3p7', 'c4r3p8', 'c4r3p9', 'c4r3p10'],
		['', '', '', '', '', '', '', '', '', '', '', '', 'c4r4p1', 'c4r4p2', 'c4r4p3', 'c4r4p4', 'c4r4p5', 'c4r4p6', '', 'c4r4p7', 'c4r4p8', 'c4r4p9', 'c4r4p10'],
		['', '', '', '', '', '', '', '', '', '', '', '', 'c4r5p1', 'c4r5p2', 'c4r5p3', 'c4r5p4', 'c4r5p5', 'c4r5p6', '', 'c4r5p7', 'c4r5p8', 'c4r5p9', 'c4r5p10'],
	],
	"allowed": ['c1', 'c2', 'c3', 'c4'],
	"buildings": {'vienna': ['c1', 'c2', 'c3', 'c4']},
	"kiosk_classes": {},
	"piscine": [],
	"default": 'c1'
}
# @formatter:on
