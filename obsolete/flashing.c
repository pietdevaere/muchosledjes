#include <bcm2835.h>
#include <sched.h>
#include <sys/mman.h>
#include <string.h>

#define RCK 18
#define SRCK 17
#define SEROUT2 4

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
    bcm2835_gpio_write(RCK, HIGH);
    bcm2835_delayMicroseconds(5);
    bcm2835_gpio_write(RCK, LOW);
}

int main(int argc, char **argv){

    struct sched_param sp;
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

    int toggle = 0;
   
    while (1){
        int i, j;

        first_row();
        
        toggle ++;
        toggle = toggle % 25;
        for (i=0; i<7; i++){
            if (toggle < 24){
                for (j=0; j<27; j++){
                    bcm2835_spi_transfer(0x00);
                }
            }
            else{
                for (j=0; j<27; j++){
                    bcm2835_spi_transfer(0xff);
                }
            }


            if (i != 0) next_row();
            show_data();
            bcm2835_delayMicroseconds(500);
    //        bcm2835_delay(1);
        }
    }



    // cloes the spi and the io
    bcm2835_spi_end();
    bcm2835_close();
    return 0;
}
