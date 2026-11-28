// Same exact DP as dpeven.c, faster: at tick t the step size is capped at floor(S/t).
// Exact because any monotone path with total <= S can be reordered with steps in decreasing order,
// and the t-th largest of steps summing to <= S is <= S/t; the cost is order-independent; zero steps go last.
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
    int K=S/t; int changed=0;
    for(int s=0;s<=S;s++){ double m=b[s]; int kk=K<s?K:s;
      for(int k=1;k<=kk;k++){ double v=b[s-k]+c[k]; if(v<m) m=v; }
      nb[s]=m; if(m<b[s]) changed=1; }
    double *tmp=b;b=nb;nb=tmp;
    if(!changed) break;
    printf("%.15g\n", b[S-1]<b[S]?b[S-1]:b[S]);
  }
  return 0;
}
