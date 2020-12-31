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
    
    def paridad (self,options):
        out = []
        
        for opt in options:
            out.append({
                **opt,
                'paridad': [],
                })
            
        for indice in out:
            candidatos = indice['dandidates']
            hombre = []
            mujeres = []
            for cand in candidatos:
                if cand['sex'] == 'H':
                    hombre.append(cand)
                elif cand['sex'] == 'M':
                    mujeres.append(cand)
                    
    
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

        return Response({})
