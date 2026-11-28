/* C4R control / planted world: Poisson sprinkling of density rho (per unit dt dx) in 1+1 Minkowski
   with light speed cp (cp=1: control; cp!=1: planted effect, analysed with c=1).
   For each ray s, sprinkle the causal diamond from (0,0) to (x=sT, t=T) [needs s<cp] independently
   and return the longest chain (strict 2D LIS in light-cone coords u=cp t+x, v=cp t-x), +1 for the origin.
   Usage: c4r_sprinkle T rho cp seed */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <stdint.h>
static uint64_t S[4];
static inline uint64_t rotl(uint64_t x,int k){return (x<<k)|(x>>(64-k));}
static inline uint64_t nxt(void){uint64_t r=rotl(S[1]*5,7)*9,t=S[1]<<17;S[2]^=S[0];S[3]^=S[1];S[1]^=S[2];S[0]^=S[3];S[2]^=t;S[3]=rotl(S[3],45);return r;}
static inline double u01(void){return ((nxt()>>11)+0.5)*(1.0/9007199254740992.0);}
static void seedit(uint64_t s){uint64_t z=s+0x5EEDULL;for(int i=0;i<4;i++){z+=0x9E3779B97F4A7C15ULL;uint64_t x=z;x=(x^(x>>30))*0xBF58476D1CE4E5B9ULL;x=(x^(x>>27))*0x94D049BB133111EBULL;S[i]=x^(x>>31);}}
static double gauss(void){double a=u01(),b=u01();return sqrt(-2*log(a))*cos(2*M_PI*b);}
typedef struct{double u,v;}P;
static int cmp(const void*a,const void*b){double d=((P*)a)->u-((P*)b)->u;return d<0?-1:d>0;}
int main(int c,char**v){
  double T=atof(v[1]),rho=atof(v[2]),cp=atof(v[3]); seedit(strtoull(v[4],0,10));
  double rays[]={0,0.25,0.5,0.75,0.9}; int nr=5;
  printf("T=%g rho=%g cp=%g seed=%s",T,rho,cp,v[4]);
  for(int r=0;r<nr;r++){
    double U=cp*T+rays[r]*T, V=cp*T-rays[r]*T, mean=rho*U*V/(2*cp);
    long N=(long)llround(mean+sqrt(mean)*gauss()); if(N<0)N=0;
    P*p=malloc(sizeof(P)*(N+1)); double*tail=malloc(sizeof(double)*(N+1));
    for(long k=0;k<N;k++){p[k].u=u01()*U;p[k].v=u01()*V;}
    qsort(p,N,sizeof(P),cmp); long L=0;
    for(long k=0;k<N;k++){double y=p[k].v; long lo=0,hi=L; while(lo<hi){long m=(lo+hi)/2; if(tail[m]<y)lo=m+1; else hi=m;} tail[lo]=y; if(lo==L)L++;}
    printf(" L%.2f=%ld",rays[r],L+1); free(p); free(tail);
  }
  printf("\n"); return 0; }
