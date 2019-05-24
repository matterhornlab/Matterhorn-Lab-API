from django.shortcuts import render
from django.views import View
from django.views.static import serve
from django.http import HttpResponse
from rest_framework import viewsets
from api.serializers import CompanySerializer, EntrySerializer
from api.models import Company, Entry

from tempfile import NamedTemporaryFile

import pandas as pd
import numpy as np
import os
import csv

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

class EntryViewSet(viewsets.ModelViewSet):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer

class DumpDataView(View):
    def get(self, request, ticker):
        c = Company.objects.filter(ticker=ticker).first()

        if c is None:
            return HttpResponse("I don't know a company with ticker {}".format(ticker))

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(ticker)

        writer = csv.writer(response)
        writer.writerow(['Date', 'Price'])

        for e in Entry.objects.filter(company=c):
            tstmp = "{}".format(e.timestamp)
            price = "{}".format(e.price)
            writer.writerow([tstmp, price])

        return response

class OverviewView(View):
    def get(self, request):
        companies = Company.objects.all()

        return render(request, "api/overview.html", {"companies": companies})

class DashboardView(View):
    def get(self, request, ticker):
        c = Company.objects.filter(ticker=ticker).first()

        if c is None:
            return HttpResponse("I don't know a company with ticker {}".format(ticker))

        entries = Entry.objects.filter(company=c)
        stats = {}

        # Change below here
        # Entries contains all entries. Taking i.e. the average:
        avg_price = 0
        data = pd.DataFrame(columns=['Date', 'Price'])

        for e in entries:
            avg_price += float(e.price) # Don't forget to cast to float here!
            # e.timestamp has the date and e.company the company
            data.append([{'Date': e.timestamp}, {'Price': e.price}])
        # Data is now a dataframe with columns date and price
        avg_price = avg_price/len(entries)
        stats["avg_price"] = avg_price

        # Don't change below here
        ctx = {
            "company": c,
            "entries": entries,
            "stats": stats,
        }
        return render(request, "api/dashboard.html", ctx)
