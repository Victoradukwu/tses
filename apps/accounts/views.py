from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from tasks import add_numbers


@api_view()
@permission_classes([AllowAny])
def test_add(request):
    task = add_numbers.delay(2, 3) # type: ignore

    return Response({
        "message": "Task queued",
        "task_id": task.id,
    })