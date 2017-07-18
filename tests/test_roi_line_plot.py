from pdsspect import roi_line_plot
from pdsspect.pdsspect_image_set import PDSSpectImageSet

from . import *  # Import Test File Paths from __init__

import pytest
import numpy as np


class TestROIHistogramModel(object):

    image_set = PDSSpectImageSet([FILE_1, FILE_3])

    @pytest.fixture()
    def test_model(self):
        self.image_set = PDSSpectImageSet([FILE_1, FILE_3])
        return roi_line_plot.ROILinePlotModel(self.image_set)

    def test_wavelengths(self, test_model):
        self.image_set.images[0].wavelength = 2
        assert test_model.wavelengths == [2]
        self.image_set.images[1].wavelength = 1
        assert test_model.wavelengths == [1, 2]
        self.image_set.images[0].wavelength = float('nan')
        assert test_model.wavelengths == [1]

    def test_data_with_color(self, test_model):
        coords = np.array([[42, 24]])
        self.image_set.add_coords_to_roi_data_with_color(coords, 'red')
        assert test_model.data_with_color('red') == []
        self.image_set.images[1].wavelength = 2
        assert len(test_model.data_with_color('red')) == 1
        assert test_model.data_with_color('red')[0][0] == 24.0
        self.image_set.images[0].wavelength = 1
        assert len(test_model.data_with_color('red')) == 2
        assert test_model.data_with_color('red')[1][0] == 24.0
