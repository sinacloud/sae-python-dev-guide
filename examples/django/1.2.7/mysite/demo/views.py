# Create your views here.

from django.http import HttpResponse
from django.template import Template, Context
from django.core.context_processors import csrf
from demo.models import Demo

def showdemo(request):
    if request.method == 'POST':
        d = Demo(text=request.POST.get('text', ''))
        d.save()

    messages = Demo.objects.all()
    t = Template("""
    {{ xxxx }}
    {% for m in messages %}
        <p>{{ m.text }}</p>
    {% endfor %}
    <form action="" method="post"> {% csrf_token %}
        <div><textarea cols="40" name="text"></textarea></div>
        <div><input type="submit" /></div>
    </form>
    """);
    d = {'messages': messages}
    d.update(csrf(request))

    return HttpResponse(t.render(Context(d)))

