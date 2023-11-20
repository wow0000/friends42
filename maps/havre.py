def exrypz(computer):
	if '-' in computer:
		return False
	if len(computer) >= 6 and 'r' in computer and 'p' in computer:
		res = {"building": "main", "p_sep": "p", "etage": computer.split('r')[0],
		       "range": computer.split('r')[1].split('p')[0],
		       "place": computer.split('p')[1]}
		return res
	return False


# @formatter:off
map = {
	"c1": [
		['R7', 'R6', 'R5', 'R4', 'R3', 'R2', 'R1'],
		['c1r7p1', 'c1r7p2', 'c1r7p3', '', '', 'c1r7p4', 'c1r7p5', 'c1r7p6', 'c1r7p7', '', '', '', 'c1r7p8', 'c1r7p9', 'c1r7p10', 'c1r7p11', 'c1r7p12', 'c1r7p13', ''],
		['c1r6p1', 'c1r6p2', 'c1r6p3', 'c1r6p4',  '', 'c1r6p5', 'c1r6p6', 'c1r6p7', 'c1r6p8', 'c1r6p9', 'c1r6p10', '', 'c1r6p11', 'c1r6p12', 'c1r6p13', 'c1r6p14', 'c1r6p15', 'c1r6p16', 'c1r6p17'],
		['', '', '', '', '', 'c1r5p1', 'c1r5p2', 'c1r5p3', 'c1r5p4', 'c1r5p5', 'c1r5p6', '', 'c1r5p7', 'c1r5p8', 'c1r5p9', 'c1r5p10', 'c1r5p11', 'c1r5p12', 'c1r5p13'],
		['', '', '', '', '', 'c1r4p1', 'c1r4p2', 'c1r4p3', 'c1r4p4', 'c1r4p5', 'c1r4p6', '', 'c1r4p7', 'c1r4p8', 'c1r4p9', 'c1r4p10', 'c1r4p11', 'c1r4p12', 'c1r4p13'],
		['', '', '', '', '', 'c1r3p1', 'c1r3p2', 'c1r3p3', 'c1r3p4', 'c1r3p5', 'c1r3p6', '', 'c1r3p7', 'c1r3p8', 'c1r3p9', 'c1r3p10', 'c1r3p11', 'c1r3p12', 'c1r3p13'],
		['', '', '', '', '', 'c1r2p1', 'c1r2p2', 'c1r2p3', 'c1r2p4', 'c1r2p5', 'c1r2p6', '', 'c1r2p7', 'c1r2p8', 'c1r2p9', 'c1r2p10', 'c1r2p11', 'c1r2p12', 'c1r2p13'],
		['', '', '', '', '', 'c1r1p1', 'c1r1p2', 'c1r1p3', 'c1r1p4', 'c1r1p5', 'c1r1p6', '', '', 'c1r1p7', 'c1r1p8', 'c1r1p9', 'c1r1p10', 'c1r1p11', 'c1r1p12'],
	],
	"c2": [
		['R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'R9', 'R10', 'R11', 'R12'],
		['c2r1p1', 'c2r1p2', 'c2r1p3', 'c2r1p4', 'c2r1p5', 'c2r1p6'],
		['c2r2p1', 'c2r2p2', 'c2r2p3', 'c2r2p4', 'c2r2p5', 'c2r2p6'],
		['c2r3p1', 'c2r3p2', 'c2r3p3', 'c2r3p4', 'c2r3p5', 'c2r3p6'],
		['c2r4p1', 'c2r4p2', 'c2r4p3', 'c2r4p4', 'c2r4p5', 'c2r4p6'],
		['c2r5p1', 'c2r5p2', 'c2r5p3', 'c2r5p4', 'c2r5p5', ''],
		['c2r6p1', 'c2r6p2', 'c2r6p3', 'c2r6p4', 'c2r6p5', 'c2r6p6'],
		['c2r7p1', 'c2r7p2', 'c2r7p3', 'c2r7p4', 'c2r7p5', 'c2r7p6'],
		['c2r8p1', 'c2r8p2', 'c2r8p3', 'c2r8p4', 'c2r8p5', 'c2r8p6'],
		['c2r9p1', 'c2r9p2', 'c2r9p3', 'c2r9p4', 'c2r9p5', ''],
		['c2r10p1', 'c2r10p2', 'c2r10p3', 'c2r10p4', 'c2r10p5', ''],
		['c2r11p1', 'c2r11p2', 'c2r11p3', 'c2r11p4', 'c2r11p5', 'c2r11p6'],
		['c2r12p1', 'c2r12p2', 'c2r12p3', 'c2r12p4', 'c2r12p5', 'c2r12p6']
	],
	"allowed": ['c1', 'c2'],
	"piscine": [''],
	"buildings": {"Havre": ['c1', 'c2']},
	"kiosk_classes": {
		"<i class='fa-solid fa-display'></i>": ['c1', 'c2'],
	},
	"default": 'c1',
	"exrypz": exrypz
}

# @formatter:on
