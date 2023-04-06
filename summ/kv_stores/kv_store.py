# -*- coding: utf-8 -*-


from typing import List, Any
from abc import ABC, abstractmethod


class KVStore(ABC):
    """ The interface for key-value storage system."""

    @abstractmethod
    def get(self, key: str) -> str:
        """ Get the value of a specific value.

        Args:
            key: a query key in string format.

        Returns:
            The corresponding value in string format.

        Raises:
            KeyError: if the key is not exist.
        """
        pass

    @abstractmethod
    def set(self, key: str,  val: str) -> Any:
        """ Insert one (key, val) pair to the storage."""
        pass

    @abstractmethod
    def keys(self) -> Any:
        """ Return all keys in the storage."""
        pass

