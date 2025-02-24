#!/usr/bin/env python3


class TestUtils:
    @staticmethod
    def get_base_process_data():
        """Returns dict with process data"""
        return {
            "tech_nm": 7,
            "voltage": 0.7,
            "metal_prefix": "M",
            "metal_layer": "M4",
            "pin_width_nm": 24,
            "pin_pitch_nm": 48,
            "metal_track_pitch_nm": 48,
            "contacted_poly_pitch_nm": 54,
            "column_mux_factor": 1,
            "fin_pitch_nm": 27,
            "manufacturing_grid_nm": 1,
            "snap_width_nm": 190,
            "snap_height_nm": 1400,
        }
