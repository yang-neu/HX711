#include "hx711.h"

// function prototype
int *get_int(int *num);

int main(int argc, char **argv)
{
  int err = 0;
  if (argc < 3)
  {
    printf("\nRequired 3 args.");
    printf("\nFirst arg is CLK pin, second arg is DATA pin (BMC numbering).");
    printf("\nThird arg is number of samples.");
    return 1;
  }

  int priority = 10;
  err = setPriority(priority);
  if (err)
  {
    printf("\n!!! Failed to set process priority to %d\n", priority);
    return 1;
  }

  HX711 hx;

  unsigned char clock_pin = (unsigned)atoi(argv[1]);
  unsigned char data_pin = (unsigned)atoi(argv[2]);
  unsigned int samples = 0;
  if (argc == 4)
  {
    samples = (unsigned)atoi(argv[3]);
  }
  err = initHX711(&hx, clock_pin, data_pin);
  if (err)
  {
    printf("\n!!! Failed to init HX711 struct !!!\n");
  }

  setupGPIO(&hx);

  reset(&hx);
  if (!samples)
  {
    samples = 1;
  }

  // START doing work

  /* err = zeroScale(&hx);
  if (err)
  {
    printf("\n!!! Failed to zero the scale.\n");
    return 1;
  }
  printf("\n Zero scale is done!");

  */
  
  double single_item_weight = getDataMean(&hx, samples);
  printf("%d", (int)single_item_weight);


  // STOP doing work

  cleanGPIO(&hx);

  return 0;
}
