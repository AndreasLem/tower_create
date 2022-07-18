# This is a sample Python script.

from tower_edit_functions import file_read_lines, tower_version_info, TowerBuilder


def main():
    pls_path = r"C:\Program Files\PLS"
    catalogues_path = r"C:\temp\pls\catalogues"
    tower_init_path = r"C:\temp\pls\python_tower"
    tower_init_file = r"test_tower_original.tow"

    input_path = r"C:\Users\AndreasLem\OneDrive - Groundline\Internal\Programming\TowerBuilder"

    lines = file_read_lines(tower_init_path, tower_init_file)
    tower_info = tower_version_info(pls_path)

    TowerBuilder.read_all_input(input_path)

    a = 1


if __name__ == '__main__':
    main()

