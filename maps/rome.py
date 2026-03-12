def exrypz(computer):
	if '-' in computer:
		return False
	if len(computer) >= 6 and 'r' in computer and 'p' in computer:
		res = {"building": computer.split('r')[0], "p_sep": "p", "etage": computer.split('r')[0],
		       "range": computer.split('r')[1].split('p')[0],
		       "place": computer.split('p')[1]}
		return res
	return False


# @formatter:off
map = {
	"e3": [
		['R1', 'R2', 'R3', '', 'R4', 'R5', 'R6', 'R7', 'R8', 'R9','', 'R10', 'R11', 'R12'],
		['e3r1p1','e3r1p2','e3r1p3','e3r1p4','e3r1p5','e3r1p6','e3r1p7','e3r1p8'],
		['e3r2p1','e3r2p2','e3r2p3','e3r2p4','e3r2p5','e3r2p6','e3r2p7','e3r2p8'],
		['e3r3p1','e3r3p2','e3r3p3','e3r3p4','e3r3p5','e3r3p6','e3r3p7','e3r3p8'],
		['','','','','','','',''],
		['e3r4p1','e3r4p2','e3r4p3','e3r4p4','e3r4p5','e3r4p6','e3r4p7','e3r4p8'],
		['e3r5p1','e3r5p2','e3r5p3','e3r5p4','e3r5p5','e3r5p6','e3r5p7','e3r5p8'],
		['e3r6p1','e3r6p2','e3r6p3','e3r6p4','e3r6p5','e3r6p6','e3r6p7','e3r6p8'],
		['e3r7p1','e3r7p2','e3r7p3','e3r7p4','e3r7p5','e3r7p6','e3r7p7','e3r7p8'],
		['e3r8p1','e3r8p2','e3r8p3','e3r8p4','e3r8p5','e3r8p6','e3r8p7','e3r8p8'],
		['e3r9p1','e3r9p2','e3r9p3','e3r9p4','e3r9p5','e3r9p6','e3r9p7','e3r9p8'],
		['','','','','','','',''],
		['e3r10p1','e3r10p2','e3r10p3','e3r10p4','e3r10p5','e3r10p6','e3r10p7','e3r10p8'],
		['e3r11p1','e3r11p2','e3r11p3','e3r11p4','e3r11p5','e3r11p6','e3r11p7','e3r11p8'],
		['e3r12p1','e3r12p2','e3r12p3','e3r12p4','e3r12p5','e3r12p6','e3r12p7','e3r12p8'],
	],
	"e4": [
		['R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'R9', 'R10', 'R11', 'R12', 'R13', 'R14'],
		['e4r1p1','e4r1p2','e4r1p3','e4r1p4'],
		['e4r2p1','e4r2p2','e4r2p3','e4r2p4'],
		['e4r3p1','e4r3p2','e4r3p3','e4r3p4'],
		['e4r4p1','e4r4p2','e4r4p3','e4r4p4'],
		['e4r5p1','e4r5p2','e4r5p3','e4r5p4'],
		['e4r6p1','e4r6p2','e4r6p3','e4r6p4'],
		['e4r7p1','e4r7p2','e4r7p3','e4r7p4'],
		['e4r8p1','e4r8p2','e4r8p3','e4r8p4'],
		['e4r9p1','e4r9p2','e4r9p3','e4r9p4'],
		['e4r10p1','e4r10p2','e4r10p3','e4r10p4'],
		['e4r11p1','e4r11p2','e4r11p3','e4r11p4'],
		['e4r12p1','e4r12p2','e4r12p3','e4r12p4'],
		['e4r13p1','e4r13p2','e4r13p3','e4r13p4'],
		['e4r14p1','e4r14p2','e4r14p3','e4r14p4'],
	],
	"allowed": ['e3', 'e4'],      # "Enabled" clusters
	"piscine": [],      # "Piscine" reserved clusters
	"buildings": {"Roma": ['e3', 'e4']},
	"kiosk_classes": {},    # kiosk icon classes
	"default": 'e3',        # Default cluster to appear on the site
	"exrypz": exrypz        # Function to parse locations
}

# @formatter:on
