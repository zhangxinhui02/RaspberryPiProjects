// UTFT_Demo_220x176_Serial (C)2013 Henning Karlsen
//web:http://qdtech.taobao.com/
// This program is a demo of how to use most of the functions
// of the library with a supported display modules.
//
// This demo was made for serial modules with a screen resolution 
// of 220x176 pixels.
//
// This program requires the UTFT library.
//Firstly,you should install the UTFT library.
/***********************************************************************************
//-----------------Instructions  for Hardware IO Connection------------------------|
//-----TFT Pin---|----Arduino Pin-----| -------------------Note--------------------|
//------LED------|---------A0---------|---Backlight Control,Hight level Enable-----|
//------CLK------|---------A1---------|-----Serial Interface Clock Signal----------|
//------SDI------|---------A2---------|-----------Serial Input Signal--------------|
//------RS-------|---------A3---------|------Command or Parameter Sellect----------|
//------RST------|---------A4---------|---------------Reset Signal-----------------|
//------CS-------|---------A5---------|----------Chip Sellect Signal---------------|
//VCC:5V DC.
//GND:Ground.
//How to save IO pin(see the notes below):
//note1:LED  is also can be connected to 3.3V or 5V,So that Backlight will be always on.
//note2:RST can be connected to MCU reset pin,to save a IO pin.
//note3:CS  can be connected to GND,So that Chip Sellect will be always Enable.
************************************************************************************/
#include <UTFT.h>

// Declare which fonts we will be using
extern uint8_t SmallFont[];
//UTFT myGLCD(Model,SDA,SCL,CS,RST,RS)
//QD220A is for QDtech 2.2inch SPI LCD Module,Driver IC:ILI9225
UTFT myGLCD(QD220A,A2,A1,A5,A4,A3);   // Remember to change the model parameter to suit your display module!



char tfont16[]=
{
0x08,0x20,0x06,0x20,0x80,0x7E,0x61,0x80,0x06,0x02,0x20,0x04,0x38,0x04,0x27,0x08,
0x20,0xD0,0x20,0x20,0x20,0xD0,0x27,0x08,0x38,0x0C,0x20,0x06,0x00,0x04,0x00,0x00,
0x00,0x00,0x08,0x40,0x30,0x40,0x24,0x40,0x24,0x40,0x24,0x42,0xA4,0x41,0x64,0xFE,
0x25,0x40,0x26,0x40,0x24,0x40,0x20,0x40,0x28,0x40,0x30,0x40,0x00,0x40,0x00,0x00,
0x10,0x20,0x8C,0x3F,0x61,0xC0,0x06,0x00,0x00,0x01,0x7F,0xE2,0x40,0x0C,0x4F,0xF0,
0x40,0x08,0x7F,0xE6,0x00,0x00,0x1F,0xE0,0x00,0x02,0x00,0x01,0xFF,0xFE,0x00,0x00,
0x02,0x00,0x42,0x00,0x3B,0xFE,0x10,0x04,0x00,0x08,0x09,0x04,0x09,0x04,0x09,0xF8,						   
0x09,0x08,0x09,0x08,0xFF,0x80,0x08,0x60,0x48,0x18,0x38,0x04,0x08,0x1E,0x00,0x00,

};
void Show_CH_Font16(int x,int y,int FontPos)
{
        char temp,t,t1,k;
	int y0=y;	
	int HZnum;

        for(t=0;t<32;t++)//每个16*16的汉字点阵 有32个字节
	{   
	  temp=tfont16[t+32*FontPos];                    
	  for(t1=0;t1<8;t1++)
	  {
	      if(temp&0x80)
              { 
                myGLCD.setColor(255, 0, 0);//FontColor
                myGLCD.drawPixel(x,y);
              }
	      else 
              { 
                myGLCD.setColor(0, 0, 0);//BackColor
                myGLCD.drawPixel(x,y);
              }

	      temp<<=1;
	      y++;
	      if((y-y0)==16)
	      {
		y=y0;
		x++;
		break;
	      }
	     
	  }  	 
	}   


}
void setup()
{
  randomSeed(analogRead(0));
  
// Setup the LCD
  myGLCD.InitLCD();
  myGLCD.setFont(SmallFont);
}
void loop()
{

// Clear the screen and draw the frame
  myGLCD.clrScr(); 
  Show_CH_Font16(0,0,0);
  Show_CH_Font16(16,0,1);
  Show_CH_Font16(32,0,2);
  Show_CH_Font16(48,0,3);
  delay (10000);
  myGLCD.setColor(255, 255, 255);
  myGLCD.setBackColor(255, 0, 0);
  
  
  myGLCD.print("That's it!", CENTER, 62);
  myGLCD.print("Restarting in a", CENTER, 88);
  myGLCD.print("few seconds...", CENTER, 101);
  
  myGLCD.setColor(0, 255, 0);
  myGLCD.setBackColor(0, 0, 255);
  myGLCD.print("Runtime: (msecs)", CENTER, 146);
  myGLCD.printNumI(millis(), CENTER, 161);

  delay (10000);
}

