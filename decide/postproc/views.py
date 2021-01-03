from rest_framework.views import APIView
from rest_framework.response import Response


class PostProcView(APIView):

    def identity(self, options):
        out = []

        for opt in options:
            out.append({
                **opt,
                'postproc': opt['votes'],
            });

        out.sort(key=lambda x: -x['postproc'])
        return Response(out)
    
    def saintelague(self, options, nSeats):
        
        #Definimos las variables

        partidos = [] 
        puntosPorPart = [] 
        escanos = [] 
        out = [] 

       #Ponemos los escaños iniciales de todos los partidos a 0
        for n in options:
            escanosIniciales = 0
            escanos.append(escanosIniciales)

        #Añadimos los votos a cada partido y a out todas las salidas anterioes mas los escaños
        for opt in options:
            partidos.append(opt['votes']) 
            out.append({
                **opt,
                'seats': 0,
                })

        #Inicializamos la lista así para que no se cambie por referencia
        puntosPorPart = partidos[:]
        escanosTotales = nSeats 
        i = 0
        while(i<escanosTotales):
            maxVotos = max(puntosPorPart) 
            index = puntosPorPart.index(maxVotos)
            if maxVotos != 0:
                
                escanos[index] += 1 
                out[index]['seats'] += 1 
                puntosPorPart[index] = partidos[index] / ((2*escanos[index])+1) 

            i=i+1
            
        out.sort(key=lambda x: -x['seats'])
        return Response(out)

        #Me faltaria hacer el saintelague modificado
    def post(self, request):
        """
         * type: IDENTITY | EQUALITY | WEIGHT
         * options: [
            {
             option: str,
             number: int,
             votes: int,
             ...extraparams
            }
           ]
        """

        t = request.data.get('type', 'IDENTITY')
        opts = request.data.get('options', [])

        if t == 'IDENTITY':
            return self.identity(opts)
        elif t == 'SAINTELAGUE':
            return self.saintelague(opts,request.data.get('nSeats'))

        return Response({})
