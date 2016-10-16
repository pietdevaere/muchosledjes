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
#define FRAME_RDY 4


int main(int argc, char **argv){

    int sock;
    struct sockaddr_in name;
    struct hostent *hp, *gethostbyname();
    int bytes;
    
    struct sched_param sp;

 //   char *displayData;
 //   displayData = calloc(189, sizeof(char));
   
    memset(&sp, 0, sizeof(sp));
    sp.sched_priority = sched_get_priority_max(SCHED_FIFO);
    sched_setscheduler(0, SCHED_FIFO, &sp);
    mlockall(MCL_CURRENT | MCL_FUTURE);

    if(!bcm2835_init())
        return 1;
    
    bcm2835_gpio_fsel(FRAME_RDY, BCM2835_GPIO_FSEL_OUTP);
    bcm2835_gpio_write(FRAME_RDY, HIGH);
    
    // start up the spi
    bcm2835_spi_begin();
    bcm2835_spi_setBitOrder(BCM2835_SPI_BIT_ORDER_MSBFIRST);
    bcm2835_spi_setDataMode(BCM2835_SPI_MODE0);
    bcm2835_spi_setClockDivider(BCM2835_SPI_CLOCK_DIVIDER_512);
    bcm2835_spi_chipSelect(BCM2835_SPI_CS0);
    bcm2835_spi_setChipSelectPolarity(BCM2835_SPI_CS0, LOW);
   

    printf("Screen activating.\n");
    
    /* Create socket from which to read */
    sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (sock < 0)   {
        perror("Opening datagram socket");
        exit(1);
    }

    /* Bind our local address so that the client can send to us */
    bzero((char *) &name, sizeof(name));
    name.sin_family = AF_INET;
    name.sin_addr.s_addr = htonl(INADDR_ANY);
    name.sin_port = htons(SERVER_PORT);

    if (bind(sock, (struct sockaddr *) &name, sizeof(name))) {
        perror("binding datagram socket");
        exit(1);
    }

    printf("Listening on UDP port number #%d\n", ntohs(name.sin_port));

    while (1){
        char displayData[189];

        int i, j, row;
        
        if ((bytes = recv(sock, displayData, 189, 0/*MSG_DONTWAIT*/)) > 0) {
            bcm2835_gpio_write(FRAME_RDY, LOW);
            for (i=0; i<189; i++){
                bcm2835_spi_transfer(displayData[i]);
            }
            bcm2835_delayMicroseconds(5);
            bcm2835_gpio_write(FRAME_RDY, HIGH);
        }
    }
    // cloes the spi and the io
    bcm2835_spi_end();
    bcm2835_close();
    return 0;
}
