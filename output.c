#include <stdio.h>
int main() {
    int x = (5 + 3);
    printf("%d\n", x);
    int count = 0;
    while ((count < 3)) {
        printf("%d\n", count);
        count = (count + 1);
    }
    return 0;
}