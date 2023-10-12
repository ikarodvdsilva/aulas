from django.contrib.auth.decorators import login_required
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import JsonResponse
import json


@csrf_exempt
@require_POST
def aluno_api(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        username = data.get("username")
        password = data.get("password")

        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                access_token_payload = refresh.access_token.payload
                access_token_payload["username"] = user.username
                return JsonResponse(
                    {
                        "status": "success",
                        "message": "Login bem-sucedido.",
                        "access_token": str(access_token_payload),
                    }
                )
            else:
                return JsonResponse(
                    {"status": "error", "message": "Credenciais inválidas."}, status=401
                )
        else:
            return JsonResponse(
                {
                    "status": "error",
                    "message": "Nome de usuário e senha são obrigatórios.",
                },
                status=400,
            )
    except json.JSONDecodeError:
        return JsonResponse(
            {"status": "error", "message": "Erro ao decodificar o JSON."}, status=400
        )
