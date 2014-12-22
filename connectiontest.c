#include <bcm2835.h>
#include <sched.h>
#include <sys/mman.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <stdio.h>
#include <fcntl.h>
#include <string.h>
#include <stdlib.h>

#define SERVER_PORT 5000

#define BLINKPIN 17

int main(int argc, char **argv){

    if(!bcm2835_init())
        return 1;

    // set the appropriate pins as outputs
    bcm2835_gpio_fsel(BLINKPIN, BCM2835_GPIO_FSEL_OUTP);

    printf("Now blinking.\n");
    
    while(1){    
    bcm2835_gpio_write(BLINKPIN, LOW);
    printf("LOW\n");
    bcm2835_delayMicroseconds(1000000);
    bcm2835_gpio_write(BLINKPIN, HIGH);
    printf("HIGH\n");
    bcm2835_delayMicroseconds(1000000);
    }
    bcm2835_close();
    return 0;
}
