"""Wrapper for JSON parser and logger file settings."""

from os import listdir
import logging
import shutil
import json


class JSONReader:
    def __init__(self, link: str):
        with open(link, "r") as f:
            self.file = f.readlines()
        self.link = link

    def get_number_of_new_log(self, destination="logs/") -> int:
        """Return count of already existing log files."""
        return len(listdir(destination))

    def create_new_log(self, destination="logs/"):
        """Creating new log file if folder.

        Args:
            destination -> logs folder, 'logs/' by default.
        """
        filename = destination + f"wargame{self.get_number_of_new_log()}.log"
        open(filename, "w+").close()

    def check_for_copy(self) -> str:
        """Checking for already played game with this config file.

        Returns:
            Filename -> if this game already played
            None -> if game not played yet.
        """
        checkline = "DEBUG:root:" + str(self.file)
        for i in range(self.get_number_of_new_log()):

            with open(f"logs\wargame{i}.log", "r") as filetmp:
                for line in filetmp:
                    if checkline in str(line):
                        return filetmp.name
                    break
        return ""

    def initiate_logger(self) -> None:
        logging.basicConfig(filename=f'logs\wargame{self.get_number_of_new_log()-1}.log',
                            level=logging.DEBUG)
        logging.debug(self.file)

    def get_parsed(self) -> json:
        """Get parsed info from json config file into python dictionary"""
        with open(self.link) as f:
            data = json.load(f)
        return data
