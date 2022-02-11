import logging
from typing import Any, MutableMapping, Optional

from cloudformation_cli_python_lib import (
    HandlerErrorCode,
    Hook,
    HookInvocationPoint,
    OperationStatus,
    ProgressEvent,
    SessionProxy,
    exceptions,
)

from .models import HookHandlerRequest, TypeConfigurationModel

# Use this logger to forward log messages to CloudWatch Logs.
LOG = logging.getLogger(__name__)
TYPE_NAME = "SQS::Queue::KmsMasterKeyId"

hook = Hook(TYPE_NAME, TypeConfigurationModel)
test_entrypoint = hook.test_entrypoint


@hook.handler(HookInvocationPoint.CREATE_PRE_PROVISION)
def pre_create_handler(
        session: Optional[SessionProxy],
        request: HookHandlerRequest,
        callback_context: MutableMapping[str, Any],
        type_configuration: TypeConfigurationModel
) -> ProgressEvent:
    try:
        request.hookContext.targetModel['resourceProperties']['KmsMasterKeyId']
        return ProgressEvent(
            status = OperationStatus.SUCCESS
        )
    except KeyError:
        return ProgressEvent(
            status = OperationStatus.FAILED,
            message = 'KmsMasterKeyId required',
            errorCode = HandlerErrorCode.NonCompliant,
        )
