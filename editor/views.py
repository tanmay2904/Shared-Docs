from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import docs
# Create your views here.
def index(request):
    return render(request,'index.html')
docid = -1
def openDoc(request):
    global docid
    if 'go' in request.POST:
        docid = request.POST['docID']
        name = request.POST['name']
        if(name == ""):
            name = "tanmay"
        #print(name)
        if docs.objects.filter(id = docid).exists():
            document = docs.objects.get(id = docid)
            doc = document.doc
            return render(request,'home.html',{'doc': doc,'docid':docid,'name':name})
        else:
            print("Document doesn't exists")
            docid = -1
            return redirect('index')
    else:
        docm = docs.objects.create()
        docm.save()
        docid = docm.id
        return render(request,'home.html',{'doc': "",'docid':docid,'name':name})


def save(request):

    text = request.POST['doc']
    docm = docs.objects.get(id = docid)
    docm.doc = text
    #docm = docs.objects.create(doc = text)
    docm.save()
    return redirect('index')