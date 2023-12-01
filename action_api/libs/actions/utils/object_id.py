import typing

import bson
import pydantic.json_schema as pydantic_json_schema
import pydantic_core


class ObjectIdPydanticAnnotation:
    @classmethod
    def validate_object_id(cls, v: typing.Any, handler: typing.Any) -> bson.ObjectId:
        if isinstance(v, bson.ObjectId):
            return v

        s = handler(v)
        if bson.ObjectId.is_valid(s):
            return bson.ObjectId(s)
        else:
            raise ValueError("Invalid bson.ObjectId")

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: bson.ObjectId, _handler: typing.Any
    ) -> pydantic_core.core_schema.CoreSchema:
        assert source_type is bson.ObjectId
        return pydantic_core.core_schema.no_info_wrap_validator_function(
            cls.validate_object_id,
            pydantic_core.core_schema.str_schema(),
            serialization=pydantic_core.core_schema.to_string_ser_schema(),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, _core_schema: typing.Any, handler: typing.Any
    ) -> pydantic_json_schema.JsonSchemaValue:
        return handler(pydantic_core.core_schema.str_schema())


CustomObjectId = typing.Annotated[bson.ObjectId, ObjectIdPydanticAnnotation]
