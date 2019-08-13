# Simple Download

Simple Python file downloader.

## Usages

```python
from simple_download import download
download('https://example.com/file.txt')
```

### Arguments

- `url` {string} -- download url
- `save_as` {string/pathlib.Path} -- output file (default: {None})
- `save_path` {string/pathlib.Path} -- folder to save downloaded file to (default: {None})

### Keyword Arguments:
- `chunk_size` {number} -- download stream chunk size (default: {4096})

### Returns

- `pathlib.Path` -- full path of downloaded file
