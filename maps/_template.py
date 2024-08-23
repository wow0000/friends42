# This is a template, copy it for your own campus

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
	"e1": [],               # Clusters
	"allowed": ['e1'],      # "Enabled" clusters
	"piscine": ['e1'],      # "Piscine" reserved clusters
	"buildings": {},        # kiosk buildings
	"kiosk_classes": {},    # kiosk icon classes
	"default": 'e1',        # Default cluster to appear on the site
	"exrypz": exrypz        # Function to parse locations
}

# @formatter:on
