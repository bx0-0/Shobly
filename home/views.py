from django.shortcuts import render

# Create your views here.

def index(request):
    """
    هذه الدالة تستقبل طلب من المستخدم (request) وترسل له صفحة HTML اسمها index.html.

    ببساطة: لما حد يفتح الموقع، هذه الدالة بتعرض له الصفحة الرئيسية.
    """
    return render(request, 'home.html')
