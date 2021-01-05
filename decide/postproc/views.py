from rest_framework.views import APIView
from rest_framework.response import Response
import math

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
        
    def simple(self, options, seats):
        out = []
        for simp in options:
            out.append({
                **simp,
                'postproc': 0,
            })
        out.sort(key=lambda x: -x['votes'])

        sea = seats
        n = 0

        for votes in out:
                n = votes['votes'] + n
        
        valEs = n/sea

        n1 = 0

        while sea > 0:
            if n1 < len(out):
                seats_ = math.trunc(out[n1]['votes']/valEs) 
                out[n1]['postproc'] = seats_
                sea = sea - seats_
                n1 = n1+1
            else:
                now = 0
                c = 1
                while c <len(out):
                    vAct = out[now]['votes']/valEs - out[now]['postproc']
                    vCom = out[c]['votes']/valEs - out[c]['postproc']
                    if(vAct >= vCom):
                        c = c + 1
                    else:
                        now=c
                        c = c + 1
                out[now]['postproc'] = out[now]['postproc'] + 1
                sea = sea - 1
        return out
        

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
                if ng == len(out) and ng < Totalseats:
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
        elif t == 'SIMPLE':
            return Response(self.simple(opts,s))

        elif t == 'MGU':
            return Response(self.mgu(opts,s))
        return Response({})
