/* C4R lattice world (independent rewrite of the review's model): sites Z, rate-1 Poisson
   record clocks, a record depends on the latest records at i-1,i,i+1; order = closure.
   best[i] = longest chain from the origin record (0,0) ending at the latest reachable record at i.
   Usage: c4r_lattice T seed  -> prints at t=T: front, and L(floor(s*T),T) for s in RAYS. */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <stdint.h>
static uint64_t S[4];
static inline uint64_t rotl(uint64_t x,int k){return (x<<k)|(x>>(64-k));}
static inline uint64_t nxt(void){uint64_t r=rotl(S[1]*5,7)*9,t=S[1]<<17;S[2]^=S[0];S[3]^=S[1];S[1]^=S[2];S[0]^=S[3];S[2]^=t;S[3]=rotl(S[3],45);return r;}
static inline double u01(void){return ((nxt()>>11)+0.5)*(1.0/9007199254740992.0);}
static void seedit(uint64_t s){uint64_t z=s+0x9E3779B97F4A7C15ULL;for(int i=0;i<4;i++){z+=0x9E3779B97F4A7C15ULL;uint64_t x=z;x=(x^(x>>30))*0xBF58476D1CE4E5B9ULL;x=(x^(x>>27))*0x94D049BB133111EBULL;S[i]=x^(x>>31);}}
int main(int c,char**v){
  double T=atof(v[1]); seedit(strtoull(v[2],0,10)+0x1A77ULL);
  long W=(long)(1.2*T)+200, M=2*W+1, o=W;
  long *b=calloc(M+2,sizeof(long)); b[o+1]=1;
  double rays[]={0,0.25,0.5,0.75,0.9}; int nr=5;
  /* superposed clock of rate M; choose a uniform site per event */
  double t=0;
  for(;;){ t+=-log(u01())/(double)M; if(t>T)break;
    long i=(long)(u01()*M); if(i>=M)i=M-1;
    long m=b[i]; if(b[i+1]>m)m=b[i+1]; if(b[i+2]>m)m=b[i+2];
    if(m>0)b[i+1]=m+1; }
  long front=0; for(long x=W;x>0;x--) if(b[o+x+1]>0){front=x;break;}
  if(front>=W-5){fprintf(stderr,"window too small\n");return 1;}
  printf("T=%.0f seed=%s front=%ld",T,v[2],front);
  for(int r=0;r<nr;r++){long x=(long)floor(rays[r]*T); printf(" L%.2f=%ld",rays[r],b[o+x+1]);}
  printf("\n"); return 0; }
