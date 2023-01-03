// WAP to print the greatest Number

#include <stdio.h>
int main(){
    int a,b;
    printf("Enter two Num: ");
    scanf("%d%d",&a,&b);
    if (a>b){
        printf("%d is greatest",a);
    }else{
        printf("%d is greatest",b);
    }
    return 0;
}