from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

from website.tasks import create_task
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def image_upload(request):
    if request.method == "POST" and request.FILES["image_file"]:
        image_file = request.FILES["image_file"]
        fs = FileSystemStorage()
        filename = fs.save(image_file.name, image_file)
        image_url = fs.url(filename)
        print(image_url)
        return render(request, "upload/upload.html", {
            "image_url": image_url
        })
    return render(request, "upload/upload.html")


@csrf_exempt
def run_task(request):
    if request.POST:
        task_type = request.POST.get("type")
        task = create_task.delay(int(task_type))
        return JsonResponse({"task_id": task.id}, status=202)