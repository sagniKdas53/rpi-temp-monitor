usage: temp.py [-h] [-d] [-l] [-n ] [-o ] [-g ] [-s ]

Measures and graphs tempertaure of raspberry pi

optional arguments:
  -h, --help          show this help message and exit
  -d , --duration     duration of each measuring cycle in seconds
  -l , --log          number of measuring cycles after which to log the value
  -n [], --count []   number of logging cycles after which to stop, can be
                      left blank to measure indefinitely (not recomended)
  -o [], --output []  name of the csv to save the data, leave blank to not
                      save
  -g [], --graph []   print a graph
  -s [], --silent []  don't display any output
