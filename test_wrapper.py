import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, ClockCycles

@cocotb.test()
async def test_wrapper(dut):
    clock = Clock(dut.wb_clk_i, 10, units="ns")
    cocotb.fork(clock.start())
    dut.VGND <= 0
    dut.VPWR <= 1
   
    dut.active <= 0

    dut.io_in <= 0
    dut.wbs_stb_i <= 0
    dut.wbs_cyc_i <= 0
    dut.wbs_we_i <= 0

    # drive wb_rst 
    dut.wb_rst_i <= 1
    await ClockCycles(dut.wb_clk_i, 5)
    dut.wb_rst_i <= 0

    await ClockCycles(dut.wb_clk_i, 10)

    # reset wb_hyperram
    dut.la_data_in <= 1 << 0
    await ClockCycles(dut.wb_clk_i, 3)
    dut.la_data_in <= 0 << 0
    await ClockCycles(dut.wb_clk_i, 3)
    
    # try triggering write to HyperRam memory space with active=0
    dut.wbs_stb_i <= 1
    dut.wbs_cyc_i <= 1
    dut.wbs_we_i <= 1
    dut.wbs_sel_i <= 7
    dut.wbs_adr_i <= 0x30000000
    dut.wbs_dat_i <= 0x13572468
    await ClockCycles(dut.wb_clk_i, 60)

    # deactivate strobe (fulfill handshake)
    dut.wbs_stb_i <= 0
    dut.wbs_cyc_i <= 0
    await ClockCycles(dut.wb_clk_i, 10)

    # activate project
    dut.active <= 1

    # reset
    dut.la_data_in <= 1 << 0
    await ClockCycles(dut.wb_clk_i, 3)
    dut.la_data_in <= 0 << 0
    await ClockCycles(dut.wb_clk_i, 3)

    # trigger write to HyperRam memory space
    dut.wbs_stb_i <= 1
    dut.wbs_cyc_i <= 1
    dut.wbs_we_i <= 1
    dut.wbs_sel_i <= 7
    dut.wbs_adr_i <= 0x30000195
    dut.wbs_dat_i <= 0x13572468
    await ClockCycles(dut.wb_clk_i, 50)

    # deactivate strobe (fulfill handshake)
    dut.wbs_stb_i <= 0
    dut.wbs_cyc_i <= 0
    await ClockCycles(dut.wb_clk_i, 10)    
    
    # trigger read from HyperRam memory space
    dut.wbs_stb_i <= 1
    dut.wbs_cyc_i <= 1
    dut.wbs_we_i <= 0
    dut.wbs_sel_i <= 7
    dut.wbs_adr_i <= 0x3000105a
    await ClockCycles(dut.wb_clk_i, 80)

    # deactivate strobe (fulfill handshake)
    dut.wbs_stb_i <= 0
    dut.wbs_cyc_i <= 0
    await ClockCycles(dut.wb_clk_i, 10)    

    # deactivate project
    dut.active <= 0
    await ClockCycles(dut.wb_clk_i, 20)
