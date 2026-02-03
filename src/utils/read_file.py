from pathlib import Path
from typing import Union, BinaryIO, Optional

def read_file_content(file_source: Union[str, Path, BinaryIO], filename: Optional[str] = None) -> str:
    """
    Reads content from a file path or file-like object.
    
    Args:
        file_source: A file path (str/Path) or a file-like object (BinaryIO).
        filename: The name of the file (required if file_source is a file-like object).
        
    Returns:
        A string formatted as "--- File: {name} ---\n{content}\n".
        
    Raises:
        FileNotFoundError: If file path does not exist.
        ValueError: If filename is missing for file-like objects.
        ImportError: If required libraries (pypdf, python-docx) are missing.
        Exception: For other read errors.
    """
    
    if isinstance(file_source, (str, Path)):
        path = Path(file_source)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")
        
        name = path.name
        suffix = path.suffix.lower()
        source = path
    else:
        if not filename:
            raise ValueError("filename must be provided for file-like objects")
        name = filename
        suffix = Path(filename).suffix.lower()
        source = file_source

    text = ""

    try:
        if suffix == ".pdf":
            try:
                import pypdf
                reader = pypdf.PdfReader(source)
                for page in reader.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted + "\n"
            except ImportError:
                raise ImportError("pypdf is required to read PDF files")
                
        elif suffix in [".docx", ".doc"]:
            try:
                import docx
                doc = docx.Document(source)
                text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            except ImportError:
                raise ImportError("python-docx is required to read DOCX files")
                
        else:
            # Text based
            if isinstance(file_source, (str, Path)):
                text = Path(file_source).read_text(encoding='utf-8')
            else:
                # Handle file-like objects (bytes)
                # Streamlit UploadedFile has getvalue(), but standard BytesIO doesn't necessarily use it for this.
                # Use read() if available, else getvalue()
                if hasattr(file_source, "getvalue"):
                    content_bytes = file_source.getvalue()
                else:
                    if hasattr(file_source, "seek"):
                        file_source.seek(0)
                    content_bytes = file_source.read()
                
                text = content_bytes.decode("utf-8")
                
    except Exception as e:
        raise Exception(f"Error processing file {name}: {str(e)}") from e

    return f"--- File: {name} ---\n{text}\n"
