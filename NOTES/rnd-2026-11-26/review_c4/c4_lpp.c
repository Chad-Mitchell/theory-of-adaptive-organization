/* Independent check of C4 (hostile review). Lattice record poset on Z:
   rate-1 Poisson clocks per site; record depends on latest records at i-1,i,i+1.
   Longest chain from origin record (0,0) = longest nearest-neighbour lazy path
   with increasing times. best[i] = longest chain ending at latest reachable record at i.
   Prints L(x,t) at snapshot times for rays s = x/t, and front position. */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <stdint.h>
static uint64_t st;
static inline uint64_t rng(void){st^=st<<13;st^=st>>7;st^=st<<17;return st;}
static inline double u01(void){return ((rng()>>11)+0.5)*(1.0/9007199254740992.0);}
int main(int argc,char**argv){
  double T=atof(argv[1]); unsigned long seed=strtoul(argv[2],0,10);
  st=0x9E3779B97F4A7C15ULL^(seed*0xD1B54A32D192ED03ULL); for(int i=0;i<20;i++)rng();
  long W=(long)(1.3*T)+60, M=2*W+1, c=W;
  long *best=calloc(M+2,sizeof(long)); /* index shift by 1; 0 = unreachable */
  best[c+1]=1; /* origin record counted */
  double snaps[]={T/16,T/8,T/4,T/2,T}; int ns=5,k=0;
  double rays[]={0,0.25,0.5,0.75,0.9,0.95}; int nr=6;
  double t=0;
  while(k<ns){
    t+= -log(u01())/(double)M;
    while(k<ns && t>snaps[k]){
      double tt=snaps[k];
      long front=0; for(long x=W;x>0;x--) if(best[c+x+1]>0){front=x;break;}
      printf("t=%.1f front=%ld",tt,front);
      for(int r=0;r<nr;r++){long x=(long)floor(rays[r]*tt); printf(" s%.2f=%ld",rays[r],best[c+x+1]);}
      /* L at front site */
      printf(" Lfront=%ld\n",best[c+front+1]);
      k++;
    }
    if(k>=ns)break;
    long i=(long)(u01()*M); if(i>=M)i=M-1;
    long m=best[i]; if(best[i+1]>m)m=best[i+1]; if(best[i+2]>m)m=best[i+2];
    if(m>0) best[i+1]=m+1;
  }
  return 0;
}
