from rest_framework.views import APIView
from rest_framework.response import Response
from pickle import TRUE, FALSE


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
<<<<<<< Updated upstream

=======
    
    def paridad (self,options):
        out = []
        escanios = 0
        candsres = []
        for opt in options: 
#            escanios = opt['escanios']
            for c in opt['candidates']:
                partidoCand = c['political_party']
                optionPartido = opt['option']
                if (partidoCand == optionPartido):
                    candsres.append(c)
            break #Solo necesito uno de los escanios. 
        
        for opt in options:
            out.append({
                **opt,
                'paridad': [],
                })
            
        for indice in out:
            candidatos = indice['candidates']
            hombres = []
            mujeres = []
            for cand in candidatos:
                if cand['sex'] == 'H':
                    hombres.append(cand)
                elif cand['sex'] == 'M':
                    mujeres.append(cand)
                    
            hom = 0
            muj = 0
            t = 2
            paridad = True
            while t > 0:
                if paridad: 
                    if muj < len(mujeres):
                        indice['paridad'].append(mujeres[muj])
                        muj = muj + 1
                    else:
                        indice['paridad'].append(hombres[hom])
                        hom = hom + 1 
                    paridad = False
                else: 
                    if hom < len(hombres):
                        indice['paridad'].append(hombres[hom])
                        hom = hom + 1
                    else: 
                        indice['paridad'].append(mujeres[muj])
                        muj = muj + 1 
                    paridad = True
                t -=1
        return out
    
>>>>>>> Stashed changes
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
            p = self.paridad(opts)
            return self.identity(opts)

        return Response({})
