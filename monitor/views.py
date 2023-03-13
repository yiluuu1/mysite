from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from monitor.models import hotbit_analysis
import pandas as pd


contract_list = ['btc_contract', 'doge_contract', 'dot_contract',
                 'etc_contract', 'eth_contract', 'fil_contract',
                 'ltc_contract', 'trx_contract', 'xrp_contract']

_dic = {}
for num in range(len(contract_list)):
    _dic[contract_list[num]] = {'token': contract_list[num]}


def monitor(request):

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = hotbit_analysis(_dic, contract_list)
        return JsonResponse({'data': pd.DataFrame(data).to_html()})
    else:
        data = hotbit_analysis(_dic, contract_list)
        return render(request, "monitor.html", {'data': pd.DataFrame(data).to_html()})


def home_view(request):
    if request.method == "POST":
        return HttpResponseRedirect(reverse("monitor"))
    return render(request, "home.html")


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})