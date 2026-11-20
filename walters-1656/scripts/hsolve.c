// Homophonic substitution solver: simulated annealing over symbol->letter key with n-gram scoring.
// usage: hsolve ngram.bin N cipher.txt restarts iters seed [chiW] [T0] [T1] [fixed.txt]
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <stdint.h>
static uint64_t rs;
static inline uint64_t rnd(){ rs^=rs<<13; rs^=rs>>7; rs^=rs<<17; return rs; }
static inline double rndu(){ return (rnd()>>11)*(1.0/9007199254740992.0); }
int NG; float *lg; double uni[26];
int *ct; int L; int S; int *key; char *pt;
int **pos; int *npos;
int *valid; // window start i valid?
static inline float win(int i){ int idx=0; for(int k=0;k<NG;k++) idx=idx*26+pt[i+k]; return lg[idx]; }
int cnt[26]; double chiW=0.3; int Nlet;
double chi(){ double x=0; for(int l=0;l<26;l++){ double e=uni[l]*Nlet; if(e<0.5) e=0.5; double d=cnt[l]-e; x+=d*d/e; } return x; }
int main(int argc,char**argv){
  NG=atoi(argv[2]); long V=1; for(int i=0;i<NG;i++) V*=26;
  lg=malloc(V*sizeof(float)); FILE*f=fopen(argv[1],"rb"); if(fread(lg,sizeof(float),V,f)!=V){fprintf(stderr,"ngram read\n");return 1;} fclose(f);
  char un[512]; snprintf(un,512,"%s.uni",argv[1]); f=fopen(un,"r"); for(int i=0;i<26;i++) if(fscanf(f,"%lf",&uni[i])!=1) return 1; fclose(f);
  f=fopen(argv[3],"r"); ct=malloc(100000*sizeof(int)); L=0; S=0; int v; while(fscanf(f,"%d",&v)==1){ ct[L++]=v; if(v+1>S) S=v+1; } fclose(f);
  int restarts=atoi(argv[4]); long iters=atol(argv[5]); rs=strtoull(argv[6],0,10)*0x9E3779B97F4A7C15ULL+88172645463325252ULL;
  if(argc>7) chiW=atof(argv[7]); double T0=argc>8?atof(argv[8]):6.0, T1=argc>9?atof(argv[9]):0.3;
  int *fixed=malloc(S*sizeof(int)); for(int s=0;s<S;s++) fixed[s]=-1;
  if(argc>10){ f=fopen(argv[10],"r"); int s; char c; while(f && fscanf(f,"%d %c",&s,&c)==2) if(s<S) fixed[s]=c-'a'; if(f) fclose(f); }
  key=malloc(S*sizeof(int)); pt=malloc(L+8); pos=malloc(S*sizeof(int*)); npos=calloc(S,sizeof(int));
  for(int i=0;i<L;i++) if(ct[i]>=0) npos[ct[i]]++;
  for(int s=0;s<S;s++){ pos[s]=malloc((npos[s]+1)*sizeof(int)); npos[s]=0; }
  for(int i=0;i<L;i++) if(ct[i]>=0) pos[ct[i]][npos[ct[i]]++]=i;
  valid=calloc(L,sizeof(int)); int nwin=0; Nlet=0;
  for(int i=0;i<L;i++){ if(ct[i]>=0) Nlet++; if(i+NG<=L){ int ok=1; for(int k=0;k<NG;k++) if(ct[i+k]<0) ok=0; valid[i]=ok; nwin+=ok; } }
  int *used=malloc(S*sizeof(int)); int nu=0; for(int s=0;s<S;s++) if(npos[s]>0 && fixed[s]<0) used[nu++]=s;
  double cum[26]; double a=0; for(int l=0;l<26;l++){ a+=uni[l]; cum[l]=a; }
  double best=-1e18; int *bkey=malloc(S*sizeof(int)); char *mark=calloc(L,1); int *wl=malloc(L*sizeof(int));
  for(int r=0;r<restarts;r++){
    for(int s=0;s<S;s++){ if(fixed[s]>=0) key[s]=fixed[s]; else { double u=rndu(); int l=0; while(l<25&&cum[l]<u) l++; key[s]=l; } }
    memset(cnt,0,sizeof(cnt)); for(int i=0;i<L;i++){ pt[i]=ct[i]>=0?key[ct[i]]:0; if(ct[i]>=0) cnt[(int)pt[i]]++; }
    double sc=0; for(int i=0;i<L;i++) if(valid[i]) sc+=win(i);
    double cx=chi(); double tot=sc-chiW*cx; double rbest=tot; int *rkey=malloc(S*sizeof(int)); memcpy(rkey,key,S*sizeof(int));
    for(long it=0;it<iters;it++){
      double T=T0+(T1-T0)*((double)it/iters);
      int s=used[rnd()%nu]; int old=key[s]; int nl;
      if(rnd()%4==0){ nl=rnd()%26; } else { double u=rndu(); nl=0; while(nl<25&&cum[nl]<u) nl++; }
      if(nl==old) continue;
      // collect windows
      int nw=0; for(int j=0;j<npos[s];j++){ int p=pos[s][j]; for(int k=0;k<NG;k++){ int i=p-k; if(i>=0&&valid[i]&&!mark[i]){ mark[i]=1; wl[nw++]=i; } } }
      double before=0; for(int j=0;j<nw;j++) before+=win(wl[j]);
      for(int j=0;j<npos[s];j++) pt[pos[s][j]]=nl;
      double after=0; for(int j=0;j<nw;j++){ after+=win(wl[j]); mark[wl[j]]=0; }
      cnt[old]-=npos[s]; cnt[nl]+=npos[s]; double ncx=chi();
      double d=(after-before)-chiW*(ncx-cx);
      if(d>=0 || rndu()<exp(d/T)){ key[s]=nl; sc+=after-before; cx=ncx; tot+=d; if(tot>rbest){ rbest=tot; memcpy(rkey,key,S*sizeof(int)); } }
      else { for(int j=0;j<npos[s];j++) pt[pos[s][j]]=old; cnt[old]+=npos[s]; cnt[nl]-=npos[s]; }
    }
    // report restart best
    memcpy(key,rkey,S*sizeof(int)); double s2=0; for(int i=0;i<L;i++) pt[i]=ct[i]>=0?key[ct[i]]:0; for(int i=0;i<L;i++) if(valid[i]) s2+=win(i);
    printf("R%d tot=%.1f ngram/win=%.3f : ",r,rbest,s2/nwin); for(int i=0;i<L&&i<150;i++) putchar(ct[i]>=0?'a'+pt[i]:' '); printf("\n"); fflush(stdout);
    if(rbest>best){ best=rbest; memcpy(bkey,rkey,S*sizeof(int)); }
    free(rkey);
  }
  printf("BEST %.1f\nKEY",best); for(int s=0;s<S;s++) printf(" %d:%c",s,npos[s]? 'a'+bkey[s]:'-'); printf("\nPT ");
  for(int i=0;i<L;i++) putchar(ct[i]>=0?'a'+bkey[ct[i]]:' '); printf("\n");
  return 0;
}
