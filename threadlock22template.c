#define _REENTRANT
#include <pthread.h>
#include <stdio.h>
#include <sys/types.h>
#include <fcntl.h>
#include <sys/time.h>
#include <sys/resource.h>
#include <stdlib.h>
/* Tested by LOH 2/1/22. */
/* compile with gcc -ofname thread-template.c -lpthread */
/* Solve with mutex locks */

struct rusage mytiming;
struct timeval mytimeval;

struct shared_dat
{
        int value; /* shared variable to store result */
};

struct shared_dat *counter;
int getpid();
int temp;
pthread_mutex_t mutex;
int mytot = 0, jumps = 0;
int flag = 1;

/****************************************************************
* This function increases the value of shared variable "counter"
  by one 3000000 times
****************************************************************/
void *
thread1(void *arg)
{
        int line = 0;

        while (line < 3000000)
        {
                if (flag == 0)
                {
                        if (pthread_mutex_trylock(&mutex))
                        {
                                line++;

                                if ((counter->value % 100) == 0)
                                {
                                        counter->value += 100;
                                        jumps++;
                                }

                                mytot += 1;
                                flag = 1;
                                pthread_mutex_unlock(&mutex);
                        }
                }
        }

        // Ignore if you like.  Your counter value is the shared variable
        // when done.  mytot should be 3,000,000.  Jumps is 0 to 30,0000.
        printf("from process1 counter  =  %d, mytot %d, jumps %d \n",
               counter->value, mytot, jumps);
        return (NULL);
}

/****************************************************************
This function increases the value of shared variable "counter"
by one 3000000 times
****************************************************************/
void *
thread2(void *arg)
{
        int line = 0;
        int count;

        while (line < 3000000)
        {
                if (flag == 1)
                {
                        if (pthread_mutex_trylock(&mutex))
                        {
                                line++;

                                count = 0;

                                /* Critical Section */
                                counter->value = counter->value + 1;
                                counter->value = counter->value * 2;
                                counter->value = counter->value / 2;
                                //   printf("Thread 2 %d \n", counter->value);
                                flag = 0;
                                pthread_mutex_unlock(&mutex);
                        }
                }
        }

        printf("from process2 counter = %d\n", counter->value);
        return (NULL);
}

/****************************************************************
 *                  Main Body                                    *
 ****************************************************************/
int main()
{
        int r = 0;
        int i;
        pthread_t tid1[1];      /* process id for thread 1 */
        pthread_t tid2[1];      /* process id for thread 2 */
        pthread_t tid3[1];      /* process id for thread 2 */
        pthread_attr_t attr[1]; /* attribute pointer array */

        pthread_mutex_init(&mutex, NULL);
        counter = (struct shared_dat *)malloc(sizeof(struct shared_dat));

        /* initialize shared memory to 0 */
        counter->value = 0;
        printf("1 - I am here %d in pid %d\n", r, getpid());

        fflush(stdout);
        /* Required to schedule thread independently.
           Otherwise use NULL in place of attr. */
        pthread_attr_init(&attr[0]);
        pthread_attr_setscope(&attr[0], PTHREAD_SCOPE_SYSTEM); /* system-wide contention */

        /* end to schedule thread independently */

        /* Create the threads */

        pthread_create(&tid2[0], &attr[0], thread2, NULL);
        pthread_create(&tid1[0], &attr[0], thread1, NULL);

        /* Wait for the threads to finish */
        pthread_join(tid2[0], NULL);
        pthread_join(tid1[0], NULL);

        printf("from parent counter  =  %d\n", counter->value);
        getrusage(RUSAGE_SELF, &mytiming);
        printf("Time used is sec: %d, usec %d\n", mytiming.ru_utime.tv_sec,
               mytiming.ru_utime.tv_usec);
        printf("System Time used is sec: %d, usec %d\n", mytiming.ru_stime.tv_sec,
               mytiming.ru_stime.tv_usec);
        printf("---------------------------------------------------------------------------\n");
        printf("\t\t	End of simulation\n");

        exit(0);
}
