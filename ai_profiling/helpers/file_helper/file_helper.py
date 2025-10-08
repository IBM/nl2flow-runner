from datetime import datetime
import os
from pathlib import Path
import pickle
import pprint
from typing import Any, Dict, Optional, Union
import json
from typing import List
from pydantic import BaseModel
import pandas as pd
from datasets import Dataset, DatasetDict
import signal
import logging


class DelayedKeyboardInterrupt:
    def __enter__(self):
        self.signal_received = False
        self.old_handler = signal.signal(signal.SIGINT, self.handler)

    def handler(self, sig, frame):
        self.signal_received = (sig, frame)
        logging.debug("SIGINT received. Delaying KeyboardInterrupt.")

    def __exit__(self, type, value, traceback):
        signal.signal(signal.SIGINT, self.old_handler)
        if self.signal_received:
            self.old_handler(*self.signal_received)


# with DelayedKeyboardInterrupt():
#     # stuff here will not be interrupted by SIGINT
#     critical_code()


def check_paths(paths: List[Path]) -> None:
    error_messages: List[str] = []
    for tmp_path in paths:
        if not os.path.exists(tmp_path):
            error_messages.append(f"{tmp_path} does not exist.")
    if len(error_messages) > 0:
        pprint.pp(error_messages)
        raise Exception("Invalid Directory Path")


def get_directory_path(tmp_path: str) -> str:
    base_path = os.path.basename(os.path.normpath(tmp_path))
    return (
        os.path.dirname(os.path.abspath(tmp_path))  # file path
        if "." in base_path
        else os.path.abspath(tmp_path)  # folder path
    )


def create_folders_recirsively_if_not_exist(tmp_path: str) -> None:
    directory_path = get_directory_path(tmp_path=tmp_path)

    if not os.path.isdir(directory_path):
        os.makedirs(directory_path)


def write_pickle_file(file_path: str, obj: Any) -> None:
    create_folders_recirsively_if_not_exist(tmp_path=file_path)
    with open(file_path, "wb") as f:
        pickle.dump(obj, f)


def read_pickle_file(file_path: str) -> Any:
    data = None
    with open(file_path, "rb") as f:
        data = pickle.load(f)
    return data


def write_txt_file(file_path: str, text: str) -> None:
    create_folders_recirsively_if_not_exist(tmp_path=file_path)
    with open(file_path, "w") as f:
        f.write(text)


def delete_file(file_path: Optional[Path]) -> None:
    if (file_path is not None) and os.path.exists(file_path):
        os.remove(file_path)  # clean up cache


def write_json_from_dict(file_path: str, dic: Dict) -> None:
    create_folders_recirsively_if_not_exist(tmp_path=file_path)
    with open(file_path, "w") as outfile:
        json.dump(dic, outfile)


def write_json(file_path: str, base_model: Union[BaseModel, List[BaseModel]]) -> None:
    create_folders_recirsively_if_not_exist(tmp_path=file_path)
    with open(file_path, "w") as f:
        if isinstance(base_model, List):
            f.write(json.dumps([model.model_dump() for model in base_model]))
        else:
            f.write(base_model.model_dump_json())


def write_json_record(file_path: Path, base_model: BaseModel) -> None:
    create_folders_recirsively_if_not_exist(tmp_path=file_path)

    with open(file_path, "w") as f:
        f.write(base_model.model_dump_json())


def write_jsons_with_base_models(file_path: str, base_models: List[BaseModel]) -> None:
    _, file_name = os.path.split(file_path)
    directory_path = get_directory_path(tmp_path=file_path)
    tmp_directory_name = file_name.split(".")[0]
    json_directory_path = os.path.join(directory_path, tmp_directory_name)

    file_path = os.path.join(json_directory_path, "combined.json")
    write_json(file_path=file_path, base_model=base_models)

    # file_extension = "json"

    # for idx, base_model in enumerate(base_models):
    #     file_name = str(idx) + "." + file_extension
    #     file_path = os.path.join(json_directory_path, file_name)
    #     write_json(file_path=file_path, base_model=base_model)


def write_jsonl(file_path: str, base_models: List[BaseModel]) -> None:
    create_folders_recirsively_if_not_exist(tmp_path=file_path)
    with open(file_path, "w") as f:
        for base_model in base_models:
            f.write(base_model.model_dump_json() + "\n")
    write_jsons_with_base_models(file_path=file_path, base_models=base_models)


def get_base_model_from_json(file_path: str, base_model: BaseModel) -> BaseModel:
    with open(file_path, "r") as f:
        tmp_dict = json.load(f)

    try:
        new_model = base_model.model_validate(tmp_dict)
    except Exception as e:
        print(e)
        raise Exception(f"Model Parsing failed: {file_path}")

    return new_model


def get_base_models_from_jsonl(file_path: str, base_model: BaseModel) -> List[BaseModel]:
    outputs: List[base_model] = list()
    with open(file_path, "r") as f:
        json_list = list(f)

    for json_str in json_list:
        tmp_dict = json.loads(json_str)
        try:
            model = base_model.model_validate(tmp_dict)
            outputs.append(model)
        except Exception as e:
            print(e)
    return outputs


def get_models_from_jsonl(file_path: str, model: BaseModel) -> List[BaseModel]:
    outputs: List[BaseModel] = list()
    with open(file_path, "r") as f:
        json_list = list(f)

    for json_str in json_list:
        tmp_dict = json.loads(json_str)
        outputs.append(model.model_validate(tmp_dict))
    return outputs


def get_environmental_variable_value(name: str, default: Any = None) -> Optional[Any]:
    if name in os.environ:
        return os.environ[name]
    return default


def get_date_time_str() -> str:
    now = datetime.now()  # current date and time
    return now.strftime("%m_%d_%Y_%H_%M_%S")


def get_file_path(file_path_without_extension: str, key_words: List[str], extension: str) -> str:
    return file_path_without_extension + "_" + "_".join(key_words) + "_" + get_date_time_str() + "." + extension


def get_dataset_from_jsonl(file_path: str, base_model: BaseModel) -> Optional[Dataset]:
    models = get_models_from_jsonl(file_path=file_path, model=base_model)
    models = list(map(lambda model: model.get_seq2seq_data_model(), models))

    if len(models) > 0:
        field_names = list(models[0].model_dump().keys())
        dict_for_data_frame = {field_name: [] for field_name in field_names}

        for model in models:
            model_dict = model.model_dump()
            for field_name in field_names:
                dict_for_data_frame[field_name].append(model_dict[field_name])

        return Dataset.from_pandas(pd.DataFrame(dict_for_data_frame))
    return None


def write_datasetdict_file_from_jsonls(
    file_paths: List[str], base_model: BaseModel, output_file_path: str
) -> DatasetDict:
    """
    file_paths should be for training, validation, and testing, respectively
    """
    create_folders_recirsively_if_not_exist(tmp_path=output_file_path)
    ds = DatasetDict()
    dataset_names = ["train", "validation", "test"]
    for idx, dataset_name in enumerate(dataset_names):
        dataset = get_dataset_from_jsonl(file_path=file_paths[idx], base_model=base_model)
        if dataset is not None:
            ds[dataset_name] = dataset
    ds.save_to_disk(dataset_dict_path=output_file_path)
    return ds


def get_files_in_folder(folder_path: Path, file_extension: Optional[str] = None) -> List[Path]:
    check_paths(paths=[folder_path])
    file_paths = (
        [
            Path(os.path.join(dp, f))
            for dp, dn, filenames in os.walk(folder_path)
            for f in filenames
            if os.path.splitext(f)[1] == ("." + file_extension)
        ]
        if file_extension is not None
        else [Path(os.path.join(dp, f)) for dp, dn, filenames in os.walk(folder_path) for f in filenames]
    )
    return sorted(file_paths, key=lambda tmp_path: str(tmp_path)) if len(file_paths) > 0 else []
