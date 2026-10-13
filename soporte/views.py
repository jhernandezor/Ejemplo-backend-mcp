import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Ticket

@csrf_exempt
def api_tickets(request):
    if request.method == 'GET':
        tickets = list(Ticket.objects.values().order_by('-id'))
        return JsonResponse({'status': 'ok', 'data': tickets})

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            asunto = data.get('asunto', '').strip()
            descripcion = data.get('descripcion', '').strip()

            if not asunto or not descripcion:
                return JsonResponse({'status': 'error', 'mensaje': 'Campos obligatorios'}, status=400)

            ticket = Ticket.objects.create(asunto=asunto, descripcion=descripcion)

            return JsonResponse({
                'status': 'ok',
                'mensaje': 'Ticket registrado desde Django',
                'ticket': {
                    'id': ticket.id,
                    'asunto': ticket.asunto,
                    'descripcion': ticket.descripcion,
                    'fecha_creacion': ticket.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S') if ticket.fecha_creacion else ''
                }
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'mensaje': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'mensaje': 'Método no permitido'}, status=405)