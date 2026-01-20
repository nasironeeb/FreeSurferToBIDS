"""
Test the FreeSurfer to BIDS conversion functionality.
"""

from functions import FormatBIDS


if __name__ == "__main__":

    # Path configuration
    BASE = "~/derivatives/"
    SOURCE = BASE + "fsreconall_versionX"
    DESTINATION = BASE + "fsreconall_versionX_formatBIDS"

    converter = FormatBIDS(SOURCE, DESTINATION)
    converter.run_conversion()
