import csv
import argparse
import json

POINTS_MAP = [
	{"max_place":1, "points":10},
	{"max_place":2, "points":9},
	{"max_place":3, "points":8},
	{"max_place":4, "points":7},
	{"max_place":8, "points":4},
	{"max_place":16, "points":2},
	{"max_place":32, "points":1},
]

class Importer(object):

	def __init__(self):
		self.league_results = {}
		self.league_events = []


	# Translates rank in an event into corresponding league points
	def get_league_points(self, cur_place, cur_map):
		for rule in cur_map:
			if cur_place <= rule['max_place']:
				return rule['points']
		return 0


	# reads a csv of fighter tournament ranks, and updates the league_results appropriately
	def read_event_from_csv(self, event_name, tourney_csv):
		with open(tourney_csv, mode='r') as tourney_data:
			# convert data in from csv to dictionary for easier manipulation
			reader = csv.DictReader(tourney_data)
			
			# loop through rows of tournament data...
			for row in reader:
				cur_key = row['name_key']
				cur_place = int(row['place'])

				# ... create a new fighter in league_results if the fighter doesn't yet exist
				if cur_key not in self.league_results.keys():
					self.league_results[cur_key] = {"fighter_name": cur_key}

				# ... add tournament result to fighter's record
				self.league_results[cur_key][event_name] = self.get_league_points(cur_place, POINTS_MAP)

		# update the list of imported events
		self.league_events.append(event_name)


	# simple output
	def print_league(self):
		for fighter in self.league_results:
			print fighter, self.league_results[fighter]

	# Calculates a fighter's total league points accumulated.
	# max_events specifies how many of the fighter's top results are included in scoring

	def calculate_results(self, max_events=3):
		for fighter in self.league_results:
			cur_results = []
			for event in self.league_events:
				if event in self.league_results[fighter]:
					cur_results.append(self.league_results[fighter][event])
			cur_results.sort(reverse=True)
			self.league_results[fighter]["league_points"] = sum(cur_results[:max_events])
			# save the highest unused ranking to be used as a tiebreaker
			if len(cur_results) > max_events:
				self.league_results[fighter]["tiebreak"] = cur_results[max_events]
			else:
				self.league_results[fighter]["tiebreak"] = 0

	# converts league_results into a ranked list (reverse by points then tiebreak value)
	def sort_results(self):
		ordered_results = []
		for fighter in self.league_results:
			ordered_results.append(self.league_results[fighter])
		ordered_results.sort(key=lambda x: (x["league_points"], x["tiebreak"]), reverse=True)
		return ordered_results

	# writes league results output  
	def write_league_to_csv(self, output_file):
		headernames = ['fighter_name'] + self.league_events + ['league_points', 'tiebreak']
		with open(output_file, 'w') as csvfile:
			outputwriter = csv.DictWriter(csvfile, fieldnames=headernames, extrasaction='ignore')
			outputwriter.writeheader()
			list_to_write = self.sort_results()
			outputwriter.writerows(list_to_write)

if __name__ == '__main__':
	parser = argparse.ArgumentParser(prog="results_importer")
	parser.add_argument('-f', '--file_list', nargs='+', default=[])
	parser.add_argument('-e', '--event_name_override', action="store_true")
	parser.add_argument('-w', '--write_output', action="store_true")
	parser.add_argument('-o', '--output_name', default="default.csv")
	inputs = parser.parse_args()
	event_list = inputs.file_list
	name_flag = inputs.event_name_override

	league = Importer()

	count = 0
	error_count = 0

	for file_name in event_list:
		if name_flag:
			while True:
				try:
					newname = raw_input("Enter event name for %s: " % file_name)
					break
				except ValueError:
					print "invalid entry"
			tourney_name = newname
		else:
			tourney_name = file_name
		cur_tourney_file = file_name
		try:
			league.read_event_from_csv(tourney_name, cur_tourney_file)
			print "%s import succeeded" % cur_tourney_file
			count += 1
		except:
			print "%s import failed" % cur_tourney_file
			error_count += 1

	print '%s event file(s) imported' % count
	if error_count > 0:
		print '%s event file(s) could not be imported' % error_count

	league.calculate_results(max_events=2)

	if inputs.write_output == True:
		league.write_league_to_csv(inputs.output_name)