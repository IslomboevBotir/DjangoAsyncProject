from django.db.models import Count
from taskAPI.models import Project


async def all_project():
    projects = await Project.objects.async_all()
    return projects


async def expensive_project():
    most_expensive_project = await Project.objects.order_by('price').afirst()
    return most_expensive_project


async def largest_project():
    most_largest_unit = await Project.objects.order_by('area').afirst()
    return most_largest_unit


async def all_villa_query():
    all_villa = ((await Project.objects.async_filter(utype='Villa'))
                 .values('unit')
                 .annotate(villa_count=Count('id')).order_by('-villa_count'))
    return all_villa


async def all_projects_query():
    all_projects = await ((Project.objects.values('unit', 'utype'))
                          .annotate(unit_type_count=Count('unit'))
                          .async_order_by('-unit_type_count'))
    return all_projects


async def search_projects_query(parameters):
    search_request = ((await Project.objects.async_filter(unit__icontains=parameters))
                      .values('unit', 'utype', 'beds', 'area', 'price', 'date'))
    return search_request


async def search_projects_for_param(unit=None, utype=None, beds=None):
    search_request = ((await Project.objects.async_filter(unit__icontains=unit))
                      .values('unit', 'utype', 'beds', 'area', 'price', 'date'))
    if utype:
        search_request = await search_request.async_filter(utype=utype)
    if beds:
        search_request = await search_request.async_filter(beds=beds)
    return search_request


async def search_param_for_post(parameters):
    search_request = ((await Project.objects.async_filter(unit__icontains=parameters))
                      .values('unit', 'utype', 'beds', 'area', 'price', 'date'))
    return search_request


async def search_for_wid(w_id):
    search_request = ((await Project.objects.async_filter(w_id=w_id))
                      .values('unit', 'utype', 'beds', 'area', 'price', 'date'))
    return search_request
