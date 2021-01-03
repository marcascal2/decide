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

    def mgu(self, options,Totalseats):
        out = []

        for o in options:

            o.append({
                **o,
                'postproc': 0,
            })
        
        out.sort(key=lambda x: -x['votes'])

        mv = out[0]['votes']
        ng=0

        for element in out:
            if element['votes']== ng:
                ng =ng + 1
            
        if ng == 1:
            out[0]['postproc'] = Totalseats
        else 
            r = Totalseats % ng
            if r== 0:
                c = Totalseats// ng
                for x in range(0,ng-1):
                   out[x]['postproc'] = c

            

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
