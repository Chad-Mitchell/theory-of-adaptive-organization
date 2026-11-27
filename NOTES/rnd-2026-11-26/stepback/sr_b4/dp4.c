// SR-b4: exact even-n DP (same as review_srb/dpfast.c / dpmix.c), printing J(n,T) for T=1..Tmax.
// Distance for even n: d(v0,vk)=sin(pi k/n), divided by cos(pi/n) when k-n/2 is odd (SR_B.md §8.6).
// Target: v_{n/2-1} or v_{n/2} (both at d=1). Step at tick t capped at floor(S/t) (exact, §8.4).
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
int main(int argc,char**argv){
  int n=atoi(argv[1]); int Tmax=atoi(argv[2]); int S=n/2;
  double *c=malloc((S+1)*sizeof(double));
  for(int k=0;k<=S;k++){ double d=sin(M_PI*k/n); if(((k-S)%2+2)%2==1) d/=cos(M_PI/n); c[k]=d*d; }
  c[0]=0;
  double *b=malloc((S+1)*sizeof(double)), *nb=malloc((S+1)*sizeof(double));
  for(int s=0;s<=S;s++) b[s]=1e300; b[0]=0;
  printf("%d",n);
  double J=1e300;
  for(int t=1;t<=Tmax;t++){
    int K=S/t; if(K<1)K=1;
    for(int s=0;s<=S;s++){ double m=b[s]; int kk=K<s?K:s;
      for(int k=1;k<=kk;k++){ double v=b[s-k]+c[k]; if(v<m) m=v; }
      nb[s]=m; }
    double *tmp=b;b=nb;nb=tmp;
    J=b[S-1]<b[S]?b[S-1]:b[S];
    printf(" %.17g",J);
  }
  printf("\n"); return 0;
}
