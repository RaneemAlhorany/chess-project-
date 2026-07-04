from typing import Any, Optional

import streamlit as st


class SessionManager:
    """
    Manages Streamlit session state in a clean OOP way.

    This class acts as a wrapper around `st.session_state`
    so the rest of the application does NOT directly depend on Streamlit.
    """

    def set(self, key: str, value: Any) -> None:
        """
        Stores a value in session state.

        Args:
            key (str): Session key.
            value (Any): Value to store.
        """

        st.session_state[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        """
        Retrieves a value from session state.

        Args:
            key (str): Session key.
            default (Any): Default value if key does not exist.

        Returns:
            Any: Stored value or default.
        """

        return st.session_state.get(key, default)

    def contains(self, key: str) -> bool:
        """
        Checks if a key exists in session state.

        Args:
            key (str): Session key.

        Returns:
            bool: True if key exists, False otherwise.
        """

        return key in st.session_state

    def remove(self, key: str) -> None:
        """
        Removes a key from session state if it exists.

        Args:
            key (str): Session key to remove.
        """

        if key in st.session_state:
            del st.session_state[key]

    def clear(self) -> None:
        """
        Clears entire session state.
        """

        st.session_state.clear()