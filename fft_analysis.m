clear all;
close all;
% data = textread('C:\Users\wjwang\Desktop\zxy\xihe_ui_v0.1\read_data_from_testmem_after_trans.txt', '%s');
data = textread('.\read_data_from_testmem_after_trans.txt', '%s');
% %data = textread([pwd,'\','memory_dump_data.txt'], '%s');

%
% % data = textread('memory_dump_rd.txt', '%s');
data = hex2dec(data);
index=data>=32768;
data(index)=data(index)-65536;

% plot(data(1:1:end))
fs = 3e9/1;      %确认时钟频率
% % fsig = 2.5e9;
% para.sigbw=100e6;
% para.dpdbw=300e6;
para.sideband=0.3e6;
para.sideband_sig=6e6;
para.fullscale=1000;
para.Rl=100;
para.num_interleave=1;
para.num_HD=3;
para.num_IMD=3;
para.window='hann';
% Read_SG_sig;
% para.nyquitst_zone=floor(Instr.SigFreRead/(fs/2))+1;
para.nyquitst_zone=1;
%

para.dacOSR=1;
para.plot_range=0;
para.simple_plot=0;
para.dc_1f_noise_cancel=5e6;      %% add cancel dc  and 1/f noise
para.dbc_th_HD=-70;                %% not add color for -70dbc
para.dbc_th_IMD=-70;
para.dbc_th_IL=-70;
para.dbc_th_SFDR=70;
para.figure_overwrite=0;
% para.imd_mode=0;
% para.refclk_ratio=divratio;
para.num_ILHD=2;
para.interleavingHD=4;
para.sig_angle=1;
% perf=fft_calc(data(1:4:end),fs,15,para);
% perf=fft_calc(data(1:2:end),fs,15,para);
% perf=fft_calc(data(1:3:end),fs,15,para);
% perf=fft_calc(data(1:4:end),fs,15,para);
% angle_arr=[]
% for i=1:8
% perf=fft_calc_tot(data_r(i:8:end),fs,15,para);
% angle_arr=[angle_arr perf.sig_angle];
% end
% perf=fft_calc_tot(data(1:8:end),fs,15,para);

data_r=reshape(data,8,length(data)/8);
 data_r=data_r([1 3 5 7 2 4 6 8],:);
data_r=data_r(:);
figure(1);
plot(data_r);
% 
% figure
% para.num_interleave=4;
% para.nyquitst_zone=1;
% para.num_HD=3;
% para.sideband_sig=0.8e6;
% para.dc_1f_noise_cancel=1e3;   
% cnt=1;
% for i=1:75:length(data)-74
%     data_osr(cnt) = mean(data_r(i:i+74));
%     cnt=cnt+1;
% end
% 
% fs=40e6
% 
% perf=fft_calc_tot(data_osr(1:1:end),fs,15,para);


% plot(data_r(1:4:end));
figure
% perf1=fft_calc_tot(data_r(1:4:end),fs/4,15,para);
% perf2=fft_calc_tot(data_r(2:4:end),fs/4,15,para);
% perf3=fft_calc_tot(data_r(3:4:end),fs/4,15,para);
% perf4=fft_calc_tot(data_r(4:4:end),fs/4,15,para);
%
 
perf=fft_calc_tot(data_r(1:1:end),fs,15,para);
scrzs=get(0,'ScreenSize');
set(gcf,'position',[0,30,scrzs(3),scrzs(4)-110]);
set(gcf,'color',[1,1,1])
%plot(data_r(1:16:end))
% figure
% plot(data_r)
