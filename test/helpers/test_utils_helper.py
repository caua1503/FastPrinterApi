import pytest
from pydantic import BaseModel
from datetime import date, datetime
from typing import List, Optional

from app.helpers.utils_helper import serialize_for_json, deserialize_from_json

class NestedModel(BaseModel):
    id: int
    description: str

class ExampleModel(BaseModel):
    name: str
    birth_date: date
    created_at: datetime
    items: List[str]
    nested: NestedModel
    optional_field: Optional[str] = None

def test_serialize_for_json():
    test_data = ExampleModel(
        name="Test Name",
        birth_date=date(2000, 1, 1),
        created_at=datetime(2023, 1, 1, 12, 0, 0),
        items=["item1", "item2"],
        nested=NestedModel(id=1, description="Nested Object")
    )

    expected_output = {
        'name': 'Test Name',
        'birth_date': '__date__2000-01-01',
        'created_at': '__datetime__2023-01-01T12:00:00',
        'items': ['item1', 'item2'],
        'nested': {
            'id': 1,
            'description': 'Nested Object'
        },
        'optional_field': None
    }

    serialized_data = serialize_for_json(test_data)

    assert serialized_data == expected_output

def test_deserialize_from_json():
    serialized_data = {
        'name': 'Test Name',
        'birth_date': '__date__2000-01-01',
        'created_at': '__datetime__2023-01-01T12:00:00',
        'items': ['item1', 'item2'],
        'nested': {
            'id': 1,
            'description': 'Nested Object'
        },
        'optional_field': None
    }

    expected_object = ExampleModel(
        name="Test Name",
        birth_date=date(2000, 1, 1),
        created_at=datetime(2023, 1, 1, 12, 0, 0),
        items=["item1", "item2"],
        nested=NestedModel(id=1, description="Nested Object"),
        optional_field=None
    )

    deserialized_object = deserialize_from_json(serialized_data, ExampleModel)

    assert deserialized_object == expected_object
