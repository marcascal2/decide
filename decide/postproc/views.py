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
    def porcentaje_genero(self, mujeres, hombres):
        suma = len(mujeres) + len(hombres)
        porcentaje_mujeres = len(mujeres)/suma
        porcentaje_hombres = len(hombres)/suma
        if(porcentaje_mujeres< 0.4) | (porcentaje_hombres <0.4):
            return False    
        else:
            return True

        return Response({})
     
