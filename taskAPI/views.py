from django.http import JsonResponse
from .models import Project
from .serializer import ProjectSerializer, UnitSerializer, AllSerializer, SearchSerializer
from django.db.models import Count
from adrf.views import APIView


class All(APIView):
    async def get(self, request):
        projects = await Project.objects.async_all()
        if projects:
            serializer = ProjectSerializer(projects, many=True)
            data = serializer.data
            return JsonResponse(data, safe=False)
        return JsonResponse({'message': 'No projects found.'})


class Expensive(APIView):
    async def get(self, request):
        most_expensive_project = await Project.objects.order_by('price').afirst()
        if most_expensive_project:
            serializer = ProjectSerializer(most_expensive_project)
            data = serializer.data
            return JsonResponse(data, safe=False)
        return JsonResponse({'message': 'No projects found.'})


class Largest(APIView):
    async def get(self, request):
        most_largest_unit = await Project.objects.order_by('area').afirst()
        if most_largest_unit:
            serializer = ProjectSerializer(most_largest_unit)
            data = serializer.data
            return JsonResponse(data, safe=False)
        return JsonResponse({'message': 'No projects found.'})


class AllVilla(APIView):
    async def get(self, request):
        all_villa = ((await Project.objects.async_filter(utype='Villa'))
                     .values('unit')
                     .annotate(villa_count=Count('id')).order_by('-villa_count'))
        if all_villa:
            serializer = UnitSerializer(all_villa, many=True)
            data = serializer.data
            return JsonResponse(data, safe=False)
        return JsonResponse({'message': 'No projects found.'})


class AllProjects(APIView):
    async def get(self, request):
        all_projects = await ((Project.objects.values('unit', 'utype'))
                              .annotate(unit_type_count=Count('unit'))
                              .async_order_by('-unit_type_count'))
        if all_projects:
            serializer = AllSerializer(all_projects, many=True)
            data = serializer.data
            return JsonResponse(data, safe=False)
        return JsonResponse({'message': 'No projects found.'})


class SearchProject(APIView):
    async def get(self, request):
        parameters = request.GET.get('unit', '')
        search_request = ((await Project.objects.async_filter(unit__icontains=parameters))
                          .values('unit', 'utype', 'beds', 'area', 'price', 'date'))
        if search_request:
            serializer = SearchSerializer(search_request, many=True)
            data = serializer.data
            return JsonResponse(data, safe=False)
        return JsonResponse({'message': 'No projects found.'})


class SearchParamProject(APIView):
    async def get(self, request):
        unit = request.GET.get('unit', '')
        utype = request.GET.get('utype', '')
        beds = request.GET.get('beds', 0)
        search_request = ((await Project.objects.async_filter(unit__icontains=unit))
                          .values('unit', 'utype', 'beds', 'area', 'price', 'date'))
        if utype:
            search_request = await search_request.async_filter(utype=utype)
        if beds:
            search_request = await search_request.async_filter(beds=beds)

        if search_request:
            serializer = SearchSerializer(search_request, many=True)
            data = serializer.data
            return JsonResponse(data, safe=False)
        return JsonResponse({'message': 'No projects found.'})


class SearchPostProject(APIView):
    async def post(self, request):
        parameters = request.data.get("unit", "")
        search_request = ((await Project.objects.async_filter(unit__icontains=parameters))
                          .values('unit', 'utype', 'beds', 'area', 'price', 'date'))
        if search_request:
            serializer = SearchSerializer(search_request, many=True)
            data = serializer.data
            return JsonResponse(data, safe=False)
        return JsonResponse({'message': 'No projects found.'})
