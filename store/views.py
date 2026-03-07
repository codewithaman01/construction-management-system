import json
from datetime import date
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.db import transaction
from django.db.models import F

from .models import Material, Stock, StockInward, StockOutward, MaterialRequirement
from projects.models import Project


# ─────────────────────────────────────────
# PAGE VIEWS
# ─────────────────────────────────────────

@login_required
def store_dashboard(request):
    return render(request, 'store/dashboard.html')


@login_required
def stock_page(request):
    return render(request, 'store/stock.html')


@login_required
def inward_page(request):
    return render(request, 'store/inward.html')


@login_required
def outward_page(request):
    return render(request, 'store/outward.html')


@login_required
def requirements_page(request):
    return render(request, 'store/requirements.html')


# ─────────────────────────────────────────
# MATERIAL APIs
# ─────────────────────────────────────────

@login_required
def get_materials(request):
    materials = Material.objects.select_related('stock', 'created_by')

    data = []
    for m in materials:
        stock_qty = m.stock.quantity if hasattr(m, 'stock') else 0
        is_low = stock_qty <= m.reorder_level

        data.append({
            'id': m.id,
            'name': m.name,
            'unit': m.unit,
            'quantity': stock_qty,
            'reorder_level': m.reorder_level,
            'is_low': is_low,
            'created_by': m.created_by.username if m.created_by else ''
        })

    return JsonResponse({'materials': data})


@login_required
@csrf_exempt
@require_POST
def add_material(request):
    data = json.loads(request.body)

    material = Material.objects.create(
        name=data['name'],
        unit=data.get('unit', 'piece'),
        reorder_level=float(data.get('reorder_level', 10)),
        created_by=request.user
    )

    Stock.objects.create(material=material, quantity=0)

    return JsonResponse({'status': 'added'})


# ─────────────────────────────────────────
# INWARD (ADD STOCK)
# ─────────────────────────────────────────

@login_required
def get_inwards(request):
    records = StockInward.objects.select_related('material', 'project')

    data = [{
        'material': r.material.name,
        'quantity': r.quantity,
        'project': r.project.name if r.project else '',
        'date': str(r.date)
    } for r in records]

    return JsonResponse({'inwards': data})


@login_required
@csrf_exempt
@require_POST
def add_inward(request):
    data = json.loads(request.body)

    material = get_object_or_404(Material, id=int(data['material']))
    qty = float(data['quantity'])

    with transaction.atomic():
        StockInward.objects.create(
            material=material,
            quantity=qty,
            received_by=request.user,
            date=date.today()
        )

        stock, _ = Stock.objects.get_or_create(material=material)
        stock.quantity += qty
        stock.save()

    return JsonResponse({'status': 'added'})


# ─────────────────────────────────────────
# OUTWARD (DEDUCT STOCK)
# ─────────────────────────────────────────

@login_required
def get_outwards(request):
    records = StockOutward.objects.select_related('material', 'project')

    data = [{
        'material': r.material.name,
        'quantity': r.quantity,
        'project': r.project.name if r.project else '',
        'date': str(r.date)
    } for r in records]

    return JsonResponse({'outwards': data})


@login_required
@csrf_exempt
@require_POST
def add_outward(request):
    data = json.loads(request.body)

    material = get_object_or_404(Material, id=int(data['material']))
    qty = float(data['quantity'])

    with transaction.atomic():
        stock, _ = Stock.objects.get_or_create(material=material)

        if stock.quantity < qty:
            return JsonResponse({'error': 'Not enough stock'}, status=400)

        StockOutward.objects.create(
            material=material,
            quantity=qty,
            issued_by=request.user,
            date=date.today()
        )

        stock.quantity -= qty
        stock.save()

    return JsonResponse({'status': 'added'})


# ─────────────────────────────────────────
# REQUIREMENT (IMPORTANT LOGIC)
# ─────────────────────────────────────────

@login_required
def get_requirements(request):
    records = MaterialRequirement.objects.select_related('material', 'project')

    data = [{
        'id': r.id,
        'material': r.material.name,
        'material_id': r.material.id,
        'quantity': r.quantity_required,
        'project': r.project.name if r.project else '',
        'status': r.status
    } for r in records]

    return JsonResponse({'requirements': data})


@login_required
@csrf_exempt
@require_POST
def add_requirement(request):
    data = json.loads(request.body)

    material = get_object_or_404(Material, id=int(data['material']))

    MaterialRequirement.objects.create(
        material=material,
        quantity_required=float(data['quantity']),
        requested_by=request.user
    )

    return JsonResponse({'status': 'added'})


@login_required
@csrf_exempt
@require_POST
def update_requirement(request):
    data = json.loads(request.body)

    req = get_object_or_404(MaterialRequirement, id=data['id'])
    new_status = data['status']

    # 🔥 AUTO STOCK DEDUCTION
    if new_status == 'approved' and req.status != 'approved':

        stock = get_object_or_404(Stock, material=req.material)

        if stock.quantity < req.quantity_required:
            return JsonResponse({'error': 'Not enough stock'}, status=400)

        stock.quantity -= req.quantity_required
        stock.save()

        # Optional: mark fulfilled
        req.status = 'fulfilled'
    else:
        req.status = new_status

    req.save()

    return JsonResponse({'status': 'updated'})


# ─────────────────────────────────────────
# DASHBOARD STATS
# ─────────────────────────────────────────

@login_required
def store_stats(request):

    total_materials = Material.objects.count()

    low_stock_count = Stock.objects.filter(
        quantity__lte=F('material__reorder_level')
    ).count()

    pending_requests = MaterialRequirement.objects.filter(status='pending').count()

    today_inward = StockInward.objects.filter(date=date.today()).count()

    return JsonResponse({
        'total_materials': total_materials,
        'low_stock_count': low_stock_count,
        'pending_requests': pending_requests,
        'today_inward': today_inward
    })
@login_required
@csrf_exempt
@require_POST
def update_material(request):
    data = json.loads(request.body)

    material = get_object_or_404(Material, id=data['id'])

    material.name = data.get('name', material.name)
    material.unit = data.get('unit', material.unit)
    material.reorder_level = float(data.get('reorder_level', material.reorder_level))

    material.save()

    return JsonResponse({'status': 'updated'})

@login_required
@csrf_exempt
@require_POST
def delete_material(request):
    data = json.loads(request.body)

    material = get_object_or_404(Material, id=data['id'])

    # ❗ Prevent delete if stock exists
    if hasattr(material, 'stock') and material.stock.quantity > 0:
        return JsonResponse({
            'error': f'Cannot delete "{material.name}" — stock exists'
        }, status=400)

    material.delete()

    return JsonResponse({'status': 'deleted'})