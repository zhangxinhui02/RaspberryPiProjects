#include<reg51.h>
#include<absacc.h>
#include<intrins.h>
#include<string.h>
#define uchar unsigned char
#define uint unsigned int
/*****************************************************************************
//����Ӳ��ƽ̨��STC12C5A60S2/STC12LE5A60S2
//��Ƶ��12MHZ
//�����Գ�����߶������£�
//�����������
//����������ֻ��Ҫ��4��IO�����������Һ��������Һ��Ƭѡ�ͱ�������ߵ�ƽ3.3V��
//���������STC12LE5A60S2/STC12C5A60S2 Ӳ��SPI����������SCLK��MOSI�������Ų����������IO
//����������ž��ɸ�����Ҫ�����޸�IO����
*******************************************************************************/
//---------------------------Һ��������˵��-------------------------------------//

sbit bl        =P3^2;//��ģ��LED���ţ�������Բ���IO���ƻ���PWM���ƣ�Ҳ����ֱ�ӽӵ��ߵ�ƽ����
sbit scl       =P1^7;//��ģ��CLK����,
sbit sda       =P1^5;//��ģ��SDI���ţ�
sbit rs        =P0^2;//��ģ��RS���ţ�//
sbit cs        =P0^3;//��ģ��CS����	 //
sbit reset     =P3^3;//��ģ��RST����

//---------------------------End ofҺ��������---------------------------------//

//����Ӳ��ƽ̨��STC12C5A60S2/STC12LE5A60S2
//��Ƶ��12MHZ
//��Ƭ��IO����������ö���
#define MCU_STC12//�����ʹ�õĵ�Ƭ������STC12ϵ��(��STC89C52)�����δ˺궨��
#define		MAIN_Fosc	22000000L	//����ʱ��
#ifdef MCU_STC12
sfr P3M1  = 0xB1;	//P3M1.n,P3M0.n 	=00--->Standard,	01--->push-pull
sfr P3M0  = 0xB2;	//					=10--->pure input,	11--->open drain
sfr AUXR1 = 0xA2;
#endif
//-----------------------------SPI ��������--------------------------------------//
#define USE_HARDWARE_SPI     1  //1:Enable Hardware SPI;0:USE Soft SPI

//-------------------------��Ļ������������--------------------------------------//
#define LCD_X_SIZE	        176
#define LCD_Y_SIZE	        220

/////////////////////////////////////�û�������///////////////////////////////////	 
//֧�ֺ��������ٶ����л�
#define USE_HORIZONTAL  		1	//�����Ƿ�ʹ�ú��� 		0,��ʹ��.1,ʹ��.

#ifdef USE_HORIZONTAL//��������˺��� 
#define X_MAX_PIXEL	        LCD_Y_SIZE
#define Y_MAX_PIXEL	        LCD_X_SIZE
#else
#define X_MAX_PIXEL	        LCD_X_SIZE
#define Y_MAX_PIXEL	        LCD_Y_SIZE
#endif
//////////////////////////////////////////////////////////////////////////////////

//STC��Ƭ��Ӳ��SPI�Ĵ�������
sfr SPSTAT = 0xCD;	//STC12C5A60S2ϵ��
sfr SPCTL  = 0xCE;	//STC12C5A60S2ϵ��
sfr SPDAT  = 0xCF;	//STC12C5A60S2ϵ��
//sfr SPCTL   = 0x85;	SPI���ƼĴ���
//   7       6       5       4       3       2       1       0    	Reset Value
//	SSIG	SPEN	DORD	MSTR	CPOL	CPHA	SPR1	SPR0		0x00
#define	SSIG		1	//1: ����SS�ţ���MSTRλ�����������Ǵӻ�		0: SS�����ھ������ӻ���
#define	SPEN		1	//1: ����SPI��								0����ֹSPI������SPI�ܽž�Ϊ��ͨIO
#define	DORD		0	//1��LSB�ȷ���								0��MSB�ȷ�
#define	MSTR		1	//1����Ϊ����								0����Ϊ�ӻ�
#define	CPOL		1	//1: ����ʱSCLKΪ�ߵ�ƽ��					0������ʱSCLKΪ�͵�ƽ
#define	CPHA		1	//
#define	SPR1		0	//SPR1,SPR0   00: fosc/4,     01: fosc/16
#define	SPR0		0	//            10: fosc/64,    11: fosc/128
#define	SPEED_4		0	// fosc/4
#define	SPEED_16	1	// fosc/16
#define	SPEED_64	2	// fosc/64
#define	SPEED_128	3	// fosc/128

//sfr SPSTAT  = 0xCD;	//SPI״̬�Ĵ���
//   7       6      5   4   3   2   1   0    	Reset Value
//	SPIF	WCOL	-	-	-	-	-	-
#define	SPIF	0x80		//SPI������ɱ�־��д��1��0��
#define	WCOL	0x40		//SPIд��ͻ��־��д��1��0��

//������ɫֵ����
#define RED  	0xf800
#define GREEN	0x07e0
#define BLUE 	0x001f
#define WHITE	0xffff
#define BLACK	0x0000
#define YELLOW  0xFFE0
#define GRAY0   0xEF7D   	//��ɫ0 3165 00110 001011 00101
#define GRAY1   0x8410      	//��ɫ1      00000 000000 00000
#define GRAY2   0x4208      	//��ɫ2  1111111111011111

typedef unsigned int   u16;
typedef unsigned char  u8;

void Lcd_Clear(u16 Color);
void Lcd_Init(void);
void  delay_ms(unsigned char ms);
void Gui_DrawPoint(u16 x,u16 y,u16 Data);
void Lcd_SetRegion(u8 xStar, u8 yStar,u8 xEnd,u8 yEnd);
void Lcd_SetXY(u16 Xpos, u16 Ypos);
void Lcd_WriteData_16Bit(u16 Data);