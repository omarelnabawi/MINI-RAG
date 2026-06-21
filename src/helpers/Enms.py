from enum import Enum

class response_signal(Enum):
    File_validate_sucess="File validated successfully"
    File_type_not_supported="File type not supported"
    File_size_exceeded="File size exceeded the limit"
    File_upload_failed="File upload failed"
    File_upload_success="File uploaded successfully"