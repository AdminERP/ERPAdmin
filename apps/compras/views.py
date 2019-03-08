from django.shortcuts import render

# Create your views here.



def cotizacion_create(request): 
    if request.method == 'POST': 
        form = CotizacionForm(request.POST) 
        if form.is_valid(): 
            form.save()
        #return redirect (index )

    else: 
        form = CotizacionForm()
    #return render (request, '/compras/cotizacion_form.html', {'form': form})


def solicitud_create(request): 
    if request.method == 'POST': 
        form = SolicitudForm(request.POST) 
        if form.is_valid(): 
            form.save()
        #return redirect (index )

    else: 
        form = SolicitudForm()
    #return render (request, '/compras/solicitud_form.html', {'form': form})

def orden_create(request): 
    if request.method == 'POST': 
        form = OrdenForm(request.POST) 
        if form.is_valid(): 
            form.save()
        #return redirect (index )

    else: 
        form = OrdenForm()
    #return render (request, '/compras/solicitud_form.html', {'form': form})

