#include <stdio.h>
#include <sys/time.h>
#include <unistd.h>
#include <pthread.h>
#include <errno.h>
#include <stdlib.h>

//pthread_t thread;
pthread_cond_t cond;
pthread_mutex_t mutex;
int flag = 0;
int NTHREAD = 4;
struct Param {
    int ThreadID;
};
struct Threading
{
	pthread_t Thread;
	unsigned r;
	void *ret;
	Param Arg;
};
 
void * thr_fn(void * arg) {
    fprintf(stderr, "thread %d\n", ((Param *)arg)->ThreadID);
    struct timeval now;
    struct timespec outtime;
    bool newchrom=true;
    if(newchrom){
        pthread_mutex_lock(&mutex);
        flag++;
        while(flag != 0 && flag != NTHREAD) {
            fprintf(stderr, "thread wait %d %d\n", ((Param *)arg)->ThreadID, flag);
            gettimeofday(&now, NULL);
            outtime.tv_sec = now.tv_sec + 1;
            pthread_cond_timedwait(&cond, &mutex, &outtime);
            fprintf(stderr, "thread reruning %d %d\n", ((Param *)arg)->ThreadID, flag);
        }
        if(flag == NTHREAD){
            fprintf(stderr, "print output\n");
            flag=0;
	    newchrom = false;
        }
        pthread_mutex_unlock(&mutex);
    }
    fprintf(stderr, "thread exit %d %d\n", ((Param *)arg)->ThreadID, flag);
}
 
int main() {
    pthread_mutex_init(&mutex, NULL);
    pthread_cond_init(&cond, NULL);
    Param param;

    Threading* Thread_Info=(Threading*) malloc(sizeof(Threading)*NTHREAD);
    for (int i=0;i<NTHREAD;i++){
      param.ThreadID=i;
      Thread_Info[i].Arg=param;
      pthread_create(&Thread_Info[i].Thread, NULL, thr_fn, (void*) &Thread_Info[i].Arg);
    }

    for (int i=0;i<NTHREAD;i++)
    {
        pthread_join(Thread_Info[i].Thread,NULL);
    }


//  char c ;
//  while ((c = getchar()) != 'q');
//  fprintf(stderr, "Now terminate the thread!\n");

//  flag = false;
//  pthread_mutex_lock(&mutex);
//  pthread_cond_signal(&cond);
//  pthread_mutex_unlock(&mutex);
//  fprintf(stderr, "Wait for thread to exit\n");
    fprintf(stderr, "Bye\n");
    return 0;
}
