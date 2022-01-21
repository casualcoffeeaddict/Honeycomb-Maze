def get_range(num):
    if num % 2 == 1:
        # odd numbers
        x = num // 2
        return -x, x
    elif num % 2 == 0:
        # even numbers
        x = 4 // 2
        return 1 - x, x

def generate_coordinates(row, col):
    cubic_coordinates = []
    row_start, row_end = get_range(row)
    column_start, column_end = get_range(col)
    for y in range(row_start, row_end + 1):
        for x in range(column_start, column_end + 1):
            cubic_coordinates.append([x, y])
    return cubic_coordinates

def cube_to_axial_conversion(list):
    hexagonal_coordinates = []
    for i in range(len(list)):
        x1 = list[i][0]
        y1 = list[i][1]
        x = int(y1)
        y = int(x1 - (y1 - (y1 & 1)) / 2)
        hexagonal_coordinates.append([x, y, -x - y])
    return hexagonal_coordinates


def main():
    # cubic_cooridinates = generate_coordinates(5, 5)
    print(cube_to_axial_conversion(generate_coordinates(5,5)))
    # print(cube_to_axial_conversion([[+1, -1]]))


if __name__ == '__main__':
    main()
