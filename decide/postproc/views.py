from rest_framework.views import APIView
from rest_framework.response import Response


class PostProcView(APIView):

    def identity(self, options):
        out = []

        for opt in options:
            out.append({
                **opt,
                'postproc': opt['votes'],
            })

        out.sort(key=lambda x: -x['postproc'])
        return Response(out)

    #Sistema D'Hondt - Metodo de promedio mayor para asignar escaños en sistemas de representación proporcional por listas electorales. Por tanto,
    # en dicho método trabajaremos con listas de partidos politicos y con un número de escaños que será pasado como parámetro. 
    #           Fórmula de D'Hondt: cociente = V/S+1    , siendo V: el número total de votosS
    #                                                            S: el num. de escaños que posee en el momento
    def dhondt(self, options, nSeats):

        #Salida
        out = [] 

        #Añadimos a options un parámetro llamado 'seat' que será donde
        #guardaremos la cantidad de escaños por opción y nuestra 'S' en la fórmula de D'Hondt
        for opt in options:
            out.append({
                **opt, 

                'seat': 0,
            })

        #Igualamos numEscanos al numero total de escaños a repartir
        numEscanos = nSeats

        #Mientras no se repartan todos los escaños hacemos lo siguiente
        while numEscanos>0:
            
            actual = 0
            
            #Comparamos todas las opciones posibles
            for i in range(1, len(out)):
                valorActual = out[actual]['votes'] / (out[actual]['seat'] + 1)
                valorComparar = out[i]['votes'] / (out[i]['seat'] + 1)

                #Si el valor a comparar es mayor que el valor actual mayor se cambian
                if(valorActual<valorComparar):
                    actual = i
            
            #Al final de recorrer todos, la opcion cuyo indice es actual es el que posee más votos y,
            #por tanto, se le añade un escaño
            out[actual]['seat'] = out[actual]['seat'] + 1
            numEscanos = numEscanos - 1
        
        #Ordenamos las diferentes opciones por su número total de escaños obtenidos durante el método
        out.sort(key = lambda x: -x['seat'])

        return Response(out)


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
        
        elif t == 'DHONDT':
            return self.dhondt(opts, request.data.get('nSeats'))

        return Response({})

