usage: temp.py [-h] -d  -l  [-n] [-o] [-b | -a] [-s | -v]

Measures and graphs tempertaure of raspberry pi

optional arguments:
  -h, --help        show this help message and exit
  -d , --duration   duration of each measuring cycle in seconds
  -l , --log        number of measuring cycles after which to log the value
  -n , --count      number of logging cycles after which to stop, can be left
                    blank to measure indefinitely (not recomended)
  -o , --output     name of the csv to save the data, leave blank to not save
  -b, --basic       print a graph in terminal
  -a, --advanced    print a advanced graph
  -s, --silent      pass this to not display any output
  -v, --verbose     display all output


## Usage
python3 args.py -d 1 -l 1 -n 100 -a image.png -o file.csv -s

python3 args.py -d 1 -l 1 -n 100 -a -o file.csv -s

python3 args.py -d 1 -l 1 -n 100 -b -o file.csv -s

python3 args.py -d 1 -l 1 -n 100 -b -o file.csv -v

python3 args.py -d 1 -l 1 -n 100 -b -s

python3 args.py -d 1 -l 1 -n 100 -o file.csv -s

python3 args.py -d 1 -l 1 -o file.csv -s