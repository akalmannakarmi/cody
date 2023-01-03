// WAP to calculate sum and average of 5 numbers

#include <stdio.h>
int main(){
    int a,b,c,d,e;
    printf("Enter 5 numbers: ");
    scanf("%d%d%d%d%d",&a,&b,&c,&d,&e);

    int sum = a+b+c+d+e;
    int average = sum/5;

    printf("Sum :%d\n",sum);
    printf("Average :%d\n",sum);
    return 0;
}