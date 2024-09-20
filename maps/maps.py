import maps.paris as map_paris
import maps.vienna as map_vienna
import maps.forty2 as map_forty2
import maps.havre as map_havre


def places(exrypz, _map: list[list[str]]):
	i = 0
	for x in _map:
		for station in x:
			if exrypz(station):
				i += 1
	return i


def count_in_cluster(cluster: str, keys: dict):
	i = 0
	for key in keys.keys():
		if cluster in key:
			i += 1
	return i


def percent_to_btn(remaining, maximum, default="primary"):
	percentage = (remaining / maximum) * 100
	if percentage < 25:
		return 'danger'
	elif percentage < 35:
		return 'warning'
	return default


def place_to_btn(info: dict, default="primary"):
	remaining = info['places']
	maximum = places(info['exrypz'], info['map'])
	return percent_to_btn(remaining, maximum, default)


def available_seats(cluster: str, _map: list, exrypz, locations_map: dict, errors_map: dict):
	return places(exrypz, _map) - count_in_cluster(cluster, locations_map) - count_in_cluster(cluster, errors_map)

def ensure_all_keys(_map: dict):
	_default = {
		"allowed": [],
		"buildings": {},
		"kiosk_classes": {},
		"piscine": [],
		"place_tutors": [],
	}
	for k,val in dict.items(_default):
		if k not in _map.map:
			print(f"key '{k}' not set in {_map.__name__}!")
			_map.map[k] = val
	return _map

paris = map_paris.map
vienna = map_vienna.map
forty2 = map_forty2.map
havre = map_havre.map
# This is to make sure every default key is set by to a know value
# It'll print an error when in debug mode
available = {campus: ensure_all_keys(_map) for (campus, _map) in dict.items(
{
	66: map_forty2,
	53: map_vienna,
	62: map_havre,
	1: map_paris
}
)}
