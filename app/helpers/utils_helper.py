import json
from datetime import date, datetime
from typing import Any, List, Type, TypeVar, Union

from pydantic import BaseModel, TypeAdapter

ModelType = TypeVar("ModelType", bound=BaseModel)


def format_date(str_time: str) -> str: ...


def serialize_data(object_model: Union[ModelType, List[ModelType]]) -> str:
    """
    Serializes a Pydantic model or list of models to JSON string
    """
    if isinstance(object_model, list):
        return json.dumps([obj.model_dump() for obj in object_model])
    return object_model.model_dump_json()


def deserialize_data(data: str, model: Type[ModelType], is_list: bool = False) -> Union[ModelType, List[ModelType]]:
    """
    Deserializes a JSON string to a Pydantic model or list of models
    """
    json_data = json.loads(data)
    if is_list:
        return TypeAdapter(List[model]).validate_python(json_data)
    return TypeAdapter(model).validate_python(json_data)


def serialize_from_json(data: Any) -> Any:
    """
    Serializes data with special handling for dates and Pydantic models
    """
    if isinstance(data, BaseModel):
        return {key: serialize_from_json(value) for key, value in data.model_dump().items()}
    elif isinstance(data, list):
        return [serialize_from_json(item) for item in data]
    elif isinstance(data, datetime):
        return f"__datetime__{data.isoformat()}"
    elif isinstance(data, date):
        return f"__date__{data.isoformat()}"
    else:
        return data


def _decode_data(data: Any) -> Any:
    """
    Internal function to decode data with special handling for dates
    """
    if isinstance(data, dict):
        return {k: _decode_data(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [_decode_data(i) for i in data]
    elif isinstance(data, str):
        if data.startswith("__date__"):
            return date.fromisoformat(data[8:])
        elif data.startswith("__datetime__"):
            return datetime.fromisoformat(data[12:])
    return data


def deserialize_from_json(data: dict, model: Type[ModelType]) -> ModelType:
    """
    Deserializes JSON data with special handling for dates into a Pydantic model
    """
    processed_data = _decode_data(data)
    return model.model_validate(processed_data)
