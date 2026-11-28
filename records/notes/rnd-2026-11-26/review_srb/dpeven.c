// Exact min-plus DP for even regular n-gon, all effects, monotone vertex paths 0 -> {n/2-1, n/2}.
// d(v0,vk)= sin(pi k/n) / (cos(pi/n) if (k-n/2) odd else 1). Prints J(T) for T=1..Tsat (until fixed point).
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
int main(int argc,char**argv){
  int n=atoi(argv[1]); int S=n/2; double *c=malloc((S+1)*sizeof(double));
  for(int k=0;k<=S;k++){ double d=sin(M_PI*k/n); if(((k-S)%2+2)%2==1) d/=cos(M_PI/n); c[k]=d*d; }
  c[0]=0;
  double *b=malloc((S+1)*sizeof(double)), *nb=malloc((S+1)*sizeof(double));
  for(int s=0;s<=S;s++) b[s]=1e300; b[0]=0;
  for(int t=1;;t++){
    int changed=0;
    for(int s=0;s<=S;s++){ double m=b[s];
      for(int k=1;k<=s;k++){ double v=b[s-k]+c[k]; if(v<m) m=v; }
      nb[s]=m; if(m<b[s]) changed=1; }
    double *tmp=b;b=nb;nb=tmp;
    double J=b[S-1]<b[S]?b[S-1]:b[S];
    if(!changed) break;
    printf("%.15g\n",J);
  }
  return 0;
}
