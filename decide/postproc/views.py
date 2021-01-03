from rest_framework.views import APIView
from rest_framework.response import Response
from pickle import TRUE, FALSE
from optparse import Option
import random

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

    
    def paridad (self,options,cands):
        out = []

        for opt in options:
            out.append({
                **opt,
                'paridad': [],
                })
        
        hombres = []
        mujeres = []
        for cand in cands:
            if cand['sex'] == 'H':
                hombres.append(cand)
            elif cand['sex'] == 'M':
                mujeres.append(cand)
        
        for indice in out:
            escanios = indice['escanio']
            hom = 0
            muj = 0
            paridad = True
            while escanios > 0:
                if paridad: 
                    if muj < len(mujeres):
                        indice['paridad'].append(mujeres[muj])
                        muj = muj + 1
                        escanios -=1
                    paridad = False
                else: 
                    if hom < len(hombres):
                        indice['paridad'].append(hombres[hom])
                        hom = hom + 1
                        escanios -=1
                    paridad = True
                if(muj == len(mujeres) and hom == len(hombres)):
                    escanios = 0
                    break
        return out
    
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
        cands = request.data.get('candidates', [])
        print(cands)
        if t == 'IDENTITY':
            return self.identity(opts)
        if t == 'PARIDAD':
            return Response(self.paridad(opts, cands))
        return Response({})
