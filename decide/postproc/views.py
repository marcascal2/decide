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
        
    def simple(self, options, seats):
        out = []
        for simp in options:
            out.append({
                **simp,
                'postprocesado': 0,
            })
        out.sort(key=lamba x: -x['votes'])

        sea = seats;
        n = 0;

        for votes in out:
                n = votes['votes']+n;
        
        valEs = n/sea;

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

        return Response({})
