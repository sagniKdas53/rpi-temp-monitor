# Temperatue monitor

    usage: monitor.py [-h] -d <number> -l <number> [-n [number]] [-o filename]
                  [-b | -a [filename [show] ...]] [-s | -v]

    Measures and graphs tempertaure of raspberry pi

    optional arguments:
      -h, --help            show this help message and exit
      -d <number>, --duration <number>
                            duration of each measuring cycle in seconds
      -l <number>, --log <number>
                            number of measuring cycles after which to log the
                            value
      -n [number], --count [number]
                            number of logging cycles after which to stop, can be
                            left blank to measure indefinitely (not recomended)
      -o filename, --output filename
                            name of the csv to save the data, leave blank to not
                            save
      -b, --basic           print a graph in terminal using plotext
      -a [filename [show] ...], --advanced [filename [show] ...]
                            show a advanced graph using matplotlib (GUI required)
                            only passing the flag will show the graph and do
                            nothing more. Pass a filename to save the graph in it.
                            Pass filename followed by "show" (without quotes) to
                            show the graph and save in in file
      -s, --silent          pass this to not display any output does not override
                            graphs
      -v, --verbose         display all output

## Usage

1. ```` python3 monitor.py -d 1 -l 1 -n 100 -a image.png show -o data.csv -v ````

    This is the most detailed you can go as of now it take in duration logging time and cycles
    then displays a graph and saves it in image.png also saves the data in data.csv while displaying
    all steps and info.

2. ```` python3 monitor.py -d 1 -l 1 -n 100 -a image.png -o data.csv -v ````
3. ```` python3 monitor.py -d 1 -l 1 -n 100 -a image.png -o data.csv -s ````
4. ```` python3 monitor.py -d 1 -l 1 -n 100 -o data.csv -s ````
5. ```` python3 monitor.py -d 1 -l 1 -n 100 -a image.png -s ````
6. ```` python3 monitor.py -d 1 -l 1 -n 100 -a image.png show -s ````
7. ```` python3 monitor.py -d 1 -l 1 -n 100 -b -s ````

## TODO

- [ ] Write details and add screenshots for the different command above
- [x] Check if the conditional statements can be simplified or remove
