import cv2
import numpy as np

from webcolors import hex_to_rgb
from scipy.spatial import KDTree
from webcolors._definitions import (
    _CSS21_HEX_TO_NAMES,
    _CSS2_HEX_TO_NAMES,
    _CSS3_HEX_TO_NAMES,
    _HTML4_HEX_TO_NAMES,
)


async def mean_color(image_path: str) -> tuple[int, int, int]:
    image = cv2.imread(image_path)
    mean_blue = int(np.mean(image[:, :, 0]))
    mean_green = int(np.mean(image[:, :, 1]))
    mean_red = int(np.mean(image[:, :, 2]))

    return (mean_red, mean_green, mean_blue)


async def convert_rgb_to_names(rgb_tuple: tuple[int, int, int]) -> str:
    colors_dbs = (
        _CSS21_HEX_TO_NAMES,
        _CSS2_HEX_TO_NAMES,
        _CSS3_HEX_TO_NAMES,
        _HTML4_HEX_TO_NAMES,
    )
    names = []
    rgb_values = []

    for color_db in colors_dbs:
        for color_hex, color_name in color_db.items():
            names.append(color_name)
            rgb_values.append(hex_to_rgb(color_hex))

    kdt_db = KDTree(rgb_values)
    distance, index = kdt_db.query(rgb_tuple)
    return names[index]
