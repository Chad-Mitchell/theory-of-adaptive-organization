// Reviewer's independent DP (own code). Distances by the edge-normal breakpoint formula (no closed form),
// forward DP over positions 0..P with ANY forward step size (no per-tick cap), both parities.
// Usage: rv_dp n Tmax [a]  -> prints "n J(1) ... J(Tmax)"; with "a" and even n the target is the antipode only (M3c rule)
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
int main(int argc,char**argv){
  int n=atoi(argv[1]),TM=atoi(argv[2]);
  double *vx=malloc(n*sizeof(double)),*vy=malloc(n*sizeof(double)),*tx=malloc(2*n*sizeof(double)),*ty=malloc(2*n*sizeof(double)),*w=malloc(2*n*sizeof(double)),*p0=malloc(2*n*sizeof(double));
  for(int i=0;i<n;i++){vx[i]=cos(2*M_PI*i/n);vy[i]=sin(2*M_PI*i/n);}
  for(int j=0;j<n;j++){double a=2*M_PI*(j+0.5)/n; tx[j]=cos(a);ty[j]=sin(a);tx[j+n]=-tx[j];ty[j+n]=-ty[j];}
  for(int j=0;j<2*n;j++){double mx=-9,mn=9; for(int i=0;i<n;i++){double p=vx[i]*tx[j]+vy[i]*ty[j]; if(p>mx)mx=p; if(p<mn)mn=p;} w[j]=mx-mn; p0[j]=tx[j];}
  int H=n/2+1; double *c=malloc((H+1)*sizeof(double)); int P=0;
  for(int k=0;k<=H;k++){ double d=0; for(int j=0;j<2*n;j++){double r=(p0[j]-(vx[k]*tx[j]+vy[k]*ty[j]))/w[j]; if(r>d)d=r;} c[k]=d*d; if(d>1-1e-12) P=k; }
  int nt=0,tg[4]; for(int k=0;k<=P;k++) if(c[k]>1-2e-12) tg[nt++]=k;
  if(argc>3 && argv[3][0]=='a' && n%2==0){ nt=1; tg[0]=n/2; if(P<n/2) P=n/2; }
  double *f=malloc((P+1)*sizeof(double)),*g=malloc((P+1)*sizeof(double));
  for(int s=0;s<=P;s++) f[s]=1e300; f[0]=0;
  printf("%d",n);
  for(int t=1;t<=TM;t++){
    for(int s=0;s<=P;s++){ double m=f[s]; for(int i=0;i<s;i++){ double v=f[i]+c[s-i]; if(v<m)m=v;} g[s]=m; }
    double *q=f;f=g;g=q; double J=1e300; for(int i=0;i<nt;i++) if(f[tg[i]]<J) J=f[tg[i]];
    printf(" %.17g",J);
  }
  printf("\n"); return 0;
}
