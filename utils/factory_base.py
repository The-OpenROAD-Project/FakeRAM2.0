#!/usr/bin/env python3


class FactoryBase:
    """Base class for factory registration and creation"""

    _registry = {}

    @classmethod
    def get_key(self, memory_type, port_config):
        """Returns the key from the memory_type and port_config"""
        return f"{port_config}_{memory_type}"

    @classmethod
    def register(self, memory_type, port_config, klass):
        """Registers a class for the given memory_type and port_config"""
        self._registry[self.get_key(memory_type, port_config)] = klass

    @classmethod
    def create(
        self,
        name,
        width_in_bits,
        depth,
        num_banks,
        memory_type,
        port_config,
        process,
        timing_data,
    ):
        """
        Creates and returns the requested object based on the factory registry
        """
        key = self.get_key(memory_type, port_config)
        klass = self._registry.get(key)
        if klass is None:
            raise ValueError(
                f"No class registered under key: {memory_type} {port_config}"
            )
        return klass(name, width_in_bits, depth, num_banks, process, timing_data)
