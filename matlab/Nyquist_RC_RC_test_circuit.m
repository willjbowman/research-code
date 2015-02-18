clear all; clf;
w = logspace(-1,6.8,100); %gamry max is 1MH, but there is some fudge factor so 10^6.8 in matlab is about the same
Cinti = [4.07e-8 4.07e-9 4.07e-10 4.07e-11] ; Cgbi = 1.17e-8;
R1 = 100.5; R2 = 1.43e3;
mark = ['k' 'b' 'r' '.'];
        for i=1:length(Cinti)
        ZA = 1./(1/R1+1i.*w*Cinti(i));
        ZB = 1./(1/R2+1i.*w*Cgbi);
        
        Z_RRC = ZA + ZB;
        Z_RRCreal = real(Z_RRC);
        Z_RRCimg = imag(Z_RRC);
      hold on
 
        plot(Z_RRCreal,-Z_RRCimg,mark(i),'LineWidth',5)
        axis([0 R1+R2 0 R1+R2])
        
        end
       legend('4.07e-8', '4.07e-9', '4.07e-10', '4.07e-11')