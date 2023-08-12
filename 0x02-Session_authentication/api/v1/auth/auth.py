#!/usr/bin/env python3
"""
Module of auth class
"""
from flask import request
from typing import List, TypeVar
import fnmatch


class Auth(object):
    """Template for all authentication system
    implemented in the project
    """

    def require_auth(self, path: str,
                     excluded_paths: List[str]) -> bool:
        """

        Args:
          - path(string): path to return
          - excluded_paths(list): list of paths to exclude

        Returns:
          - True if is authenticated otherwise false
        """
        if path is None:
            return True

        if excluded_paths is None or not excluded_paths:
            return True

        for excluded_path in excluded_paths:
            if fnmatch.fnmatch(path, excluded_path):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """

        Args:
          - request(Flask request): request object to make

        Returns:
          - The string: 'None - request'
        """
        if request is None:
            return None

        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        """

        Args:
          - request(request object): request object to make

        Returns:
          - Any type
        """
        return None
