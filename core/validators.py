from pathlib import Path
from django.core.exceptions import ValidationError
from PIL import Image, UnidentifiedImageError

def validate_file(value):
    if value.size > 5 * 1024 * 1024:
        raise ValidationError('Files must be 5 MB or smaller.')
    suffix = Path(value.name).suffix.lower()
    if suffix not in {'.pdf', '.csv'}:
        raise ValidationError('Only PDF and CSV documents are allowed.')
    value.seek(0)
    content = value.read()
    value.seek(0)
    if suffix == '.pdf' and not content.startswith(b'%PDF-'):
        raise ValidationError('Upload a valid PDF document.')
    if suffix == '.csv':
        try:
            decoded = content.decode('utf-8-sig')
        except UnicodeDecodeError as exc:
            raise ValidationError('CSV files must use UTF-8 encoding.') from exc
        if '\x00' in decoded or '<script' in decoded.lower():
            raise ValidationError('Invalid CSV content.')

def validate_resume(value):
    validate_file(value)
    if Path(value.name).suffix.lower() != '.pdf':
        raise ValidationError('Resumes must be PDF documents.')

def validate_image(value):
    if value.size > 5 * 1024 * 1024:
        raise ValidationError('Images must be 5 MB or smaller.')
    if Path(value.name).suffix.lower() not in {'.jpg', '.jpeg', '.png', '.webp'}:
        raise ValidationError('Use a .jpg, .jpeg, .png, or .webp image file.')
    try:
        value.seek(0)
        with Image.open(value) as img:
            if img.format not in {'JPEG', 'PNG', 'WEBP'} or img.width * img.height > 20000000:
                raise ValidationError('Use a JPEG, PNG or WebP image under 20 megapixels.')
            img.verify()
    except (UnidentifiedImageError, OSError, Image.DecompressionBombError) as exc:
        raise ValidationError('Upload a valid image.') from exc
    finally:
        value.seek(0)
