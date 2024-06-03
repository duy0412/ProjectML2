import cv2 
import numpy as np
import os

def get_staff_lines(width, height, in_img, threshold = 0.8):
    # initial_lines: list of all initial lines that maybe extended #
    initial_lines = []

    # row_histogram: histogram of all row, contains number of black cell for each row #
    row_histogram = [0] * height

    # staff_lines: list of staff lines in our image #
    staff_lines = []
    staff_lines_thicknesses = []

    # Calculate histogram for rows #
    for r in range(height):
        for c in range(width):
            if in_img[r][c] == 0:
                row_histogram[r] += 1

    # Get only rows which have black pixels larger that threshold #
    for row in range(len(row_histogram)):
        if row_histogram[row] >= (width * threshold):
            initial_lines.append(row)

    # it: iterator over all doubtful lines #
    it = 0

    # cur_thinkneed: current thickness of line which may extended #
    cur_thickness = 1

    while it < len(initial_lines):
        # Save starting row of staff line #
        if cur_thickness == 1:
            staff_lines.append(initial_lines[it])

        if it == int(len(initial_lines) - 1):
            staff_lines_thicknesses.append(cur_thickness)

        # Try to extend line thickness #
        # If Failed: 1.save current thickness, 2.rest thickness #
        elif initial_lines[it] + 1 == initial_lines[it + 1]:
            cur_thickness += 1
        else:
            staff_lines_thicknesses.append(cur_thickness)
            cur_thickness = 1

        it += 1

    # Return the staff lines thicknesses and staff lines
    return staff_lines_thicknesses, staff_lines

def remove_single_line(line_thickness, line_start, in_img, width):
    # line_end: end pixel of the current staff line #
    line_end = line_start + line_thickness - 1

    for col in range(width):
        if in_img.item(line_start, col) == 0 or in_img.item(line_end, col) == 0:
            # If current staff is clear (up-down), then remove it directly #
            if in_img.item(line_start - 1, col) == 255 and in_img.item(line_end + 1, col) == 255:
                for j in range(line_thickness):
                    in_img.itemset((line_start + j, col), 255)

            # If current staff can be extended up, then extend #
            elif in_img.item(line_start - 1, col) == 255 and in_img.item(line_end + 1, col) == 0:
                if (col > 0 and in_img.item(line_end + 1, col - 1) != 0) and (col < width - 1 and in_img.item(line_end + 1, col + 1) != 0):
                    thick = line_thickness + 1
                    if thick < 1:
                        thick = 1
                    for j in range(int(thick)):
                        in_img.itemset((line_start + j, col), 255)

            # If current staff can be extended down, then extend #
            elif in_img.item(line_start - 1, col) == 0 and in_img.item(line_end + 1, col) == 255:
                if (col > 0 and in_img.item(line_start - 1, col - 1) != 0) and (col < width - 1 and in_img.item(line_start - 1, col + 1) != 0):
                    thick = line_thickness + 1
                    if thick < 1:
                        thick = 1
                    for j in range(int(thick)):
                        in_img.itemset((line_end - j, col), 255)
    return in_img

def remove_staff_lines(in_img, width, staff_lines, staff_lines_thicknesses):
    it = 0

    # Iterate over all staff lines and remove them line by line#
    while it < len(staff_lines):
        line_start = staff_lines[it]
        line_thickness = staff_lines_thicknesses[it]
        in_img = remove_single_line(line_thickness, line_start, in_img, width)
        it += 1
    return in_img

def preprocess(img):
    height= img.shape[0]
    width = img.shape[1]
    staff_lines_thicknesses, staff_lines = get_staff_lines(width, height, img)
    img = remove_staff_lines(img, width, staff_lines, staff_lines_thicknesses)
    return img



        
    