import openai
from django.http import JsonResponse
import json
import os
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

openai.api_key = os.getenv("OPENAI_API_KEY")

@csrf_exempt
@api_view(['POST'])
def chat_with_openai(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            prompt = data.get("prompt", "")

            # OpenAI ChatCompletion 호출
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "당신은 유머러스한 살말 개구리봇입니다."},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=200,
                temperature=0.7,
            )

            # 응답 반환
            return JsonResponse({"message": response["choices"][0]["message"]["content"]})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method."}, status=400)