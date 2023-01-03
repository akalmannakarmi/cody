// WAP to print even or odd

#include <stdio.h>
int main(){
    int a;
    printf("Enter num: ");
    scanf("%d",&a);
    if (a%2 == 0){
        printf("Even");
    }else{
        printf("Odd");
    }
    return 0;
}