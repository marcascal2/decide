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

    def mgu(self, options,Totalseats):
        out = []

        for o in options:

            out.append({
                **o,
                'postproc': 0,
            })
        
        out.sort(key=lambda x: -x['votes'])

        mv = out[0]['votes']
        ng=0

        for element in out:
            if element['votes']== mv:
                ng =ng + 1
            
        if ng == 1:
            out[0]['postproc'] = Totalseats
        else:
            r = Totalseats % ng
            c = Totalseats// ng
            if r== 0:
                a=0
                for x in range(0,ng):
                   out[x]['postproc'] = c
            else:
                if ng == len(out):
                    out[0]['postproc'] = c + r
                    for x in range(1,ng):
                        out[x]['postproc'] = c
                else:
                    if ng > Totalseats:
                        for x in range(0,r):
                          out[x]['postproc'] = 1
                    else:
                        for x in range(0,ng):
                            out[x]['postproc'] =c
                        out[ng]['postproc'] =r
        return out
            

    def post(self, request):
        """
         * type: IDENTITY | EQUALITY | WEIGHT | MGU
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
        s = request.data.get('seats')

        if t == 'IDENTITY':
            return self.identity(opts)
        elif t == 'MGU':
            return Response(self.mgu(opts,s))
        return Response({})
