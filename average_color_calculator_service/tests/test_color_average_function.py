import os, pytest, cv2
import numpy as np

from src.color_calc_functions import mean_color


@pytest.fixture(scope="module")
def setup_images():

    test_dir = "test_images"
    os.makedirs(test_dir, exist_ok=True)

    red_image_path = os.path.join(test_dir, "red_image.png")
    green_image_path = os.path.join(test_dir, "green_image.png")
    blue_image_path = os.path.join(test_dir, "blue_image.png")

    red_image = np.zeros((100, 100, 3), dtype=np.uint8)
    red_image[:] = (0, 0, 255)
    cv2.imwrite(red_image_path, red_image)

    green_image = np.zeros((100, 100, 3), dtype=np.uint8)
    green_image[:] = (0, 255, 0)
    cv2.imwrite(green_image_path, green_image)

    blue_image = np.zeros((100, 100, 3), dtype=np.uint8)
    blue_image[:] = (255, 0, 0)
    cv2.imwrite(blue_image_path, blue_image)

    yield {
        "red_image_path": red_image_path,
        "green_image_path": green_image_path,
        "blue_image_path": blue_image_path,
    }

    for file in os.listdir(test_dir):
        file_path = os.path.join(test_dir, file)
        os.remove(file_path)
    os.rmdir(test_dir)


@pytest.mark.asyncio
async def test_mean_color_red_image(setup_images):
    expected_color = (255, 0, 0)
    result = await mean_color(setup_images["red_image_path"])
    assert result == expected_color


@pytest.mark.asyncio
async def test_mean_color_green_image(setup_images):
    expected_color = (0, 255, 0)
    result = await mean_color(setup_images["green_image_path"])
    assert result == expected_color


@pytest.mark.asyncio
async def test_mean_color_blue_image(setup_images):
    expected_color = (0, 0, 255)
    result = await mean_color(setup_images["blue_image_path"])
    assert result == expected_color
