from collections import namedtuple


DataIngestionArtifact = namedtuple("DataIngestionArtifact", 
                                   ["main_file_path","is_ingested", "message"])