from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow import validates, ValidationError
from app.models.workspace import Workspace

class WorkspaceSchema(SQLAlchemySchema):
    class Meta:
        model = Workspace
        load_instance = True

    id = auto_field(dump_only=True)

    name = auto_field(
        required=True,
        error_messages={"required": "Workspace name is required."}
    )

    description = auto_field(allow_none=True)

    invite_code = auto_field(
        required=False,
        error_messages={"required": "Invite code is required."}
    )

    created_at = auto_field(dump_only=True)

    @validates("name")
    def validate_name(self, value, **kwargs):
        if len(value.strip()) < 3:
            raise ValidationError("Workspace name must be at least 3 characters long.")

    @validates("invite_code")
    def validate_invite_code(self, value, **kwargs):
        if len(value.strip()) < 5:
            raise ValidationError("Invite code must be at least 5 characters long.")
