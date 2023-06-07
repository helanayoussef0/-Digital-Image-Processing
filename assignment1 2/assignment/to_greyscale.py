import numpy as np
import sys

def read_ppm(path):
    with open(path, "r") as f:
        data = f.readlines()
        header = data[:3]
        pixels = data[3:]
        return header, pixels

def write_pgm(path, header, pixels):
    with open(path, "w") as f:
        header[0] = "P2\n"
        header[1] = header[1].split()[0] + " " + header[1].split()[1] + "\n"
        header[2] = "255\n"
        f.writelines(header)
        for p in pixels:
            values = p.split()
            if len(values) < 3:
                break
            grey = int(sum(map(int, values)) / 3)
            f.write(str(grey) + " ")
        f.write("\n")

def to_greyscale(input_path, output_path):
    header, pixels = read_ppm(input_path)
    write_pgm(output_path, header, pixels)

if __name__ == "__main__":
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    to_greyscale(input_path, output_path)
