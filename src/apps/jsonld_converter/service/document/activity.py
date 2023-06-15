import asyncio
from copy import deepcopy
from typing import Type
from uuid import uuid4

from apps.activities.domain.activity_create import (
    ActivityCreate,
    ActivityItemCreate,
)
from apps.activities.domain.conditional_logic import ConditionalLogic
from apps.jsonld_converter.errors import (
    ConditionalLogicError,
    JsonLDNotSupportedError,
)
from apps.jsonld_converter.service.document.base import (
    CommonFieldsMixin,
    ContainsNestedMixin,
    LdDocumentBase,
    LdKeyword,
)
from apps.jsonld_converter.service.document.conditional_logic import (
    ConditionalLogicParser,
)
from apps.jsonld_converter.service.document.field import (
    ReproFieldABTrailIpad,
    ReproFieldABTrailMobile,
    ReproFieldAge,
    ReproFieldAudio,
    ReproFieldAudioStimulus,
    ReproFieldBase,
    ReproFieldDate,
    ReproFieldDrawing,
    ReproFieldGeolocation,
    ReproFieldMessage,
    ReproFieldPhoto,
    ReproFieldRadio,
    ReproFieldRadioStacked,
    ReproFieldSlider,
    ReproFieldSliderStacked,
    ReproFieldText,
    ReproFieldTime,
    ReproFieldTimeRange,
    ReproFieldVideo,
)


class ReproActivity(LdDocumentBase, ContainsNestedMixin, CommonFieldsMixin):
    ld_pref_label: str | None = None
    ld_alt_label: str | None = None
    ld_description: dict[str, str] | None = None
    ld_about: dict[str, str] | None = None
    ld_schema_version: str | None = None
    ld_version: str | None = None
    ld_image: str | None = None
    ld_splash: str | None = None
    ld_is_vis: str | bool | None = None
    ld_is_reviewer: bool | None = None
    ld_is_one_page: bool | None = None

    properties: dict
    nested_by_order: list[LdDocumentBase] | None = None

    extra: dict | None = None
    is_skippable: bool = False
    is_back_disabled: bool = False

    @classmethod
    def supports(cls, doc: dict) -> bool:
        ld_types = [
            "reproschema:Activity",
            *cls.attr_processor.resolve_key("reproschema:Activity"),
        ]
        return cls.attr_processor.first(
            doc.get(LdKeyword.type)
        ) in ld_types and cls.supports_activity_type(doc)

    @classmethod
    def supports_activity_type(cls, doc: dict) -> bool:
        _type = cls.get_activity_type(doc)
        return not _type or _type == "NORMAL"

    @classmethod
    def get_activity_type(cls, doc: dict) -> str | None:
        _type = cls.attr_processor.get_attr_value(
            doc, "reproschema:activityType"
        )
        if not _type:
            # try fetch from compact
            _type = doc.get("activityType")

        return _type

    @classmethod
    def get_supported_types(cls) -> list[Type[LdDocumentBase]]:
        return [
            ReproFieldText,
            ReproFieldRadio,
            ReproFieldSlider,
            ReproFieldSliderStacked,
            ReproFieldPhoto,
            ReproFieldVideo,
            ReproFieldAudio,
            ReproFieldDrawing,
            ReproFieldMessage,
            ReproFieldTimeRange,
            ReproFieldDate,
            ReproFieldTime,
            ReproFieldGeolocation,
            ReproFieldAge,
            ReproFieldRadioStacked,
            ReproFieldAudioStimulus,
        ]

    async def load(self, doc: dict, base_url: str | None = None):
        await super().load(doc, base_url)

        processed_doc: dict = deepcopy(self.doc_expanded)
        self.ld_version = self._get_ld_version(processed_doc)
        self.ld_schema_version = self._get_ld_schema_version(processed_doc)
        self.ld_pref_label = self._get_ld_pref_label(processed_doc)
        self.ld_alt_label = self._get_ld_alt_label(processed_doc)
        self.ld_description = self._get_ld_description(
            processed_doc, drop=True
        )
        self.ld_about = self._get_ld_about(processed_doc, drop=True)
        self.ld_image = self._get_ld_image(processed_doc, drop=True)
        self.ld_splash = self.attr_processor.get_translation(
            processed_doc, "schema:splash", lang=self.lang, drop=True
        )
        self.ld_is_vis = self._is_visible(processed_doc, drop=True)
        self.ld_is_reviewer = self.attr_processor.get_attr_value(
            processed_doc, "reproschema:isReviewerActivity"
        )
        self.ld_is_one_page = self.attr_processor.get_attr_value(
            processed_doc, "reproschema:isOnePageAssessment"
        )

        allow_list = self._get_allow_list(processed_doc)
        self.is_skippable = self._is_skippable(allow_list)
        self.is_back_disabled = self._is_back_disabled(allow_list)

        self.properties = self._get_ld_properties_formatted(processed_doc)
        self.nested_by_order = await self._get_nested_items(processed_doc)

        self._load_extra(processed_doc)

    async def _get_nested_items(self, doc: dict, drop=False) -> list:
        nested_items = []
        if items := self.attr_processor.get_attr_list(
            doc, "reproschema:order", drop=drop
        ):
            nested = await asyncio.gather(
                *[self._load_nested_doc(item) for item in items]
            )
            nested_items = [node for node in nested if node]

        return nested_items

    async def _load_nested_doc(self, doc: dict):
        try:
            node = await self.load_supported_document(
                doc, self.base_url, settings=self.settings
            )
            # override from properties
            if node.ld_id in self.properties:
                for prop, val in self.properties[node.ld_id].items():
                    if val is not None and hasattr(node, prop):
                        setattr(node, prop, val)
            return node
        except JsonLDNotSupportedError:
            return None  # TODO

    def _load_extra(self, doc: dict):
        if self.extra is None:
            self.extra = {}
        for k, v in doc.items():
            self.extra[k] = v

    def _export_items(self) -> list[ActivityItemCreate]:
        var_item_map = {
            item.ld_variable_name: item
            for item in self.nested_by_order or []
            if isinstance(item, ReproFieldBase)
        }
        models = []
        for item in var_item_map.values():
            model: ActivityItemCreate = item.export()

            expression = item.ld_is_vis
            if isinstance(expression, str):
                try:
                    match, conditions = ConditionalLogicParser(
                        expression
                    ).parse()
                    resolved_conditions = []
                    for condition in conditions:
                        condition_item: ReproFieldBase = var_item_map.get(  # type: ignore # noqa: E501
                            condition.var_name
                        )
                        if condition_item is None:
                            raise ConditionalLogicError(expression)
                        resolved_conditions.append(
                            condition_item.resolve_condition(condition)
                        )
                    model.conditional_logic = ConditionalLogic(
                        match=match, conditions=resolved_conditions
                    )

                except ConditionalLogicError:
                    ...  # TODO
                    raise

            models.append(model)

        return models

    def export(self) -> ActivityCreate:
        items = self._export_items()

        return ActivityCreate(
            key=uuid4(),
            name=self.ld_pref_label or self.ld_alt_label,
            description=self.ld_description or {},
            splash_screen=self.ld_splash or "",  # TODO not loaded
            show_all_at_once=bool(self.ld_is_one_page),
            is_skippable=self.is_skippable,
            is_reviewable=bool(self.ld_is_reviewer),
            response_is_editable=(not self.is_back_disabled),
            is_hidden=self.ld_is_vis is False,
            image=self.ld_image or "",
            items=items,
            extra_fields=self.extra,
        )


class ABTrailsIpadActivity(ReproActivity):
    @classmethod
    def supports_activity_type(cls, doc: dict) -> bool:
        return cls.get_activity_type(doc) == "TRAILS_IPAD"

    @classmethod
    def get_supported_types(cls) -> list[Type[LdDocumentBase]]:
        return [ReproFieldABTrailIpad]


class ABTrailsMobileActivity(ReproActivity):
    @classmethod
    def supports_activity_type(cls, doc: dict) -> bool:
        return cls.get_activity_type(doc) == "TRAILS_MOBILE"

    @classmethod
    def get_supported_types(cls) -> list[Type[LdDocumentBase]]:
        return [ReproFieldABTrailMobile]


class GyroActivity(ReproActivity):
    @classmethod
    def supports_activity_type(cls, doc: dict) -> bool:
        return cls.get_activity_type(doc) == "CST_GYRO"

    @classmethod
    def get_supported_types(cls) -> list[Type[LdDocumentBase]]:
        return [ReproFieldABTrailMobile]
