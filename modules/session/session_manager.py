from typing import Any, Optional

import streamlit as st


class SessionManager:
    """
    Provides a wrapper around Streamlit's session state.

    This class centralizes all interactions with
    `st.session_state`, allowing the rest of the
    application to remain independent of Streamlit's
    session management implementation.
    """


    def set(self, key: str, value: Any) -> None:
        """
        Store a value in the current session.

        Associates the specified key with the provided value
        inside Streamlit's session state.

        Args:
            key: The session key.
            value: The value to store.
        """

        st.session_state[key] = value



    def get(self, key: str, default: Any = None) -> Any:
        """
        Retrieve a value from the current session.

        Returns the value associated with the specified
        session key. If the key does not exist, the
        provided default value is returned instead.

        Args:
            key: The session key.
            default: The value to return if the key
                does not exist.

        Returns:
            The stored session value if found;
            otherwise the provided default value.
        """

        return st.session_state.get(key, default)


    def contains(self, key: str) -> bool:
        """
        Check whether a session key exists.

        Determines whether the specified key is currently
        stored in the active session.

        Args:
            key: The session key.

        Returns:
            True if the key exists;
            otherwise False.
        """

        return key in st.session_state


    def remove(self, key: str) -> None:
        """
        Remove a value from the current session.

        Deletes the specified key from the active session
        if it exists. If the key is not present, no action
        is performed.

        Args:
            key: The session key to remove.
        """

        if key in st.session_state:
            del st.session_state[key]


    def clear(self) -> None:
        """
        Clear the current session.

        Removes all values stored in the active
        Streamlit session state.
        """

        st.session_state.clear()

