from __future__ import annotations

from pathlib import Path

from spikeinterface.core.core_tools import define_function_from_class

from .neobaseextractor import NeoBaseRecordingExtractor, NeoBaseSortingExtractor


class NeuronexusRecordingExtractor(NeoBaseRecordingExtractor):
    """
    Class for reading data from Neuronexus Allego.

    Based on :py:class:`neo.rawio.NeuronexusRawIO`

    Parameters
    ----------
    file_path : str
        The file path to the metadata .xdat.json file of an Allego session
    stream_id : str, default: None
        If there are several streams, specify the stream id you want to load.
    stream_name : str, default: None
        If there are several streams, specify the stream name you want to load.
    all_annotations : bool, default: False
        Load exhaustively all annotations from neo.
    use_names_as_ids : bool, default: False
        Determines the format of the channel IDs used by the extractor. If set to True, the channel IDs will be the
        names from NeoRawIO. If set to False, the channel IDs will be the ids provided by NeoRawIO.

        In Neuronexus the ids provided by NeoRawIO are the hardware channel ids stored as `ntv_chan_name` within
        the metada and the names are the `chan_names`


    """

    NeoRawIOClass = "NeuronexusRawIO"

    def __init__(
        self,
        file_path,
        stream_id=None,
        stream_name=None,
        all_annotations=False,
        use_names_as_ids=False,
    ):
        neo_kwargs = self.map_to_neo_kwargs(file_path)
        NeoBaseRecordingExtractor.__init__(
            self,
            stream_id=stream_id,
            stream_name=stream_name,
            all_annotations=all_annotations,
            use_names_as_ids=use_names_as_ids,
            **neo_kwargs,
        )

        self._kwargs.update(dict(file_path=str(Path(file_path).absolute())))

    @classmethod
    def map_to_neo_kwargs(cls, file_path):

        neo_kwargs = {"filename": str(file_path)}

        return neo_kwargs


read_neuronexus = define_function_from_class(source_class=NeuronexusRecordingExtractor, name="read_neuronexus")
