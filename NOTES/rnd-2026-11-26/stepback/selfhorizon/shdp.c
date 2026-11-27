// SH-noise: exact forward DP (SR_B §8.4 step cap) for any n, both target rules.
// Distances by the breakpoint method: d(v0,vk)=max over the 2n edge-normal directions of <v0-vk,th>/width(th).
// Output: line 1 "n M3h J(1..T)", line 2 "n MIX J(1..T)". Targets: positions 0..P on one side (reflection).
// M3h: any vertex with d=1 (|d-1|<1e-12) at index<=n/2; MIX: antipode (n/2) for even n, farthest (n-1)/2 for odd n.
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
int main(int argc,char**argv){
  int n=atoi(argv[1]), Tm=atoi(argv[2]); int H=n/2;
  double *vx=malloc(n*sizeof(double)),*vy=malloc(n*sizeof(double));
  for(int i=0;i<n;i++){vx[i]=cos(2*M_PI*i/n);vy[i]=sin(2*M_PI*i/n);}
  int m=2*n; double *tx=malloc(m*sizeof(double)),*ty=malloc(m*sizeof(double)),*w=malloc(m*sizeof(double));
  for(int j=0;j<n;j++){double a=2*M_PI*(j+0.5)/n; tx[j]=cos(a);ty[j]=sin(a);tx[j+n]=-tx[j];ty[j+n]=-ty[j];}
  for(int j=0;j<m;j++){double mx=-1e9,mn=1e9; for(int i=0;i<n;i++){double p=vx[i]*tx[j]+vy[i]*ty[j]; if(p>mx)mx=p; if(p<mn)mn=p;} w[j]=mx-mn;}
  double *c=malloc((H+1)*sizeof(double)); c[0]=0;
  for(int k=1;k<=H;k++){double best=0; for(int j=0;j<m;j++){double v=((vx[0]-vx[k])*tx[j]+(vy[0]-vy[k])*ty[j])/w[j]; if(v>best)best=v;} c[k]=best*best;}
  int tg[4],nt=0; for(int k=1;k<=H;k++) if(fabs(sqrt(c[k])-1)<1e-12) tg[nt++]=k;
  int P=H; double *b=malloc((P+1)*sizeof(double)),*nb=malloc((P+1)*sizeof(double));
  int tmix=(n%2==0)?H:(n-1)/2;
  double *J1=malloc(Tm*sizeof(double)),*J2=malloc(Tm*sizeof(double));
  for(int s=0;s<=P;s++)b[s]=1e300; b[0]=0;
  for(int t=1;t<=Tm;t++){ int K=P/t; if(K<1)K=1;
    for(int s=0;s<=P;s++){double mm=b[s]; int kk=K<s?K:s; for(int k=1;k<=kk;k++){double v=b[s-k]+c[k]; if(v<mm)mm=v;} nb[s]=mm;}
    double*tp=b;b=nb;nb=tp;
    double j1=1e300; for(int i=0;i<nt;i++) if(b[tg[i]]<j1) j1=b[tg[i]];
    J1[t-1]=j1; J2[t-1]=b[tmix]; }
  printf("%d M3h",n); for(int t=0;t<Tm;t++) printf(" %.17g",J1[t]); printf("\n");
  printf("%d MIX",n); for(int t=0;t<Tm;t++) printf(" %.17g",J2[t]); printf("\n");
  fprintf(stderr,"%d targets:",n); for(int i=0;i<nt;i++) fprintf(stderr," %d",tg[i]); fprintf(stderr," dmin=%.6g\n",sqrt(c[1]));
  return 0; }
