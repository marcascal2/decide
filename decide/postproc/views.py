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
    
    def comprobar(self,opts):
        comprueba = False   
        out = []
        for opt in opts:
            out.append({
                **opt
            })
        for i in out:
            candidatos=i['candidates'] 
            mujeres =[]
            hombres=[]
            for c in candidatos:
                if c['sex'] == 'M':
                    mujeres.append(c)
                elif c['sex'] == 'H':
                    hombres.append(c)
            comprueba= self.porcentaje_genero(hombres,mujeres)
            if ~comprueba:
                break
        return comprueba
        
    def porcentaje_genero(self, mujeres, hombres):
        suma = len(mujeres) + len(hombres)
        porcentaje_mujeres = len(mujeres)/suma
        porcentaje_hombres = len(hombres)/suma
        if(porcentaje_mujeres< 0.4) or (porcentaje_hombres <0.4):
            return False    
        else:
            return True

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

        t = request.data.get('type')
        opts = request.data.get('options', [])
        cands = request.data.get('candidates', [])
        print(cands)
        if t == 'IDENTITY':
            return self.identity(self, opts)
        if t == 'PARIDAD':
            comprueba= self.comprobar(opts)
            if comprueba:
                return Response(self.paridad(opts,cands))
            else:
                return Response({'message' : 'la diferencia del numero de hombres y mujeres es de más de un 60% - 40%'})
        
        return Response({})



        
     
