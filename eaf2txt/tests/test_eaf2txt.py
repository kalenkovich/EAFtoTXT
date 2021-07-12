from pathlib import Path
from shutil import copy
import os

from ..eaf2txt import convert_eaf_to_txt


def test_convert_eaf_to_txt(tmp_path, request, capsys):
    source_eaf = Path(request.fspath.dirpath('5959-0GS0.eaf'))
    correct_txt = source_eaf.with_suffix('.txt')

    eaf_copy = tmp_path / source_eaf.name
    copy(source_eaf, eaf_copy)

    converted = convert_eaf_to_txt(eaf_path=eaf_copy, order=False)
    assert isinstance(converted, os.PathLike)
    assert converted.exists()
    assert correct_txt.read_text() == converted.read_text()

    converted = convert_eaf_to_txt(eaf_path=eaf_copy, order=True)
    correct_ordered = correct_txt.with_stem(correct_txt.stem + '_ordered')
    assert isinstance(converted, os.PathLike)
    assert converted.exists()
    assert correct_ordered.read_text() == converted.read_text()

    converted = convert_eaf_to_txt(eaf_path=eaf_copy, summary=True)
    out, err = capsys.readouterr()
    assert out == (
        'Participant CHI had the highest total turn count: 38\n'
        'Participant FA1 had the highest total total speaking duration: 39367\n'
        'Participant CHI had the highest total non-speaking turn count: 38\n')
