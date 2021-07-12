from pathlib import Path
from shutil import copy
import os

from ..eaf2txt import convert_eaf_to_txt


def test_convert_eaf_to_txt(tmp_path, request):
    source_eaf = Path(request.fspath.dirpath('5959-0GS0.eaf'))
    correct_txt = source_eaf.with_suffix('.txt')

    eaf_copy = tmp_path / source_eaf.name
    copy(source_eaf, eaf_copy)

    converted = convert_eaf_to_txt(eaf_path=eaf_copy)
    assert isinstance(converted, os.PathLike)
    assert converted.exists()
    assert correct_txt.read_text() == converted.read_text()
