#include <stdio.h>
#include <ucontext.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

int main()
{
    int i = 0;
    ucontext_t *ucp = (ucontext_t*)(malloc(sizeof(ucontext_t)));
    getcontext(ucp);
    printf("sizeof ucontext_t~~ : %d\n" , sizeof(ucontext_t));
    printf("uc_link~~ : %x\n" , (ucp->uc_link));
    printf("sizeof sigset_t ~~ : %d\n", sizeof(ucp->uc_sigmask));
    printf("sizeof stack_t ~~ : %d\n", sizeof(ucp->uc_stack));
    printf("sizeof mcontext_t : %d\n", sizeof(ucp->uc_mcontext));
    int * a = (int*)ucp;
    int cont = open("sample_context",O_RDWR | O_CREAT);
    if(cont < 0) return 0;
    write(cont,ucp, sizeof(ucontext_t));
}
