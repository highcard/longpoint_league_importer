# longpoint_league_importer

Simple CSV reader & writer for importing tournament results for Historical European Martial Arts and calculating league standings

## Usage

Prepare csv files for import using two columns with the headers `name_key` and `place`. `name_key` values should be consistent for a fighter across multiple tournaments, and the `place` value should be an integer indicating that fighter's final ranking for that tournament.

For a simple import and export, from the command line run:

```
$ python league_rating.py -f filename [additional_filenames] -w
filename import successful
1 event file(s) imported
Output written to file export.csv
```
## Additional flags

`-e` flag triggers prompts to request user input for overriding input filenames in export headers
```
$ python league_rating.py -f filename [additional_filename] -we
Enter event name for filename: foobar
filename import successful
1 event file(s) imported
Output written to export.csv
```

`-o` flag specifies string to override default export name (export.csv)
```
$ python league_rating.py -f filename [additional_filenames] -wo export_filename
filename import successful
1 event file(s) imported
Output written to file export_filename
```

`-m` flag specifies maximum number of events to use in calculating a fighter's league points. (0 denotes use all inputs.) default: 0.


## Example Usage

```
$ python league_rating.py -f sample/test_1.csv sample/test_2.csv sample/test_3.csv -weo sample_export.csv -m 2
```