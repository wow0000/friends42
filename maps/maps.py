import maps.paris as map_paris
import maps.vienna as map_vienna
import maps.forty2 as map_forty2
import maps.havre as map_havre
import maps.angouleme as map_angouleme


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


paris = map_paris.map
vienna = map_vienna.map
forty2 = map_forty2.map
havre = map_havre.map
angouleme = map_angouleme.map
available = {
	31: map_angouleme,
	66: map_forty2,
	53: map_vienna,
	62: map_havre,
	1: map_paris
}
