# This is a template, copy it for your own campus

def exrypz(computer):
	if '-' in computer and len(computer) >= 8:
		floor = computer.split('r')[0]
		row = computer.split('r')[1].split('s')[0]
		seat = computer.split('s')[1]
		res = {"building": computer.split('-')[0], "p_sep": "s", "etage": floor, "range": row,
		       "place": seat}
		return res
	if len(computer) >= 6:
		res = {"building": "main", "p_sep": "s", "etage": computer.split('r')[0],
		       "range": computer.split('r')[1].split('s')[0],
		       "place": computer.split('s')[1]}
		return res
	return False


# @formatter:off
map = {
	"c1": [
		['R1', 'R2', '', 'R3', 'R4'],
		['c1r1s1', '', 'c1r1s2', '', 'c1r1s3', '', 'c1r1s4', '', 'c1r1s5', 'd', 'c1r1s6', '', 'c1r1s7', '', 'c1r1s8', '', 'c1r1s9', ''],
		['c1r2s1', 'c1r2s2', 'c1r2s3', 'c1r2s4', 'c1r2s5', 'c1r2s6', 'c1r2s7', 'c1r2s8', 'c1r2s9', '', 'c1r2s10', 'c1r2s11', 'c1r2s12', 'c1r2s13', 'c1r2s14', 'c1r2s15', 'c1r2s16', 'c1r2s17'],
		['d', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
		['c1r3s1', 'c1r3s2', 'c1r3s3', 'c1r3s4', 'c1r3s5', 'c1r3s6', 'c1r3s7', 'c1r3s8', 'c1r3s9', '', 'c1r3s10', 'c1r3s11', 'c1r3s12', 'c1r3s13', 'c1r3s14', 'c1r3s15', 'c1r3s16', 'c1r3s17'],
		['c1r4s1', '', 'c1r4s2', '', 'c1r4s3', '', 'c1r4s4', '', 'c1r4s5', 'd', 'c1r4s6', '', 'c1r4s7', '', 'c1r4s8', '', 'c1r4s9', ''],
	],
	"c2": [
		['R1', 'R2', '', 'R3', 'R4'],
		['c2r1s1', '', 'c2r1s2', '', 'c2r1s3', '', 'c2r1s4', '', 'c2r1s5', 'd', 'c2r1s6', '', 'c2r1s7', '', 'c2r1s8', '', 'c2r1s9', ''],
		['c2r2s1', 'c2r2s2', 'c2r2s3', 'c2r2s4', 'c2r2s5', 'c2r2s6', 'c2r2s7', 'c2r2s8', 'c2r2s9', '', 'c2r2s10', 'c2r2s11', 'c2r2s12', 'c2r2s13', 'c2r2s14', 'c2r2s15', 'c2r2s16', 'c2r2s17'],
		['d', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
		['c2r3s1', 'c2r3s2', 'c2r3s3', 'c2r3s4', 'c2r3s5', 'c2r3s6', 'c2r3s7', 'c2r3s8', 'c2r3s9', '', 'c2r3s10', 'c2r3s11', 'c2r3s12', 'c2r3s13', 'c2r3s14', 'c2r3s15', 'c2r3s16', 'c2r3s17'],
		['c2r4s1', '', 'c2r4s2', '', 'c2r4s3', '', 'c2r4s4', '', 'c2r4s5', 'd', 'c2r4s6', '', 'c2r4s7', '', 'c2r4s8', '', 'c2r4s9', ''],
	],
	"c3": [
		['R1', 'R2', '', 'R3', 'R4'],
		['c3r1s1', '', 'c3r1s2', '', 'c3r1s3', '', 'c3r1s4', '', 'c3r1s5', 'd', 'c3r1s6', '', 'c3r1s7', '', 'c3r1s8', '', 'c3r1s9', ''],
		['c3r2s1', 'c3r2s2', 'c3r2s3', 'c3r2s4', 'c3r2s5', 'c3r2s6', 'c3r2s7', 'c3r2s8', 'c3r2s9', '', 'c3r2s10', 'c3r2s11', 'c3r2s12', 'c3r2s13', 'c3r2s14', 'c3r2s15', 'c3r2s16', 'c3r2s17'],
		['d', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
		['c3r3s1', 'c3r3s2', 'c3r3s3', 'c3r3s4', 'c3r3s5', 'c3r3s6', 'c3r3s7', 'c3r3s8', 'c3r3s9', '', 'c3r3s10', 'c3r3s11', 'c3r3s12', 'c3r3s13', 'c3r3s14', 'c3r3s15', 'c3r3s16', 'c3r3s17'],
		['c3r4s1', '', 'c3r4s2', '', 'c3r4s3', '', 'c3r4s4', '', 'c3r4s5', 'd', 'c3r4s6', '', 'c3r4s7', '', 'c3r4s8', '', 'c3r4s9', ''],
	],
	"c4": [
		['R1', 'R2', '', 'R3', 'R4'],
		['c4r1s1', '', 'c4r1s2', '', 'c4r1s3', '', 'c4r1s4', '', 'c4r1s5', 'd', 'c4r1s6', '', 'c4r1s7', '', 'c4r1s8', '', 'c4r1s9', ''],
		['c4r2s1', 'c4r2s2', 'c4r2s3', 'c4r2s4', 'c4r2s5', 'c4r2s6', 'c4r2s7', 'c4r2s8', 'c4r2s9', '', 'c4r2s10', 'c4r2s11', 'c4r2s12', 'c4r2s13', 'c4r2s14', 'c4r2s15', 'c4r2s16', 'c4r2s17'],
		['d', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
		['c4r3s1', 'c4r3s2', 'c4r3s3', 'c4r3s4', 'c4r3s5', 'c4r3s6', 'c4r3s7', 'c4r3s8', 'c4r3s9', '', 'c4r3s10', 'c4r3s11', 'c4r3s12', 'c4r3s13', 'c4r3s14', 'c4r3s15', 'c4r3s16', 'c4r3s17'],
		['c4r4s1', '', 'c4r4s2', '', 'c4r4s3', '', 'c4r4s4', '', 'c4r4s5', 'd', 'c4r4s6', '', 'c4r4s7', '', 'c4r4s8', '', 'c4r4s9', ''],
	],
	"allowed": ['c1', 'c2', 'c3', 'c4'],
	"piscine": [''],
	"silent": [],
	"buildings": {},
	"kiosk_classes": {},
	"default": 'c1',
	"exrypz": exrypz  
}

# @formatter:on
