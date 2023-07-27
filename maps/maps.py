import maps.paris as map_paris
import maps.vienna as map_vienna


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


def place_to_btn(info: dict):
	remaining = info['places']
	maximum = places(info['exrypz'], info['map'])
	percentage = (remaining / maximum) * 100
	if percentage < 25:
		return 'danger'
	elif percentage < 35:
		return 'warning'
	return 'primary'


def available_seats(cluster: str, _map: list, exrypz, locations_map: dict, errors_map: dict):
	return places(exrypz, _map) - count_in_cluster(cluster, locations_map) - count_in_cluster(cluster, errors_map)


paris = map_paris.map
vienna = map_vienna.map
available = {
	53: map_vienna,
	1: map_paris
}
