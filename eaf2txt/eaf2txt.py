from pathlib import Path
from xml.etree import ElementTree

import pandas as pd


def _parse_annotation(annotation: ElementTree.Element, tier: ElementTree.Element):
    """
    ANNOTATIONs are nested within TIERs which have PARTICIPANT and TIER_ID attributes we need to save.
    ANNOTATIONs contain either:
    - an ALIGNABLE_ANNOTATION that has TIME_SLOT_REF1 and TIME_SLOT_REF2 properties that correspond to start and end
    of the event, or
    - a REF_ANNOTATION that refers to an ALIGNABLE_ANNOTATION
    Both types contain an ANNOTATION_VALUE node whose text we need to save.

    :param annotation: ANNOTATION node from the parsed eaf file
    :param tier: its parent TIER node
    :return: dict with all the attributes/values listed above.
    """
    child = annotation.find('ALIGNABLE_ANNOTATION') or annotation.find('REF_ANNOTATION')
    if child.tag == 'ALIGNABLE_ANNOTATION':
        parsed = dict(
            time_slot_ref_1=child.get('TIME_SLOT_REF1'),
            time_slot_ref_2=child.get('TIME_SLOT_REF2'))
    elif child.tag == 'REF_ANNOTATION':
        parsed = dict(
            annotation_ref=child.get('ANNOTATION_REF')
        )

    parsed.update(
        annotation_id=child.get('ANNOTATION_ID'),
        participant=tier.get('PARTICIPANT'),
        tier_id=tier.get('TIER_ID'),
        value=child.find('ANNOTATION_VALUE').text
    )

    return parsed


def _parse_eaf(eaf_path: (str, Path)) -> (pd.DataFrame, pd.DataFrame):
    """
    Extracts all the necessary data from the EAF file: all time slots (ids and times) and annotations (tier id,
    participant id, start/end time slots, annotation id, (or the reference annotation id in case of reference
    annotations)
    :param eaf_path: path to the EAF file
    :return: (times, annotations) - time and annotation data dataframes
    """
    parsed = ElementTree.parse(eaf_path)

    # Times are stored as elements of the TIME_ORDER node. each time has its id
    times = pd.DataFrame(
        [dict(time_slot_id=el.get('TIME_SLOT_ID'),
              time_value=el.get('TIME_VALUE'))
         for el in parsed.find('TIME_ORDER')])

    # ANNOTATIONs are nested within TIERs.
    annotations = pd.DataFrame(
        [_parse_annotation(annotation, tier)
         for tier in parsed.findall('TIER')
         for annotation in tier.findall('ANNOTATION')])

    return times, annotations


def convert_eaf_to_txt(eaf_path: (str, Path)) -> Path:
    pass
