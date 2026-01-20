"""
Convert FreeSurfer output structures into a BIDS-compatible format.
This script reorganizes nested FreeSurfer data and verifies transfer integrity.
"""

import logging
import shutil
from pathlib import Path

# Configure logging for better traceability
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


class FormatBIDS:
    """
    Handles the conversion of FreeSurfer derivatives to a BIDS session structure.
    """

    def __init__(self, freesurfer_path, bids_output_path, move_files=False):
        """
        Initialize the converter.

        Args:
            freesurfer_path (str/Path): Path to the source fsreconall folder.
            bids_output_path (str/Path): Path to the destination BIDS folder.
            move_files (bool): If True, move files instead of copying.
        """
        self.fs_path = Path(freesurfer_path)
        self.bids_path = Path(bids_output_path)
        self.move_files = move_files
        self.expected_elements = {
            "channels.txt", "label", "mri", "scripts", "stats", "surf", "tmp",
            "touch", "trash", "xhemi", "xhemi-textures.npy"
        }

        # Ensure the destination root exists
        if not self.bids_path.exists():
            self.bids_path.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def get_size(path):
        """
        Calculate the total size of a file or directory in bytes.
        """
        path = Path(path)
        if path.is_file():
            return path.stat().st_size
        return sum(f.stat().st_size for f in path.rglob('*') if f.is_file())

    def _find_folder_depth(self, base_dir, max_depth=3):
        """
        Identifies the depth at which the actual FreeSurfer data resides.
        """
        for i in range(max_depth):
            pattern = "/".join(["*"] * (i + 1))
            current_elements = {item.name for item in base_dir.glob(pattern)}
            # Check if our expected core folders are a subset of what's found
            if self.expected_elements.issubset(current_elements):
                return i + 1
        return None

    def _transfer_item(self, src, dst):
        """
        Copies or moves a single item and verifies its size integrity.
        """
        src_size = self.get_size(src)

        try:
            if src.is_dir():
                # symlinks=True preserves fsaverage links (crucial for FreeSurfer)
                shutil.copytree(src, dst, dirs_exist_ok=True, symlinks=True)
            else:
                shutil.copy2(src, dst)

            # Verification logic
            dst_size = self.get_size(dst)
            if src_size == dst_size:
                logging.info("  [OK] %s transferred correctly.", src.name)
            else:
                logging.error("  [ERROR] Size mismatch for %s! (Src: %d, Dst: %d)",
                              src.name, src_size, dst_size)

        except (shutil.Error, OSError) as err:
            logging.error("  [FAILED] Could not transfer %s: %s", src.name, err)

    def run_conversion(self):
        """
        Iterates through subjects and sessions to perform the reorganization.
        """
        logging.info("Starting conversion from %s", self.fs_path)

        for subject_dir in self.fs_path.iterdir():
            if not (subject_dir.is_dir() and subject_dir.name.startswith("sub-")):
                continue

            sub_id = subject_dir.name
            logging.info("Processing subject: %s", sub_id)

            for session_dir in subject_dir.iterdir():
                if not (session_dir.is_dir() and session_dir.name.startswith("ses-")):
                    continue

                ses_id = session_dir.name
                # Final destination: .../sub-ID/ses-ID/
                target_session_path = self.bids_path / sub_id / ses_id
                target_session_path.mkdir(parents=True, exist_ok=True)

                # Locate the FreeSurfer content (e.g., inside the nested sub-ID folder)
                depth = self._find_folder_depth(session_dir)
                if depth:
                    pattern = "/".join(["*"] * depth)
                    for item in session_dir.glob(pattern):
                        self._transfer_item(item, target_session_path / item.name)
                else:
                    logging.warning("No FreeSurfer data found for %s/%s", sub_id, ses_id)

