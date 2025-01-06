
from django.core.exceptions import ValidationError
import os
def validate_video_file(value):
    """Validate uploaded video file format and size."""
    # Check file size (limit: 50MB, adjust as needed)
    max_size_mb = 50
    if value.size > max_size_mb * 1024 * 1024:
        raise ValidationError(f"The maximum file size allowed is {max_size_mb}MB.")
    
    # Validate file extension (common video formats)
    valid_extensions = ['.mp4', '.mov', '.avi', '.mkv']

    ext = os.path.splitext(value.name)[1].lower()
    if ext not in valid_extensions:
        raise ValidationError(f"Unsupported file extension '{ext}'. Allowed extensions: {', '.join(valid_extensions)}.")
