"""
Test the FreeSurfer to BIDS conversion functionality.
"""

from functions import FormatBIDS


if __name__ == "__main__":

    # Path configuration
    BASE = "~/derivatives/"
    SOURCE = BASE + "fsreconall_versionX"
    DESTINATION = BASE + "fsreconall_versionX_formatBIDS"
    MOVE_FILES = False  # Set to True to move files instead of copying
    DRY_RUN = False  # Set to True to simulate the operation without making changes

    converter = FormatBIDS(SOURCE, DESTINATION, move_files=MOVE_FILES, dry_run=DRY_RUN)
    converter.run_conversion()
