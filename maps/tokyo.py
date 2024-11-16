def exrypz(computer):
	if '-' in computer:
		return False
	if len(computer) >= 6 and 'r' in computer and 's' in computer:
		res = {"building": "main", "p_sep": "s", "etage": computer.split('r')[0],
		       "range": computer.split('r')[1].split('s')[0],
		       "place": computer.split('s')[1]}
		return res
	return False


# @formatter:off
map = {
	"c1 - KOI": [
		["R01", "R02", "R03", "R04", "R05", "R06", "R07"],
		["c1r1s1", "c1r1s2", "c1r1s3", "c1r1s4", "c1r1s5", "c1r1s6", "c1r1s7", "c1r1s8"],
		["c1r2s1", "c1r2s2", "c1r2s3", "c1r2s4", "c1r2s5", "c1r2s6", "c1r2s7", "c1r2s8"],
		["c1r3s1", "c1r3s2", "c1r3s3", "c1r3s4", "c1r3s5", "c1r3s6", "c1r3s7", "c1r3s8"],
		["c1r4s1", "c1r4s2", "c1r4s3", "c1r4s4", "c1r4s5", "c1r4s6", "c1r4s7", "c1r4s8"],
		["c1r5s1", "c1r5s2", "c1r5s3", "c1r5s4", "c1r5s5", "c1r5s6", "c1r5s7", "c1r5s8"],
		["c1r6s1", "c1r6s2", "c1r6s3", "c1r6s4", "c1r6s5", "c1r6s6", "c1r6s7", "c1r6s8"],
		["c1r7s1", "c1r7s2", "c1r7s3", "c1r7s4", "c1r7s5", "c1r7s6", "c1r7s7", "c1r7s8"],
	],
	"c2 - UME": [
		["R01", "R02", "R03", "R04", "R05", "R06", "R07", "R08", "R09"],
		["c2r1s1", "c2r1s2", "c2r1s3", "c2r1s4", "c2r1s5", "c2r1s6", "", "", "", ""],
		["c2r2s1", "c2r2s2", "c2r2s3", "c2r2s4", "c2r2s5", "c2r2s6", "c2r2s7", "c2r2s8", "c2r2s9", "c2r2s10"],
		["c2r3s1", "c2r3s2", "c2r3s3", "c2r3s4", "c2r3s5", "c2r3s6", "c2r3s7", "c2r3s8", "c2r3s9", "c2r3s10"],
		["c2r4s1", "c2r4s2", "c2r4s3", "c2r4s4", "", "", "", "", "", ""],
		["c2r5s1", "c2r5s2", "c2r5s3", "c2r5s4", "c2r5s5", "c2r5s6", "c2r5s7", "c2r5s8", "c2r5s9", "c2r5s10"],
		["c2r6s1", "c2r6s2", "c2r6s3", "c2r6s4", "c2r6s5", "c2r6s6", "c2r6s7", "c2r6s8", "c2r6s9", "c2r6s10"],
		["c2r7s1", "c2r7s2", "c2r7s3", "c2r7s4", "c2r7s5", "c2r7s6", "c2r7s7", "c2r7s8", "c2r7s9", "c2r7s10"],
		["c2r8s1", "c2r8s2", "c2r8s3", "c2r8s4", "c2r8s5", "c2r8s6", "c2r8s7", "c2r8s8", "c2r8s9", "c2r8s10"], 
		["c2r9s1", "c2r9s2", "c2r9s3", "c2r9s4", "", "", "", "", "", ""],
	],
	"c3 - WASHI": [
		["R01", "R02", "R03", "R04", "R05", "R06"],
		["c3r1s1", "c3r1s2", "c3r1s3", "c3r1s4", "c3r1s5", "c3r1s6", "", ""],
		["c3r2s1", "c3r2s2", "c3r2s3", "c3r2s4", "c3r2s5", "c3r2s6", "c3r2s7", "c3r2s8"],
		["c3r3s1", "c3r3s2", "c3r3s3", "c3r3s4", "c3r3s5", "c3r3s6", "c3r3s7", "c3r3s8"],
		["c3r4s1", "c3r4s2", "c3r4s3", "c3r4s4", "c3r4s5", "c3r4s6", "c3r4s7", "c3r4s8"],
		["c3r5s1", "c3r5s2", "c3r5s3", "c3r5s4", "c3r5s5", "c3r5s6", "c3r5s7", "c3r5s8"],
		["c3r6s1", "c3r6s2", "c3r6s3", "c3r6s4", "c3r6s5", "c3r6s6", "c3r6s7", "c3r6s8"],
	],
	"c4 - FUJI": [
		["R01", "R02", "R03"],
		["c4r1s1", "c4r1s2", "c4r1s3", "c4r1s4", "c4r1s5", "c4r1s6", "c4r1s7", "c4r1s8", "c4r1s9", "c4r1s10", "c4r1s11", "c4r1s12", "", "", "", "", "", ""],
		["c4r2s1", "c4r2s2", "c4r2s3", "c4r2s4", "c4r2s5", "c4r2s6", "c4r2s7", "c4r2s8", "c4r2s9", "c4r2s10", "c4r2s11", "c4r2s12", "c4r2s13", "c4r2s14", "c4r2s15", "c4r2s16", "c4r2s17", "c4r2s18"],
		["c4r3s1", "c4r3s2", "c4r3s3", "c4r3s4", "c4r3s5", "c4r3s6", "c4r3s7", "c4r3s8", "c4r3s9", "c4r3s10", "c4r3s11", "c4r3s12", "c4r3s13", "c4r3s14", "c4r3s15", "c4r3s16", "c4r3s17", "c4r3s18"],
	],
	"c5 - SAKURA": [
		["R01", "R02", "R03", "R04"],
		["c5r1s1", "c5r1s2", "c5r1s3", "c5r1s4", "c5r1s5", "c5r1s6", "c5r1s7", "c5r1s8", "", "", "", "", "", ""],
		["c5r2s1", "c5r2s2", "c5r2s3", "c5r2s4", "c5r2s5", "c5r2s6", "c5r2s7", "c5r2s8", "c5r2s9", "c5r2s10", "c5r2s11", "c5r2s12", "c5r2s13", "c5r2s14"],
		["c5r3s1", "c5r3s2", "c5r3s3", "c5r3s4", "c5r3s5", "c5r3s6", "c5r3s7", "c5r3s8", "c5r3s9", "c5r3s10", "c5r3s11", "c5r3s12", "c5r3s13", "c5r3s14"],
		["c5r4s1", "c5r4s2", "c5r4s3", "c5r4s4", "c5r4s5", "c5r4s6", "c5r4s7", "c5r4s8", "c5r4s9", "", "", "", "", ""],
	],
	"c6 - TSURU": [
		["R01", "R02", "R03", "R04"],
		["c6r1s1", "c6r1s2", "c6r1s3", "c6r1s4", "c6r1s5", "c6r1s6", "c6r1s7", "c6r1s8", "c6r1s9", "c6r1s10", "c6r1s11", "c6r1s12", "c6r1s13", "c6r1s14"],
		["c6r2s1", "c6r2s2", "c6r2s3", "c6r2s4", "c6r2s5", "c6r2s6", "c6r2s7", "c6r2s8", "c6r2s9", "c6r2s10", "c6r2s11", "c6r2s12", "c6r2s13", "c6r2s14"],
		["c6r3s1", "c6r3s2", "c6r3s3", "c6r3s4", "c6r3s5", "c6r3s6", "c6r3s7", "c6r3s8", "c6r3s9", "c6r3s10", "c6r3s11", "c6r3s12", "c6r3s13", "c6r3s14"],
		["c6r4s1", "c6r4s2", "c6r4s3", "c6r4s4", "c6r4s5", "c6r4s6", "", "", "", "", "", "", "", ""],

	],
	"allowed": ['c1 - KOI', 'c2 - UME', 'c3 - WASHI', 'c4 - FUJI', 'c5 - SAKURA', 'c6 - TSURU'],      # "Enabled" clusters
	"piscine": [],      # "Piscine" reserved clusters
	"buildings": {"Tokyo": ['c1 - KOI', 'c2 - UME', 'c3 - WASHI', 'c4 - FUJI', 'c5 - SAKURA', 'c6 - TSURU']},
	"kiosk_classes": {},    # kiosk icon classes
	"default": 'c1 - KOI',        # Default cluster to appear on the site
	"exrypz": exrypz        # Function to parse locations
}

# @formatter:on
