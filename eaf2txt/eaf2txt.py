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


def convert_eaf_to_data_frame(eaf_path: (str, Path)) -> pd.DataFrame:
    times, annotations = _parse_eaf(eaf_path)

    # Get the times for aligned annotations
    annotations = (annotations
        .merge(
        times.rename(columns=dict(time_value='start')),
        left_on='time_slot_ref_1',
        right_on='time_slot_id',
        how='left')
        .merge(
        times.rename(columns=dict(time_value='end')),
        left_on='time_slot_ref_2',
        right_on='time_slot_id',
        how='left'))

    # Get the times for the reference annotations by finding an annotation whose id is the one in the `annotation_ref`
    # column of the reference annotation. Some reference annotations refer to other reference annotations so we
    # need to do it iteratively.


    # The update methods aligns on indices
    annotations.set_index('annotation_ref', inplace=True)
    # Keep the number of annotations without times so that we stop when this number stops reducing.
    na_count = annotations.start.isnull().sum()
    na_count_new = 0
    while na_count_new != na_count:
        na_count = na_count_new
        annotations.update(
            annotations[['annotation_id', 'start', 'end']].dropna().set_index('annotation_id'))
        na_count_new = annotations.start.isnull().sum()
    annotations.reset_index(inplace=True)

    # Covert times to ints, add duration
    annotations['start'] = annotations.start.astype(int)
    annotations['end'] = annotations.end.astype(int)
    annotations['duration'] = annotations.end - annotations.start

    # Return a subset of columns in the correct order
    return annotations[['tier_id', 'participant', 'start', 'end', 'duration', 'value']]


def convert_eaf_to_txt(eaf_path: (str, Path), order=True) -> Path:
    """
    Converts eaf file to a tab-delimited file with ".txt" extension and no column names.
    Columns extracted: 'tier_id', 'participant', 'start', 'end', 'duration', 'value'
    :param order: order annotations chronolagically, list subtier annotations below the parent tier
    :param eaf_path: path to the EAF file
    :return: path to the txt file
    """
    annotations_df = convert_eaf_to_data_frame(eaf_path)

    if order:
        annotations_df = (annotations_df
            .assign(is_subtier=annotations_df.tier_id.str.contains('@'))
            .sort_values(by=['start', 'end', 'is_subtier', 'tier_id'])
            .drop(columns=['is_subtier'])
            .reset_index(drop=True))

    output_path = eaf_path.with_suffix('.txt')
    annotations_df.to_csv(output_path,
                          sep='\t',
                          index=False,
                          header=False)
    return output_path
