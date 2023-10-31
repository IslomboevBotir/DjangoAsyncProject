from asgiref.sync import sync_to_async
from django.db import IntegrityError
from django.http import JsonResponse, Http404
from .serializer import ProjectSerializer, UnitSerializer, AllSerializer, SearchSerializer, InsertProjectsSerializer
from adrf.views import APIView
from taskAPI import repository


class All(APIView):
    async def get(self, request):
        projects = await repository.all_project()
        if projects:
            serializer = ProjectSerializer(projects, many=True)
            data = serializer.data
            return JsonResponse(data, safe=False)


class Expensive(APIView):
    async def get(self, request):
        most_expensive_project = await repository.expensive_project()
        if most_expensive_project:
            serializer = ProjectSerializer(most_expensive_project)
            data = serializer.data
            return JsonResponse(data, safe=False)


class Largest(APIView):
    async def get(self, request):
        most_largest_unit = await repository.largest_project()
        if most_largest_unit:
            serializer = ProjectSerializer(most_largest_unit)
            data = serializer.data
            return JsonResponse(data, safe=False)


class AllVilla(APIView):
    async def get(self, request):
        all_villa = await repository.all_villa_query()
        if all_villa:
            serializer = UnitSerializer(all_villa, many=True)
            data = serializer.data
            return JsonResponse(data, safe=False)


class AllProjects(APIView):
    async def get(self, request):
        all_projects = await repository.all_projects_query()
        if all_projects:
            serializer = AllSerializer(all_projects, many=True)
            data = serializer.data
            return JsonResponse(data, safe=False)


class SearchProject(APIView):
    async def get(self, request):
        parameters = request.GET.get('unit', '')
        search_request = await repository.search_projects_query(parameters)
        if search_request:
            serializer = SearchSerializer(search_request, many=True)
            data = serializer.data
            return JsonResponse(data, safe=False)
        raise Http404("Project not Found")


class SearchParamProject(APIView):
    async def get(self, request):
        unit = request.GET.get('unit', '')
        utype = request.GET.get('utype', '')
        beds = request.GET.get('beds', 0)
        search_request = await repository.search_projects_for_param(unit, utype, beds)
        if search_request:
            serializer = SearchSerializer(search_request, many=True)
            data = serializer.data
            return JsonResponse(data, safe=False)
        raise Http404("Project not found")


class SearchPostProject(APIView):
    async def post(self, request):
        parameters = request.data.get("unit", "")
        search_request = await repository.search_param_for_post(parameters)
        if search_request:
            serializer = SearchSerializer(search_request, many=True)
            data = serializer.data
            return JsonResponse(data, safe=False)
        raise Http404("Project not found")


class SearchWid(APIView):
    async def get(self, request, w_id):
        search_request = await repository.search_for_wid(w_id=w_id)
        if search_request:
            serializer = SearchSerializer(search_request)
            data = serializer.data
            return JsonResponse(data, safe=False)


class InsertUnit(APIView):
    @sync_to_async
    def insert_projects(self, data):
        try:
            insert_unit = InsertProjectsSerializer(data=data)
            insert_unit.is_valid(raise_exception=True)
            insert_unit.save()
            return {'post': insert_unit.data}
        except IntegrityError:
            return {'error': 'w_id already exists'}

    async def put(self, request):
        data = await self.insert_projects(request.data)
        return JsonResponse(data)
