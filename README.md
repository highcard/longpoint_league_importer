# longpoint_league_importer

Simple CSV reader & writer for importing tournament results for Historical European Martial Arts and calculating league standings

## Usage

Prepare csv files for import using two columns with the headers `name_key` and `place`. `name_key` values should be consistent for a fighter across multiple tournaments, and the `place` value should be an integer indicating that fighter's final ranking for that tournament.

For a simple import and export, from the command line run:

```
$ python league_rating.py -f filename [additional_filenames] -w
filename import successful
1 event file(s) imported
Output written to file default.csv
```
Additional flags:

`-e` Requests user input for overriding input filenames in export headers
```
$ python league_rating.py -f filename [additional_filename] -we
Enter event name for filename: foobar
filename import successful
1 event file(s) imported
Enter max # of events for use in scoring: 2
Output written to default.csv
```

`-o` Input to override default export name
```
$ python league_rating.py -f filename [additional_filenames] -wo export_filename
filename import successful
1 event file(s) imported
Output written to file export_filename
```

## Example Usage

```
$ python league_rating.py -f tests/test_1.csv tests/test_2.csv tests/test_3.csv -weo test_export.csv
```