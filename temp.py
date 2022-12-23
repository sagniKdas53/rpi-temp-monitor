import argparse
import subprocess
from datetime import datetime, timedelta
from time import sleep

import plotext as plt


def save_csv(x_axis, y_axis_CPU, y_axis_GPU):
    pass


def plot(x_axis, y_axis_CPU, y_axis_GPU):
    plt.date_form('I:M:S')
    plt.plot(x_axis, y_axis_CPU, label="CPU")
    plt.plot(x_axis, y_axis_GPU, label="GPU")
    plt.title("Temperature plot")
    plt.xlabel("time")
    plt.ylabel("temp")
    plt.show()


def main():
    parser = argparse.ArgumentParser(
        description="Measures and graphs tempertaure of raspberry pi")
    parser.add_argument('-d', '--duration', type=int, metavar="",
                        help="duration of each measuring cycle in seconds")
    parser.add_argument('-l', '--log', type=int, metavar="",
                        help="number of measuring cycles after which to log the value")
    parser.add_argument('-n', '--count', type=int, metavar="", nargs='?',  const=None, default=None,
                        help="number of logging cycles after which to stop, can be left blank to measure indefinitely (not recomended)")
    parser.add_argument('-o', '--output', type=str, metavar="", nargs='?',  const=None, default=None,
                        help='name of the csv to save the data, leave blank to not save')
    parser.add_argument('-g', '--graph', type=bool, metavar="", nargs='?',  const=False, default=False,
                        help='print a graph')
    parser.add_argument('-s', '--silent', type=bool, metavar="", nargs='?',  const=False, default=False,
                        help="don't display any output")
    opts = parser.parse_args()
    if opts.count == None:
        stop = -1
    else:
        stop = opts.count
    counter = 0
    avg_GPU = 0
    avg_CPU = 0
    cycle_duration = opts.duration
    delta = timedelta(seconds=10, minutes=21, hours=5)
    x_axis = [(datetime.now()-delta).strftime("%I:%M:%S")]
    y_axis_GPU = []
    y_axis_CPU = []
    while True:
        try:
            counter += 1
            GPU_temp = float(str(subprocess.Popen(
                ["vcgencmd", "measure_temp"], stdout=subprocess.PIPE).communicate()[0], 'UTF-8')[5:9])
            CPU_temp = int(subprocess.Popen(
                ["cat", "/sys/class/thermal/thermal_zone0/temp"], stdout=subprocess.PIPE).communicate()[0])/1000
            if opts.silent == False:
                print(
                    f'\rCPU temp: {CPU_temp:05.2f} GPU temp: {GPU_temp:05.2f}', end='')
            avg_GPU += GPU_temp
            avg_CPU += CPU_temp
            if (counter % opts.log == 0):
                y_axis_CPU.append(CPU_temp)
                y_axis_GPU.append(GPU_temp)
                x_axis.append((datetime.now()-delta).strftime("%I:%M:%S"))
                if stop > 0:
                    stop -= 1
                if stop == 0:
                    break
            sleep(cycle_duration)
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(str(e))
            break
    if opts.silent == False:
        print(
            f'\nAvg CPU temp: {(avg_CPU/counter):05.2f} Avg GPU temp: {(avg_GPU/counter):05.2f} Data recorded over: {((counter*cycle_duration)/60):05.2f} minutes')
    if opts.graph == True:
        plot(x_axis, y_axis_CPU, y_axis_GPU)
    if opts.output != None:
        save_csv(x_axis, y_axis_CPU, y_axis_GPU, opts.output)


if __name__ == "__main__":
    main()
