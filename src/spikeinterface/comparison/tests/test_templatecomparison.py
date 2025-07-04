import shutil
import pytest
import numpy as np

from spikeinterface.core import create_sorting_analyzer, generate_ground_truth_recording
from spikeinterface.comparison import compare_templates, compare_multiple_templates


# def setup_module():
#     if test_dir.is_dir():
#         shutil.rmtree(test_dir)
#     test_dir.mkdir(exist_ok=True)


def test_compare_multiple_templates():
    duration = 60
    num_channels = 8

    seed = 0
    rec, sort = generate_ground_truth_recording(
        durations=[duration],
        num_channels=num_channels,
        seed=seed,
    )

    # split recording in 3 equal slices
    fs = rec.get_sampling_frequency()
    rec1 = rec.frame_slice(start_frame=0 * fs, end_frame=duration / 3 * fs)
    rec2 = rec.frame_slice(start_frame=duration / 3 * fs, end_frame=2 / 3 * duration * fs)
    rec3 = rec.frame_slice(start_frame=2 / 3 * duration * fs, end_frame=duration * fs)
    sort1 = sort.frame_slice(start_frame=0 * fs, end_frame=duration / 3 * fs)
    sort2 = sort.frame_slice(start_frame=duration / 3 * fs, end_frame=2 / 3 * duration * fs)
    sort3 = sort.frame_slice(start_frame=2 / 3 * duration * fs, end_frame=duration * fs)

    # compute waveforms
    sorting_analyzer_1 = create_sorting_analyzer(sort1, rec1, format="memory")
    sorting_analyzer_2 = create_sorting_analyzer(sort2, rec2, format="memory")
    sorting_analyzer_3 = create_sorting_analyzer(sort3, rec3, format="memory")

    for sorting_analyzer in (sorting_analyzer_1, sorting_analyzer_2, sorting_analyzer_3):
        sorting_analyzer.compute(["random_spikes", "templates"])

    # paired comparison
    temp_cmp = compare_templates(sorting_analyzer_1, sorting_analyzer_2)

    for u1 in temp_cmp.hungarian_match_12.index.values:
        u2 = temp_cmp.hungarian_match_12[u1]
        if u2 != -1 and u2 != "":
            assert u1 == u2

    # multi-comparison
    temp_mcmp = compare_multiple_templates([sorting_analyzer_1, sorting_analyzer_2, sorting_analyzer_3])
    # assert unit ids are the same across sessions (because of initial slicing)
    for unit_dict in temp_mcmp.units.values():
        unit_ids = unit_dict["unit_ids"].values()
        if len(unit_ids) > 1:
            assert len(np.unique(unit_ids)) == 1


if __name__ == "__main__":
    test_compare_multiple_templates()
