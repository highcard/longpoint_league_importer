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

# constant strings for output
LEAGUE_POINTS = 'league_points'
TIE_BREAK = 'tie_break'
FIGHTER_NAME = 'fighter_name'
RANK = "rank"


class LeagueImporter(object):

    # Initialize dictionary to store fighter's event results and list of imported events
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
                    self.league_results[cur_key] = {FIGHTER_NAME: cur_key}

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
    def calculate_results(self, max_events):
        for fighter in self.league_results:
            cur_results = []
            for event in self.league_events:
                if event in self.league_results[fighter]:
                    cur_results.append(self.league_results[fighter][event])
            cur_results.sort(reverse=True)
            if max_events == 0:
                cur_max = len(cur_results)
            else:
                cur_max = max_events
            self.league_results[fighter][LEAGUE_POINTS] = sum(cur_results[:cur_max])
            # save the highest unused ranking to be used as a tiebreaker
            if len(cur_results) > cur_max:
                self.league_results[fighter][TIE_BREAK] = cur_results[cur_max]
            else:
                self.league_results[fighter][TIE_BREAK] = 0


    # converts league_results into a ranked list (reverse by points then tie_break value)
    def sort_results(self):
        ordered_results = []
        for fighter in self.league_results:
            ordered_results.append(self.league_results[fighter])
        ordered_results.sort(key=lambda x: (x[LEAGUE_POINTS], x[TIE_BREAK]), reverse=True)

        cur_rank = 1
        cur_place = 1

        for x, y in zip(ordered_results, ordered_results[1:] + [None]):
            x[RANK] = cur_rank
            cur_place += 1
            if self.not_same_rank(x, y):
                cur_rank = cur_place
        return ordered_results

    def not_same_rank(self, fighter1, fighter2):
        if fighter2 == None:
            return False
        return fighter1[LEAGUE_POINTS] != fighter2[LEAGUE_POINTS] or fighter1[TIE_BREAK] != fighter2[TIE_BREAK]

    # writes league results output  
    def write_league_to_csv(self, output_file):
        headernames = [RANK, FIGHTER_NAME] + self.league_events + [LEAGUE_POINTS, TIE_BREAK]
        with open(output_file, 'w') as csvfile:
            outputwriter = csv.DictWriter(csvfile, fieldnames=headernames, extrasaction='ignore')
            outputwriter.writeheader()
            list_to_write = self.sort_results()
            outputwriter.writerows(list_to_write)

def get_name_from_input(file_name):
    while True:
        try:
            newname = raw_input("Enter event name for %s: " % file_name)
            break
        except ValueError:
            print "invalid entry"
    return newname

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="results_importer")
    parser.add_argument('-f', '--file_list', nargs='+', default=[])
    parser.add_argument('-e', '--event_name_override', action="store_true")
    parser.add_argument('-w', '--write_output', action="store_true")
    parser.add_argument('-o', '--output_name', default="export.csv")
    parser.add_argument('-m', '--max_events', type=int, default=0)

    inputs = parser.parse_args()

    event_list = inputs.file_list
    name_flag = inputs.event_name_override
    max_events = inputs.max_events

    league = LeagueImporter()

    # Import counts for verbose messaging
    count = 0
    error_count = 0



    # Loop through list of event results
    for file_name in event_list:
        # Handles command line flag for overriding file names in export
        if name_flag:
            tourney_name = get_name_from_input(file_name)
        else:
            tourney_name = file_name

        # Attempt to read from the the current file in the list
        try:
            league.read_event_from_csv(tourney_name, file_name)
            print "%s import successful" % file_name
            count += 1
        # CSV import error handling and reporting
        except:
            print "%s import failed" % file_name
            error_count += 1
            continue

    # Messaging
    print '%s event file(s) imported' % count
    if error_count > 0:
        print '%s event file(s) could not be imported' % error_count

    league.calculate_results(max_events=max_events)

    if inputs.write_output == True and count > 0:
        league.write_league_to_csv(inputs.output_name)
        print 'Output written to file %s' % inputs.output_name