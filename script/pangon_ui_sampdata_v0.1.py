#######################
# Created by gchliu
# 2023/08/01
######################
import time

import ControlSPI
from ctypes import *
import xlrd

class op_spi():
    def __init__(self,freq):
        self.freq = freq

    def write_atom(self,addr,data):
        print ('write addr = '+hex(addr)+' data = '+hex(data))
        write_buffer = (c_ubyte * 8)()
        addr_str = '{:0>8x}'.format(addr*2048)
        data_str = '{:0>8x}'.format(data)
        write_buffer[0] = int(addr_str[0:2],16)
        write_buffer[1] = int(addr_str[2:4],16)
        write_buffer[2] = int(addr_str[4:6],16)
        write_buffer[3] = int(addr_str[6:], 16)
        write_buffer[4] = int(data_str[0:2],16)
        write_buffer[5] = int(data_str[2:4],16)
        write_buffer[6] = int(data_str[4:6],16)
        write_buffer[7] = int(data_str[6:8],16)
        nRet = ControlSPI.VSI_WriteBytes(ControlSPI.VSI_USBSPI, 0, 0, write_buffer, 8)
    def read_atom(self,addr):
        write_buffer = (c_ubyte * 4)()
        read_value = (c_ubyte * 4)()
        addr_str = '{:0>8x}'.format(addr*2048)
        write_buffer[0] = int(addr_str[0:2], 16)+128
        write_buffer[1] = int(addr_str[2:4], 16)
        write_buffer[2] = int(addr_str[4:6], 16)
        write_buffer[3] = int(addr_str[6:8], 16)
        nRet = ControlSPI.VSI_WriteReadBytes(ControlSPI.VSI_USBSPI, 0, 0, write_buffer, 4, read_value, 4)
        return_data = read_value[0] * 16777216 + read_value[1] * 65536 + read_value[2] * 256 + read_value[3]
        print ('read addr = '+hex(addr)+' data = '+ hex(return_data))




    def read_mem_atom(self, addr):
        write_buffer = (c_ubyte * 4)()
        read_value = (c_ubyte * 4)()
        addr_str = '{:0>8x}'.format(addr*2048)
        write_buffer[0] = int(addr_str[0:2], 16)+128
        write_buffer[1] = int(addr_str[2:4], 16)
        write_buffer[2] = int(addr_str[4:6], 16)
        write_buffer[3] = int(addr_str[6:8], 16)
        nRet = ControlSPI.VSI_WriteReadBytes(ControlSPI.VSI_USBSPI, 0, 0, write_buffer, 4, read_value, 4)
        return read_value



    def spi_config(self):
        # Scan device
        nRet = ControlSPI.VSI_ScanDevice(1)
        if (nRet <= 0):
            print("未发现设备")
        else:
            print("已发现设备")
        # Open device
        nRet = ControlSPI.VSI_OpenDevice(ControlSPI.VSI_USBSPI, 0, 0)
        if (nRet != ControlSPI.ERR_SUCCESS):
            print("打开设备失败")
        else:
            print("打开设备成功")
        # Initialize device
        SPI_Init = ControlSPI.VSI_INIT_CONFIG()
        SPI_Init.ClockSpeed = int(self.freq)
        SPI_Init.ControlMode = 3
        SPI_Init.CPHA = 0
        SPI_Init.CPOL = 0
        SPI_Init.LSBFirst = 0
        SPI_Init.MasterMode = 1
        SPI_Init.SelPolarity = 0
        SPI_Init.TranBits = 8
        nRet = ControlSPI.VSI_InitSPI(ControlSPI.VSI_USBSPI, 0, byref(SPI_Init))
        if (nRet != ControlSPI.ERR_SUCCESS):
            print('连接失败')
        else:
            print('连接成功')


if __name__ == '__main__':
    spi = op_spi(freq=1125000)
    spi.spi_config()
    spi.read_atom(0x351)
    spi.write_atom(0x351,0x0)
    spi.read_atom(0x351)
    spi.read_atom(0x40200)
    time.sleep(0.1)




###################################################################################################
    path_DAC_reg = r'DATA_SAMPLE_XIHEV200.xlsx'
    wb_reg = xlrd.open_workbook(path_DAC_reg)
    reg_sheet = wb_reg.sheet_by_name('XIHEV200_SMP_INIT')
    spi.write_atom(0x40b, 0xf)  #
    spi.write_atom(0x4e1, 0x0)  #
    # cols = 2
    rows = reg_sheet.nrows
    addr_buffer = []
    data_buffer = []

    for row in range(0,29):
        addr_buffer.append(int(reg_sheet.cell_value(row,0),16))
        data_buffer.append(int(reg_sheet.cell_value(row,1),16))
    print(addr_buffer,data_buffer)

    # spi = op_spi(freq=1125000)
    # spi.spi_config()
    for i in range(0,29):
        # spi.read_atom(addr_buffer[i])
        spi.write_atom(addr_buffer[i], data_buffer[i])
        time.sleep(0.01)
        # spi.read_atom(0x1)
        spi.read_atom(addr_buffer[i])
        time.sleep(0.01)

        path_DAC_reg = r'DATA_SAMPLE_XIHEV200.xlsx'
        wb_reg = xlrd.open_workbook(path_DAC_reg)
        reg_sheet = wb_reg.sheet_by_name('XIHEV200_ADC_MEMORYREAD')

    # cols = 2
    rows = reg_sheet.nrows
    addr_buffer = []
    data_buffer = []

    for row in range(0,14):
        addr_buffer.append(int(reg_sheet.cell_value(row, 0), 16))
        data_buffer.append(int(reg_sheet.cell_value(row, 1), 16))
    print(addr_buffer, data_buffer)

    # spi = op_spi(freq=1125000)
    # spi.spi_config()
    for i in range(0,14):
        # spi.read_atom(addr_buffer[i])
        spi.write_atom(addr_buffer[i], data_buffer[i])
        time.sleep(0.01)
        # spi.read_atom(0x1)
        spi.read_atom(addr_buffer[i])
        time.sleep(0.01)

#################################################### data sample ###################################


    spi.write_atom(0x4c8, 0x0)
    spi.write_atom(0x4c4, 0x0)
    spi.write_atom(0x4c1, 0x2)
    # self.write_atom(0x470, 0x0)
    # self.write_atom(0x470, 0x40000)
    # self.write_atom(0x470, 0x0)
    read_len = 4  # byte
    memory_wid = 4  # byte, 32bit
    memory_depth = 32*1024  * memory_wid  # by0te
    addr_step = int(read_len / memory_wid)
    read_times = int(memory_depth / read_len)
    fp = open('memory_dump_data.txt', 'w')
    return_value = (c_ubyte * 4)()
    for i in range(0, read_times):
        spi.write_atom(0x4c0, i * 4 * addr_step)
        spi.write_atom(0x4c0, 0x40000 + i * 4 * addr_step)
        spi.write_atom(0x4c0, i * 4 * addr_step)
        read_buffer = spi.read_mem_atom(0x4cc)
        spi.write_atom(0x4c0, i * 4 * addr_step)
        spi.write_atom(0x4c0, 0x40000 + i * 4 * addr_step)
        spi.write_atom(0x4c0, i * 4 * addr_step)
        read_buffer = spi.read_mem_atom(0x4cc)
        for k in range(0, int(len(read_buffer) / 4)):
            fp.write("0x")
            for j in range(0, 4):
                fp.write("%02x" % (read_buffer[k * 4 + j]))
            fp.write("\n")
    fp.close()
    spi.write_atom(0x4c1, 0x0)


########################## read calibration #########################

spi.read_atom(0x1068D)
spi.read_atom(0x1068E)
spi.read_atom(0x1068F)
spi.read_atom(0x10690)
spi.read_atom(0x10691)
spi.read_atom(0x10692)
spi.read_atom(0x10693)
spi.read_atom(0x10694)