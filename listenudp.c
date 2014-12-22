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

#define RCK 18
#define SRCK 17
#define SEROUT2 4
#define GVERT 22

void next_row(){
    bcm2835_gpio_write(SRCK, HIGH);
    bcm2835_delayMicroseconds(5);
    bcm2835_gpio_write(SRCK, LOW);
}

void first_row(){
    bcm2835_gpio_write(SEROUT2, LOW);
    bcm2835_delayMicroseconds(5);
    next_row();
    bcm2835_gpio_write(SEROUT2, HIGH);
}


void show_data(){
    bcm2835_gpio_write(GVERT, HIGH);
    bcm2835_gpio_write(RCK, HIGH);
    bcm2835_delayMicroseconds(5);
    bcm2835_gpio_write(RCK, LOW);
    bcm2835_gpio_write(GVERT, LOW);
}

int main(int argc, char **argv){

    int sock;
    struct sockaddr_in name;
    struct hostent *hp, *gethostbyname();
    int bytes;
    
    struct sched_param sp;

 //   char *displayData;
 //   displayData = calloc(189, sizeof(char));
    char displayData[] = {0, 0, 7, 128, 0, 0, 0, 32, 0, 0, 24, 0, 0, 0, 0, 0, 16, 2, 14, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 64, 0, 0, 0, 32, 0, 0, 36, 0, 0, 0, 0, 0, 0, 2, 17, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 86, 57, 227, 150, 113, 16, 14, 32, 0, 0, 0, 0, 30, 48, 231, 1, 52, 228, 78, 56, 5, 142, 0, 0, 0, 0, 7, 153, 69, 20, 89, 33, 16, 17, 112, 0, 0, 0, 0, 17, 17, 18, 13, 77, 20, 65, 68, 6, 81, 0, 0, 0, 0, 4, 16, 69, 231, 208, 32, 240, 17, 32, 0, 0, 0, 0, 30, 17, 242, 21, 69, 244, 79, 124, 4, 31, 0, 0, 0, 0, 4, 16, 69, 4, 16, 36, 16, 17, 32, 0, 0, 0, 0, 16, 17, 2, 85, 69, 2, 145, 64, 196, 16, 0, 0, 0, 0, 4, 16, 57, 3, 144, 24, 224, 14, 32, 0, 0, 0, 0, 16, 56, 225, 142, 60, 225, 15, 56, 196, 14, 0, 0};
   
    memset(&sp, 0, sizeof(sp));
    sp.sched_priority = sched_get_priority_max(SCHED_FIFO);
    sched_setscheduler(0, SCHED_FIFO, &sp);
    mlockall(MCL_CURRENT | MCL_FUTURE);

    if(!bcm2835_init())
        return 1;

    // set the appropriate pins as outputs
    bcm2835_gpio_fsel(RCK, BCM2835_GPIO_FSEL_OUTP);
    bcm2835_gpio_fsel(SRCK, BCM2835_GPIO_FSEL_OUTP);
    bcm2835_gpio_fsel(SEROUT2, BCM2835_GPIO_FSEL_OUTP);
    bcm2835_gpio_fsel(GVERT, BCM2835_GPIO_FSEL_OUTP);

    // set then to their idle values
    bcm2835_gpio_write(RCK, LOW);
    bcm2835_gpio_write(SRCK, LOW);
    bcm2835_gpio_write(SEROUT2, HIGH);

    // start up the spi
    bcm2835_spi_begin();
    bcm2835_spi_setBitOrder(BCM2835_SPI_BIT_ORDER_MSBFIRST);
    bcm2835_spi_setDataMode(BCM2835_SPI_MODE0);
    bcm2835_spi_setClockDivider(BCM2835_SPI_CLOCK_DIVIDER_64);
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
        int i, j, row;

        if ((bytes = recv(sock, displayData, 189, MSG_DONTWAIT)) > 0) {
 //           displayData[bytes] = '\0';
 //           printf("recv: %s\n", displayData);
        }

        first_row();
        for (i=0; i<189; i++){
            bcm2835_spi_transfer(displayData[i]);
            if ((i+1) % 27 == 0){
              if (i != 26) next_row();
              // i'll probably have to disable the display here for a moment, to prevent dimly lit leds
              show_data();
              bcm2835_delayMicroseconds(500);
            }
        }
    }



    // cloes the spi and the io
    bcm2835_spi_end();
    bcm2835_close();
    return 0;
}
