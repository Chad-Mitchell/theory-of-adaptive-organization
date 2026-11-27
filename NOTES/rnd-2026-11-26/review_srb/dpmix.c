// dpfast.c's exact even-n DP, printing mixture expectations directly:
// geometric p(T)=(1-q)q^(T-1), T>=1, for q in QS; uniform on 1..H for H in HS. J flat beyond saturation.
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
static const double QS[]={0.99,0.993,0.995,0.996,0.997,0.998,0.999,0.9995};
static const int HS[]={200,500,1000,2000};
#define NQ 8
#define NH 4
int main(int argc,char**argv){
  int n=atoi(argv[1]); int S=n/2; double *c=malloc((S+1)*sizeof(double));
  for(int k=0;k<=S;k++){ double d=sin(M_PI*k/n); if(((k-S)%2+2)%2==1) d/=cos(M_PI/n); c[k]=d*d; }
  c[0]=0;
  double *b=malloc((S+1)*sizeof(double)), *nb=malloc((S+1)*sizeof(double));
  for(int s=0;s<=S;s++) b[s]=1e300; b[0]=0;
  long double Eg[NQ]={0}, pw[NQ]; long double Eu[NH]={0};
  for(int i=0;i<NQ;i++) pw[i]=1.0L; // q^(T-1)
  double J=1e300; int t;
  for(t=1;;t++){
    int K=S/t; int changed=0;
    for(int s=0;s<=S;s++){ double m=b[s]; int kk=K<s?K:s;
      for(int k=1;k<=kk;k++){ double v=b[s-k]+c[k]; if(v<m) m=v; }
      nb[s]=m; if(m<b[s]) changed=1; }
    double *tmp=b;b=nb;nb=tmp;
    if(!changed) break;
    J=b[S-1]<b[S]?b[S-1]:b[S];
    for(int i=0;i<NQ;i++){ Eg[i]+=(1-QS[i])*pw[i]*J; pw[i]*=QS[i]; }
    for(int h=0;h<NH;h++) if(t<=HS[h]) Eu[h]+=J/HS[h];
  }
  // t-1 ticks recorded; beyond: J constant
  int L=t-1;
  printf("%d",n);
  for(int i=0;i<NQ;i++) printf(" %.17Lg",Eg[i]+pw[i]*J);
  for(int h=0;h<NH;h++){ long double e=Eu[h]; if(HS[h]>L) e+=(long double)(HS[h]-L)*J/HS[h]; printf(" %.17Lg",e);}
  printf("\n"); return 0;
}
