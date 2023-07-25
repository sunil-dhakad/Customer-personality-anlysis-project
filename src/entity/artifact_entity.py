from collections import namedtuple


DataIngestionArtifact = namedtuple("DataIngestionArtifact", 
                                   ["main_file_path","is_ingested", "message"])

DataValidationArtifact = namedtuple("DataValidationArtifact",
                                    ["schema_file_path","is_validated","message"])