from fastapi.routing import APIRouter
from starlette import status

from apps.answers.api import (
    answers_existence_check,
    applet_activity_answer_retrieve,
    applet_activity_answers_list,
    applet_activity_assessment_create,
    applet_activity_assessment_retrieve,
    applet_activity_identifiers_retrieve,
    applet_activity_versions_retrieve,
    applet_answer_assessment_delete,
    applet_answer_reviews_retrieve,
    applet_answers_export,
    applet_completed_entities,
    applet_flow_answer_retrieve,
    applet_flow_identifiers_retrieve,
    applet_flow_submissions_list,
    applet_submit_date_list,
    applet_validate_multiinformant_assessment,
    applets_completed_entities,
    create_anonymous_answer,
    create_answer,
    note_add,
    note_delete,
    note_edit,
    note_list,
    review_activity_list,
    review_flow_list,
    summary_activity_flow_list,
    summary_activity_list,
    summary_latest_report_retrieve,
)
from apps.answers.domain import (
    ActivitySubmissionResponse,
    AnswerExistenceResponse,
    AnswerNoteDetailPublic,
    AnswerReviewPublic,
    AppletActivityAnswerPublic,
    AppletCompletedEntities,
    AssessmentAnswerPublic,
    FlowSubmissionResponse,
    PublicAnswerDates,
    PublicAnswerExport,
    PublicFlowSubmissionsResponse,
    PublicReviewActivity,
    PublicReviewFlow,
    PublicSummaryActivity,
    PublicSummaryActivityFlow,
)
from apps.answers.domain.answers import MultiinformantAssessmentValidationResponse
from apps.applets.api.applets import applet_flow_versions_data_retrieve
from apps.applets.domain.applet_history import VersionPublic
from apps.shared.domain import AUTHENTICATION_ERROR_RESPONSES, Response, ResponseMulti
from apps.shared.domain.response import DEFAULT_OPENAPI_RESPONSE

router = APIRouter(prefix="/answers", tags=["Answers"])
public_router = APIRouter(prefix="/public/answers", tags=["Answers"])

# Answers for activity item create
router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    responses={
        **DEFAULT_OPENAPI_RESPONSE,
        **AUTHENTICATION_ERROR_RESPONSES,
    },
)(create_answer)

# Anonymous Answers for activity item create
public_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    responses={
        **DEFAULT_OPENAPI_RESPONSE,
        **AUTHENTICATION_ERROR_RESPONSES,
    },
)(create_anonymous_answer)

router.get(
    "/applet/{applet_id}/review/activities",
    status_code=status.HTTP_200_OK,
    response_model=ResponseMulti[PublicReviewActivity],
    responses={
        **DEFAULT_OPENAPI_RESPONSE,
        **AUTHENTICATION_ERROR_RESPONSES,
    },
)(review_activity_list)

router.get(
    "/applet/{applet_id}/review/flows",
    status_code=status.HTTP_200_OK,
    response_model=ResponseMulti[PublicReviewFlow],
    responses={
        **DEFAULT_OPENAPI_RESPONSE,
        **AUTHENTICATION_ERROR_RESPONSES,
    },
)(review_flow_list)

router.get(
    "/applet/{applet_id}/summary/activities",
    status_code=status.HTTP_200_OK,
    response_model=ResponseMulti[PublicSummaryActivity],
    responses={
        **DEFAULT_OPENAPI_RESPONSE,
        **AUTHENTICATION_ERROR_RESPONSES,
    },
)(summary_activity_list)

router.get(
    "/applet/{applet_id}/summary/flows",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": ResponseMulti[PublicSummaryActivityFlow]},
        **DEFAULT_OPENAPI_RESPONSE,
        **AUTHENTICATION_ERROR_RESPONSES,
    },
)(summary_activity_flow_list)

router.get(
    "/applet/{applet_id}/summary/activities/{activity_id}/identifiers",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": ResponseMulti[str]},
        **DEFAULT_OPENAPI_RESPONSE,
        **AUTHENTICATION_ERROR_RESPONSES,
    },
)(applet_activity_identifiers_retrieve)

router.get(
    "/applet/{applet_id}/flows/{flow_id}/identifiers",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": ResponseMulti[str]},
        **DEFAULT_OPENAPI_RESPONSE,
        **AUTHENTICATION_ERROR_RESPONSES,
    },
)(applet_flow_identifiers_retrieve)

router.get(
    "/applet/{applet_id}/summary/activities/{activity_id}/versions",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": ResponseMulti[VersionPublic]},
        **DEFAULT_OPENAPI_RESPONSE,
        **AUTHENTICATION_ERROR_RESPONSES,
    },
)(applet_activity_versions_retrieve)

router.get(
    "/applet/{applet_id}/flows/{flow_id}/versions",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": ResponseMulti[VersionPublic]},
        **DEFAULT_OPENAPI_RESPONSE,
        **AUTHENTICATION_ERROR_RESPONSES,
    },
)(applet_flow_versions_data_retrieve)

router.get(
    "/applet/{applet_id}/activities/{activity_id}/answers",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": ResponseMulti[AppletActivityAnswerPublic]},
        **DEFAULT_OPENAPI_RESPONSE,
        **AUTHENTICATION_ERROR_RESPONSES,
    },
)(applet_activity_answers_list)

router.get(
    "/applet/{applet_id}/flows/{flow_id}/submissions",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": PublicFlowSubmissionsResponse},
        **DEFAULT_OPENAPI_RESPONSE,
        **AUTHENTICATION_ERROR_RESPONSES,
    },
)(applet_flow_submissions_list)

router.post(
    "/applet/{applet_id}/activities/{activity_id}/subjects/{subject_id}/latest_report",
    status_code=status.HTTP_200_OK,
    responses={
        **DEFAULT_OPENAPI_RESPONSE,
        **AUTHENTICATION_ERROR_RESPONSES,
    },
)(summary_latest_report_retrieve)

router.get(
    "/applet/{applet_id}/dates",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": Response[PublicAnswerDates]},
        **DEFAULT_OPENAPI_RESPONSE,
        **AUTHENTICATION_ERROR_RESPONSES,
    },
)(applet_submit_date_list)

router.get(
    "/applet/{applet_id}/activities/{activity_id}/answers/{answer_id}",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": Response[ActivitySubmissionResponse]},
        **DEFAULT_OPENAPI_RESPONSE,
        **AUTHENTICATION_ERROR_RESPONSES,
    },
)(applet_activity_answer_retrieve)

router.get(
    "/applet/{applet_id}/flows/{flow_id}/submissions/{submit_id}",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": Response[FlowSubmissionResponse]},
        **DEFAULT_OPENAPI_RESPONSE,
        **AUTHENTICATION_ERROR_RESPONSES,
    },
)(applet_flow_answer_retrieve)

router.get(
    "/applet/{applet_id}/answers/{answer_id}/reviews",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": ResponseMulti[AnswerReviewPublic]},
        **DEFAULT_OPENAPI_RESPONSE,
        **AUTHENTICATION_ERROR_RESPONSES,
    },
)(applet_answer_reviews_retrieve)

router.get(
    "/applet/{applet_id}/answers/{answer_id}/assessment",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": Response[AssessmentAnswerPublic]},
        **DEFAULT_OPENAPI_RESPONSE,
        **AUTHENTICATION_ERROR_RESPONSES,
    },
)(applet_activity_assessment_retrieve)

router.delete(
    "/applet/{applet_id}/answers/{answer_id}/assessment/{assessment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)(applet_answer_assessment_delete)

router.post(
    "/applet/{applet_id}/answers/{answer_id}/assessment",
    status_code=status.HTTP_201_CREATED,
    responses={
        **DEFAULT_OPENAPI_RESPONSE,
        **AUTHENTICATION_ERROR_RESPONSES,
    },
)(applet_activity_assessment_create)

router.post(
    "/applet/{applet_id}/answers/{answer_id}/activities/{activity_id}/notes",
    status_code=status.HTTP_201_CREATED,
    responses={
        **DEFAULT_OPENAPI_RESPONSE,
        **AUTHENTICATION_ERROR_RESPONSES,
    },
)(note_add)

router.get(
    "/applet/{applet_id}/answers/{answer_id}/activities/{activity_id}/notes",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": Response[AnswerNoteDetailPublic]},
        **DEFAULT_OPENAPI_RESPONSE,
        **AUTHENTICATION_ERROR_RESPONSES,
    },
)(note_list)

router.put(
    "/applet/{applet_id}/answers/{answer_id}/activities/" "{activity_id}/notes/{note_id}",
    # noqa: E501
    status_code=status.HTTP_200_OK,
    responses={
        **DEFAULT_OPENAPI_RESPONSE,
        **AUTHENTICATION_ERROR_RESPONSES,
    },
)(note_edit)

router.delete(
    "/applet/{applet_id}/answers/{answer_id}/activities/" "{activity_id}/notes/{note_id}",
    # noqa: E501
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        **DEFAULT_OPENAPI_RESPONSE,
        **AUTHENTICATION_ERROR_RESPONSES,
    },
)(note_delete)

router.get(
    "/applet/{applet_id}/data",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": Response[PublicAnswerExport]},
        **DEFAULT_OPENAPI_RESPONSE,
        **AUTHENTICATION_ERROR_RESPONSES,
    },
)(applet_answers_export)

router.get(
    "/applet/{applet_id}/completions",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": Response[AppletCompletedEntities]},
        **DEFAULT_OPENAPI_RESPONSE,
        **AUTHENTICATION_ERROR_RESPONSES,
    },
)(applet_completed_entities)

router.get(
    "/applet/completions",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": ResponseMulti[AppletCompletedEntities]},
        **DEFAULT_OPENAPI_RESPONSE,
        **AUTHENTICATION_ERROR_RESPONSES,
    },
)(applets_completed_entities)

router.post(
    "/check-existence",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": Response[AnswerExistenceResponse]},
        **DEFAULT_OPENAPI_RESPONSE,
        **AUTHENTICATION_ERROR_RESPONSES,
    },
)(answers_existence_check)

router.get(
    "/applet/{applet_id}/multiinformant-assessment/validate",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": Response[MultiinformantAssessmentValidationResponse]},
        **DEFAULT_OPENAPI_RESPONSE,
        **AUTHENTICATION_ERROR_RESPONSES,
    },
)(applet_validate_multiinformant_assessment)
