#include <stdio.h>

// Example program to analyze with GDB

// Reads input and parses it as in integer
int read_int(void) {
    char buf[128];
    int i;
    gets(buf);
    i = atoi(buf);
    return i;
}

int main(int ac, char **av) {
    int x = read_int();
    printf("x=%d\n", x);
}
