#!/usr/bin/env python3


class RWPortGroup:
    """
    Collection of related ports on a memory. Includes:

        clock
        write enable
        address bus
        data input bus
        data output bus
    """

    def __init__(self, suffix=None):
        """
        Initializer
        """

        # Defaults
        self._default_write_enable_name = "we_"
        self._default_addr_bus_name = "addr_"
        self._default_data_input_bus_name = "din_"
        self._default_data_output_bus_name = "dout_"
        self._default_clk_name = "clk_"

        # If non-empty suffix is passed in, use it to name the busses.
        # Otherwise, the port group name need to be defined separately
        self._suffix = suffix
        if suffix and suffix != "":
            self._set_names_by_suffix(suffix)
        else:
            self._write_enable_name = None
            self._addr_bus_name = None
            self._data_input_bus_name = None
            self._data_output_bus_name = None
            self._clk_name = None

    def set_clock_name(self, name):
        """Sets the clock port name"""
        self._clk_name = name

    def get_clock_name(self):
        """Gets the clock port name"""
        return self._clk_name

    def set_write_enable_name(self, name):
        """Sets the write enable port name"""
        self._write_enable_name = name

    def get_write_enable_name(self):
        """Gets the write enable port name"""
        return self._write_enable_name

    def set_address_bus_name(self, name):
        """Sets the address bus name"""
        self._addr_bus_name = name

    def get_address_bus_name(self):
        """Gets the address bus name"""
        return self._addr_bus_name

    def set_data_input_bus_name(self, name):
        """Sets the data input bus name"""
        self._data_input_bus_name = name

    def get_data_input_bus_name(self):
        """Gets the data input bus name"""
        return self._data_input_bus_name

    def set_data_output_bus_name(self, name):
        """Sets the data output bus name"""
        self._data_output_bus_name = name

    def get_data_output_bus_name(self):
        """Gets the data output bus name"""
        return self._data_output_bus_name

    def _set_names_by_suffix(self, suffix):
        """
        Sets the port & bus names based on the default for the port or bus
        along with the suffix
        """

        self.set_write_enable_name(self._default_write_enable_name + suffix)
        self.set_address_bus_name(self._default_addr_bus_name + suffix)
        self.set_data_input_bus_name(self._default_data_input_bus_name + suffix)
        self.set_data_output_bus_name(self._default_data_output_bus_name + suffix)
        self.set_clock_name(self._default_clk_name + suffix)

    def get_suffix(self):
        """Returns the suffix"""
        return self._suffix
