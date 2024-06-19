import pytest
from src.color_calc_functions import convert_rgb_to_names


@pytest.mark.asyncio
async def test_convert_rgb_to_names_red():
    rgb_tuple = (255, 0, 0)
    expected_name = "red"

    result = await convert_rgb_to_names(rgb_tuple)
    assert result == expected_name


@pytest.mark.asyncio
async def test_convert_rgb_to_names_green():
    rgb_tuple = (0, 255, 0)
    expected_name = "lime"

    result = await convert_rgb_to_names(rgb_tuple)
    assert result == expected_name


@pytest.mark.asyncio
async def test_convert_rgb_to_names_blue():
    rgb_tuple = (0, 0, 255)
    expected_name = "blue"

    result = await convert_rgb_to_names(rgb_tuple)
    assert result == expected_name


@pytest.mark.asyncio
async def test_convert_rgb_to_names_black():
    rgb_tuple = (0, 0, 0)
    expected_name = "black"

    result = await convert_rgb_to_names(rgb_tuple)
    assert result == expected_name


@pytest.mark.asyncio
async def test_convert_rgb_to_names_white():
    rgb_tuple = (255, 255, 255)
    expected_name = "white"

    result = await convert_rgb_to_names(rgb_tuple)
    assert result == expected_name


@pytest.mark.asyncio
async def test_convert_rgb_to_closest_name_firebrick():
    rgb_tuple = (170, 30, 38)  # 178, 34, 34 Firebrick
    expected_name = "firebrick"

    result = await convert_rgb_to_names(rgb_tuple)
    assert result == expected_name


@pytest.mark.asyncio
async def test_convert_rgb_to_closest_name_brown():
    rgb_tuple = (165, 30, 38)  # 165, 42, 42 Firebrick
    expected_name = "brown"

    result = await convert_rgb_to_names(rgb_tuple)
    assert result == expected_name
