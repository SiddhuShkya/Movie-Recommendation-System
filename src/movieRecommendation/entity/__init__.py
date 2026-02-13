from dataclasses import dataclass


@dataclass
class DataIngestionConfig:
    root_dir: str
    drive_file_id: str
    local_data_file: str
    unzip_dir: str
