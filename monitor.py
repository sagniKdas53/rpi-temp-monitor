import argparse
import csv
import subprocess
from datetime import datetime, timedelta
from time import sleep
import matplotlib.pyplot as mplt

import plotext as plt


def save_csv(x_axis, y_axis_CPU, y_axis_GPU, csv_file):
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["time", "CPU", "GPU"])
        for time, CPU, GPU in zip(x_axis, y_axis_CPU, y_axis_GPU):
            writer.writerow([time, CPU, GPU])


def plot(x_axis, y_axis_CPU, y_axis_GPU):
    plt.date_form('I:M:S')
    plt.plot(x_axis, y_axis_CPU, label="CPU")
    plt.plot(x_axis, y_axis_GPU, label="GPU")
    plt.title("Temperature plot")
    plt.xlabel("time")
    plt.ylabel("temp")
    plt.show()


def plot_matplotlib(x_axis, y_axis_CPU, y_axis_GPU, save=True):
    mplt.plot(x_axis, y_axis_CPU, label="CPU")
    mplt.plot(x_axis, y_axis_GPU, label="GPU")
    mplt.ylabel('Temperature ($^\circ$C)')
    mplt.xlabel('Time H:M:S')
    mplt.title("Temperature plot")
    mplt.legend(loc="upper left")
    # mplt.show()
    if save:
        mplt.savefig('graph.png')


def main():
    parser = argparse.ArgumentParser(
        description="Measures and graphs tempertaure of raspberry pi")
    parser.add_argument('-d', '--duration', type=int, metavar="", required=True,
                        help="duration of each measuring cycle in seconds")
    parser.add_argument('-l', '--log', type=int, metavar="", required=True,
                        help="number of measuring cycles after which to log the value")
    parser.add_argument('-n', '--count', type=int, metavar="",  const=None, default=None,
                        help="number of logging cycles after which to stop, can be left blank to measure indefinitely (not recomended)")
    parser.add_argument('-o', '--output', type=str, metavar="", const=None, default=None,
                        help='name of the csv to save the data, leave blank to not save')

    group_graph = parser.add_mutually_exclusive_group()
    group_graph.add_argument('-b', '--basic', action="store_true",
                             help='print a graph in terminal')
    group_graph.add_argument('-a', '--advanced', action="store_true",
                             help='print a advanced graph')
    group_disp = parser.add_mutually_exclusive_group()
    group_disp.add_argument('-s', '--silent', action="store_true",
                            help="pass this to not display any output")
    group_disp.add_argument('-v', '--verbose', action="store_true",
                            help="display all output")
    opts = parser.parse_args()
    if opts.count == None:
        opts.count = -1
    counter = 0
    avg_GPU = 0
    avg_CPU = 0
    cycle_duration = opts.duration
    # Don't know why but this delta is needed to print the graph
    delta = timedelta(seconds=10, minutes=21, hours=5)
    x_axis_printable = [datetime.now().strftime("%I:%M:%S")]
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
                x_axis_printable.append(datetime.now().strftime("%I:%M:%S"))
                if opts.count > 0:
                    opts.count -= 1
                if opts.count == 0:
                    break
            sleep(cycle_duration)
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(str(e))
            break
    x_axis = x_axis[:-1]
    x_axis_printable = x_axis_printable[:-1]
    if opts.silent == False:
        print(
            f'\nAvg CPU temp: {(avg_CPU/counter):05.2f} Avg GPU temp: {(avg_GPU/counter):05.2f} Data recorded over: {((counter*cycle_duration)/60):05.2f} minutes')
    if opts.output != None:
        if '.' in opts.output:
            if 'csv' in opts.output.split('.') and opts.verbose == True:
                print('Saving data in:', opts.output)
        else:
            opts.output = opts.output+'.csv'
            if opts.verbose == True:
                print('Saving data in:', opts.output)
        save_csv(x_axis_printable, y_axis_CPU, y_axis_GPU, opts.output)
    if opts.basic == True or opts.advanced == True:
        if opts.verbose == True:
            print(
                f'\ny_axis_CPU= {y_axis_CPU}\ny_axis_GPU= {y_axis_GPU}\nx_axis= {x_axis_printable}')
        if opts.advanced == True:
            plot_matplotlib(x_axis_printable, y_axis_CPU, y_axis_GPU)
        elif opts.basic == True:
            plot(x_axis, y_axis_CPU, y_axis_GPU)


if __name__ == "__main__":
    main()